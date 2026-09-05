"""Bitacora append-only de la unidad, en la constante fija `BITACORA_PATH_UNIDAD`.

La ruta se compone con la raiz del repositorio y esa constante. No se deriva del directorio del
mecanismo: una bitacora que viviera junto al mecanismo se reiniciaria al crear un directorio
nuevo, y mover pasaria a ser indistinguible de reiniciar.
"""

import io
import os

INICIO = "INICIO"
CIERRE = "CIERRE"


def ruta_de_unidad(raiz_repo, constante):
    """Unica forma de obtener la ruta. `N24` alimenta la forma defectuosa al evaluador."""
    return os.path.join(raiz_repo, constante.replace("/", os.sep))


def leer(path):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding="utf-8") as fh:
        return [l.rstrip("\n") for l in fh if l.strip()]


def marca(evento, identidad, blob):
    return "%s %s %s" % (evento, identidad, blob)


def agregar(path, linea):
    with io.open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(linea + "\n")


def propias(lineas, identidad):
    return [l for l in lineas if identidad in l]


def ajenas(lineas, identidad):
    return [l for l in lineas if identidad not in l]


def tiene_inicio(lineas, identidad):
    return any(l.startswith(INICIO + " ") for l in propias(lineas, identidad))
