"""Pre-vuelo X0: resolubilidad de las identidades congeladas, y nada mas.

Estrictamente anterior a INICIO. No lee el candidato, no ejecuta casos, no evalua criterios y no
observa material de la corrida.

Este modulo importa unicamente su ayudante de sondeo. No importa candidato, corpus, orquestador,
estructurales, autoridad ni el cuerpo de la corrida, ni al cargarse ni dentro de sus funciones:
sin importarlos no puede alcanzarlos.
"""

import sondas


def ejecutar(identidades):
    """[(nombre, repo, sha)] -> [(nombre, repo, sha, resuelve)]. Una sonda por identidad."""
    resultado = []
    for nombre, repo, sha in identidades:
        resultado.append((nombre, repo, sha, sondas.resolver(repo, sha)))
    return resultado


def irresolubles(resultado):
    return [(n, r, s) for n, r, s, ok in resultado if not ok]
