"""Intercepción de la conducta del pre-vuelo.

Las trazas se obtienen interceptando, nunca preguntándole a X0 qué hizo. Un pre-vuelo que se
auto-reportara sería otra comprobación incapaz de fallar.

Dos capas:

```text
externa   invocaciones de proceso y aperturas de archivo
interna   llamadas de función registradas por el intérprete
```
"""

import builtins
import subprocess
import sys

MODULOS_DE_LA_CORRIDA = frozenset({
    "candidato", "casos", "metodo", "estructurales", "verificar",
})


class Traza:
    def __init__(self):
        self.procesos = []
        self.archivos = []
        self.llamadas = []

    def modulos_llamados(self):
        return sorted({m for m, _ in self.llamadas})

    def llamadas_a_la_corrida(self):
        return sorted({(m, f) for m, f in self.llamadas if m in MODULOS_DE_LA_CORRIDA})


def observar(fn):
    """Ejecuta fn() bajo intercepción externa e interna. Devuelve (resultado, traza)."""
    traza = Traza()

    run_original = subprocess.run
    open_original = builtins.open

    def run_espia(cmd, *a, **k):
        traza.procesos.append(list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)])
        return run_original(cmd, *a, **k)

    def open_espia(*a, **k):
        traza.archivos.append(a[0] if a else None)
        return open_original(*a, **k)

    def tracer(frame, evento, arg):
        if evento == "call":
            modulo = frame.f_globals.get("__name__", "?")
            traza.llamadas.append((modulo, frame.f_code.co_name))
        return None

    subprocess.run = run_espia
    builtins.open = open_espia
    sys.settrace(tracer)
    try:
        resultado = fn()
    finally:
        sys.settrace(None)
        builtins.open = open_original
        subprocess.run = run_original
    return resultado, traza
