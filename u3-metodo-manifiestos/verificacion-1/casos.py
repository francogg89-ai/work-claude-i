"""Corpus de casos. Cada caso declara la obligacion del candidato que lo gobierna.

Dos formas:

```text
llamada       invoca el metodo con entradas explicitas y compara con el resultado que la
              obligacion predice
estructural   afirma una propiedad del mecanismo o del documento, y trae el mutante que debe
              hacerla fallar
```

El mecanismo no lee `esperado`: lo produce, y la comparacion es posterior.
"""

import re

import metodo

# -- entradas explicitas ------------------------------------------------------

PAQUETE_BASE = {
    "WORK_ID": "trabajo-x", "CARRIL": "A",
    "METHOD_REPO": "https://github.com/x/metodo",
    "METHOD_SHA": "a" * 40,
    "MANIFEST_REPO": "https://github.com/x/manifiestos",
    "MANIFEST_PATH": "manifiestos/trabajo-x/MANIFIESTO_TRABAJO.md",
    "MANIFEST_SHA": "b" * 40,
    "WORK_REPO": "https://github.com/x/work",
    "AUDIT_REPO": "https://github.com/x/audit",
    "SOURCE_REPOS": ["https://github.com/x/lecciones"],
    "ROOT_LOCAL": "C:\\x",
    "LOCAL_PATHS": {"WORK_REPO": "C:\\x\\work"},
    "ENTORNOS_RELEVANTES": ["GitHub remoto"],
    "CAPACIDADES_CONSTRUCTOR": ["escritura en work"],
    "CAPACIDADES_AUDITOR": ["escritura en audit"],
    "REFERENCIAS_SEGURAS_A_CREDENCIALES": ["TOKEN_FUDO -> variable de entorno FUDO_TOKEN"],
    "POLITICAS_DE_EJECUCION_INICIALES": ["reconstruir desde Git"],
}

PROJECT_CAMPOS = {"PROJECT_REPO": "https://github.com/x/manifiestos",
                  "PROJECT_PATH": "manifiestos/trabajo-x/PROJECT.md",
                  "PROJECT_SHA": "c" * 40}

RESPUESTAS_COMPLETAS = {
    "aprobacion": "explicita", "identidades_de_git": True, "tiene_project": True,
    "paquete": dict(PAQUETE_BASE, **PROJECT_CAMPOS),
}

RESPUESTAS_AISLADO = {
    "aprobacion": "explicita", "identidades_de_git": True, "tiene_project": False,
    "paquete": dict(PAQUETE_BASE),
}

CERRADAS = {c: "cerrado" for c in metodo.CIERRES_INTENCION + metodo.CIERRES_CONTEXTO}


def _sin(d, clave):
    x = dict(d)
    x["paquete"] = dict(d["paquete"])
    del x["paquete"][clave]
    return x


def _con(d, clave, valor):
    x = dict(d)
    x["paquete"] = dict(d["paquete"])
    x["paquete"][clave] = valor
    return x


def L(id_, obl, fn, esperado, negativo=None):
    return {"id": id_, "obligacion": obl, "tipo": "llamada", "fn": fn,
            "esperado": esperado, "negativo": negativo}


