"""Ayudante de sondeo del pre-vuelo.

Una sonda de resolubilidad resuelve exactamente una identidad Git y no devuelve el contenido del
objeto: `cat-file -e` informa por codigo de retorno y no emite el objeto. Esa es la diferencia
entre resolver y leer.

Este modulo no importa nada de la corrida.
"""

import subprocess


def comando(repo, sha):
    return ["git", "-C", repo, "cat-file", "-e", sha + "^{object}"]


def resolver(repo, sha):
    """True si la identidad resuelve en ese repositorio. No devuelve contenido."""
    r = subprocess.run(comando(repo, sha),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0
