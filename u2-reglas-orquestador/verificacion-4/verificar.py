"""Corrida única del contrato previo congelado de U2.

Congelado en audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933.

Toda invocación —la real y las sintéticas de N17 y N18— atraviesa `correr()`. La guardia X4 vive
ahí y no en el punto de entrada, de modo que romperla haga fallar los controles.

Semántica de terminación: T1 veredicto EXITO con CIERRE; T2 veredicto FALLO con CIERRE, incluida
la excepción capturada como F11; T3 terminación sin veredicto, que deja INICIO sin CIERRE y que
ningún mecanismo puede producir de sí mismo.

Uso:
    python verificar.py --repo-metodo <ruta> --repo-work <ruta> --repo-audit <ruta>
"""

import argparse
import io
import inspect
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
import orquestador as mod_orquestador
import sinteticos as mod_sinteticos

P_C_WORK_SHA = "7292639ddc2706a12c86d244b2a7352a8025b733"
P_C_AUDIT_SHA = "d6dba9decf6091078fa1b7f4f49b044e59f4df02"

IDENT_REAL = {"contrato": mod_bitacora.CONTRATO, "candidato": mod_bitacora.CANDIDATO}

NEGATIVOS_EXIGIDOS = ["N%d" % i for i in range(1, 21)]


# -- utilidades ---------------------------------------------------------------

def ejecutar_traza(caso, ctx):
    orq = mod_orquestador.Orquestador(
        mod_corpus.WORK_ID, ctx["autoridad"],
        instancias=caso["inicio"].get("instancias"),
        ultimo_turn_id=caso["inicio"].get("ultimo_turn_id", 0))
    traza = []
    for op in caso["ops"]:
        nombre = op[0]
        if nombre == "arranque":
            traza.extend(orq.arranque_externo(op[1]))
        elif nombre == "recibir":
            traza.extend(orq.recibir(op[1]))
        elif nombre == "despachar":
            traza.extend(orq.despachar())
        elif nombre == "detener":
            traza.extend(orq.detener())
        elif nombre == "continuar":
            traza.extend(orq.continuar(op[1]))
        else:
            raise RuntimeError("operacion no declarada por el candidato: %s" % nombre)
    return [tuple(a) for a in traza]


def evaluar_estructural(comprobar, mutante, ctx):
    ok_real, obs_real, det_real = comprobar(mod_estructurales.REAL, ctx)
    ok_mut, obs_mut, det_mut = comprobar(mutante(), ctx)
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


def ruta_es_constante_de_unidad(fuente, ruta_relativa):
    """E17: la ruta es una constante de unidad y no se deriva del directorio del mecanismo."""
    m = re.search(r"^RUTA_RELATIVA\s*=\s*(.+)$", fuente, re.M)
    if not m:
        return False, "no se declara RUTA_RELATIVA"
    asignacion = m.group(1)
    derivada = any(t in asignacion for t in ("__file__", "dirname", "abspath", "os.path"))
    esperada = ruta_relativa == "u2-reglas-orquestador/BITACORA.txt"
    return (esperada and not derivada,
            "asignacion=%s | derivada=%s | esperada=%s" % (asignacion.strip(), derivada, esperada))


# -- cuerpo -------------------------------------------------------------------

