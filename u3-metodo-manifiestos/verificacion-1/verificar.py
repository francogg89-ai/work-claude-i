"""Corrida unica del contrato previo congelado de U3.

Congelado en audit-chatgpt-i@af2f37e9dba513523222c79a910ec049030deff6.

Orden: X0 estrictamente antes de INICIO. Frontera de red de dos interacciones, R1 en X0 y R2 en
el cuerpo. Toda invocacion atraviesa `correr()`, donde vive la guardia X4.

Uso:
    python verificar.py --repo-work <ruta>
"""

import argparse
import inspect
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

import bitacora as mod_bitacora
import candidato as mod_candidato
import casos as mod_casos
import estructurales as mod_estructurales
import instrumentacion as mod_instr
import metodo as mod_metodo
import prevuelo as mod_prevuelo
import sinteticos as mod_sinteticos
import sondas as mod_sondas

V1 = "25a6e890351a5f402867dd6343bf80c041dd8cfc"
V2 = "f44f2a0797cde6f569cca6fe5397d45917680258"
V3 = "636a5d095574130b56c232da7958691f87234516"
V4 = "5bd6b0f582c7970a7b8c6c838b9971a70df43dfc"
V5_REMOTO = "origin"
V5_REF = "refs/heads/main"

IDENT_REAL = {"contrato": mod_bitacora.CONTRATO, "candidato": mod_bitacora.CANDIDATO}

SUPERFICIE_DISJUNTA = {"repo": "work-claude-i", "paths": ("u1-contratos-transversales/",)}
SUPERFICIE_SOLAPADA = {"repo": "work-claude-i", "paths": ("u3-metodo-manifiestos/",)}

NEGATIVOS_EXIGIDOS = ["N%d" % i for i in range(1, 28)]


def vinculaciones(repo_work):
    """Lista literal congelada. No se infiere ni se deriva escaneando SHAs."""
    return [
        ("V1", "local", repo_work, V1),
        ("V2", "local", repo_work, V2),
        ("V3", "local", repo_work, V3),
        ("V4", "local", repo_work, V4),
        ("V5", "remota", repo_work, (V5_REMOTO, V5_REF)),
    ]


def satisface(cmd, vincs):
    nombres = []
    for nombre, clase, repo, arg in vincs:
        esperado = (mod_sondas.comando_local(repo, arg) if clase == "local"
                    else mod_sondas.comando_remoto(repo, arg[0], arg[1]))
        if cmd == esperado:
            nombres.append(nombre)
    return nombres


def cobertura_nominal(procesos, vincs):
    mapeo, cubiertas, no_sondas = [], set(), []
    for i, cmd in enumerate(procesos):
        nombres = satisface(cmd, vincs)
        mapeo.append((i, cmd, nombres))
        if nombres:
            cubiertas.update(nombres)
        else:
            no_sondas.append(cmd)
    return {"mapeo": mapeo, "cubiertas": cubiertas, "no_sondas": no_sondas,
            "sin_cubrir": [n for n, _, _, _ in vincs if n not in cubiertas]}


def cobertura_por_valor(vincs):
    """Medicion defectuosa. Contra-insumo de N23; no evalua la corrida."""
    return len({(r, str(a)) for _, _, r, a in vincs})


