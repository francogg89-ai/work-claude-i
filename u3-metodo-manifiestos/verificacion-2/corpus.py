"""Corpus de casos de llamada. Cada caso declara la obligacion del candidato que lo gobierna.

El caso invoca el constituyente con entradas explicitas y compara con el resultado que su
obligacion predice. El mecanismo no lee `predice`: lo produce, y la comparacion es posterior.

Las obligaciones que se cumplen conduciendose de cierto modo, y no devolviendo cierto valor, no
viven aca: viven en `comprobaciones.py`, que las observa por conducta.
"""

import inspect

import constituyente as C

PAQUETE_BASE = {
    "WORK_ID": "trabajo-x", "CARRIL": "A",
    "METHOD_REPO": "https://github.com/x/metodo", "METHOD_SHA": "a" * 40,
    "MANIFEST_REPO": "https://github.com/x/manifiestos",
    "MANIFEST_PATH": "manifiestos/trabajo-x/MANIFIESTO_TRABAJO.md", "MANIFEST_SHA": "b" * 40,
    "WORK_REPO": "https://github.com/x/work", "AUDIT_REPO": "https://github.com/x/audit",
    "SOURCE_REPOS": ["https://github.com/x/lecciones"], "ROOT_LOCAL": "C:\\x",
    "LOCAL_PATHS": {"WORK_REPO": "C:\\x\\work"}, "ENTORNOS_RELEVANTES": ["GitHub remoto"],
    "CAPACIDADES_CONSTRUCTOR": ["escritura en work"], "CAPACIDADES_AUDITOR": ["escritura en audit"],
    "REFERENCIAS_SEGURAS_A_CREDENCIALES": ["TOKEN_FUDO -> variable de entorno FUDO_TOKEN"],
    "POLITICAS_DE_EJECUCION_INICIALES": ["reconstruir desde Git"],
}

CAMPOS_PROJECT = {"PROJECT_REPO": "https://github.com/x/manifiestos",
                  "PROJECT_PATH": "manifiestos/trabajo-x/PROJECT.md", "PROJECT_SHA": "c" * 40}

CON_PROJECT = {"aprobacion": "explicita", "identidades_de_git": True, "tiene_project": True,
               "paquete": dict(PAQUETE_BASE, **CAMPOS_PROJECT)}

AISLADO = {"aprobacion": "explicita", "identidades_de_git": True, "tiene_project": False,
           "paquete": dict(PAQUETE_BASE)}

TODO_CERRADO = {c: "cerrado" for c in C.CIERRES_INTENCION + C.CIERRES_CONTEXTO}


def _sin(base, campo):
    x = dict(base)
    x["paquete"] = dict(base["paquete"])
    del x["paquete"][campo]
    return x


def _con(base, campo, valor):
    x = dict(base)
    x["paquete"] = dict(base["paquete"])
    x["paquete"][campo] = valor
    return x


class Caso(object):
    def __init__(self, ident, obligacion, invocar, predice, control=None):
        self.id = ident
        self.obligacion = obligacion
        self.invocar = invocar
        self.predice = predice
        self.control = control


