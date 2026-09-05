"""Unica funcion de corrida. Aqui vive la guardia `X4`, y por aqui pasa toda invocacion.

La invocacion real y las invocaciones sinteticas de `N16` y `N17` atraviesan esta misma funcion.
`E15` lo exige y `observador.Travesia` lo observa: no alcanza con decir que la atraviesan.

```text
X1  lee la bitacora, busca INICIO de la identidad congelada y, si no lo hay, anota el suyo
X2  toda invocacion que anoto INICIO es una ejecucion observada, cualquiera sea su final
X4  si al abrir hay un INICIO previo de esta identidad, es un reintento: FALLO, sin anotar y
    sin evaluar criterios
T1  EXITO  anota CIERRE     T2  FALLO  anota CIERRE     T3  sin veredicto, no anota CIERRE
```
"""

import bitacora

REINTENTO = "REINTENTO"


def correr(ruta, identidad, blob, cuerpo):
    """`cuerpo` no recibe nada y devuelve (veredicto, datos). Una excepcion se resuelve como T2."""
    previas = bitacora.leer(ruta)
    ajenas_antes = bitacora.ajenas(previas, identidad)

    if bitacora.tiene_inicio(previas, identidad):
        return {"terminacion": REINTENTO, "veredicto": "FALLO", "anoto_inicio": False,
                "anoto_cierre": False, "evaluo_criterios": False, "criterios": {"F14": [True]},
                "datos": None, "ajenas_antes": ajenas_antes}

    bitacora.agregar(ruta, bitacora.marca(bitacora.INICIO, identidad, blob))

    try:
        veredicto, datos = cuerpo()
        excepcion = None
    except Exception as error:                                   # T2: excepcion capturada
        veredicto, datos, excepcion = "FALLO", None, repr(error)

    bitacora.agregar(ruta, bitacora.marca(bitacora.CIERRE, identidad, blob))

    terminacion = "T1" if veredicto == "EXITO" and excepcion is None else "T2"
    resultado = {"terminacion": terminacion, "veredicto": veredicto, "anoto_inicio": True,
                 "anoto_cierre": True, "evaluo_criterios": excepcion is None,
                 "criterios": {} if excepcion is None else {"F13": [excepcion]},
                 "datos": datos, "ajenas_antes": ajenas_antes}
    if excepcion is not None:
        resultado["excepcion"] = excepcion
    return resultado
