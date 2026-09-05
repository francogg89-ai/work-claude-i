"""Ayudante de sondeo del pre-vuelo.

Dos clases de sonda, ambas de solo lectura y ninguna devuelve contenido del objeto:

```text
local   resuelve un objeto en un clon: cat-file -e informa por codigo de retorno
remota  resuelve una referencia en un remoto: ls-remote --exit-code informa si existe
```

La sonda remota devuelve unicamente si la referencia existe. Su valor no se lee aqui: obtenerlo
es conducta de P-C1, dentro del cuerpo.

Este modulo no importa nada de la corrida.
"""

import subprocess


def comando_local(repo, sha):
    return ["git", "-C", repo, "cat-file", "-e", sha + "^{object}"]


def comando_remoto(repo, remoto, ref):
    return ["git", "-C", repo, "ls-remote", "--exit-code", remoto, ref]


def resolver_local(repo, sha):
    r = subprocess.run(comando_local(repo, sha),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0


def resolver_remota(repo, remoto, ref):
    """True si la referencia existe en el remoto. No devuelve su valor."""
    r = subprocess.run(comando_remoto(repo, remoto, ref),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0