def cuerpo(args, log, fallos, controles, fallar_en):
    if fallar_en:
        raise RuntimeError("falla inyectada en el cuerpo: %s" % fallar_en)

    texto, blob = mod_candidato.leer(args.repo_work)
    cand = mod_candidato.Candidato(texto)
    coincide = blob == mod_candidato.CANDIDATE_BLOB_SHA
    log("E9 IDENTIDAD DEL CANDIDATO")
    log("  leido     %s" % blob)
    log("  congelado %s" % mod_candidato.CANDIDATE_BLOB_SHA)
    log("  coincide  %s" % coincide)
    if not coincide:
        fallos.append(("F10", "-", "blob leido distinto del congelado"))
    log("")

    obligaciones = cand.obligaciones()
    ids = {o[0] for o in obligaciones}
    log("SUPERFICIE NORMATIVA EXTRAIDA DEL CANDIDATO")
    log("  obligaciones            %d" % len(obligaciones))
    log("  identificadores unicos  %d" % len(ids))
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
    cubiertas = set()
    emitidos = set()
    for caso in mod_corpus.CASOS:
        obl = caso["obligacion"]
        cubiertas.add(obl)
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
                fallos.append(("F8", caso["id"], "el observable no difiere entre real y mutante"))
        log("  %-5s %-5s %-26s%s %s" % ("OK" if ok else "FALLO", caso["id"], obl, neg, detalle))
        if not ok:
            fallos.append(("F1", caso["id"], detalle))
    log("")

    log("E2 ATRIBUCION DE RECHAZOS")
    ajenos = sorted(emitidos - ids)
    log("  identificadores emitidos: %d" % len(emitidos))
    log("  ajenos al candidato: %s" % (ajenos or "ninguno"))
    if ajenos:
        fallos.append(("F2", "-", "identificadores ajenos: %s" % ajenos))
        fallos.append(("F4", "-", "reglas no respaldadas: %s" % ajenos))
    log("")

    log("E3 COBERTURA CONTRA EL CANDIDATO")
    sin_caso = sorted(ids - cubiertas)
    sobrantes = sorted(cubiertas - ids)
    log("  obligaciones %d, ejercitadas %d" % (len(ids), len(cubiertas & ids)))
    log("  sin caso: %s" % (sin_caso or "ninguna"))
    log("  casos sobre obligaciones inexistentes: %s" % (sobrantes or "ninguno"))
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

    h13 = mod_candidato.Candidato(mod_sinteticos.N13_SECCION_SIN_OBLIGACION).secciones_sin_obligacion()
    log("  N13 seccion sintetica sin obligacion -> F5 = %s (%s)" % (bool(h13), h13))
    if not h13:
        fallos.append(("F7", "N13", "no se detecta una seccion huerfana"))

    v14 = mod_candidato.Candidato(mod_sinteticos.N14_CONTENIDO_FUERA_DE_FORMA).violaciones_de_forma()
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
    log("  N16 mutante sintetico inerte -> F8 = %s (obs_real=%s obs_mut=%s)"
        % (d16, r16["obs_real"], r16["obs_mut"]))
    if not d16:
        fallos.append(("F7", "N16", "no se detecta un mutante que no altera el observable"))

    # -- N17: aborto capturado, atravesando correr() --------------------------
    ruta17 = mod_sinteticos.N17_BITACORA
    if os.path.exists(ruta17):
        os.remove(ruta17)
    r17 = correr(args, mod_sinteticos.IDENT_SINTETICA, ruta17, controles=False,
                 fallar_en="N17")
    lin17 = mod_bitacora.leer(ruta17)
    tiene_f11 = any(f[0] == "F11" for f in r17["fallos"])
    ok17 = (r17["ruta"] == "corrida" and tiene_f11 and r17["veredicto"] == "FALLO"
            and len(mod_bitacora.propias(lin17, mod_sinteticos.IDENT_SINTETICA)) == 2)
    log("  N17 aborto capturado via correr() -> ruta=%s F11=%s veredicto=%s bitacora=%s"
        % (r17["ruta"], tiene_f11, r17["veredicto"], lin17))
    if not ok17:
        fallos.append(("F16", "N17", "el control de aborto no exhibio T2"))

    # -- N18: reintento, atravesando la misma correr() ------------------------
    ruta18 = mod_sinteticos.N18_BITACORA
    if os.path.exists(ruta18):
        os.remove(ruta18)
    mod_bitacora.agregar("INICIO", ruta18, mod_sinteticos.IDENT_SINTETICA)
    antes18 = mod_bitacora.leer(ruta18)
    r18 = correr(args, mod_sinteticos.IDENT_SINTETICA, ruta18, controles=False)
    despues18 = mod_bitacora.leer(ruta18)
    ok18 = (r18["ruta"] == "reintento" and not r18["criterios_evaluados"]
            and antes18 == despues18)
    log("  N18 reintento via correr() -> ruta=%s criterios=%s bitacora sin cambios=%s"
        % (r18["ruta"], r18["criterios_evaluados"], antes18 == despues18))
    if not ok18:
        fallos.append(("F15", "N18", "el control de reintento no exhibio la guardia X4"))

    # -- N19: historia ajena alterada -> F18 ---------------------------------
    ruta19 = mod_sinteticos.N19_BITACORA
    if os.path.exists(ruta19):
        os.remove(ruta19)
    mod_bitacora.agregar("INICIO", ruta19, mod_sinteticos.IDENT_AJENA)
    mod_bitacora.agregar("CIERRE", ruta19, mod_sinteticos.IDENT_AJENA)
    previas19 = mod_bitacora.leer(ruta19)
    intacta, det_i = mod_bitacora.historia_intacta(previas19, previas19,
                                                   mod_sinteticos.IDENT_SINTETICA)
    mutilada = previas19[:-1]
    rota, det_r = mod_bitacora.historia_intacta(previas19, mutilada,
                                                mod_sinteticos.IDENT_SINTETICA)
    d19 = intacta and not rota
    log("  N19 historia ajena: intacta=%s (%s) | alterada detectada=%s (%s)"
        % (intacta, det_i, not rota, det_r))
    if not d19:
        fallos.append(("F7", "N19", "la comprobacion de historia no discrimina"))

    # -- N20: ruta derivada del propio directorio -> F19 ---------------------
    ok_real20, det_real20 = ruta_es_constante_de_unidad(
        inspect.getsource(mod_bitacora), mod_bitacora.RUTA_RELATIVA)
    ok_mut20, det_mut20 = ruta_es_constante_de_unidad(
        mod_sinteticos.N20_FUENTE_DERIVADA, "derivada")
    d20 = ok_real20 and not ok_mut20
    log("  N20 ruta de bitacora: real=%s (%s) | mutante derivado=%s"
        % (ok_real20, det_real20, ok_mut20))
    if not ok_real20:
        fallos.append(("F19", "-", "la ruta de la bitacora no es constante de unidad"))
    if not d20:
        fallos.append(("F7", "N20", "la comprobacion de ruta no discrimina"))
    log("")

    log("CONTROLES NEGATIVOS DEL CORPUS")
    presentes = {c["negativo"] for c in mod_corpus.CASOS if c.get("negativo")}
    presentes |= {"N12", "N13", "N14", "N15", "N16", "N17", "N18", "N19", "N20"}
    faltan = [n for n in NEGATIVOS_EXIGIDOS if n not in presentes]
    log("  exigidos  %s" % NEGATIVOS_EXIGIDOS)
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


