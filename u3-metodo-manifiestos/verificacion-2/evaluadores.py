"""Evaluadores puros. Cada uno decide un criterio a partir de observaciones ya recogidas.

Son puros a proposito: la corrida real los alimenta con lo que observo, y los controles negativos
los alimentan con observaciones sinteticas. Asi un control puede demostrar que un criterio sabe
fallar sin obligar al mecanismo a fallar de verdad —sin una tercera interaccion de red, sin
escribir en la bitacora de la unidad y sin tocar el candidato.
"""

import os

CALIFICACION = "calificacion"
CONTROL = "control"


def _sumar(fallos, codigo, detalle):
    fallos.setdefault(codigo, []).append(detalle)


# -- regla de identidad del control: E29, E30, E31 / F31, F32, F33 ------------

def evaluar_atadura(registros, identidades_registradas):
    """Ata cada control a la comprobacion efectiva que califico al candidato.

    `identidades_registradas` es lo declarado: sid -> identidad de su bloque de codigo.
    `registros` es lo observado: que se atraveso de verdad en cada invocacion.
    """
    fallos = {}
    calificacion = [r for r in registros if r["motivo"] == CALIFICACION]
    controles = [r for r in registros if r["motivo"] == CONTROL]

    for r in registros:
        esperada = identidades_registradas.get(r["sid_declarado"])
        if esperada is None or r["identidad"] != esperada:
            _sumar(fallos, "F33", (r["sid_declarado"], r["identidad"], esperada))

    por_obligacion = {}
    clases = {}
    for r in calificacion:
        por_obligacion.setdefault(r["obligacion"], set()).add(r["identidad"])
        clases.setdefault(r["obligacion"], set()).add(r["clase_observable"])

    for r in controles:
        if r["obligacion"] not in por_obligacion:
            _sumar(fallos, "F32", ("obligacion sin comprobacion real", r["obligacion"]))
            continue
        if r["identidad"] not in por_obligacion[r["obligacion"]]:
            _sumar(fallos, "F31", (r["sid_declarado"], r["obligacion"], r["identidad"]))
        if r["clase_observable"] not in clases[r["obligacion"]]:
            _sumar(fallos, "F31", ("otro observable", r["sid_declarado"], r["clase_observable"]))

    solo_control = ({r["identidad"] for r in controles} -
                    {r["identidad"] for r in calificacion})
    for identidad in sorted(map(repr, solo_control)):
        _sumar(fallos, "F32", ("comprobacion alcanzable solo desde controles", identidad))
    return fallos


# -- regla de alcance: E25, E26, E27 / F27, F28, F29 --------------------------

def evaluar_alcance(items, obligaciones_del_candidato):
    """`items`: {sid, superficie, tipo, obligacion, observable, variantes {nombre: observable}}."""
    fallos = {}
    for it in items:
        if not it["superficie"]:
            _sumar(fallos, "F27", (it["sid"], "sin superficie declarada"))
            continue
        if it["tipo"] == "documento" and it["obligacion"] not in obligaciones_del_candidato:
            _sumar(fallos, "F27", (it["sid"], "superficie ajena al candidato"))
        for nombre, observable in sorted(it["variantes"].items()):
            if observable != it["observable"]:
                _sumar(fallos, "F28", (it["sid"], nombre, it["observable"], observable))
    return fallos


def evaluar_discriminacion(items):
    """`items`: {sid, ok_mutante, obs_real, obs_mutante, extracto_real, extracto_mutante}."""
    fallos = {}
    for it in items:
        if it["ok_mutante"]:
            _sumar(fallos, "F7", (it["sid"], "el mutante no la hizo fallar"))
        if it["obs_real"] == it["obs_mutante"]:
            _sumar(fallos, "F8", (it["sid"], it["obs_real"]))
        if it["extracto_real"] == it["extracto_mutante"]:
            _sumar(fallos, "F29", (it["sid"], "el mutante no altero la superficie leida"))
    return fallos


def evaluar_conducta_prohibida(solo_nombra_ok, mantiene_ok):
    """E28 / F30: la prohibicion se mide por conducta, no por la ocurrencia lexica del nombre."""
    if solo_nombra_ok and not mantiene_ok:
        return {}
    return {"F30": [("solo nombra -> %s" % solo_nombra_ok, "mantiene -> %s" % mantiene_ok)]}


# -- X0, su frontera y su forma: E16..E19, E23, E24 / F18..F20, F24..F26 ------

def evaluar_conjunto_x0(nombres_resueltos, nominales):
    if tuple(nombres_resueltos) != tuple(nominales):
        return {"F25": [(list(nombres_resueltos), list(nominales))]}
    return {}


def evaluar_forma_x0(resuelto):
    impropios = sorted(n for n, v in resuelto.items() if not isinstance(v, bool))
    if impropios:
        return {"F26": [(n, type(resuelto[n]).__name__) for n in impropios]}
    return {}