def imports_de(fuente):
    return sorted(set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", fuente, re.M)))


def ruta_es_constante_de_unidad(fuente, ruta_relativa):
    m = re.search(r"^RUTA_RELATIVA\s*=\s*(.+)$", fuente, re.M)
    if not m:
        return False, "no se declara RUTA_RELATIVA"
    asignacion = m.group(1)
    derivada = any(t in asignacion for t in ("__file__", "dirname", "abspath", "os.path"))
    esperada = ruta_relativa == "u3-metodo-manifiestos/BITACORA.txt"
    return esperada and not derivada, "asignacion=%s derivada=%s" % (asignacion.strip(), derivada)


def historia_con_merge():
    """Historia Git sintetica con un merge. Devuelve (ruta, log)."""
    d = tempfile.mkdtemp(prefix="n9_")
    g = ["git", "-C", d]
    env = {"GIT_AUTHOR_NAME": "n9", "GIT_AUTHOR_EMAIL": "n9@x",
           "GIT_COMMITTER_NAME": "n9", "GIT_COMMITTER_EMAIL": "n9@x"}
    entorno = dict(os.environ, **env)

    def run(*a):
        subprocess.run(g + list(a), check=True, env=entorno,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["git", "init", "-q", "-b", "main", d], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    io.open(os.path.join(d, "a.txt"), "w").write("1\n")
    run("add", "-A"); run("commit", "-q", "-m", "base")
    run("checkout", "-q", "-b", "rama")
    io.open(os.path.join(d, "b.txt"), "w").write("2\n")
    run("add", "-A"); run("commit", "-q", "-m", "rama-1")
    io.open(os.path.join(d, "b.txt"), "w").write("3\n")
    run("add", "-A"); run("commit", "-q", "-m", "rama-2")
    run("checkout", "-q", "main")
    io.open(os.path.join(d, "a.txt"), "w").write("4\n")
    run("add", "-A"); run("commit", "-q", "-m", "main-1")
    run("merge", "-q", "--no-ff", "-m", "merge", "rama")
    log = subprocess.run(g + ["log", "--oneline", "--graph", "--all"], check=True,
                         env=entorno, stdout=subprocess.PIPE).stdout.decode()
    return d, log


# -- cuerpo -------------------------------------------------------------------

def cuerpo(args, log, fallos, controles, fallar_en, x0):
    if fallar_en:
        raise RuntimeError("falla inyectada en el cuerpo: %s" % fallar_en)

    vincs = vinculaciones(args.repo_work)

    log("E16 RESULTADO DE X0, VINCULACION POR VINCULACION")
    for nombre, clase, repo, arg, ok in x0["resultado"]:
        log("  %-4s %-7s %-40s resuelve=%s" % (nombre, clase, str(arg), ok))
    log("  forma del resultado: solo booleanos = %s"
        % mod_prevuelo.solo_booleanos(x0["resultado"]))
    if not mod_prevuelo.solo_booleanos(x0["resultado"]):
        fallos.append(("F26", "-", "X0 transporta algo distinto de un booleano"))
    log("")

    tr = x0["traza"]
    cob = cobertura_nominal(tr.procesos, vincs)
    log("E17 TRAZA EXTERNA DE X0, COBERTURA NOMINAL")
    for i, cmd, nombres in cob["mapeo"]:
        log("  #%d %s" % (i + 1, " ".join(cmd)))
        log("     satisface: %s" % (", ".join(nombres) if nombres else "NINGUNA"))
    log("  declaradas %d  cubiertas %s  sin cubrir %s  no-sondas %d  archivos %d"
        % (len(vincs), sorted(cob["cubiertas"]), cob["sin_cubrir"] or "ninguna",
           len(cob["no_sondas"]), len(tr.archivos)))
    if cob["sin_cubrir"] or cob["no_sondas"] or tr.archivos:
        fallos.append(("F18", "-", "traza externa de X0 fuera de la frontera"))
    log("")

    log("E18 / E19 TRAZA INTERNA E IMPORTS DEL PRE-VUELO")
    log("  modulos llamados: %s" % tr.modulos_llamados())
    ajenas = tr.llamadas_a_la_corrida()
    log("  llamadas a modulos de la corrida: %s" % (ajenas or "ninguna"))
    if ajenas:
        fallos.append(("F19", "-", "traza interna de X0 alcanza la corrida: %s" % ajenas))
    for mod in (mod_prevuelo, mod_sondas):
        imps = imports_de(inspect.getsource(mod))
        cruce = sorted(set(imps) & mod_instr.MODULOS_DE_LA_CORRIDA)
        log("  %-9s importa %s  cruce: %s" % (mod.__name__, imps, cruce or "ninguno"))
        if cruce:
            fallos.append(("F20", "-", "%s importa %s" % (mod.__name__, cruce)))
    log("")

    texto, blob = mod_candidato.leer(args.repo_work)
    cand = mod_candidato.Candidato(texto)
    coincide = blob == mod_candidato.CANDIDATE_BLOB_SHA
    log("E11 IDENTIDAD DEL CANDIDATO, LEIDA DESPUES DE INICIO")
    log("  leido %s  congelado %s  coincide %s"
        % (blob, mod_candidato.CANDIDATE_BLOB_SHA, coincide))
    if not coincide:
        fallos.append(("F12", "-", "blob leido distinto del congelado"))
    log("")

    obligaciones = cand.obligaciones()
    ids = {o[0] for o in obligaciones}
    log("SUPERFICIE NORMATIVA EXTRAIDA DEL CANDIDATO")
    log("  obligaciones %d  unicas %d  secciones %s  no mecanicas %s"
        % (len(obligaciones), len(ids), [s[0] for s in cand.secciones_numeradas()],
           sorted(cand.no_mecanicas)))
    huerfanas = cand.secciones_sin_obligacion()
    log("  secciones mecanicas sin obligacion: %s" % (huerfanas or "ninguna"))
    if huerfanas:
        fallos.append(("F5", "-", "secciones sin obligacion: %s" % huerfanas))
    violaciones = cand.violaciones_de_forma()
    log("  violaciones de forma: %s" % (violaciones or "ninguna"))
    if violaciones:
        fallos.append(("F6", "-", "violaciones de forma: %d" % len(violaciones)))
    log("")

    ctx = {"repo_work": args.repo_work, "V1": V1, "V2": V2, "V3": V3, "V4": V4}

    log("P-C1 REFERENCIA REMOTA VIGENTE (R2)")
    vigente = mod_metodo.referencia_remota(args.repo_work, V5_REMOTO, V5_REF)
    log("  %s %s -> %s" % (V5_REMOTO, V5_REF, vigente))
    log("")

    log("P-C2 DISCRIMINACION SOBRE LOS CORTES CONGELADOS")
    paths = mod_metodo.paths_modificados(args.repo_work, V3, V4)
    log("  paths modificados %s..%s: %s" % (V3[:8], V4[:8], sorted(paths)))
    for nombre, sup in (("disjunta", SUPERFICIE_DISJUNTA), ("solapada", SUPERFICIE_SOLAPADA)):
        r = mod_metodo.descubrir(paths, sup)
        log("  superficie %-9s interseccion=%s procede=%s ruteo=%s"
            % (nombre, r["interseccion"] or "vacia", r["procede"], bool(r["ruteo"])))
    log("")

    log("CASOS DE LLAMADA")
    cubiertas_obl, emitidos = set(), set()
    for caso in mod_casos.CASOS_LLAMADA:
        cubiertas_obl.add(caso["obligacion"])
        producido = caso["fn"](ctx)
        ok = producido == caso["esperado"]
        if isinstance(producido, str) and producido.startswith("R-"):
            emitidos.add(producido)
        neg = " [%s]" % caso["negativo"] if caso.get("negativo") else ""
        log("  %-5s %-5s %-24s%s %s" % ("OK" if ok else "FALLO", caso["id"],
                                        caso["obligacion"], neg,
                                        "" if ok else "producido %r != esperado %r"
                                        % (producido, caso["esperado"])))
        if not ok:
            fallos.append(("F1", caso["id"], "producido %r" % (producido,)))
    log("")

    log("CASOS ESTRUCTURALES")
    for id_, obl, comprobar, mutante, neg in mod_estructurales.construir(texto):
        cubiertas_obl.add(obl)
        ok_real, obs_real, det_real = comprobar(mod_estructurales.sujeto_real(texto), ctx)
        ok_mut, obs_mut, det_mut = comprobar(mutante(), ctx)
        difiere = obs_real != obs_mut
        ok = ok_real and not ok_mut and difiere
        log("  %-5s %-5s %-24s real=%s mut=%s difiere=%s | %s | %s"
            % ("OK" if ok else "FALLO", id_, obl, ok_real, ok_mut, difiere, obs_real, obs_mut))
        if ok_real and ok_mut:
            fallos.append(("F7", id_, "la comprobacion no falla sobre su mutante"))
        if not difiere:
            fallos.append(("F8", id_, "el observable no difiere"))
        if not ok:
            fallos.append(("F1", id_, det_real))
    log("")

    log("E2 / E3 ATRIBUCION Y COBERTURA")
    ajenos = sorted(emitidos - ids)
    sin_caso = sorted(ids - cubiertas_obl)
    sobrantes = sorted(cubiertas_obl - ids)
    log("  identificadores emitidos %d, ajenos: %s" % (len(emitidos), ajenos or "ninguno"))
    log("  obligaciones %d, ejercitadas %d" % (len(ids), len(cubiertas_obl & ids)))
    log("  sin caso: %s | sobre obligaciones inexistentes: %s"
        % (sin_caso or "ninguna", sobrantes or "ninguno"))
    if ajenos:
        fallos.append(("F2", "-", "identificadores ajenos: %s" % ajenos))
    if sin_caso:
        fallos.append(("F3", "-", "obligaciones sin caso: %s" % sin_caso))
    if sobrantes:
        fallos.append(("F4", "-", "casos sobre obligaciones inexistentes: %s" % sobrantes))
    log("")

    if not controles:
        return

    log("CONTROLES SOBRE EL PROPIO MECANISMO")
    d9, log9 = historia_con_merge()
    try:
        completa = mod_metodo.derivar_cadencia(d9, "HEAD")
        primer_padre = mod_metodo.cadencia_por_primer_padre(d9, "HEAD")
        log("  N9 historia sintetica con merge: efectiva=%d primer_padre=%d difieren=%s"
            % (completa, primer_padre, completa != primer_padre))
        for l in log9.rstrip().split("\n"):
            log("     %s" % l)
        io.open("N9_HISTORIA.txt", "w", encoding="utf-8", newline="\n").write(
            "efectiva=%d\nprimer_padre=%d\n\n%s" % (completa, primer_padre, log9))
        if completa == primer_padre:
            fallos.append(("F7", "N9", "la historia sintetica no discrimina"))
    finally:
        shutil.rmtree(d9, ignore_errors=True)

    c11 = mod_candidato.Candidato(mod_sinteticos.N11_OBLIGACION_SIN_CASO)
    f11 = sorted({o[0] for o in c11.obligaciones()} - set(mod_sinteticos.N11_CASOS))
    log("  N11 obligacion sintetica sin caso -> F3 = %s (%s)" % (bool(f11), f11))
    if not f11:
        fallos.append(("F7", "N11", "no detecta obligacion sin caso"))

    h12 = mod_candidato.Candidato(
        mod_sinteticos.N12_SECCION_SIN_OBLIGACION).secciones_sin_obligacion()
    log("  N12 seccion sintetica sin obligacion -> F5 = %s (%s)" % (bool(h12), h12))
    if not h12:
        fallos.append(("F7", "N12", "no detecta seccion huerfana"))

    v13 = mod_candidato.Candidato(
        mod_sinteticos.N13_CONTENIDO_FUERA_DE_FORMA).violaciones_de_forma()
    log("  N13 contenido sintetico fuera de forma -> F6 = %s" % bool(v13))
    if not v13:
        fallos.append(("F7", "N13", "no detecta contenido colado"))

    d14 = mod_sinteticos.N14_BLOB_AJENO != mod_candidato.CANDIDATE_BLOB_SHA
    log("  N14 blob sintetico ajeno -> F12 = %s" % d14)
    if not d14:
        fallos.append(("F7", "N14", "la identidad no discrimina"))

    base15 = mod_estructurales.sujeto_real(texto)
    c15 = mod_estructurales.c_sin_acciones({"NO_EXISTE"})
    ok_r, obs_r, _ = c15(base15, ctx)
    ok_m, obs_m, _ = c15(mod_estructurales.mutante(base15, texto=texto), ctx)
    log("  N15 mutante sintetico inerte -> F8 = %s (obs iguales = %s)"
        % (obs_r == obs_m, obs_r == obs_m))
    if obs_r != obs_m:
        fallos.append(("F7", "N15", "no detecta un mutante inerte"))

    r16 = mod_sinteticos.N16_BITACORA
    if os.path.exists(r16):
        os.remove(r16)
    res16 = correr(args, mod_sinteticos.IDENT_SINTETICA, r16, x0, controles=False,
                   fallar_en="N16")
    lin16 = mod_bitacora.leer(r16)
    ok16 = (res16["ruta"] == "corrida" and res16["veredicto"] == "FALLO"
            and any(f[0] == "F13" for f in res16["fallos"])
            and len(mod_bitacora.propias(lin16, mod_sinteticos.IDENT_SINTETICA)) == 2)
    log("  N16 aborto capturado via correr() -> ruta=%s veredicto=%s propias=%d"
        % (res16["ruta"], res16["veredicto"],
           len(mod_bitacora.propias(lin16, mod_sinteticos.IDENT_SINTETICA))))
    if not ok16:
        fallos.append(("F16", "N16", "el control de aborto no exhibio T2"))

    r17 = mod_sinteticos.N17_BITACORA
    if os.path.exists(r17):
        os.remove(r17)
    mod_bitacora.agregar("INICIO", r17, mod_sinteticos.IDENT_SINTETICA)
    antes17 = mod_bitacora.leer(r17)
    res17 = correr(args, mod_sinteticos.IDENT_SINTETICA, r17, x0, controles=False)
    ok17 = (res17["ruta"] == "reintento" and not res17["criterios_evaluados"]
            and antes17 == mod_bitacora.leer(r17))
    log("  N17 reintento via correr() -> ruta=%s criterios=%s sin cambios=%s"
        % (res17["ruta"], res17["criterios_evaluados"], antes17 == mod_bitacora.leer(r17)))
    if not ok17:
        fallos.append(("F16", "N17", "el control de reintento no exhibio X4"))

    r18 = mod_sinteticos.N18_BITACORA
    if os.path.exists(r18):
        os.remove(r18)
    mod_bitacora.agregar("INICIO", r18, mod_sinteticos.IDENT_AJENA)
    mod_bitacora.agregar("CIERRE", r18, mod_sinteticos.IDENT_AJENA)
    prev18 = mod_bitacora.leer(r18)
    intacta, _ = mod_bitacora.historia_intacta(prev18, prev18, mod_sinteticos.IDENT_SINTETICA)
    rota, _ = mod_bitacora.historia_intacta(prev18, prev18[:-1], mod_sinteticos.IDENT_SINTETICA)
    log("  N18 historia ajena -> intacta=%s alterada detectada=%s" % (intacta, not rota))
    if not (intacta and not rota):
        fallos.append(("F7", "N18", "la comprobacion de historia no discrimina"))

    v19 = [("SINTETICA", "local", args.repo_work, "0" * 40)]
    r19, _ = mod_instr.observar(lambda: mod_prevuelo.ejecutar(v19))
    log("  N19 vinculacion sintetica irresoluble -> NO_EJECUTABLE = %s"
        % bool(mod_prevuelo.irresolubles(r19)))
    if not mod_prevuelo.irresolubles(r19):
        fallos.append(("F7", "N19", "el pre-vuelo no detecta una irresoluble"))

    def x0_espia():
        r = mod_prevuelo.ejecutar(vincs)
        subprocess.run(["git", "-C", args.repo_work, "show", "%s:%s" % (V1, "PLAN.md")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return r

    _, tr20 = mod_instr.observar(x0_espia)
    no_s20 = cobertura_nominal(tr20.procesos, vincs)["no_sondas"]
    log("  N20 X0 sintetico que lee el candidato -> F18 = %s, traza difiere = %s"
        % (bool(no_s20), tr20.procesos != tr.procesos))
    if not (no_s20 and tr20.procesos != tr.procesos):
        fallos.append(("F7", "N20", "la traza externa no distingue un X0 que lee"))

    def x0_memoria(_m=mod_metodo):
        r = mod_prevuelo.ejecutar(vincs)
        _m.orden_de_publicacion(True)
        return r

    _, tr21 = mod_instr.observar(x0_memoria)
    aj21 = tr21.llamadas_a_la_corrida()
    log("  N21 X0 sintetico que ejecuta en memoria -> F19 = %s (%s), traza interna difiere = %s"
        % (bool(aj21), aj21, aj21 != tr.llamadas_a_la_corrida()))
    if not (aj21 and aj21 != tr.llamadas_a_la_corrida()):
        fallos.append(("F7", "N21", "la traza interna no distingue ejecucion en memoria"))

    cruce22 = sorted(set(imports_de(mod_sinteticos.N22_FUENTE_IMPORTADORA))
                     & mod_instr.MODULOS_DE_LA_CORRIDA)
    log("  N22 pre-vuelo sintetico que importa la corrida -> F20 = %s (%s)"
        % (bool(cruce22), cruce22))
    if not cruce22:
        fallos.append(("F7", "N22", "el aislamiento por importacion no discrimina"))

    v23 = [("ALFA", "local", args.repo_work, V2), ("BETA", "local", args.repo_work, V2)]
    cob23 = cobertura_nominal([mod_sondas.comando_local(args.repo_work, V2)], v23)
    nominal23, valor23 = len(cob23["cubiertas"]), cobertura_por_valor(v23)
    log("  N23 dos vinculaciones con el mismo valor -> nominal=%d valor=%d declaradas=%d"
        % (nominal23, valor23, len(v23)))
    if not (nominal23 == len(v23) and valor23 < len(v23)):
        fallos.append(("F7", "N23", "la regla de medicion no discrimina el colapso"))

    ok_r24, _ = ruta_es_constante_de_unidad(inspect.getsource(mod_bitacora),
                                            mod_bitacora.RUTA_RELATIVA)
    ok_m24, _ = ruta_es_constante_de_unidad(mod_sinteticos.N24_FUENTE_DERIVADA, "derivada")
    log("  N24 ruta de bitacora -> real=%s mutante derivado=%s" % (ok_r24, ok_m24))
    if not ok_r24:
        fallos.append(("F22", "-", "la ruta de la bitacora no es constante de unidad"))
    if not (ok_r24 and not ok_m24):
        fallos.append(("F7", "N24", "la comprobacion de ruta no discrimina"))

    def red_extra():
        subprocess.run(["git", "-C", args.repo_work, "ls-remote", "origin", "refs/heads/main"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    _, tr25 = mod_instr.observar(red_extra)
    remotas25 = [c for c in tr25.procesos if "ls-remote" in c]
    log("  N25 interaccion de red adicional fuera de fase -> F24 = %s (%d)"
        % (bool(remotas25), len(remotas25)))
    if not remotas25:
        fallos.append(("F7", "N25", "la frontera de red no distingue una interaccion extra"))

    v26 = vincs[:3]
    log("  N26 conjunto sintetico distinto de V1-V5 -> F25 = %s" % (len(v26) != len(vincs)))
    if len(v26) == len(vincs):
        fallos.append(("F7", "N26", "el denominador no discrimina"))

    sint27 = [(n, c, r, a, "valor-de-referencia") for n, c, r, a, _ in x0["resultado"]]
    log("  N27 X0 sintetico que transporta el valor -> F26 = %s"
        % (not mod_prevuelo.solo_booleanos(sint27)))
    if mod_prevuelo.solo_booleanos(sint27):
        fallos.append(("F7", "N27", "la forma del resultado no discrimina"))
    log("")

    log("CONTROLES NEGATIVOS")
    presentes = {c["negativo"] for c in mod_casos.CASOS_LLAMADA if c.get("negativo")}
    presentes |= {"N9"} | {"N%d" % i for i in range(11, 28)}
    faltan = [n for n in NEGATIVOS_EXIGIDOS if n not in presentes]
    log("  exigidos N1..N27")
    log("  presentes %s" % sorted(presentes, key=lambda x: int(x[1:])))
    if faltan:
        fallos.append(("F3", "-", "controles negativos ausentes: %s" % faltan))
    log("")


# -- funcion de corrida compartida --------------------------------------------

def correr(args, ident, ruta_bitacora, x0, controles=True, fallar_en=None):
    lineas = []
    log = lineas.append
    fallos = []

    log("REGLA DE EJECUCION")
    log("  contrato  %s" % ident["contrato"])
    log("  candidato %s" % ident["candidato"])
    log("  bitacora  %s" % os.path.abspath(ruta_bitacora))
    previas = mod_bitacora.leer(ruta_bitacora)
    log("  lineas al abrir: %d (ajenas: %d)"
        % (len(previas), len(mod_bitacora.ajenas(previas, ident))))

    if mod_bitacora.hay_inicio_previo(ruta_bitacora, ident):
        log("  X4 ya existe INICIO de esta identidad: reintento")
        log("")
        log("VEREDICTO=FALLO")
        log("  F14 - reintento bajo un contrato ya ejecutado")
        return {"ruta": "reintento", "criterios_evaluados": False, "veredicto": "FALLO",
                "fallos": [("F14", "-", "reintento")], "lineas": lineas}

    log("  E13 no existe INICIO previo de esta identidad")
    mod_bitacora.agregar("INICIO", ruta_bitacora, ident)
    log("  INICIO anotado antes del primer caso")
    log("")

    try:
        cuerpo(args, log, fallos, controles, fallar_en, x0)
    except Exception:
        log("")
        log("F13 EXCEPCION CAPTURADA DESPUES DE INICIO (T2)")
        for l in traceback.format_exc().rstrip().split("\n"):
            log("  " + l)
        fallos.append(("F13", "-", "el cuerpo produjo una excepcion, resuelta en el veredicto"))
        log("")

    mod_bitacora.agregar("CIERRE", ruta_bitacora, ident)
    actuales = mod_bitacora.leer(ruta_bitacora)
    ok_coh, det_coh = mod_bitacora.coherente(ruta_bitacora, ident)
    ok_hist, det_hist = mod_bitacora.historia_intacta(previas, actuales, ident)
    log("E12 / E14 BITACORA")
    for l in actuales:
        log("  %s" % l)
    log("  coherente=%s (%s) | historia ajena intacta=%s (%s)"
        % (ok_coh, det_coh, ok_hist, det_hist))
    if not (ok_coh and ok_hist):
        fallos.append(("F15", "-", "bitacora: %s / %s" % (det_coh, det_hist)))
    log("")

    veredicto = "EXITO" if not fallos else "FALLO"
    log("VEREDICTO=%s" % veredicto)
    for c, k, d in fallos:
        log("  %s %s %s" % (c, k, d))
    return {"ruta": "corrida", "criterios_evaluados": True, "veredicto": veredicto,
            "fallos": fallos, "lineas": lineas}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-work", required=True)
    ap.add_argument("--salida", default="salida.txt")
    args = ap.parse_args()

    cab = ["X0 PRE-VUELO, ESTRICTAMENTE ANTES DE INICIO"]
    vincs = vinculaciones(args.repo_work)
    resultado, traza = mod_instr.observar(lambda: mod_prevuelo.ejecutar(vincs))
    for nombre, clase, repo, arg, ok in resultado:
        cab.append("  %-4s %-7s %-40s resuelve=%s" % (nombre, clase, str(arg), ok))
    irres = mod_prevuelo.irresolubles(resultado)
    cab.append("  irresolubles: %s" % ([n for n, _, _, _ in irres] or "ninguna"))
    cab.append("  R1 interacciones de red en X0: %d"
               % len([c for c in traza.procesos if "ls-remote" in c]))
    cab.append("")

    x0 = {"resultado": resultado, "traza": traza}

    if irres:
        cab += ["NO_EJECUTABLE",
                "  no se anota INICIO, no se evalua criterio, no se consume el contrato"]
        texto = "\n".join(cab) + "\n"
        io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
        sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
        return 2

    r = correr(args, IDENT_REAL, mod_bitacora.ruta_real(args.repo_work), x0)
    texto = "\n".join(cab + r["lineas"]) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
    sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
    return 0 if r["veredicto"] == "EXITO" else 1


if __name__ == "__main__":
    sys.exit(main())
