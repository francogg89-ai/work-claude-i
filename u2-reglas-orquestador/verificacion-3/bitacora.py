"""Bitácora append-only de la corrida.

Convierte X2, X4 y X5 en hechos comprobables. Una línea por evento, sólo se agrega.

```text
INICIO  <identidad de contrato>  <blob del candidato>
CIERRE  <identidad de contrato>  <blob del candidato>
```

La identidad de contrato es la del congelamiento: una corrida bajo otro contrato escribe otra
identidad y no colisiona con ésta.
"""

import io
import os

RUTA = "BITACORA.txt"

CONTRATO = "audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0"
CANDIDATO = "b871240fd38d28430fc86fc4b14f1b851dad1f10"


def leer(ruta=RUTA):
    if not os.path.exists(ruta):
        return []
    with io.open(ruta, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f if l.strip()]


def _linea(evento, contrato, candidato):
    return "%-6s %s %s" % (evento, contrato, candidato)


def agregar(evento, ruta=RUTA, contrato=CONTRATO, candidato=CANDIDATO):
    with io.open(ruta, "a", encoding="utf-8", newline="\n") as f:
        f.write(_linea(evento, contrato, candidato) + "\n")


def eventos(lineas, evento, contrato=CONTRATO, candidato=CANDIDATO):
    """Líneas que corresponden a ese evento para esta identidad exacta."""
    marca = _linea(evento, contrato, candidato)
    return [l for l in lineas if l == marca]


def hay_inicio_previo(ruta=RUTA, contrato=CONTRATO, candidato=CANDIDATO):
    return bool(eventos(leer(ruta), "INICIO", contrato, candidato))


def coherente(ruta=RUTA, contrato=CONTRATO, candidato=CANDIDATO):
    """(ok, detalle) tras el cierre: exactamente un INICIO y un CIERRE de esta identidad."""
    lineas = leer(ruta)
    inicios = len(eventos(lineas, "INICIO", contrato, candidato))
    cierres = len(eventos(lineas, "CIERRE", contrato, candidato))
    ajenas = [l for l in lineas
              if l not in (_linea("INICIO", contrato, candidato),
                           _linea("CIERRE", contrato, candidato))]
    ok = inicios == 1 and cierres == 1 and not ajenas
    return ok, "INICIO=%d CIERRE=%d ajenas=%d" % (inicios, cierres, len(ajenas))
