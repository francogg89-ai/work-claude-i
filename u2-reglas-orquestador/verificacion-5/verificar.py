"""Corrida única del contrato previo congelado de U2.

Congelado en audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59.

Orden: X0 estrictamente antes de INICIO. Si alguna identidad congelada no resuelve, termina
NO_EJECUTABLE sin anotar nada y sin evaluar criterios. Si todas resuelven, la corrida atraviesa
`correr()`, donde vive la guardia X4, y evalúa E1-E21, F1-F23 y N1-N24.

Uso:
    python verificar.py --repo-metodo <ruta> --repo-work <ruta> --repo-audit <ruta>
"""

import argparse
import inspect
import io
import os
import re
import subprocess
import sys
import traceback

import autoridad as mod_autoridad
import bitacora as mod_bitacora
import candidato as mod_candidato
import corpus as mod_corpus
import estructurales as mod_estructurales
import instrumentacion as mod_instr
import orquestador as mod_orquestador
import prevuelo as mod_prevuelo
import sinteticos as mod_sinteticos
import sondas as mod_sondas

P_C_WORK_SHA = "f2429c2be622c305d4cfd6cebcd00837ea3ed42d"
P_C_AUDIT_SHA = "063cb3ac7edaa9a1457708a17be1789a862f6bd9"

IDENT_REAL = {"contrato": mod_bitacora.CONTRATO, "candidato": mod_bitacora.CANDIDATO}

NEGATIVOS_EXIGIDOS = ["N%d" % i for i in range(1, 25)]


def identidades_congeladas(args):
    return [
        ("CANDIDATE_WORK_SHA", args.repo_work, mod_candidato.CANDIDATE_WORK_SHA),
        ("CANDIDATE_BLOB_SHA", args.repo_work, mod_candidato.CANDIDATE_BLOB_SHA),
        ("TRANSPORT_AUTHORITY_SHA", args.repo_metodo, mod_autoridad.TRANSPORT_AUTHORITY_SHA),
        ("P_C_WORK_SHA", args.repo_work, P_C_WORK_SHA),
        ("P_C_AUDIT_SHA", args.repo_audit, P_C_AUDIT_SHA),
    ]


def es_sonda(cmd, identidades):
    for _, repo, sha in identidades:
        if cmd == mod_sondas.comando(repo, sha):
            return (repo, sha)
    return None


