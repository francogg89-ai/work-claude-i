"""Intercepcion. Lo que este modulo produce son observaciones, no declaraciones.

Tres observadores, con propositos distintos:

```text
Externa    intercepta subprocess.run y builtins.open. Da la traza externa de X0 y la frontera
           de red de toda la corrida, con la fase en que ocurrio cada interaccion
Interna    intercepta las llamadas de X0 con sys.settrace y dice a que archivos entro
Travesia   intercepta las llamadas de una comprobacion y dice que codigo se atraveso
```

`Travesia` es lo que vuelve observable, y no declarada, la identidad de la comprobacion que un
control ejercita: la identidad es el primer bloque de codigo en el que entro la invocacion.
"""

import builtins
import os
import subprocess
import sys

REMOTAS = ("ls-remote", "fetch", "push", "clone", "pull")


def es_remota(argv):
    return any(a in REMOTAS for a in argv)


def clase_de_sonda(argv):
    if "cat-file" in argv:
        return "sonda-local"
    if "ls-remote" in argv:
        return "sonda-remota"
    return "no-sonda"


class Externa(object):
    """Registra toda invocacion de subprocess.run y toda apertura de archivo, con su fase."""

    def __init__(self):
        self.invocaciones = []
        self.aperturas = []
        self.fase = "previa"
        self._run = None
        self._open = None
        self._vigilar_archivos = False

    def _envolver_run(self, real):
        def run(argv, *a, **kw):
            registro = {"fase": self.fase, "argv": list(argv), "remota": es_remota(argv),
                        "clase": clase_de_sonda(argv), "devolvio_contenido": False}
            self.invocaciones.append(registro)
            res = real(argv, *a, **kw)
            salida = getattr(res, "stdout", None)
            registro["devolvio_contenido"] = bool(salida)
            return res
        return run

    def _envolver_open(self, real):
        def abrir(archivo, *a, **kw):
            if self._vigilar_archivos:
                self.aperturas.append({"fase": self.fase, "archivo": str(archivo)})
            return real(archivo, *a, **kw)
        return abrir

    def activar(self):
        self._run, subprocess.run = subprocess.run, self._envolver_run(subprocess.run)
        self._open, builtins.open = builtins.open, self._envolver_open(builtins.open)

    def desactivar(self):
        if self._run is not None:
            subprocess.run = self._run
        if self._open is not None:
            builtins.open = self._open

    def vigilar_archivos(self, valor):
        self._vigilar_archivos = valor

    def de_fase(self, fase):
        return [i for i in self.invocaciones if i["fase"] == fase]

    def remotas(self):
        return [i for i in self.invocaciones if i["remota"]]


class Interna(object):
    """Traza interna: a que archivos entro la ejecucion mientras estuvo activa."""

    def __init__(self):
        self.archivos = []
        self.llamadas = []

    def __enter__(self):
        def trazar(frame, evento, arg):
            if evento == "call":
                nombre = os.path.basename(frame.f_code.co_filename)
                self.archivos.append(nombre)
                self.llamadas.append((nombre, frame.f_code.co_name))
            return None
        sys.settrace(trazar)
        return self

    def __exit__(self, *e):
        sys.settrace(None)
        return False

    def modulos(self):
        return sorted({a[:-3] for a in self.archivos if a.endswith(".py")})


def clave(codigo):
    """Identidad observable de un bloque de codigo."""
    return (os.path.basename(codigo.co_filename), codigo.co_name, codigo.co_firstlineno)


class Travesia(object):
    """Observa que comprobacion se atraveso realmente, sin creerle a ninguna etiqueta."""

    def __init__(self, archivos):
        self.archivos = set(archivos)
        self.entradas = []

    def __enter__(self):
        def trazar(frame, evento, arg):
            if evento == "call":
                k = clave(frame.f_code)
                if k[0] in self.archivos:
                    self.entradas.append(k)
            return None
        sys.settrace(trazar)
        return self

    def __exit__(self, *e):
        sys.settrace(None)
        return False

    def identidad(self):
        """El primer bloque de codigo en el que entro: la comprobacion efectivamente ejercida."""
        return self.entradas[0] if self.entradas else None
