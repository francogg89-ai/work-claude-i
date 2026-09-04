"""Lectura del candidato congelado y extracción de su superficie normativa.

El denominador de la cobertura no vive aquí ni en el mecanismo: se extrae del candidato.

Solo lectura. Sin red. Sin modelo de lenguaje.
"""

import re
import subprocess

CANDIDATE_WORK_SHA = "5f5e2ee8e9bcc7f471cabcd0ecd865ff5cfa0a39"
CANDIDATE_PATH = "u2-reglas-orquestador/REGLAS-ORQUESTADOR.md"
CANDIDATE_BLOB_SHA = "4cfc8f88ead6a1466f61522496605b6c89ed4057"

OBLIGACION = re.compile(r"^(R-[A-Za-z0-9.\-]+)\s{2,}(\S.*)$")
CONTINUACION = re.compile(r"^ {4,}\S")
ENCABEZADO = re.compile(r"^(#{1,6}) (.*)$")
NUMERADA = re.compile(r"^(\d+(?:\.\d+)?)\. ")
NO_MECANICAS = re.compile(r"^SECCIONES_NO_MECANICAS\s+(.+)$", re.M)
NOTA = re.compile(r"^Nota\.")
CERCA = re.compile(r"^```")


def leer(repo, work_sha=CANDIDATE_WORK_SHA, path=CANDIDATE_PATH):
    """Devuelve (texto, blob_sha) del candidato en su identidad exacta."""
    texto = subprocess.run(
        ["git", "-C", repo, "show", "%s:%s" % (work_sha, path)],
        check=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    blob = subprocess.run(
        ["git", "-C", repo, "rev-parse", "%s:%s" % (work_sha, path)],
        check=True, stdout=subprocess.PIPE).stdout.decode().strip()
    return texto, blob


class Candidato:
    def __init__(self, texto):
        self.texto = texto
        self.lineas = texto.split("\n")
        self._secciones = self._partir()
        m = NO_MECANICAS.search(texto)
        self.no_mecanicas = set(m.group(1).split()) if m else set()

    # -- estructura -----------------------------------------------------------

    def _partir(self):
        """Lista de (numero|None, indice_encabezado, indice_fin_exclusivo)."""
        cortes = []
        for i, linea in enumerate(self.lineas):
            m = ENCABEZADO.match(linea)
            if m:
                n = NUMERADA.match(m.group(2))
                cortes.append((n.group(1) if n else None, i))
        secciones = []
        for k, (numero, i) in enumerate(cortes):
            fin = cortes[k + 1][1] if k + 1 < len(cortes) else len(self.lineas)
            secciones.append((numero, i, fin))
        return secciones

    def secciones_numeradas(self):
        return [s for s in self._secciones if s[0] is not None]

    def secciones_mecanicas(self):
        return [s for s in self.secciones_numeradas() if s[0] not in self.no_mecanicas]

    def _bloque_obligaciones(self, inicio, fin):
        """(ini, fin) exclusivos del contenido del primer bloque cercado, o None."""
        abierto = None
        for i in range(inicio + 1, fin):
            if CERCA.match(self.lineas[i]):
                if abierto is None:
                    abierto = i
                else:
                    return abierto, i
        return None

    # -- superficie normativa -------------------------------------------------

    def obligaciones(self):
        """[(id, enunciado, seccion)] leidas de los bloques de las secciones mecanicas."""
        salida = []
        for numero, ini, fin in self.secciones_mecanicas():
            bloque = self._bloque_obligaciones(ini, fin)
            if bloque is None:
                continue
            a, b = bloque
            actual = None
            for i in range(a + 1, b):
                linea = self.lineas[i]
                m = OBLIGACION.match(linea)
                if m:
                    actual = [m.group(1), m.group(2), numero]
                    salida.append(actual)
                elif CONTINUACION.match(linea) and actual is not None:
                    actual[1] += " " + linea.strip()
        return [tuple(x) for x in salida]

    def secciones_sin_obligacion(self):
        con = {o[2] for o in self.obligaciones()}
        return [n for n, _, _ in self.secciones_mecanicas() if n not in con]

    def violaciones_de_forma(self):
        """Contenido no vacio fuera de la forma declarada por el candidato.

        Forma: encabezado, bloque de obligaciones, y contenido libre solo a partir
        del primer marcador Nota.
        """
        fallas = []
        for numero, ini, fin in self.secciones_mecanicas():
            bloque = self._bloque_obligaciones(ini, fin)
            if bloque is None:
                fallas.append((numero, ini + 1, "sin bloque de obligaciones"))
                continue
            a, b = bloque
            for i in range(ini + 1, a):
                if self.lineas[i].strip():
                    fallas.append((numero, i + 1, "contenido antes del bloque: %r"
                                   % self.lineas[i]))
            primera_nota = None
            for i in range(b + 1, fin):
                if NOTA.match(self.lineas[i]):
                    primera_nota = i
                    break
            limite = primera_nota if primera_nota is not None else fin
            for i in range(b + 1, limite):
                if self.lineas[i].strip():
                    fallas.append((numero, i + 1,
                                   "contenido no vacio entre el bloque y la primera Nota.: %r"
                                   % self.lineas[i]))
        return fallas