CASOS_LLAMADA = [
    # -- 2. la entrevista -----------------------------------------------------
    L("L01", "R-2-cierra",
      lambda ctx: sorted(metodo.pendientes_entrevista(
          {"aplicables": metodo.CIERRES_INTENCION, "objetivo": "x"})),
      sorted(c for c in metodo.CIERRES_INTENCION if c != "objetivo")),
    L("L02", "R-2-contexto",
      lambda ctx: sorted(metodo.pendientes_entrevista(
          {"aplicables": metodo.CIERRES_CONTEXTO, "entornos": "x"})),
      sorted(c for c in metodo.CIERRES_CONTEXTO if c != "entornos")),
    L("L03", "R-2-solo-lo-material",
      lambda ctx: metodo.preguntas_a_formular(dict(CERRADAS, aplicables=metodo.CIERRES_INTENCION)),
      []),
    L("L04", "R-2-no-repite",
      lambda ctx: metodo.preguntas_a_formular(
          {"aplicables": ("objetivo", "motivo"), "objetivo": "ya respondido"}),
      ["motivo"]),
    L("L05", "R-2-no-formulario",
      lambda ctx: metodo.preguntas_a_formular({"aplicables": ("objetivo",), "objetivo": "x"}),
      []),
    L("L06", "R-2-traduce", lambda ctx: metodo.traducir("alta criticidad", [])[1],
      "R-2-traduce"),

    # -- 3. aprobacion y publicacion ------------------------------------------
    L("L07", "R-3-no-publica", lambda ctx: metodo.publicar({})[1], "R-3-no-publica",
      negativo=None),
    L("L08", "R-3-no-silencio", lambda ctx: metodo.publicar({"aprobacion": "silencio"})[1],
      "R-3-no-silencio", negativo=None),
    L("L09", "R-3-orden", lambda ctx: metodo.orden_de_publicacion(True),
      ["publicar_manifiesto", "obtener_identidad_manifiesto", "publicar_project",
       "obtener_identidad_project", "producir_paquete"]),

    # -- 4. paquete de constitucion -------------------------------------------
    L("L10", "R-4-campos",
      lambda ctx: metodo.constituir(_sin(RESPUESTAS_COMPLETAS, "WORK_ID"))[1],
      "R-4-campos", negativo="N1"),
    L("L11", "R-4-project",
      lambda ctx: metodo.constituir(dict(RESPUESTAS_AISLADO,
                                         paquete=dict(PAQUETE_BASE, PROJECT_SHA="d" * 40)))[1],
      "R-4-project", negativo="N4"),
    L("L12", "R-4-aplicables",
      lambda ctx: metodo.constituir(_con(RESPUESTAS_COMPLETAS, "CARRIL", "PENDIENTE"))[1],
      "R-4-aplicables"),
    L("L13", "R-4-identidades",
      lambda ctx: metodo.constituir(_con(RESPUESTAS_COMPLETAS, "MANIFEST_SHA", "b" * 7))[1],
      "R-4-identidades", negativo="N2"),
    L("L14", "R-4-sin-secretos",
      lambda ctx: metodo.constituir(
          _con(RESPUESTAS_COMPLETAS, "REFERENCIAS_SEGURAS_A_CREDENCIALES",
               ["FUDO_TOKEN=abc123"]))[1],
      "R-4-sin-secretos", negativo="N3"),
    L("L15", "R-4-no-bootstrap",
      lambda ctx: metodo.es_bootstrap(metodo.constituir(RESPUESTAS_COMPLETAS)[0]), False),
    L("L16", "R-4-campos",
      lambda ctx: sorted(k for k in metodo.constituir(RESPUESTAS_AISLADO)[0]
                         if not k.startswith("_")),
      sorted(metodo.CAMPOS_OBLIGATORIOS)),

    # -- 5. politica periodica de relevo --------------------------------------
    L("L17", "R-5-opciones", lambda ctx: metodo.politica_relevo("otra")[1], "R-5-opciones"),
    L("L18", "R-5-sin-contadores",
      lambda ctx: metodo.politica_relevo("cada_n", persiste_contador=True)[1],
      "R-5-sin-contadores", negativo="N8"),
    L("L19", "R-5-constitucion",
      lambda ctx: metodo.politica_relevo("cada_n")[0]["vive_en"], "constitucion"),
    L("L20", "R-5-multiplos",
      lambda ctx: [metodo.corresponde_relevo(n, 10) for n in (10, 15, 20, 25, 30)],
      [True, False, True, False, True]),
    L("L21", "R-5-hechos",
      lambda ctx: metodo.derivar_cadencia(ctx["repo_work"], ctx["V3"]) > 0, True),
    L("L22", "R-5-derivacion",
      lambda ctx: metodo.derivar_cadencia(ctx["repo_work"], ctx["V4"]) >
                  metodo.derivar_cadencia(ctx["repo_work"], ctx["V3"]), True),
    L("L23", "R-5-uniforme",
      lambda ctx: metodo.derivar_cadencia(ctx["repo_work"], ctx["V1"]) >
                  metodo.derivar_cadencia(ctx["repo_work"], ctx["V4"]), True),

    # -- 6. PROJECT.md y concurrencia -----------------------------------------
    L("L24", "R-6-contrato", lambda ctx: metodo.validar_project(None)[1], "R-6-contrato"),
    L("L25", "R-6-contenido",
      lambda ctx: metodo.validar_project({"campo_inventado": 1})[1], "R-6-contenido"),
    L("L26", "R-6-prohibido",
      lambda ctx: metodo.validar_project({"ultimo_sha": "x"})[1], "R-6-prohibido",
      negativo="N7"),
    L("L27", "R-6-aislado",
      lambda ctx: metodo.validar_project({"PROJECT_ID": "p"}, aislado=True)[1], "R-6-aislado"),
    L("L28", "R-6-superficie", lambda ctx: metodo.declarar_superficie("r", [])[1],
      "R-6-superficie"),
    L("L29", "R-6-descubrimiento",
      lambda ctx: sorted(metodo.paths_modificados(ctx["repo_work"], ctx["V3"], ctx["V4"])),
      ["u3-metodo-manifiestos/EVENTO.md", "u3-metodo-manifiestos/METODO-MANIFIESTOS.md"]),
    L("L30", "R-6-no-presuncion",
      lambda ctx: metodo.descubrir(
          metodo.paths_modificados(ctx["repo_work"], ctx["V3"], ctx["V4"]),
          {"repo": "work", "paths": ("u3-metodo-manifiestos/",)})["procede"],
      False, negativo="N5"),
    L("L31", "R-6-no-presuncion",
      lambda ctx: metodo.descubrir(
          metodo.paths_modificados(ctx["repo_work"], ctx["V3"], ctx["V4"]),
          {"repo": "work", "paths": ("u1-contratos-transversales/",)})["procede"],
      True, negativo="N6"),
    L("L32", "R-6-rutea",
      lambda ctx: metodo.descubrir(
          metodo.paths_modificados(ctx["repo_work"], ctx["V3"], ctx["V4"]),
          {"repo": "work", "paths": ("u3-metodo-manifiestos/",)})["ruteo"] is not None,
      True),

    # -- 7. fuentes auxiliares ------------------------------------------------
    L("L33", "R-7-source-repos",
      lambda ctx: metodo.admitir_fuente({"repositorio": "r", "funcion": "f"})[1],
      "R-7-source-repos"),
    L("L34", "R-7-solo-lectura",
      lambda ctx: metodo.admitir_fuente({"repositorio": "r", "identidad": "i", "funcion": "f",
                                         "escritura": True})[1], "R-7-solo-lectura"),
    L("L35", "R-7-no-autoriza",
      lambda ctx: metodo.admitir_fuente({"repositorio": "r", "identidad": "i", "funcion": "f",
                                         "amplia_capacidad": True})[1], "R-7-no-autoriza",
      negativo="N10"),
    L("L36", "R-7-utilidad",
      lambda ctx: metodo.admitir_fuente({"repositorio": "r", "identidad": "i",
                                         "funcion": "f"})[0]["en"], "SOURCE_REPOS"),
]


# -- comprobaciones estructurales y de documento ------------------------------

def _acciones(s):
    return set(s["acciones"])


def _texto(s):
    return s["texto"]


def c_sin_acciones(prohibidas):
    def f(s, ctx):
        cruce = sorted(_acciones(s) & set(prohibidas))
        return not cruce, repr(cruce), "acciones prohibidas = %s" % cruce
    return f


def c_con_acciones(exigidas):
    def f(s, ctx):
        faltan = sorted(set(exigidas) - _acciones(s))
        return not faltan, repr(faltan), "acciones faltantes = %s" % faltan
    return f


def c_texto_contiene(fragmentos):
    def f(s, ctx):
        t = _texto(s)
        faltan = [x for x in fragmentos if x not in t]
        return not faltan, repr(faltan), "fragmentos ausentes = %s" % faltan
    return f


def c_texto_no_contiene(patron):
    def f(s, ctx):
        hallados = sorted(set(re.findall(patron, _texto(s))))
        return not hallados, repr(hallados), "hallados = %s" % hallados
    return f
