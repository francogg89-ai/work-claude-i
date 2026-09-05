"""Implementacion determinista de las obligaciones del candidato.

Implementa unicamente lo que el candidato declara. Los identificadores que este modulo emite en
sus rechazos deben existir en el candidato: el denominador de la cobertura lo aporta
`superficie.py`, leyendo el documento, y no esta lista.

No mantiene estado entre invocaciones. Las estructuras de modulo son constantes; ninguna funcion
las muta. `R-6-sin-registro` y `R-8-no-estado` se comprueban por conducta, observando eso.
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

POLITICAS_RELEVO = ("nunca", "solo_manual", "cada_n", "limites_de_unidad", "combinacion_definida")

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

ESTADO_DE_EJECUCION = (
    "unidad_actual", "ultima_entrega", "ultimo_auditor", "estado_del_loop", "work_sha_vigente",
    "audit_sha_vigente",
)

ACCIONES = frozenset({
    "ENTREVISTAR", "PROPONER", "REDACTAR", "SENALAR_CONTRADICCION", "SUGERIR",
    "PUBLICAR_MANIFIESTO", "OBTENER_IDENTIDAD", "PRODUCIR_PAQUETE",
})

CAMPOS_DE_TRANSPORTE_AGREGADOS = ()

SHA_EXACTO = re.compile(r"^[0-9a-f]{40}$")
REFERENCIA_SEGURA = re.compile(r"^\S+ -> variable de entorno \S+$")
VALOR_SECRETO = re.compile(r"(?i)(token|secret|password|api[_-]?key)\s*[=:]\s*\S+")


# -- 1. cadena del sistema ----------------------------------------------------

def referencias_externas():
    """R-1-referencias, R-1-sin-sha y R-8-no-circular: repositorio, path y contrato. Sin SHA.

    La forma del registro no tiene campo donde un SHA pueda viajar.
    """
    return (
        {"contrato": "CT-6", "repositorio": "manifiestos-trabajo-ai", "path": "README.md"},
        {"contrato": "CT-7", "repositorio": "reglas-orquestador-ai",
         "path": "REGLAS-ORQUESTADOR.md"},
    )


# -- 2. la entrevista ---------------------------------------------------------

def pendientes(respuestas):
    """R-2-cierra y R-2-contexto: que queda por cerrar, entre lo aplicable."""
    aplicables = respuestas.get("aplicables", CIERRES_INTENCION + CIERRES_CONTEXTO)
    return [c for c in aplicables if not respuestas.get(c)]


def preguntas(respuestas):
    """R-2-solo-lo-material, R-2-no-repite y R-2-no-formulario: solo lo pendiente y aplicable."""
    return pendientes(respuestas)


def traducir(categoria, obligaciones):
    """R-2-traduce: una categoria de entrevista solo vale traducida a obligaciones concretas."""
    if not obligaciones:
        return None, "R-2-traduce"
    return {"categoria": categoria, "obligaciones": tuple(obligaciones)}, None


# -- 3. aprobacion y publicacion ----------------------------------------------

def publicar(respuestas):
    """R-3-no-publica y R-3-no-silencio."""
    aprobacion = respuestas.get("aprobacion")
    if aprobacion == "explicita":
        return {"publicado": True}, None
    if aprobacion in ("silencio", "sin_objecion", "continuacion"):
        return None, "R-3-no-silencio"
    return None, "R-3-no-publica"


def orden_de_publicacion(tiene_project):
    """R-3-orden."""
    pasos = ["publicar_manifiesto", "obtener_identidad_manifiesto"]
    if tiene_project:
        pasos += ["publicar_project", "obtener_identidad_project"]
    return pasos + ["producir_paquete"]


# -- 4. el paquete de constitucion --------------------------------------------

def constituir(respuestas):
    """Devuelve (paquete, rechazo). El rechazo cita un identificador del candidato."""
    _, rechazo = publicar(respuestas)
    if rechazo:
        return None, rechazo

    datos = respuestas.get("paquete", {})
    tiene_project = bool(respuestas.get("tiene_project"))

    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in datos:
            return None, "R-4-campos"
        if datos[campo] in ("", None, [], {}, "PENDIENTE", "N/A"):
            return None, "R-4-aplicables"

    presentes = [c for c in CAMPOS_PROJECT if c in datos]
    if tiene_project and len(presentes) != len(CAMPOS_PROJECT):
        return None, "R-4-project"
    if not tiene_project and presentes:
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
    """R-4-no-bootstrap: el paquete es la entrada del bootstrap, no el bootstrap."""
    return "BOOTSTRAP" in paquete or paquete.get("_clase") == "bootstrap"


# -- 5. politica periodica de relevo ------------------------------------------

def politica_relevo(eleccion, persiste_contador=False):
    """R-5-pregunta, R-5-opciones, R-5-sin-contadores y R-5-constitucion.

    No hay politica por defecto: sin eleccion explicita se rechaza.
    """
    if persiste_contador:
        return None, "R-5-sin-contadores"
    if eleccion not in POLITICAS_RELEVO:
        return None, "R-5-opciones"
    return {"politica": eleccion, "vive_en": "constitucion"}, None


def derivar_cadencia(repo, corte):
    """R-5-derivacion. Unica funcion de derivacion del mecanismo.

    Cuenta el conjunto completo de commits alcanzables desde el corte exacto: sin recorrido por
    primer padre, sin filtro por path y sin leer mensajes de commit. `N9` ejercita esta misma
    funcion, y `E20` exige que no haya otra.
    """
    salida = subprocess.run(["git", "-C", repo, "rev-list", "--count", corte],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return int(salida.stdout.decode().strip())


def cadencia_por_primer_padre(repo, corte):
    """Contra-insumo de N9. Ningun camino real la usa: existe para que N9 tenga con que comparar."""
    salida = subprocess.run(["git", "-C", repo, "rev-list", "--count", "--first-parent", corte],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return int(salida.stdout.decode().strip())


def entregas_alcanzables(repo, corte):
    """R-5-hechos: una entrega es un commit alcanzable desde el corte. Misma derivacion."""
    return derivar_cadencia(repo, corte)


def corresponde_relevo(n, cadencia):
    """R-5-multiplos y R-5-uniforme: multiplos absolutos, sin excepcion por clase de entrega."""
    return cadencia > 0 and n % cadencia == 0


# -- 6. PROJECT.md y trabajos concurrentes ------------------------------------

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


def vigencia_remota(repo, remoto, referencia):
    """R-6-remoto y R2 de la frontera: la vigencia se obtiene del remoto, no de un clon local."""
    salida = subprocess.run(["git", "-C", repo, "ls-remote", remoto, referencia],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    partes = salida.stdout.decode().split()
    return partes[0] if partes else None


def paths_modificados(repo, origen, destino):
    salida = subprocess.run(["git", "-C", repo, "diff", "--name-only", origen, destino],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return [p for p in salida.stdout.decode().split("\n") if p.strip()]


def descubrir(paths, superficie_propia):
    """R-6-descubrimiento, R-6-no-presuncion, R-6-rutea, R-6-sin-registro y R-6-sha-constitutivo.

    Funcion de sus argumentos. No lee ni escribe registro alguno, no muta sus entradas y no
    guarda nada entre invocaciones.
    """
    interseccion = sorted(p for p in paths
                          if any(p.startswith(pref) for pref in superficie_propia["paths"]))
    if interseccion:
        return {"interseccion": interseccion, "procede": False,
                "ruteo": "el CONSTRUCTOR preserva y entrega; el AUDITOR determina"}
    return {"interseccion": [], "procede": True, "ruteo": None}


# -- 7. fuentes auxiliares ----------------------------------------------------

def admitir_fuente(fuente):
    """R-7-source-repos, R-7-solo-lectura, R-7-no-autoriza, R-7-capacidades y R-7-utilidad."""
    for campo in ("repositorio", "identidad", "funcion"):
        if not fuente.get(campo):
            return None, "R-7-source-repos"
    if fuente.get("escritura"):
        return None, "R-7-solo-lectura"
    if fuente.get("amplia_capacidad"):
        return None, "R-7-no-autoriza"
    return {"en": "SOURCE_REPOS", "fuente": dict(fuente)}, None


def capacidades(constitucion, decisiones_humanas, fuentes):
    """R-7-capacidades: se derivan de la constitucion mas las decisiones. Una fuente no amplia."""
    return sorted(set(constitucion) | set(decisiones_humanas))


def campos_de_transporte_agregados():
    """R-7-sin-campos: admitir fuentes auxiliares no agrega ningun campo al transporte."""
    return CAMPOS_DE_TRANSPORTE_AGREGADOS


# -- 8. lo que este metodo no hace --------------------------------------------

def acciones():
    """R-1-no-ejecuta, R-1-no-decide, R-8-* : el vocabulario es cerrado y no las contiene."""
    return set(ACCIONES)
