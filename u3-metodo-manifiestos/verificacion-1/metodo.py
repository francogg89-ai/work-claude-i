"""Implementacion determinista de las obligaciones del candidato METODO-MANIFIESTOS.md.

Implementa unicamente lo que el candidato declara. Los identificadores que emite deben existir en
el candidato: el denominador de la cobertura lo aporta `candidato.py`, no este modulo.
"""

import re
import subprocess

# -- vocabulario cerrado ------------------------------------------------------

CAMPOS_OBLIGATORIOS = (
    "WORK_ID", "CARRIL", "METHOD_REPO", "METHOD_SHA", "MANIFEST_REPO", "MANIFEST_PATH",
    "MANIFEST_SHA", "WORK_REPO", "AUDIT_REPO", "SOURCE_REPOS", "ROOT_LOCAL", "LOCAL_PATHS",
    "ENTORNOS_RELEVANTES", "CAPACIDADES_CONSTRUCTOR", "CAPACIDADES_AUDITOR",
    "REFERENCIAS_SEGURAS_A_CREDENCIALES", "POLITICAS_DE_EJECUCION_INICIALES",
)

CAMPOS_PROJECT = ("PROJECT_REPO", "PROJECT_PATH", "PROJECT_SHA")

CAMPOS_SHA = ("METHOD_SHA", "MANIFEST_SHA", "PROJECT_SHA")

CIERRES_INTENCION = (
    "objetivo", "motivo", "resultado_observable", "alcance", "exclusiones", "restricciones",
    "riesgos", "criterios_exito", "decisiones_delegadas", "decisiones_reservadas",
)

CIERRES_CONTEXTO = (
    "proyecto", "repositorios", "entornos", "capacidades", "evidencia_y_rigor",
    "reproducibilidad", "politicas_relevo",
)

POLITICAS_RELEVO_SOPORTADAS = (
    "nunca", "solo_manual", "cada_n", "limites_de_unidad", "combinacion_definida",
)

PROJECT_PERMITIDO = (
    "PROJECT_ID", "identidad", "repositorios", "superficies_compartidas", "entornos",
    "limites_integracion", "recursos_protegidos", "superficie_afectable",
    "superficie_no_afectable", "coexistencia", "reglas_concurrencia", "reglas_integracion",
    "criterio_solapamiento", "autoridad_conflictos",
)

PROJECT_PROHIBIDO = (
    "trabajo_activo", "trabajo_terminado", "ultimo_sha", "ultimo_despliegue", "ultimo_actor",
    "locks", "semaforos", "contadores", "lista_de_carriles",
)

CONTADORES_PROHIBIDOS = (
    "CONSTRUCTOR_COUNT", "AUDITOR_COUNT", "relay_pending",
)

# Este metodo no decide nada de esto. El vocabulario es cerrado y no los contiene.
ACCIONES = frozenset({
    "ENTREVISTAR", "PROPONER", "REDACTAR", "SENALAR_CONTRADICCION", "SUGERIR",
    "PUBLICAR_MANIFIESTO", "OBTENER_IDENTIDAD", "PRODUCIR_PAQUETE",
})

SHA_EXACTO = re.compile(r"^[0-9a-f]{40}$")
REFERENCIA_SEGURA = re.compile(r"^\S+ -> variable de entorno \S+$")
VALOR_SECRETO = re.compile(r"(?i)(token|secret|password|api[_-]?key)\s*[=:]\s*\S+")


# -- entrevista ---------------------------------------------------------------

def pendientes_entrevista(respuestas):
    """R-2-cierra y R-2-contexto: que falta cerrar, entre lo aplicable."""
    aplicables = respuestas.get("aplicables", CIERRES_INTENCION + CIERRES_CONTEXTO)
    return [c for c in aplicables if not respuestas.get(c)]


def preguntas_a_formular(respuestas):
    """R-2-solo-lo-material y R-2-no-repite: solo lo pendiente y aplicable."""
    return pendientes_entrevista(respuestas)


def traducir(categoria, obligaciones):
    """R-2-traduce: una categoria de entrevista solo vale traducida a obligaciones."""
    if not obligaciones:
        return None, "R-2-traduce"
    return {"categoria": categoria, "obligaciones": tuple(obligaciones)}, None


# -- aprobacion y publicacion -------------------------------------------------

def publicar(respuestas):
    """R-3-no-publica y R-3-no-silencio."""
    aprobacion = respuestas.get("aprobacion")
    if aprobacion != "explicita":
        return None, "R-3-no-silencio" if aprobacion in ("silencio", "sin_objecion",
                                                         "continuacion") else "R-3-no-publica"
    return {"publicado": True}, None


def orden_de_publicacion(tiene_project):
    """R-3-orden."""
    pasos = ["publicar_manifiesto", "obtener_identidad_manifiesto"]
    if tiene_project:
        pasos += ["publicar_project", "obtener_identidad_project"]
    pasos.append("producir_paquete")
    return pasos


# -- paquete de constitucion --------------------------------------------------

