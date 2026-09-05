"""Controles negativos. Ninguno se ejerce contra el candidato real.

Dos familias, con la misma regla de identidad:

```text
sobre la materia    N1-N10   invocan el constituyente con insumos sinteticos
sobre el mecanismo  N11-N33  alimentan con observaciones sinteticas al mismo evaluador o a la
                             misma comprobacion que califico al candidato
```

Un control cambia el sujeto; no cambia la comprobacion. Los controles que ejercen una comprobacion
pasan por `registro.ejercer`, que observa cual se atraveso y deja ese registro en la evidencia.
Los que ejercen un criterio llaman al evaluador que ese criterio usa en la corrida real.
"""

import io
import os
import shutil
import subprocess
import tempfile

import comprobaciones as K
import constituyente as C
import corpus
import corrida
import evaluadores as EV
import observador
import prevuelo
import registro
import superficie


def _control(ident, espera, obtenido, discrimina, detalle=""):
    return {"id": ident, "espera": espera, "obtenido": obtenido,
            "discrimina": bool(discrimina), "detalle": detalle}


# -- N1 a N10: sobre la materia del candidato ---------------------------------

def sobre_la_materia(ctx):
    salida = []
    base = corpus.CON_PROJECT

    r = C.constituir(corpus._sin(base, "WORK_ID"))[1]
    salida.append(_control("N1", "R-4-campos", r, r == "R-4-campos"))

    r = C.constituir(corpus._con(base, "MANIFEST_SHA", "b" * 7))[1]
    salida.append(_control("N2", "R-4-identidades", r, r == "R-4-identidades"))

    r = C.constituir(corpus._con(base, "REFERENCIAS_SEGURAS_A_CREDENCIALES",
                                ["FUDO_TOKEN=abc123"]))[1]
    salida.append(_control("N3", "R-4-sin-secretos", r, r == "R-4-sin-secretos"))

    r = C.constituir(dict(corpus.AISLADO,
                          paquete=dict(corpus.PAQUETE_BASE, PROJECT_SHA="d" * 40)))[1]
    salida.append(_control("N4", "R-4-project", r, r == "R-4-project"))

    solapado_falso = {"interseccion": ["u3/x.md"], "procede": True, "ruteo": None}
    f = EV.evaluar_descubrimiento(solapado_falso, ctx["disjunto"])
    salida.append(_control("N5", "F11", sorted(f), "F11" in f))

    disjunto_falso = {"interseccion": [], "procede": False, "ruteo": None}
    f = EV.evaluar_descubrimiento(ctx["solapado"], disjunto_falso)
    salida.append(_control("N6", "F11", sorted(f), "F11" in f))

    r1 = C.validar_project({"ultimo_sha": "x"})[1]
    r2 = C.validar_project({"lista_de_carriles": ["I"]})[1]
    salida.append(_control("N7", "R-6-prohibido", (r1, r2),
                           r1 == r2 == "R-6-prohibido"))

    r = C.politica_relevo("cada_n", persiste_contador=True)[1]
    salida.append(_control("N8", "R-5-sin-contadores", r, r == "R-5-sin-contadores"))

    salida.append(_n9(ctx))

    r = C.admitir_fuente({"repositorio": "r", "identidad": "i", "funcion": "f",
                          "amplia_capacidad": True})[1]
    salida.append(_control("N10", "R-7-no-autoriza", r, r == "R-7-no-autoriza"))
    return salida


def _n9(ctx):
    """La derivacion efectiva, la misma que implementa R-5-derivacion, sobre historia con merge."""
    raiz = tempfile.mkdtemp(prefix="n9-")
    try:
        log = _historia_con_merge(raiz)
        with observador.Travesia(("constituyente.py",)) as t:
            efectiva = C.derivar_cadencia(raiz, "HEAD")
        primer_padre = C.cadencia_por_primer_padre(raiz, "HEAD")
        ctx["n9"] = {"log": log, "efectiva": efectiva, "primer_padre": primer_padre,
                     "identidad_derivacion": t.identidad()}
        io.open(os.path.join(ctx["dir_evidencia"], "N9_HISTORIA.txt"), "w",
                encoding="utf-8", newline="\n").write(
            "historia sintetica con merge\n\n%s\n\nderivacion efectiva     %d\n"
            "recorrido primer padre  %d\nidentidad atravesada    %s\n"
            % (log, efectiva, primer_padre, t.identidad()))
        return _control("N9", "efectiva > primer padre", (efectiva, primer_padre),
                        efectiva > primer_padre,
                        "identidad de la derivacion: %s" % (t.identidad(),))
    finally:
        shutil.rmtree(raiz, ignore_errors=True)