def evaluar_traza_externa(invocaciones, aperturas, nominales, satisfechas):
    fallos = {}
    sin_cubrir = [n for n in nominales if n not in satisfechas]
    if sin_cubrir:
        _sumar(fallos, "F18", ("vinculaciones sin cubrir", sin_cubrir))
    for inv in invocaciones:
        if inv["clase"] == "no-sonda":
            _sumar(fallos, "F18", ("invocacion que no es sonda", inv["argv"]))
        if inv["devolvio_contenido"]:
            _sumar(fallos, "F18", ("la sonda devolvio contenido", inv["argv"]))
    for a in aperturas:
        _sumar(fallos, "F18", ("apertura de archivo en X0", a["archivo"]))
    return fallos


def evaluar_traza_interna(modulos_entrados, modulos_de_la_corrida):
    cruce = sorted(set(modulos_entrados) & set(modulos_de_la_corrida))
    return {"F19": [cruce]} if cruce else {}


def evaluar_imports(importados, modulos_de_la_corrida):
    cruce = sorted(set(importados) & set(modulos_de_la_corrida))
    return {"F20": [cruce]} if cruce else {}


def evaluar_frontera(invocaciones, remoto):
    """E23 / F24: exactamente dos interacciones remotas, R1 en X0 y R2 en el cuerpo."""
    fallos = {}
    remotas = [i for i in invocaciones if i["remota"]]
    fases = [i["fase"] for i in remotas]
    if fases != ["X0", "cuerpo"]:
        _sumar(fallos, "F24", ("fases de las interacciones remotas", fases))
    for i in remotas:
        if remoto not in i["argv"]:
            _sumar(fallos, "F24", ("remoto no declarado", i["argv"]))
    return fallos


# -- materia del candidato: E10, E11 / F11, F12 ------------------------------

def evaluar_descubrimiento(solapado, disjunto):
    """E10 / F11: procede con interseccion vacia y no procede con interseccion no vacia."""
    fallos = {}
    if solapado["procede"] or not solapado["interseccion"] or solapado["ruteo"] is None:
        _sumar(fallos, "F11", ("superficie solapada", solapado))
    if not disjunto["procede"] or disjunto["interseccion"]:
        _sumar(fallos, "F11", ("superficie disjunta", disjunto))
    return fallos


def evaluar_blob(leido, congelado):
    """E11 / F12: el candidato leido es exactamente el blob congelado."""
    return {} if leido == congelado else {"F12": [(leido, congelado)]}


# -- bitacora: E12, E13, E14, E21 / F13, F14, F15, F22 -----------------------

def evaluar_ruta_bitacora(ruta, raiz, constante, directorio_del_mecanismo):
    esperada = os.path.join(raiz, constante.replace("/", os.sep))
    fallos = {}
    if os.path.normcase(ruta) != os.path.normcase(esperada):
        _sumar(fallos, "F22", ("ruta distinta de la constante", ruta, esperada))
    if os.path.normcase(os.path.dirname(ruta)).startswith(
            os.path.normcase(directorio_del_mecanismo)):
        _sumar(fallos, "F22", ("ruta derivada del directorio del mecanismo", ruta))
    return fallos


def evaluar_bitacora(ajenas_antes, ajenas_despues, propias_despues, identidad):
    """E12, E13, E14 / F15. Las lineas de otras identidades no se cuentan y no se alteran."""
    fallos = {}
    if ajenas_antes != ajenas_despues:
        _sumar(fallos, "F15", ("lineas ajenas alteradas", len(ajenas_antes),
                               len(ajenas_despues)))
    inicios = [l for l in propias_despues if l.startswith("INICIO ")]
    cierres = [l for l in propias_despues if l.startswith("CIERRE ")]
    if len(inicios) != 1 or len(cierres) != 1:
        _sumar(fallos, "F15", ("INICIO=%d CIERRE=%d de %s" % (len(inicios), len(cierres),
                                                              identidad),))
    return fallos


# -- cobertura del candidato: E3, E4, E5 / F3, F5, F6 ------------------------

def evaluar_cobertura(obligaciones, ejercitadas):
    sin_caso = sorted(set(obligaciones) - set(ejercitadas))
    return {"F3": [sin_caso]} if sin_caso else {}


def evaluar_secciones(secciones, no_mecanicas, con_obligaciones):
    fallos = {}
    for numero in sorted(secciones):
        if numero in no_mecanicas:
            continue
        if numero not in con_obligaciones:
            _sumar(fallos, "F5", ("seccion sin obligacion y no declarada no mecanica", numero))
    return fallos


def evaluar_forma_secciones(defectos, no_mecanicas):
    fallos = {}
    for numero, detalle in defectos:
        if numero not in no_mecanicas:
            _sumar(fallos, "F6", (numero, detalle))
    return fallos


def fusionar(*conjuntos):
    salida = {}
    for c in conjuntos:
        for codigo, detalles in c.items():
            salida.setdefault(codigo, []).extend(detalles)
    return salida