def constituir(respuestas):
    """Devuelve (paquete, rechazo). El rechazo cita una obligacion del candidato."""
    ok, rechazo = publicar(respuestas)
    if rechazo:
        return None, rechazo

    datos = respuestas.get("paquete", {})
    tiene_project = bool(respuestas.get("tiene_project"))

    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in datos:
            return None, "R-4-campos"
        valor = datos[campo]
        if valor in ("", None, [], {}, "PENDIENTE", "N/A"):
            return None, "R-4-aplicables"

    presentes_project = [c for c in CAMPOS_PROJECT if c in datos]
    if tiene_project and len(presentes_project) != len(CAMPOS_PROJECT):
        return None, "R-4-project"
    if not tiene_project and presentes_project:
        return None, "R-4-project"

    if not respuestas.get("identidades_de_git"):
        return None, "R-4-identidades"
    for campo in CAMPOS_SHA:
        if campo in datos and not SHA_EXACTO.match(str(datos[campo])):
            return None, "R-4-identidades"

    for entrada in datos["REFERENCIAS_SEGURAS_A_CREDENCIALES"]:
        if not REFERENCIA_SEGURA.match(entrada):
            return None, "R-4-sin-secretos"
    for valor in datos.values():
        if VALOR_SECRETO.search(str(valor)):
            return None, "R-4-sin-secretos"

    paquete = dict(datos)
    paquete["_orden"] = tuple(orden_de_publicacion(tiene_project))
    return paquete, None


def es_bootstrap(paquete):
    """R-4-no-bootstrap: el paquete es entrada, no el bootstrap ni su sustituto."""
    return "BOOTSTRAP" in paquete or paquete.get("_clase") == "bootstrap"


# -- politica periodica de relevo ---------------------------------------------

def politica_relevo(eleccion, persiste_contador=False):
    """R-5-opciones y R-5-sin-contadores."""
    if persiste_contador:
        return None, "R-5-sin-contadores"
    if eleccion not in POLITICAS_RELEVO_SOPORTADAS:
        return None, "R-5-opciones"
    return {"politica": eleccion, "vive_en": "constitucion"}, None


def derivar_cadencia(repo, corte):
    """R-5-derivacion. Unica funcion de derivacion: cuenta el conjunto alcanzable completo.

    Sin recorrido por primer padre, sin filtro por path y sin leer mensajes de commit.
    """
    salida = subprocess.run(["git", "-C", repo, "rev-list", "--count", corte],
                            check=True, stdout=subprocess.PIPE).stdout.decode().strip()
    return int(salida)


def cadencia_por_primer_padre(repo, corte):
    """Derivacion defectuosa. Contra-insumo de N9: no la usa ningun camino real."""
    salida = subprocess.run(["git", "-C", repo, "rev-list", "--count", "--first-parent", corte],
                            check=True, stdout=subprocess.PIPE).stdout.decode().strip()
    return int(salida)


def corresponde_relevo(n, cadencia):
    """R-5-multiplos: multiplos absolutos, un relevo manual no reinicia."""
    return cadencia > 0 and n % cadencia == 0


# -- PROJECT.md y concurrencia ------------------------------------------------

def validar_project(project, aislado=False):
    """R-6-contrato, R-6-contenido, R-6-prohibido y R-6-aislado."""
    if aislado:
        return (None, "R-6-aislado") if project else (None, None)
    if not project:
        return None, "R-6-contrato"
    for clave in project:
        if clave in PROJECT_PROHIBIDO:
            return None, "R-6-prohibido"
        if clave not in PROJECT_PERMITIDO:
            return None, "R-6-contenido"
    return dict(project), None


def declarar_superficie(repo, paths):
    """R-6-superficie: repositorio mas conjunto de paths."""
    if not repo or not paths:
        return None, "R-6-superficie"
    return {"repo": repo, "paths": tuple(paths)}, None


def referencia_remota(repo, remoto, ref):
    """R2 de la frontera de red. P-C1: obtiene el valor vigente de la referencia."""
    salida = subprocess.run(["git", "-C", repo, "ls-remote", remoto, ref],
                            check=True, stdout=subprocess.PIPE).stdout.decode().split()
    return salida[0] if salida else None


def paths_modificados(repo, origen, destino):
    salida = subprocess.run(["git", "-C", repo, "diff", "--name-only", origen, destino],
                            check=True, stdout=subprocess.PIPE).stdout.decode().split("\n")
    return [p for p in salida if p.strip()]


def descubrir(paths, superficie):
    """R-6-descubrimiento, R-6-no-presuncion y R-6-rutea."""
    interseccion = sorted(p for p in paths
                          if any(p.startswith(pref) for pref in superficie["paths"]))
    if interseccion:
        return {"interseccion": interseccion, "procede": False,
                "ruteo": "el CONSTRUCTOR preserva y entrega; el AUDITOR determina"}
    return {"interseccion": [], "procede": True, "ruteo": None}


# -- fuentes auxiliares -------------------------------------------------------

def admitir_fuente(fuente):
    """R-7-source-repos, R-7-solo-lectura, R-7-no-autoriza y R-7-capacidades."""
    for campo in ("repositorio", "identidad", "funcion"):
        if not fuente.get(campo):
            return None, "R-7-source-repos"
    if fuente.get("escritura"):
        return None, "R-7-solo-lectura"
    if fuente.get("amplia_capacidad"):
        return None, "R-7-no-autoriza"
    return {"en": "SOURCE_REPOS", "fuente": dict(fuente)}, None
