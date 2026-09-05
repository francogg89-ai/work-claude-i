"""Lee el candidato y extrae su superficie normativa, conforme a lo que el propio candidato
declara en su seccion 10. El mecanismo no trae catalogo propio de obligaciones.

```text
obligacion        linea etiquetada dentro del bloque de obligaciones de una seccion mecanica
continuacion      linea que empieza con cuatro o mas espacios
superficie        la linea etiquetada de una obligacion mas sus continuaciones, y nada mas
seccion mecanica  encabezado, bloque de obligaciones, y desde el primer marcador Nota. contenido
                  libre. Cualquier otra cosa entre medio esta fuera de forma
```

Las variantes de documento existen para volver observable la regla de alcance: si el observable de
una comprobacion cambia cuando se altera algo fuera de su superficie, esa comprobacion lee de mas.
"""

import re

RE_SECCION = re.compile(r"^# (\d+)\. (.+)$")
RE_OBLIGACION = re.compile(r"^(R-[A-Za-z0-9\-]+)\s{2,}(\S.*)$")
RE_CONTINUACION = re.compile(r"^ {4,}(\S.*)$")
RE_CERCA = re.compile("^" + "`" * 3)
RE_NOTA = re.compile(r"^Nota\.")
RE_NO_MECANICAS = re.compile(r"^SECCIONES_NO_MECANICAS\s+(.+)$")


def plano(texto):
    return " ".join(texto.split())


class Obligacion(object):
    def __init__(self, ident, seccion, lineas):
        self.id = ident
        self.seccion = seccion
        self.lineas = list(lineas)
        self.plano = plano("\n".join(lineas))
        self.ini = None
        self.fin = None


class Seccion(object):
    def __init__(self, numero, titulo, lineas):
        self.numero = numero
        self.titulo = titulo
        self.lineas = list(lineas)
        self.obligaciones = []
        self.tiene_bloque = False
        self.defectos = []


class Sujeto(object):
    """Lo que una comprobacion de documento recibe. Solo expone superficies, nunca el documento."""

    def __init__(self, texto_plano, spans, etiqueta):
        self._plano = texto_plano
        self._spans = dict(spans)
        self.etiqueta = etiqueta

    def superficie(self, obligacion):
        ini, fin = self._spans[obligacion]
        return self._plano[ini:fin]

    def obligaciones(self):
        return sorted(self._spans)


class Documento(object):
    def __init__(self, texto):
        self.texto = texto
        self.plano = plano(texto)
        self.lineas = texto.split("\n")
        self.secciones = {}
        self.obligaciones = {}
        self.no_mecanicas = set()
        self.defectos_de_forma = []
        self.ambiguas = []
        self._parsear()
        self._ubicar()

    # -- parseo ---------------------------------------------------------------

    def _parsear(self):
        actual = None
        for linea in self.lineas:
            m = RE_SECCION.match(linea)
            if m:
                actual = Seccion(int(m.group(1)), m.group(2), [])
                self.secciones[actual.numero] = actual
                continue
            if linea.startswith("# "):
                actual = None
                continue
            if actual is not None:
                actual.lineas.append(linea)
            m = RE_NO_MECANICAS.match(linea)
            if m:
                self.no_mecanicas = {int(x) for x in m.group(1).split()}
        for seccion in self.secciones.values():
            self._leer_seccion(seccion)

    def _leer_seccion(self, seccion):
        bloque, antes, entre = self._partir(seccion.lineas)
        seccion.tiene_bloque = bloque is not None
        if antes:
            seccion.defectos.append("contenido entre el encabezado y el bloque: %r" % antes[:1])
        if entre:
            seccion.defectos.append("contenido entre el bloque y el primer Nota.: %r" % entre[:1])
        if bloque is None:
            return
        pendiente = None
        for linea in bloque:
            m = RE_OBLIGACION.match(linea)
            if m:
                if pendiente is not None:
                    self._guardar(pendiente, seccion)
                pendiente = Obligacion(m.group(1), seccion.numero, [linea])
                continue
            c = RE_CONTINUACION.match(linea)
            if c and pendiente is not None:
                pendiente.lineas.append(linea)
                pendiente.plano = plano("\n".join(pendiente.lineas))
        if pendiente is not None:
            self._guardar(pendiente, seccion)

    def _guardar(self, obligacion, seccion):
        self.obligaciones[obligacion.id] = obligacion
        seccion.obligaciones.append(obligacion.id)

    def _partir(self, lineas):
        """Devuelve (bloque, contenido antes del bloque, contenido entre bloque y primer Nota.)."""
        i = 0
        antes = []
        while i < len(lineas) and not RE_CERCA.match(lineas[i]):
            if lineas[i].strip():
                if RE_NOTA.match(lineas[i]):
                    return None, antes, []
                antes.append(lineas[i])
            i += 1
        if i >= len(lineas):
            return None, antes, []
        j = i + 1
        bloque = []
        while j < len(lineas) and not RE_CERCA.match(lineas[j]):
            bloque.append(lineas[j])
            j += 1
        entre = []
        k = j + 1
        while k < len(lineas) and not RE_NOTA.match(lineas[k]):
            if lineas[k].strip():
                entre.append(lineas[k])
            k += 1
        return bloque, antes, entre

    # -- ubicacion de superficies --------------------------------------------

    def _ubicar(self):
        for obligacion in self.obligaciones.values():
            apariciones = _todas(self.plano, obligacion.plano)
            if len(apariciones) != 1:
                self.ambiguas.append((obligacion.id, len(apariciones)))
                continue
            obligacion.ini = apariciones[0]
            obligacion.fin = apariciones[0] + len(obligacion.plano)
        for seccion in self.secciones.values():
            for d in seccion.defectos:
                self.defectos_de_forma.append((seccion.numero, d))

    def spans(self):
        return {o.id: (o.ini, o.fin) for o in self.obligaciones.values() if o.ini is not None}

    def sujeto(self, etiqueta="real"):
        return Sujeto(self.plano, self.spans(), etiqueta)

    def superficie(self, obligacion):
        return self.obligaciones[obligacion].plano

    def secciones_mecanicas(self):
        return sorted(n for n in self.secciones if n not in self.no_mecanicas)