def _git(raiz, *args):
    entorno = dict(os.environ, GIT_AUTHOR_NAME="n9", GIT_AUTHOR_EMAIL="n9@local",
                   GIT_COMMITTER_NAME="n9", GIT_COMMITTER_EMAIL="n9@local")
    return subprocess.run(["git", "-C", raiz] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, env=entorno).stdout.decode()


def _historia_con_merge(raiz):
    def commit(nombre):
        io.open(os.path.join(raiz, nombre), "w", encoding="utf-8", newline="\n").write(nombre)
        _git(raiz, "add", nombre)
        _git(raiz, "commit", "-m", nombre)
    _git(raiz, "init", "-b", "main")
    commit("a")
    _git(raiz, "checkout", "-b", "rama")
    commit("b")
    commit("c")
    _git(raiz, "checkout", "main")
    commit("d")
    _git(raiz, "merge", "--no-ff", "-m", "merge", "rama")
    return _git(raiz, "log", "--graph", "--oneline", "--all")


# -- N11 a N15, N18, N20 a N27, N30, N32, N33: criterios con insumo sintetico --

def sobre_los_criterios(ctx):
    salida = []

    f = EV.evaluar_cobertura(("R-X-sintetica", "R-Y-sintetica"), ("R-Y-sintetica",))
    salida.append(_control("N11", "F3", sorted(f), "F3" in f))

    f = EV.evaluar_secciones({1: "x", 2: "y"}, no_mecanicas=set(), con_obligaciones={1})
    salida.append(_control("N12", "F5", sorted(f), "F5" in f))

    f = EV.evaluar_forma_secciones([(3, "contenido fuera de forma")], no_mecanicas=set())
    salida.append(_control("N13", "F6", sorted(f), "F6" in f))

    f = EV.evaluar_blob("0" * 40, ctx["blob_congelado"])
    salida.append(_control("N14", "F12", sorted(f), "F12" in f))

    f = EV.evaluar_discriminacion([{"sid": "S-sintetica", "ok_mutante": False,
                                    "obs_real": "igual", "obs_mutante": "igual",
                                    "extracto_real": "a", "extracto_mutante": "b"}])
    salida.append(_control("N15", "F8", sorted(f), "F8" in f))

    salida.extend(_n16_n17(ctx))

    ajenas = ["INICIO otra-identidad blob", "CIERRE otra-identidad blob"]
    f = EV.evaluar_bitacora(ajenas, ["INICIO otra-identidad ALTERADA", ajenas[1]],
                            ["INICIO x b", "CIERRE x b"], "x")
    salida.append(_control("N18", "F15", sorted(f), "F15" in f))

    estado, resuelto = prevuelo.resolver([("VX", "local", ctx["repo"], "f" * 40)])
    salida.append(_control("N19", "NO_EJECUTABLE", estado, estado == prevuelo.NO_EJECUTABLE,
                           "irresolubles: %s" % prevuelo.irresolubles(resuelto)))

    sintetica = [{"fase": "X0", "argv": ["git", "cat-file", "-e", "x"], "remota": False,
                  "clase": "sonda-local", "devolvio_contenido": False}]
    aperturas = [{"fase": "X0", "archivo": "METODO-MANIFIESTOS.md"}]
    f = EV.evaluar_traza_externa(sintetica, aperturas, ctx["nominales"], ctx["nominales"])
    salida.append(_control("N20", "F18", sorted(f), "F18" in f,
                           "traza externa distinta de la real: %d apertura(s)" % len(aperturas)))

    f = EV.evaluar_traza_interna(["sondas", "corpus"], ctx["modulos_corrida"])
    salida.append(_control("N21", "F19", sorted(f), "F19" in f,
                           "traza interna distinta de la real"))

    f = EV.evaluar_imports(["sondas", "constituyente"], ctx["modulos_corrida"])
    salida.append(_control("N22", "F20", sorted(f), "F20" in f))

    par = [("VA", "local", ctx["repo"], ctx["sha_repetido"]),
           ("VB", "local", ctx["repo"], ctx["sha_repetido"])]
    _, resuelto = prevuelo.resolver(par)
    por_valor = len({v[3] for v in par})
    salida.append(_control("N23", "nominal 2, por valor 1", (len(resuelto), por_valor),
                           len(resuelto) == 2 and por_valor == 1))

    ruta_propia = os.path.join(ctx["dir_mecanismo"], "BITACORA.txt")
    f = EV.evaluar_ruta_bitacora(ruta_propia, ctx["raiz"], ctx["constante_bitacora"],
                                 ctx["dir_mecanismo"])
    salida.append(_control("N24", "F22", sorted(f), "F22" in f))

    tercera = [{"fase": "X0", "argv": ["git", "ls-remote", "origin", "r"], "remota": True,
                "clase": "sonda-remota", "devolvio_contenido": False},
               {"fase": "cuerpo", "argv": ["git", "ls-remote", "origin", "r"], "remota": True,
                "clase": "sonda-remota", "devolvio_contenido": True},
               {"fase": "cuerpo", "argv": ["git", "ls-remote", "otro", "r"], "remota": True,
                "clase": "sonda-remota", "devolvio_contenido": True}]
    f = EV.evaluar_frontera(tercera, ctx["remoto"])
    salida.append(_control("N25", "F24", sorted(f), "F24" in f,
                           "la traza la distingue de la real: 3 remotas contra 2"))

    f = EV.evaluar_conjunto_x0(("V1", "V2", "V3"), ctx["nominales"])
    salida.append(_control("N26", "F25", sorted(f), "F25" in f))

    sintetico = {"V1": True, "V5": "05041ddf0e7a687cc8ed1982a3d824570fe57710"}
    f = EV.evaluar_forma_x0(sintetico)
    salida.append(_control("N27", "F26", sorted(f), "F26" in f,
                           "forma distinta de la real: %s contra solo booleanos"
                           % sorted({type(v).__name__ for v in sintetico.values()})))

    f = EV.evaluar_discriminacion([{"sid": "S-sintetica", "ok_mutante": False,
                                    "obs_real": "[1, 2]", "obs_mutante": "[3, 4]",
                                    "extracto_real": "misma superficie",
                                    "extracto_mutante": "misma superficie"}])
    salida.append(_control("N30", "F29", sorted(f), "F29" in f,
                           "el observable difiere y aun asi no discrimina"))

    salida.extend(_n32_n33(ctx))
    return salida


