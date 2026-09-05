"""Comprobaciones estructurales. Cada una declara la superficie material que lee.

```text
documento   lee la superficie de UNA obligacion: su linea etiquetada con sus continuaciones
conducta    lee UNA conducta del mecanismo, nombrada por su clave en el sujeto
```

Una comprobacion es una funcion propia, con su bloque de codigo propio. Esa es su identidad, y es
lo que `observador.Travesia` observa cuando un control la ejercita: por eso un control no puede
declarar que atraviesa `S01` y atravesar otra cosa.

Ninguna comprobacion de documento mira el documento entero. Ninguna comprobacion de prohibicion de
estado busca un nombre en la fuente: observa si el mecanismo lo mantiene o lo usa.
"""

import copy

DOCUMENTO = "documento"
CONDUCTA = "conducta"

ACCIONES_DE_EJECUCION = ("IMPLEMENTAR", "DESPLEGAR", "EJECUTAR_TRABAJO", "ESCRIBIR_CODIGO")
ACCIONES_DE_DECISION = ("DECIDIR_UNIDAD", "DECIDIR_NECESIDAD", "APROBAR_ENTREGA",
                        "OTORGAR_PERMISO", "DECLARAR_VEREDICTO")
ACCIONES_DE_RELEVO = ("DECIDIR_RELEVO", "CONTAR_ENTREGAS", "DERIVAR_CADENCIA_EN_TRANSPORTE")
ACCIONES_DE_MODELO = ("ELEGIR_MODELO", "SELECCIONAR_RUNTIME", "FIJAR_REGLAS_DE_COSTO")

ESTADO_DE_EJECUCION = ("unidad_actual", "ultima_entrega", "ultimo_auditor", "estado_del_loop",
                       "work_sha_vigente", "audit_sha_vigente")

ARCHIVO = "comprobaciones.py"


# -- utilidades leidas por las comprobaciones ---------------------------------

def _posiciones(texto, fragmentos):
    return [texto.find(f) for f in fragmentos]

def _ausentes(texto, fragmentos):
    return [f for f in fragmentos if f not in texto]

def _prohibidas(acciones, familia):
    return sorted(set(acciones) & set(familia))

def _faltantes(acciones, familia):
    return sorted(set(familia) - set(acciones))

def _huella_de_estado(fn):
    """Estado mutable que la funcion podria estar manteniendo: globales y celdas de clausura."""
    mutables = []
    for nombre, valor in sorted(getattr(fn, "__globals__", {}).items()):
        if isinstance(valor, (dict, list, set)):
            mutables.append((nombre, repr(sorted(map(repr, valor)))))
    for i, celda in enumerate(getattr(fn, "__closure__", None) or ()):
        try:
            valor = celda.cell_contents
        except ValueError:
            continue
        if isinstance(valor, (dict, list, set)):
            mutables.append(("celda-%d" % i, repr(sorted(map(repr, valor)))))
    return mutables

def _ejercer_descubrimiento(fn, registro_aperturas):
    """Invoca dos veces con las mismas entradas y observa que quedo del otro lado."""
    antes = _huella_de_estado(fn)
    marca = len(registro_aperturas)
    paths = ["comun/a.md", "propio/b.md"]
    superficie = {"repo": "r", "paths": ("propio/",)}
    fn(list(paths), copy.deepcopy(superficie))
    fn(list(paths), copy.deepcopy(superficie))
    return antes, _huella_de_estado(fn), registro_aperturas[marca:]

def _sha_aparente(valor):
    texto = str(valor)
    return len(texto) == 40 and all(c in "0123456789abcdef" for c in texto)


# -- 1. cadena del sistema ----------------------------------------------------

def c_S01(sujeto, ctx):
    """R-1-cadena: los cinco eslabones, en orden, dentro de la obligacion que los enuncia."""
    texto = sujeto.superficie("R-1-cadena")
    posiciones = _posiciones(texto, ctx["cadena"])
    ok = all(p >= 0 for p in posiciones) and posiciones == sorted(posiciones)
    return ok, posiciones


def c_S02(sujeto, ctx):
    """R-1-no-sustituye."""
    texto = sujeto.superficie("R-1-no-sustituye")
    ausentes = _ausentes(texto, ctx["no_sustituye"])
    return not ausentes, ausentes


def c_S03(sujeto, ctx):
    """R-1-no-amplia."""
    texto = sujeto.superficie("R-1-no-amplia")
    ausentes = _ausentes(texto, ctx["no_amplia"])
    return not ausentes, ausentes


def c_S04(sujeto, ctx):
    """R-1-no-ejecuta: el vocabulario de acciones no contiene ninguna de ejecucion."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_EJECUCION)
    return not cruce, cruce


def c_S05(sujeto, ctx):
    """R-1-no-decide: el vocabulario no contiene ninguna accion de decision de ejecucion."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_DECISION)
    return not cruce, cruce


def c_S06(sujeto, ctx):
    """R-1-referencias: CT-6 y CT-7 localizables por repositorio, path y contrato."""
    texto = sujeto.superficie("R-1-referencias")
    ausentes = _ausentes(texto, ctx["referencias"])
    return not ausentes, ausentes


