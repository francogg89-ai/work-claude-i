"""Pre-vuelo X0: resolubilidad de las vinculaciones congeladas, y nada mas.

Estrictamente anterior a INICIO. No lee el candidato, no ejecuta casos, no evalua criterios y no
observa material de la corrida.

El resultado de cada vinculacion es un booleano de alcanzabilidad. Ninguna tupla lleva un campo
donde el valor de una referencia pueda viajar: R1 pregunta si esta, no que dice.

Este modulo importa unicamente su ayudante de sondeo.
"""

import sondas


def ejecutar(vinculaciones):
    """[(nombre, clase, repo, arg)] -> [(nombre, clase, repo, arg, resuelve)].

    clase 'local'  -> arg es un SHA
    clase 'remota' -> arg es (remoto, ref)
    """
    resultado = []
    for nombre, clase, repo, arg in vinculaciones:
        if clase == "local":
            ok = sondas.resolver_local(repo, arg)
        elif clase == "remota":
            ok = sondas.resolver_remota(repo, arg[0], arg[1])
        else:
            raise RuntimeError("clase de vinculacion no declarada: %s" % clase)
        resultado.append((nombre, clase, repo, arg, ok))
    return resultado


def irresolubles(resultado):
    return [(n, c, r, a) for n, c, r, a, ok in resultado if not ok]


def solo_booleanos(resultado):
    """True si ningun elemento del resultado transporta algo distinto de un booleano."""
    return all(isinstance(fila[4], bool) and len(fila) == 5 for fila in resultado)
