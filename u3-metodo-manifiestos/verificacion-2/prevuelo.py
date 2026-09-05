"""X0. Resuelve las vinculaciones congeladas que recibe y no comprueba ninguna otra cosa.

Recibe la lista literal desde afuera: no la elige, no la infiere y no la deriva escaneando SHAs.
No importa ningun modulo de la corrida, no lee el candidato y no abre archivos.

El resultado es un booleano por vinculacion nominal. No tiene campo donde un valor de referencia
pueda viajar.
"""

import sondas

NO_EJECUTABLE = "NO_EJECUTABLE"
EJECUTABLE = "EJECUTABLE"


def resolver(vinculaciones):
    """vinculaciones: [(nombre, clase, repo, *argumentos)] -> (estado, {nombre: bool})."""
    resuelto = {}
    for v in vinculaciones:
        nombre, clase, repo = v[0], v[1], v[2]
        if clase == "local":
            resuelto[nombre] = bool(sondas.resolver_local(repo, v[3]))
        elif clase == "remota":
            resuelto[nombre] = bool(sondas.resolver_remota(repo, v[3], v[4]))
        else:
            resuelto[nombre] = False
    estado = EJECUTABLE if all(resuelto.values()) else NO_EJECUTABLE
    return estado, resuelto


def irresolubles(resuelto):
    return sorted(n for n, ok in resuelto.items() if not ok)