def imports_de(fuente):
    return sorted(set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", fuente, re.M)))


# -- utilidades de la corrida -------------------------------------------------

def ejecutar_traza(caso, ctx):
    orq = mod_orquestador.Orquestador(
        mod_corpus.WORK_ID, ctx["autoridad"],
        instancias=caso["inicio"].get("instancias"),
        ultimo_turn_id=caso["inicio"].get("ultimo_turn_id", 0))
    t = []
    for op in caso["ops"]:
        n = op[0]
        if n == "arranque":
            t.extend(orq.arranque_externo(op[1]))
        elif n == "recibir":
            t.extend(orq.recibir(op[1]))
        elif n == "despachar":
            t.extend(orq.despachar())
        elif n == "detener":
            t.extend(orq.detener())
        elif n == "continuar":
            t.extend(orq.continuar(op[1]))
        else:
            raise RuntimeError("operacion no declarada por el candidato: %s" % n)
    return [tuple(a) for a in t]


def evaluar_estructural(comprobar, mutante, ctx):
    ok_real, obs_real, _ = comprobar(mod_estructurales.REAL, ctx)
    ok_mut, obs_mut, _ = comprobar(mutante(), ctx)
    return {"ok_real": ok_real, "obs_real": obs_real, "ok_mut": ok_mut,
            "obs_mut": obs_mut, "difiere": obs_real != obs_mut}


def derivar_p_c(repo_work, repo_audit):
    def contar(repo, sha):
        s = subprocess.run(["git", "-C", repo, "rev-list", "--count", sha],
                           check=True, stdout=subprocess.PIPE).stdout.decode().strip()
        return int(s)

    def enumerar(repo, sha):
        s = subprocess.run(["git", "-C", repo, "log", "--format=%H", sha],
                           check=True, stdout=subprocess.PIPE).stdout.decode().split()
        return len(set(s))

    return {"N_CONSTRUCTOR": (contar(repo_work, P_C_WORK_SHA), enumerar(repo_work, P_C_WORK_SHA)),
            "N_AUDITOR": (contar(repo_audit, P_C_AUDIT_SHA), enumerar(repo_audit, P_C_AUDIT_SHA))}


# -- cuerpo -------------------------------------------------------------------

def cuerpo(args, log, fallos, controles, fallar_en, x0):
    if fallar_en:
        raise RuntimeError("falla inyectada en el cuerpo: %s" % fallar_en)

    ids = identidades_congeladas(args)

    log("E18 RESULTADO DE X0, IDENTIDAD POR IDENTIDAD")
    for nombre, repo, sha, ok in x0["resultado"]:
        log("  %-24s %-40s %s  resuelve=%s" % (nombre, sha, os.path.basename(repo), ok))
    log("")

    log("E19 TRAZA EXTERNA DE X0 (interceptada)")
    tr = x0["traza"]
    for cmd in tr.procesos:
        marca = es_sonda(cmd, ids)
        log("  proceso  %s   sonda=%s" % (" ".join(cmd), bool(marca)))
    log("  aperturas de archivo: %d" % len(tr.archivos))
    no_sondas = [c for c in tr.procesos if not es_sonda(c, ids)]
    cubiertas = {es_sonda(c, ids) for c in tr.procesos if es_sonda(c, ids)}
    esperadas = {(r, s) for _, r, s in ids}
    ok_e19 = (not no_sondas and not tr.archivos and cubiertas == esperadas
              and len(tr.procesos) == len(esperadas))
    log("  sondas=%d identidades=%d no-sondas=%d archivos=%d -> E19=%s"
        % (len(tr.procesos), len(esperadas), len(no_sondas), len(tr.archivos), ok_e19))
    if not ok_e19:
        fallos.append(("F21", "-", "traza externa de X0 fuera de la frontera"))
    log("")

    log("E20 TRAZA INTERNA DE X0 (interceptada)")
    log("  modulos llamados: %s" % tr.modulos_llamados())
    ajenas = tr.llamadas_a_la_corrida()
    log("  llamadas a modulos de la corrida: %s" % (ajenas or "ninguna"))
    log("  lectura aplicada: la clausula operativa, ninguna llamada a %s"
        % sorted(mod_instr.MODULOS_DE_LA_CORRIDA))
    log("  nota: una lectura literal de 'solo prevuelo o sondas' incluiria los frames de la")
    log("        biblioteca estandar que toda sonda Git necesita, y ninguna implementacion")
    log("        correcta podria satisfacerla. Queda declarado para lectura del AUDITOR.")
    if ajenas:
        fallos.append(("F22", "-", "traza interna de X0 alcanza la corrida: %s" % ajenas))
    log("")

    log("E21 AISLAMIENTO POR IMPORTACION DEL PRE-VUELO")
    for mod in (mod_prevuelo, mod_sondas):
        imps = imports_de(inspect.getsource(mod))
        cruce = sorted(set(imps) & mod_instr.MODULOS_DE_LA_CORRIDA)
        log("  %-12s importa %s   cruce con la corrida: %s"
            % (mod.__name__, imps, cruce or "ninguno"))
        if cruce:
            fallos.append(("F23", "-", "%s importa %s" % (mod.__name__, cruce)))
    log("")

    texto, blob = mod_candidato.leer(args.repo_work)
    cand = mod_candidato.Candidato(texto)
    coincide = blob == mod_candidato.CANDIDATE_BLOB_SHA
    log("E9 IDENTIDAD DEL CANDIDATO, LEIDA DESPUES DE INICIO")
    log("  leido     %s" % blob)
    log("  congelado %s" % mod_candidato.CANDIDATE_BLOB_SHA)
    log("  coincide  %s" % coincide)
    if not coincide:
        fallos.append(("F10", "-", "blob leido distinto del congelado"))
    log("")

    obligaciones = cand.obligaciones()
    ids_obl = {o[0] for o in obligaciones}
    log("SUPERFICIE NORMATIVA EXTRAIDA DEL CANDIDATO")
    log("  obligaciones            %d" % len(obligaciones))
    log("  identificadores unicos  %d" % len(ids_obl))
    log("  secciones numeradas     %s" % [s[0] for s in cand.secciones_numeradas()])
    log("  no mecanicas declaradas %s" % sorted(cand.no_mecanicas))
    log("  secciones mecanicas     %d" % len(cand.secciones_mecanicas()))
    log("")

    aut = mod_autoridad.Autoridad(args.repo_metodo)
    log("AUTORIDAD DE TRANSPORTE (derivada, no inventada)")
    log("  fuente %s:%s" % (mod_autoridad.TRANSPORT_AUTHORITY_SHA,
                            mod_autoridad.TRANSPORT_AUTHORITY_PATH))
    log("  campos %s" % ", ".join(aut.campos))
    log("  formas admitidas %s" % (aut.formas,))
    log("")

    ctx = {"autoridad": aut, "work_id": mod_corpus.WORK_ID,
           "sobre": mod_corpus.sobre, "salida": mod_corpus.salida}

    huerfanas = cand.secciones_sin_obligacion()
    log("E4 SECCIONES CON OBLIGACION")
    log("  mecanicas sin obligacion: %s" % (huerfanas or "ninguna"))
    if huerfanas:
        fallos.append(("F5", "-", "secciones sin obligacion: %s" % huerfanas))
    log("")

    violaciones = cand.violaciones_de_forma()
    log("E5 FORMA DE LAS SECCIONES MECANICAS")
    if violaciones:
        for numero, linea, detalle in violaciones:
            log("  VIOLACION seccion %s linea %d: %s" % (numero, linea, detalle))
        fallos.append(("F6", "-", "violaciones de forma: %d" % len(violaciones)))
    else:
        log("  sin violaciones")
    log("")

    log("CASOS")
    cubiertas_obl = set()
    emitidos = set()
    for caso in mod_corpus.CASOS:
        obl = caso["obligacion"]
        cubiertas_obl.add(obl)
        neg = " [%s]" % caso["negativo"] if caso.get("negativo") else ""
        if caso["tipo"] == "traza":
            producido = ejecutar_traza(caso, ctx)
            esperado = [tuple(a) for a in caso["esperado"]]
            ok = producido == esperado
            detalle = "" if ok else "producido %s != esperado %s" % (producido, esperado)
            for accion in producido:
                if accion[0] == "DETENER_REPORTAR":
                    emitidos.add(accion[1])
        else:
            comprobar, mutante = mod_estructurales.COMPROBACIONES[obl]
            r = evaluar_estructural(comprobar, mutante, ctx)
            ok = r["ok_real"] and not r["ok_mut"] and r["difiere"]
            detalle = ("real=%s mutante=%s difiere=%s | obs_real=%s | obs_mut=%s"
                       % (r["ok_real"], r["ok_mut"], r["difiere"], r["obs_real"], r["obs_mut"]))
            if r["ok_real"] and r["ok_mut"]:
                fallos.append(("F7", caso["id"], "la comprobacion no falla sobre su mutante"))
            if not r["difiere"]:
                fallos.append(("F8", caso["id"], "el observable no difiere"))
        log("  %-5s %-5s %-26s%s %s" % ("OK" if ok else "FALLO", caso["id"], obl, neg, detalle))
        if not ok:
            fallos.append(("F1", caso["id"], detalle))
    log("")

    log("E2 ATRIBUCION DE RECHAZOS")
    ajenos = sorted(emitidos - ids_obl)
    log("  identificadores emitidos: %d | ajenos: %s" % (len(emitidos), ajenos or "ninguno"))
    if ajenos:
        fallos.append(("F2", "-", "identificadores ajenos: %s" % ajenos))
        fallos.append(("F4", "-", "reglas no respaldadas: %s" % ajenos))
    log("")

    log("E3 COBERTURA CONTRA EL CANDIDATO")
    sin_caso = sorted(ids_obl - cubiertas_obl)
    sobrantes = sorted(cubiertas_obl - ids_obl)
    log("  obligaciones %d, ejercitadas %d" % (len(ids_obl), len(cubiertas_obl & ids_obl)))
    log("  sin caso: %s | sobre obligaciones inexistentes: %s"
        % (sin_caso or "ninguna", sobrantes or "ninguno"))
    if sin_caso:
        fallos.append(("F3", "-", "obligaciones sin caso: %s" % sin_caso))
    if sobrantes:
        fallos.append(("F4", "-", "casos sobre obligaciones inexistentes: %s" % sobrantes))
    log("")

    if not controles:
        return

    log("CONTROLES SOBRE EL PROPIO MECANISMO")
    c12 = mod_candidato.Candidato(mod_sinteticos.N12_OBLIGACION_SIN_CASO)
    f12 = sorted({o[0] for o in c12.obligaciones()} - set(mod_sinteticos.N12_CASOS))
    log("  N12 obligacion sintetica sin caso -> F3 = %s (%s)" % (bool(f12), f12))
    if not f12:
        fallos.append(("F7", "N12", "la cobertura no detecta una obligacion sin caso"))

    h13 = mod_candidato.Candidato(
        mod_sinteticos.N13_SECCION_SIN_OBLIGACION).secciones_sin_obligacion()
    log("  N13 seccion sintetica sin obligacion -> F5 = %s (%s)" % (bool(h13), h13))
    if not h13:
        fallos.append(("F7", "N13", "no se detecta una seccion huerfana"))

    v14 = mod_candidato.Candidato(
        mod_sinteticos.N14_CONTENIDO_FUERA_DE_FORMA).violaciones_de_forma()
    log("  N14 contenido sintetico fuera de forma -> F6 = %s" % bool(v14))
    if not v14:
        fallos.append(("F7", "N14", "no se detecta contenido colado"))

    d15 = mod_sinteticos.N15_BLOB_AJENO != mod_candidato.CANDIDATE_BLOB_SHA
    log("  N15 blob sintetico ajeno -> F10 = %s" % d15)
    if not d15:
        fallos.append(("F7", "N15", "la comprobacion de identidad no discrimina"))

    r16 = evaluar_estructural(mod_estructurales.c_sintetica,
                              mod_estructurales.m_sintetico_inerte, ctx)
    d16 = not r16["difiere"]
    log("  N16 mutante sintetico inerte -> F8 = %s" % d16)
    if not d16:
        fallos.append(("F7", "N16", "no se detecta un mutante inerte"))

    ruta17 = mod_sinteticos.N17_BITACORA
    if os.path.exists(ruta17):
        os.remove(ruta17)
    r17 = correr(args, mod_sinteticos.IDENT_SINTETICA, ruta17, x0,
                 controles=False, fallar_en="N17")
    lin17 = mod_bitacora.leer(ruta17)
    tiene_f11 = any(f[0] == "F11" for f in r17["fallos"])
    ok17 = (r17["ruta"] == "corrida" and tiene_f11 and r17["veredicto"] == "FALLO"
            and len(mod_bitacora.propias(lin17, mod_sinteticos.IDENT_SINTETICA)) == 2)
    log("  N17 aborto capturado via correr() -> ruta=%s F11=%s veredicto=%s propias=%d"
        % (r17["ruta"], tiene_f11, r17["veredicto"],
           len(mod_bitacora.propias(lin17, mod_sinteticos.IDENT_SINTETICA))))
    if not ok17:
        fallos.append(("F16", "N17", "el control de aborto no exhibio T2"))

    ruta18 = mod_sinteticos.N18_BITACORA
    if os.path.exists(ruta18):
        os.remove(ruta18)
    mod_bitacora.agregar("INICIO", ruta18, mod_sinteticos.IDENT_SINTETICA)
    antes18 = mod_bitacora.leer(ruta18)
    r18 = correr(args, mod_sinteticos.IDENT_SINTETICA, ruta18, x0, controles=False)
    ok18 = (r18["ruta"] == "reintento" and not r18["criterios_evaluados"]
            and antes18 == mod_bitacora.leer(ruta18))
    log("  N18 reintento via correr() -> ruta=%s criterios=%s bitacora sin cambios=%s"
        % (r18["ruta"], r18["criterios_evaluados"], antes18 == mod_bitacora.leer(ruta18)))
    if not ok18:
        fallos.append(("F15", "N18", "el control de reintento no exhibio X4"))

    ruta19 = mod_sinteticos.N19_BITACORA
    if os.path.exists(ruta19):
        os.remove(ruta19)
    mod_bitacora.agregar("INICIO", ruta19, mod_sinteticos.IDENT_AJENA)
    mod_bitacora.agregar("CIERRE", ruta19, mod_sinteticos.IDENT_AJENA)
    prev19 = mod_bitacora.leer(ruta19)
    intacta, _ = mod_bitacora.historia_intacta(prev19, prev19, mod_sinteticos.IDENT_SINTETICA)
    rota, _ = mod_bitacora.historia_intacta(prev19, prev19[:-1], mod_sinteticos.IDENT_SINTETICA)
    log("  N19 historia ajena -> intacta=%s alterada detectada=%s" % (intacta, not rota))
    if not (intacta and not rota):
        fallos.append(("F7", "N19", "la comprobacion de historia no discrimina"))

    ok_r20, _ = ruta_es_constante_de_unidad(inspect.getsource(mod_bitacora),
                                            mod_bitacora.RUTA_RELATIVA)
    ok_m20, _ = ruta_es_constante_de_unidad(mod_sinteticos.N20_FUENTE_DERIVADA, "derivada")
    log("  N20 ruta de bitacora -> real=%s mutante derivado=%s" % (ok_r20, ok_m20))
    if not ok_r20:
        fallos.append(("F19", "-", "la ruta de la bitacora no es constante de unidad"))
    if not (ok_r20 and not ok_m20):
        fallos.append(("F7", "N20", "la comprobacion de ruta no discrimina"))

    ids_n21 = [("SINTETICA_IRRESOLUBLE", args.repo_work, "0" * 40)]
    r21, tr21 = mod_instr.observar(lambda: mod_prevuelo.ejecutar(ids_n21))
    irres21 = mod_prevuelo.irresolubles(r21)
    log("  N21 identidad sintetica irresoluble -> NO_EJECUTABLE = %s (%s)"
        % (bool(irres21), [n for n, _, _ in irres21]))
    if not irres21:
        fallos.append(("F7", "N21", "el pre-vuelo no detecta una identidad irresoluble"))

    def x0_espia():
        r = mod_prevuelo.ejecutar(ids)
        subprocess.run(["git", "-C", args.repo_work, "show",
                        "%s:%s" % (mod_candidato.CANDIDATE_WORK_SHA,
                                   mod_candidato.CANDIDATE_PATH)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return r

    _, tr22 = mod_instr.observar(x0_espia)
    no_sondas22 = [c for c in tr22.procesos if not es_sonda(c, ids)]
    difiere22 = tr22.procesos != tr.procesos
    log("  N22 X0 sintetico que lee el candidato -> F21 = %s, traza difiere = %s"
        % (bool(no_sondas22), difiere22))
    if not (no_sondas22 and difiere22):
        fallos.append(("F7", "N22", "la traza externa no distingue un X0 que lee"))

    def x0_en_memoria(_corpus=mod_corpus):
        r = mod_prevuelo.ejecutar(ids)
        _corpus.sobre(turn_id=7)
        return r

    _, tr23 = mod_instr.observar(x0_en_memoria)
    ajenas23 = tr23.llamadas_a_la_corrida()
    difiere23 = tr23.llamadas_a_la_corrida() != tr.llamadas_a_la_corrida()
    sin_extra23 = [c for c in tr23.procesos if not es_sonda(c, ids)] == [] and not tr23.archivos
    log("  N23 X0 sintetico que ejecuta en memoria -> F22 = %s (%s), traza interna difiere = %s,"
        " sin interaccion externa extra = %s"
        % (bool(ajenas23), ajenas23, difiere23, sin_extra23))
    if not (ajenas23 and difiere23):
        fallos.append(("F7", "N23", "la traza interna no distingue un X0 que ejecuta en memoria"))

    imps24 = imports_de(mod_sinteticos.N24_FUENTE_IMPORTADORA)
    cruce24 = sorted(set(imps24) & mod_instr.MODULOS_DE_LA_CORRIDA)
    log("  N24 pre-vuelo sintetico que importa la corrida -> F23 = %s (%s)"
        % (bool(cruce24), cruce24))
    if not cruce24:
        fallos.append(("F7", "N24", "el aislamiento por importacion no discrimina"))
    log("")

    log("CONTROLES NEGATIVOS DEL CORPUS")
    presentes = {c["negativo"] for c in mod_corpus.CASOS if c.get("negativo")}
    presentes |= {"N%d" % i for i in range(12, 25)}
    faltan = [n for n in NEGATIVOS_EXIGIDOS if n not in presentes]
    log("  exigidos  N1..N24")
    log("  presentes %s" % sorted(presentes, key=lambda x: int(x[1:])))
    if faltan:
        fallos.append(("F3", "-", "controles negativos ausentes: %s" % faltan))
    log("")

    log("E8 P-C DERIVACION FUERA DEL ORQUESTADOR")
    log("  work  %s@%s" % (args.repo_work, P_C_WORK_SHA))
    log("  audit %s@%s" % (args.repo_audit, P_C_AUDIT_SHA))
    for nombre, (a, b) in sorted(derivar_p_c(args.repo_work, args.repo_audit).items()):
        log("  %-14s rev-list --count = %d   git log unico = %d   coincide = %s"
            % (nombre, a, b, a == b))
        if a != b:
            fallos.append(("F9", nombre, "%d != %d" % (a, b)))
    log("")


def ruta_es_constante_de_unidad(fuente, ruta_relativa):
    m = re.search(r"^RUTA_RELATIVA\s*=\s*(.+)$", fuente, re.M)
    if not m:
        return False, "no se declara RUTA_RELATIVA"
    asignacion = m.group(1)
    derivada = any(t in asignacion for t in ("__file__", "dirname", "abspath", "os.path"))
    esperada = ruta_relativa == "u2-reglas-orquestador/BITACORA.txt"
    return (esperada and not derivada,
            "asignacion=%s | derivada=%s" % (asignacion.strip(), derivada))


# -- función de corrida compartida --------------------------------------------

def correr(args, ident, ruta_bitacora, x0, controles=True, fallar_en=None):
    lineas = []
    log = lineas.append
    fallos = []

    log("REGLA DE EJECUCION")
    log("  contrato  %s" % ident["contrato"])
    log("  candidato %s" % ident["candidato"])
    log("  bitacora  %s" % os.path.abspath(ruta_bitacora))

    previas = mod_bitacora.leer(ruta_bitacora)
    log("  lineas al abrir: %d (ajenas a esta identidad: %d)"
        % (len(previas), len(mod_bitacora.ajenas(previas, ident))))

    if mod_bitacora.hay_inicio_previo(ruta_bitacora, ident):
        log("  X4 ya existe un INICIO de esta identidad: la invocacion es un reintento")
        log("  no anota, no evalua criterios y no reemplaza el resultado anterior")
        log("")
        log("VEREDICTO=FALLO")
        log("  F12 - reintento bajo un contrato ya ejecutado")
        return {"ruta": "reintento", "criterios_evaluados": False, "veredicto": "FALLO",
                "fallos": [("F12", "-", "reintento")], "lineas": lineas}

    log("  E11 no existe INICIO previo de esta identidad")
    mod_bitacora.agregar("INICIO", ruta_bitacora, ident)
    log("  INICIO anotado antes del primer caso")
    log("")

    try:
        cuerpo(args, log, fallos, controles, fallar_en, x0)
    except Exception:
        log("")
        log("F11 EXCEPCION CAPTURADA DESPUES DE INICIO (T2)")
        for l in traceback.format_exc().rstrip().split("\n"):
            log("  " + l)
        fallos.append(("F11", "-", "el cuerpo produjo una excepcion, resuelta en el veredicto"))
        log("")

    mod_bitacora.agregar("CIERRE", ruta_bitacora, ident)
    actuales = mod_bitacora.leer(ruta_bitacora)
    ok_coh, det_coh = mod_bitacora.coherente(ruta_bitacora, ident)
    ok_hist, det_hist = mod_bitacora.historia_intacta(previas, actuales, ident)
    log("E12 / E16 BITACORA")
    for l in actuales:
        log("  %s" % l)
    log("  coherente = %s (%s)" % (ok_coh, det_coh))
    log("  historia ajena intacta = %s (%s)" % (ok_hist, det_hist))
    if not ok_coh:
        fallos.append(("F13", "-", "bitacora incoherente: %s" % det_coh))
    if not ok_hist:
        fallos.append(("F18", "-", "historia ajena alterada: %s" % det_hist))
    log("")

    veredicto = "EXITO" if not fallos else "FALLO"
    log("VEREDICTO=%s" % veredicto)
    for c, k, d in fallos:
        log("  %s %s %s" % (c, k, d))
    return {"ruta": "corrida", "criterios_evaluados": True, "veredicto": veredicto,
            "fallos": fallos, "lineas": lineas}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-metodo", required=True)
    ap.add_argument("--repo-work", required=True)
    ap.add_argument("--repo-audit", required=True)
    ap.add_argument("--salida", default="salida.txt")
    args = ap.parse_args()

    cabecera = []
    ids = identidades_congeladas(args)
    cabecera.append("X0 PRE-VUELO, ESTRICTAMENTE ANTES DE INICIO")
    resultado, traza = mod_instr.observar(lambda: mod_prevuelo.ejecutar(ids))
    for nombre, repo, sha, ok in resultado:
        cabecera.append("  %-24s %s  resuelve=%s" % (nombre, sha, ok))
    irres = mod_prevuelo.irresolubles(resultado)
    cabecera.append("  identidades irresolubles: %s" % ([n for n, _, _ in irres] or "ninguna"))
    cabecera.append("")

    x0 = {"resultado": resultado, "traza": traza}

    if irres:
        cabecera.append("NO_EJECUTABLE")
        cabecera.append("  no se anota INICIO, no se evalua ningun criterio, no se emite")
        cabecera.append("  veredicto y el contrato no queda consumido")
        texto = "\n".join(cabecera) + "\n"
        io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
        sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
        return 2

    ruta = mod_bitacora.ruta_real(args.repo_work)
    r = correr(args, IDENT_REAL, ruta, x0)

    texto = "\n".join(cabecera + r["lineas"]) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
    sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
    return 0 if r["veredicto"] == "EXITO" else 1


if __name__ == "__main__":
    sys.exit(main())