def _todas(texto, aguja):
    salida, i = [], texto.find(aguja)
    while i >= 0:
        salida.append(i)
        i = texto.find(aguja, i + 1)
    return salida


# -- variantes de documento, para volver observable la regla de alcance --------

def _rearmar(plano_nuevo, superficie, etiqueta):
    apariciones = _todas(plano_nuevo, superficie)
    if len(apariciones) != 1:
        raise ValueError("la superficie dejo de ser unica en la variante %s" % etiqueta)
    ini = apariciones[0]
    return ini, ini + len(superficie)


def sin_ocurrencias_fuera(documento, obligacion, fragmentos):
    """Borra toda ocurrencia de los fragmentos que caiga FUERA de la superficie."""
    superficie = documento.superficie(obligacion)
    ini, fin = documento.spans()[obligacion]
    izquierda, derecha = documento.plano[:ini], documento.plano[fin:]
    for f in fragmentos:
        izquierda = izquierda.replace(f, "")
        derecha = derecha.replace(f, "")
    nuevo = izquierda + superficie + derecha
    return Sujeto(nuevo, {obligacion: _rearmar(nuevo, superficie, "sin-ocurrencias-fuera")},
                  "sin-ocurrencias-fuera")


def con_ruido_antes(documento, obligacion, fragmentos):
    """Inserta los fragmentos, desordenados, ANTES de la superficie y fuera de ella."""
    superficie = documento.superficie(obligacion)
    ini, fin = documento.spans()[obligacion]
    ruido = " RUIDO FUERA DE SUPERFICIE: " + " ".join(reversed(list(fragmentos))) + " . "
    nuevo = documento.plano[:ini] + ruido + superficie + documento.plano[fin:]
    return Sujeto(nuevo, {obligacion: _rearmar(nuevo, superficie, "con-ruido-antes")},
                  "con-ruido-antes")


def alterado_dentro(documento, obligacion, viejo, nuevo_texto):
    """Mutante: altera la superficie misma que la comprobacion lee."""
    superficie = documento.superficie(obligacion)
    if viejo not in superficie:
        raise ValueError("el mutante de %s no toca su superficie" % obligacion)
    superficie_mutada = superficie.replace(viejo, nuevo_texto, 1)
    ini, fin = documento.spans()[obligacion]
    nuevo = documento.plano[:ini] + superficie_mutada + documento.plano[fin:]
    return Sujeto(nuevo, {obligacion: _rearmar(nuevo, superficie_mutada, "mutante")}, "mutante")