def _n16_n17(ctx):
    """La misma funcion de corrida, con bitacora sintetica. `E15` observa que se atraveso."""
    raiz = tempfile.mkdtemp(prefix="n16-")
    try:
        ruta = os.path.join(raiz, "BITACORA.txt")
        identidad, blob = "identidad-sintetica", "0" * 40

        def cuerpo_que_falla():
            raise RuntimeError("falla inyectada")

        with observador.Travesia(("corrida.py",)) as t16:
            r16 = corrida.correr(ruta, identidad, blob, cuerpo_que_falla)
        lineas = io.open(ruta, encoding="utf-8").read().split("\n")
        ok16 = (r16["terminacion"] == "T2" and "F13" in r16["criterios"] and
                sum(1 for l in lineas if l.startswith("INICIO ")) == 1 and
                sum(1 for l in lineas if l.startswith("CIERRE ")) == 1)

        with observador.Travesia(("corrida.py",)) as t17:
            r17 = corrida.correr(ruta, identidad, blob, lambda: ("EXITO", None))
        ok17 = (r17["terminacion"] == corrida.REINTENTO and not r17["anoto_inicio"]
                and not r17["evaluo_criterios"])

        ctx["identidad_corrida"] = {"N16": t16.identidad(), "N17": t17.identidad()}
        return [
            _control("N16", "T2 con F13, INICIO y CIERRE", r16["terminacion"], ok16,
                     "atraveso %s" % (t16.identidad(),)),
            _control("N17", "REINTENTO sin anotar ni evaluar", r17["terminacion"], ok17,
                     "atraveso %s" % (t17.identidad(),)),
        ]
    finally:
        shutil.rmtree(raiz, ignore_errors=True)