# -- función de corrida compartida --------------------------------------------

def correr(args, ident, ruta_bitacora, controles=True, fallar_en=None):
    """Único camino hacia una ejecución. La guardia X4 vive aquí."""
    lineas = []
    log = lineas.append
    fallos = []

    log("REGLA DE EJECUCION")
    log("  contrato  %s" % ident["contrato"])
    log("  candidato %s" % ident["candidato"])
    log("  bitacora  %s" % os.path.abspath(ruta_bitacora))

    previas = mod_bitacora.leer(ruta_bitacora)
    log("  lineas presentes al abrir: %d (ajenas a esta identidad: %d)"
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
        cuerpo(args, log, fallos, controles, fallar_en)
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
    for criterio, caso, detalle in fallos:
        log("  %s %s %s" % (criterio, caso, detalle))

    return {"ruta": "corrida", "criterios_evaluados": True, "veredicto": veredicto,
            "fallos": fallos, "lineas": lineas}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-metodo", required=True)
    ap.add_argument("--repo-work", required=True)
    ap.add_argument("--repo-audit", required=True)
    ap.add_argument("--salida", default="salida.txt")
    args = ap.parse_args()

    ruta = mod_bitacora.ruta_real(args.repo_work)
    r = correr(args, IDENT_REAL, ruta)

    texto = "\n".join(r["lineas"]) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
    sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
    return 0 if r["veredicto"] == "EXITO" else 1


if __name__ == "__main__":
    sys.exit(main())