def casos():
    return [
        # -- 2. la entrevista -------------------------------------------------
        Caso("L01", "R-2-cierra",
             lambda x: sorted(C.pendientes({"aplicables": C.CIERRES_INTENCION, "objetivo": "y"})),
             sorted(c for c in C.CIERRES_INTENCION if c != "objetivo")),
        Caso("L02", "R-2-contexto",
             lambda x: sorted(C.pendientes({"aplicables": C.CIERRES_CONTEXTO, "entornos": "y"})),
             sorted(c for c in C.CIERRES_CONTEXTO if c != "entornos")),
        Caso("L03", "R-2-solo-lo-material",
             lambda x: C.preguntas(dict(TODO_CERRADO, aplicables=C.CIERRES_INTENCION)), []),
        Caso("L04", "R-2-no-repite",
             lambda x: C.preguntas({"aplicables": ("objetivo", "motivo"), "objetivo": "resuelto"}),
             ["motivo"]),
        Caso("L05", "R-2-no-formulario",
             lambda x: C.preguntas({"aplicables": ("objetivo",), "objetivo": "resuelto"}), []),
        Caso("L06", "R-2-traduce", lambda x: C.traducir("alta criticidad", [])[1], "R-2-traduce"),

        # -- 3. aprobacion y publicacion --------------------------------------
        Caso("L07", "R-3-no-publica", lambda x: C.publicar({})[1], "R-3-no-publica"),
        Caso("L08", "R-3-no-silencio",
             lambda x: C.publicar({"aprobacion": "silencio"})[1], "R-3-no-silencio"),
        Caso("L09", "R-3-orden", lambda x: C.orden_de_publicacion(True),
             ["publicar_manifiesto", "obtener_identidad_manifiesto", "publicar_project",
              "obtener_identidad_project", "producir_paquete"]),

        # -- 4. el paquete de constitucion ------------------------------------
        Caso("L10", "R-4-campos", lambda x: C.constituir(_sin(CON_PROJECT, "WORK_ID"))[1],
             "R-4-campos", control="N1"),
        Caso("L11", "R-4-campos",
             lambda x: sorted(k for k in C.constituir(AISLADO)[0] if not k.startswith("_")),
             sorted(C.CAMPOS_OBLIGATORIOS)),
        Caso("L12", "R-4-project",
             lambda x: C.constituir(dict(AISLADO,
                                         paquete=dict(PAQUETE_BASE, PROJECT_SHA="d" * 40)))[1],
             "R-4-project", control="N4"),
        Caso("L13", "R-4-aplicables",
             lambda x: C.constituir(_con(CON_PROJECT, "CARRIL", "PENDIENTE"))[1],
             "R-4-aplicables"),
        Caso("L14", "R-4-identidades",
             lambda x: C.constituir(_con(CON_PROJECT, "MANIFEST_SHA", "b" * 7))[1],
             "R-4-identidades", control="N2"),
        Caso("L15", "R-4-sin-secretos",
             lambda x: C.constituir(_con(CON_PROJECT, "REFERENCIAS_SEGURAS_A_CREDENCIALES",
                                         ["FUDO_TOKEN=abc123"]))[1],
             "R-4-sin-secretos", control="N3"),
        Caso("L16", "R-4-no-bootstrap",
             lambda x: C.es_bootstrap(C.constituir(CON_PROJECT)[0]), False),

        # -- 5. politica periodica de relevo ----------------------------------
        Caso("L17", "R-5-opciones", lambda x: C.politica_relevo("otra")[1], "R-5-opciones"),
        Caso("L18", "R-5-sin-contadores",
             lambda x: C.politica_relevo("cada_n", persiste_contador=True)[1],
             "R-5-sin-contadores", control="N8"),
        Caso("L19", "R-5-constitucion",
             lambda x: C.politica_relevo("cada_n")[0]["vive_en"], "constitucion"),
        Caso("L20", "R-5-multiplos",
             lambda x: [C.corresponde_relevo(n, 10) for n in (10, 15, 20, 25, 30)],
             [True, False, True, False, True]),
        Caso("L21", "R-5-hechos",
             lambda x: C.entregas_alcanzables(x["repo"], x["V3"]) ==
                       C.derivar_cadencia(x["repo"], x["V3"]) > 0, True),
        Caso("L22", "R-5-derivacion",
             lambda x: C.derivar_cadencia(x["repo"], x["V4"]) >
                       C.derivar_cadencia(x["repo"], x["V3"]), True),
        Caso("L23", "R-5-uniforme",
             lambda x: sorted(inspect.signature(C.derivar_cadencia).parameters) +
                       sorted(inspect.signature(C.corresponde_relevo).parameters),
             ["corte", "repo", "cadencia", "n"]),

        # -- 6. PROJECT.md y trabajos concurrentes ----------------------------
        Caso("L24", "R-6-contrato", lambda x: C.validar_project(None)[1], "R-6-contrato"),
        Caso("L25", "R-6-contenido",
             lambda x: C.validar_project({"campo_inventado": 1})[1], "R-6-contenido"),
        Caso("L26", "R-6-prohibido",
             lambda x: C.validar_project({"ultimo_sha": "x"})[1], "R-6-prohibido", control="N7"),
        Caso("L27", "R-6-aislado",
             lambda x: C.validar_project({"PROJECT_ID": "p"}, aislado=True)[1], "R-6-aislado"),
        Caso("L28", "R-6-superficie",
             lambda x: C.declarar_superficie("r", [])[1], "R-6-superficie"),
        Caso("L29", "R-6-descubrimiento",
             lambda x: sorted(C.paths_modificados(x["repo"], x["V3"], x["V4"])),
             ["u3-metodo-manifiestos/EVENTO.md", "u3-metodo-manifiestos/METODO-MANIFIESTOS.md"]),
        Caso("L30", "R-6-no-presuncion",
             lambda x: C.descubrir(C.paths_modificados(x["repo"], x["V3"], x["V4"]),
                                   x["superficie_solapada"])["procede"], False, control="N5"),
        Caso("L31", "R-6-no-presuncion",
             lambda x: C.descubrir(C.paths_modificados(x["repo"], x["V3"], x["V4"]),
                                   x["superficie_disjunta"])["procede"], True, control="N6"),
        Caso("L32", "R-6-rutea",
             lambda x: C.descubrir(C.paths_modificados(x["repo"], x["V3"], x["V4"]),
                                   x["superficie_solapada"])["ruteo"] is not None, True),

        # -- 7. fuentes auxiliares --------------------------------------------
        Caso("L33", "R-7-source-repos",
             lambda x: C.admitir_fuente({"repositorio": "r", "funcion": "f"})[1],
             "R-7-source-repos"),
        Caso("L34", "R-7-solo-lectura",
             lambda x: C.admitir_fuente({"repositorio": "r", "identidad": "i", "funcion": "f",
                                         "escritura": True})[1], "R-7-solo-lectura"),
        Caso("L35", "R-7-no-autoriza",
             lambda x: C.admitir_fuente({"repositorio": "r", "identidad": "i", "funcion": "f",
                                         "amplia_capacidad": True})[1], "R-7-no-autoriza",
             control="N10"),
        Caso("L36", "R-7-utilidad",
             lambda x: C.admitir_fuente({"repositorio": "r", "identidad": "i",
                                         "funcion": "f"})[0]["en"], "SOURCE_REPOS"),
    ]