def _n32_n33(ctx):
    """La atadura entre control y calificacion, con registros sinteticos."""
    A = ("comprobaciones.py", "c_S01", 10)
    B = ("comprobaciones.py", "c_S01_localizada", 900)
    Cc = ("comprobaciones.py", "c_S02", 20)

    def reg(sid, obligacion, motivo, identidad, clase="list"):
        return {"sid_declarado": sid, "obligacion": obligacion, "motivo": motivo,
                "identidad": identidad, "clase_observable": clase}

    registradas = {"S01": A, "S01-localizada": B, "S02": Cc}

    paralela = [reg("S01", "R-1-cadena", EV.CALIFICACION, A),
                reg("S01-localizada", "R-1-cadena", EV.CONTROL, B)]
    f32 = EV.evaluar_atadura(paralela, registradas)
    n32 = _control("N32", "F31 y F32", sorted(f32), "F31" in f32 and "F32" in f32,
                   "identidades: calificacion %s, control %s" % (A, B))

    mal = [reg("S01", "R-1-cadena", EV.CALIFICACION, A),
           reg("S01", "R-1-cadena", EV.CONTROL, Cc)]
    bien = [reg("S01", "R-1-cadena", EV.CALIFICACION, A),
            reg("S01", "R-1-cadena", EV.CONTROL, A)]
    f33 = EV.evaluar_atadura(mal, registradas)
    limpio = EV.evaluar_atadura(bien, registradas)
    n33 = _control("N33", "F33 en el declarado, nada en el que si la atraviesa",
                   (sorted(f33), sorted(limpio)),
                   "F33" in f33 and not limpio,
                   "declara S01 y atraviesa %s" % (Cc,))
    return [n32, n33]


# -- N28, N29, N31: la misma comprobacion, otro sujeto ------------------------

def sobre_las_comprobaciones(documento, ctx_comp, comprobaciones_por_sid):
    """Ejercen la comprobacion REAL sobre sujetos sinteticos. Devuelven (resultados, registros)."""
    resultados, registros = [], []

    s01 = comprobaciones_por_sid["S01"]
    real = registro.ejercer(s01, documento.sujeto(), ctx_comp, EV.CALIFICACION,
                            etiqueta="real-para-N28-N29")

    fuera = superficie.con_ruido_antes(documento, "R-1-cadena", registro.CADENA)
    r28 = registro.ejercer(s01, fuera, ctx_comp, EV.CONTROL, etiqueta="cadena-alterada-fuera")
    resultados.append(_control("N28", "observable igual al real",
                               (real["observable"], r28["observable"]),
                               r28["observable"] == real["observable"],
                               "atraveso %s" % (r28["identidad"],)))

    dentro = superficie.alterado_dentro(documento, "R-1-cadena",
                                        "metodo-manifiestos-ai produce", "AJENO produce")
    r29 = registro.ejercer(s01, dentro, ctx_comp, EV.CONTROL, etiqueta="cadena-alterada-dentro")
    resultados.append(_control("N29", "observable distinto del real",
                               (real["observable"], r29["observable"]),
                               r29["observable"] != real["observable"],
                               "atraveso %s" % (r29["identidad"],)))

    s13 = comprobaciones_por_sid["S13"]
    solo_nombra = dict(ctx_comp["sujeto_conducta"], descubrir=_descubrir_que_solo_nombra())
    mantiene_sujeto = registro._descubrir_con_registro(ctx_comp["sujeto_conducta"])

    r31a = registro.ejercer(s13, solo_nombra, ctx_comp, EV.CONTROL, etiqueta="solo-nombra")
    r31b = registro.ejercer(s13, mantiene_sujeto, ctx_comp, EV.CONTROL, etiqueta="mantiene-estado")
    f30 = EV.evaluar_conducta_prohibida(r31a["ok"], r31b["ok"])
    resultados.append(_control("N31", "solo nombra pasa, mantiene falla",
                               (r31a["ok"], r31b["ok"]), not f30,
                               "misma comprobacion en ambos: %s y %s"
                               % (r31a["identidad"], r31b["identidad"])))

    registros.extend([r28, r29, r31a, r31b])
    return resultados, registros, real


PROHIBIDAS_QUE_SOLO_SE_NOMBRAN = ("EVENT.md", "lista_de_carriles", "registro_central")


def _descubrir_que_solo_nombra():
    """Nombra las claves prohibidas para rechazarlas, y no mantiene ninguna. Debe pasar."""
    def descubrir(paths, superficie_propia):
        for clave in PROHIBIDAS_QUE_SOLO_SE_NOMBRAN:
            if clave in superficie_propia.get("paths", ()):
                return {"interseccion": [], "procede": False, "ruteo": "rechazado"}
        return C.descubrir(paths, superficie_propia)
    return descubrir
