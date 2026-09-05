"""Sondas de resolucion. Resuelven identidades; no leen contenido.

```text
sonda local    resuelve un objeto en un clon y no devuelve su contenido
sonda remota   resuelve una referencia en un remoto y devuelve solo si existe
```

Ambas devuelven un booleano. Ninguna devuelve, guarda ni transporta el valor que resolvio.
"""

import subprocess


def _correr(argv):
    return subprocess.run(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def resolver_local(repo, sha):
    """R1 no aplica aca: es disco. `cat-file -e` responde existe / no existe."""
    return _correr(["git", "-C", repo, "cat-file", "-e", sha + "^{object}"]) == 0


def resolver_remota(repo, remoto, ref):
    """R1. `ls-remote --exit-code` responde existe / no existe, con el valor descartado."""
    return _correr(["git", "-C", repo, "ls-remote", "--exit-code", remoto, ref]) == 0