def c_S07(sujeto, ctx):
    """R-1-sin-sha: las referencias que el mecanismo emite no llevan SHA ni campo donde ponerlo."""
    entradas = sujeto["referencias"]()
    con_sha = sorted(k for e in entradas for k, v in e.items() if _sha_aparente(v))
    campos = sorted({k for e in entradas for k in e})
    return not con_sha, (con_sha, campos)


# -- 2 y 3. entrevista, aprobacion --------------------------------------------

def c_S08(sujeto, ctx):
    """R-2-alternativas: proponer alternativas esta entre lo que el metodo puede hacer."""
    faltan = _faltantes(sujeto["acciones"], ("PROPONER",))
    return not faltan, faltan


def c_S09(sujeto, ctx):
    """R-3-puede: entrevistar, proponer, redactar, senalar contradicciones y sugerir."""
    faltan = _faltantes(sujeto["acciones"],
                        ("ENTREVISTAR", "PROPONER", "REDACTAR", "SENALAR_CONTRADICCION",
                         "SUGERIR"))
    return not faltan, faltan


# -- 5. politica periodica de relevo ------------------------------------------

def c_S10(sujeto, ctx):
    """R-5-pregunta: no hay politica por defecto; sin eleccion explicita se rechaza."""
    rechazo = sujeto["politica_relevo"](None)[1]
    return rechazo == "R-5-opciones", rechazo


def c_S11(sujeto, ctx):
    """R-5-no-orquestador: el vocabulario no contiene contar, derivar ni decidir relevos."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_RELEVO)
    return not cruce, cruce


# -- 6. PROJECT.md y concurrencia ---------------------------------------------

def c_S12(sujeto, ctx):
    """R-6-remoto: la vigencia se obtuvo del remoto declarado, no de un clon local."""
    argv = sujeto["vigencia"]["argv"]
    ok = "ls-remote" in argv and ctx["remoto"] in argv and "rev-parse" not in argv
    return ok, [a for a in argv if a in ("ls-remote", "rev-parse", ctx["remoto"])]


def c_S13(sujeto, ctx):
    """R-6-sin-registro: el descubrimiento no lleva registro. Conducta, no mencion del nombre."""
    antes, despues, aperturas = _ejercer_descubrimiento(sujeto["descubrir"], ctx["aperturas"])
    return (antes == despues and not aperturas), (antes != despues, [a for a in aperturas])


def c_S14(sujeto, ctx):
    """R-6-sha-constitutivo: consultar la vigencia no reescribe lo congelado."""
    paths = ["a/x.md", "b/y.md"]
    superficie = {"repo": "r", "paths": ("a/",)}
    original = (list(paths), dict(superficie))
    sujeto["descubrir"](paths, superficie)
    despues = (list(paths), dict(superficie))
    return original == despues, despues


# -- 7. fuentes auxiliares ----------------------------------------------------

def c_S15(sujeto, ctx):
    """R-7-capacidades: una fuente auxiliar no amplia las capacidades."""
    sin_fuente = sujeto["capacidades"](("leer",), ("escribir",), ())
    con_fuente = sujeto["capacidades"](("leer",), ("escribir",), ("skill-que-pide-mas",))
    return sin_fuente == con_fuente, (sin_fuente, con_fuente)


def c_S16(sujeto, ctx):
    """R-7-sin-campos: admitir fuentes no agrega campos al contrato de transporte."""
    antes = tuple(sujeto["campos_transporte"]())
    sujeto["admitir"]({"repositorio": "r", "identidad": "i", "funcion": "f"})
    despues = tuple(sujeto["campos_transporte"]())
    return antes == despues == (), (antes, despues)


# -- 8. lo que este metodo no hace --------------------------------------------

def c_S17(sujeto, ctx):
    """R-8-no-ejecuta."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_EJECUCION)
    return not cruce, cruce


def c_S18(sujeto, ctx):
    """R-8-no-reemplaza."""
    texto = sujeto.superficie("R-8-no-reemplaza")
    ausentes = _ausentes(texto, ctx["no_reemplaza"])
    return not ausentes, ausentes


def c_S19(sujeto, ctx):
    """R-8-no-decide."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_DECISION)
    return not cruce, cruce


def c_S20(sujeto, ctx):
    """R-8-no-estado: el paquete producido no lleva estado de ejecucion del trabajo."""
    paquete = sujeto["constituir"](ctx["respuestas"])[0] or {}
    cruce = sorted(set(paquete) & set(ESTADO_DE_EJECUCION))
    return not cruce, cruce


def c_S21(sujeto, ctx):
    """R-8-no-circular: las dependencias se declaran por repositorio, path y contrato."""
    entradas = sujeto["referencias"]()
    con_sha = sorted(k for e in entradas for k, v in e.items() if _sha_aparente(v))
    por_contrato = all({"repositorio", "path", "contrato"} <= set(e) for e in entradas)
    return (not con_sha) and por_contrato, (con_sha, por_contrato)


def c_S22(sujeto, ctx):
    """R-8-no-modelo: el vocabulario no contiene elegir modelo, runtime ni reglas de costo."""
    cruce = _prohibidas(sujeto["acciones"], ACCIONES_DE_MODELO)
    return not cruce, cruce
