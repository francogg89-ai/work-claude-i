"""Bitácora append-only de la unidad.

Una sola bitácora para U2, compartida por todos los contratos. Su ruta es una constante de la
unidad, relativa al repositorio, y no se deriva del directorio del mecanismo: una bitácora que
viviera junto al mecanismo se reiniciaría al crear un directorio nuevo, y mover pasaría a ser
indistinguible de reiniciar.

Todo criterio se califica exclusivamente sobre las líneas de la identidad congelada. Las líneas
de otras identidades no se cuentan y deben quedar byte a byte.
"""

import io
import os

# Constante de unidad. No se deriva de este archivo ni de su directorio.
RUTA_RELATIVA = "u2-reglas-orquestador/BITACORA.txt"

CONTRATO = "audit-chatgpt-i@e7894d2d65b0d35cadd04987420a15522a5ce93d"
CANDIDATO = "b871240fd38d28430fc86fc4b14f1b851dad1f10"


def ruta_real(repo_work):
    return os.path.join(repo_work, RUTA_RELATIVA)


def leer(ruta):
    if not os.path.exists(ruta):
        return []
    with io.open(ruta, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f if l.strip()]


def linea(evento, ident):
    return "%-6s %s %s" % (evento, ident["contrato"], ident["candidato"])


def agregar(evento, ruta, ident):
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)
    with io.open(ruta, "a", encoding="utf-8", newline="\n") as f:
        f.write(linea(evento, ident) + "\n")


def propias(lineas, ident):
    marcas = {linea("INICIO", ident), linea("CIERRE", ident)}
    return [l for l in lineas if l in marcas]


def ajenas(lineas, ident):
    marcas = {linea("INICIO", ident), linea("CIERRE", ident)}
    return [l for l in lineas if l not in marcas]


def hay_inicio_previo(ruta, ident):
    marca = linea("INICIO", ident)
    return any(l == marca for l in leer(ruta))


def coherente(ruta, ident):
    """(ok, detalle) tras el cierre: un INICIO y un CIERRE de esta identidad."""
    lineas = leer(ruta)
    i = sum(1 for l in lineas if l == linea("INICIO", ident))
    c = sum(1 for l in lineas if l == linea("CIERRE", ident))
    return (i == 1 and c == 1,
            "propias: INICIO=%d CIERRE=%d | ajenas=%d" % (i, c, len(ajenas(lineas, ident))))


def historia_intacta(previas, actuales, ident):
    """Las líneas de otras identidades presentes al abrir están byte a byte al cerrar."""
    antes = ajenas(previas, ident)
    despues = ajenas(actuales, ident)
    return antes == despues, "ajenas antes=%d despues=%d iguales=%s" % (
        len(antes), len(despues), antes == despues)
