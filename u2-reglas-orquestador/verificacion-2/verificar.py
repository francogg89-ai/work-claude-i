"""Corrida única del contrato previo congelado de U2.

Congelado en audit-chatgpt-i@fd356b9369cf5bd80a9a15a6695453f2e191dcfe.

El mecanismo produce su resultado y la comparación con el resultado normativo esperado es
posterior. Evalúa E1-E8, F1-F9 y N1-N15. No existe tercera salida.

Uso:
    python verificar.py --repo-metodo <ruta> --repo-work <ruta> --repo-audit <ruta>
"""

import argparse
import io
import subprocess
import sys

import autoridad as mod_autoridad
import candidato as mod_candidato
import corpus as mod_corpus
import estructurales as mod_estructurales
import orquestador as mod_orquestador
import sinteticos as mod_sinteticos

P_C_WORK_SHA = "5f5e2ee8e9bcc7f471cabcd0ecd865ff5cfa0a39"
P_C_AUDIT_SHA = "9f8512f1e7228fb81692c62b33414b11d974bd8d"

NEGATIVOS_EXIGIDOS = ["N%d" % i for i in range(1, 16)]


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


def derivar_p_c(repo_work, repo_audit):
    def contar(repo, sha):
        s = subprocess.run(["git", "-C", repo, "rev-list", "--count", sha],
                           check=True, stdout=subprocess.PIPE).stdout.decode().strip()
        return int(s)

    def enumerar(repo, sha):
        s = subprocess.run(["git", "-C", repo, "log", "--format=%H", sha],
                           check=True, stdout=subprocess.PIPE).stdout.decode().split()
        return len(set(s))

    return {
        "N_CONSTRUCTOR": (contar(repo_work, P_C_WORK_SHA), enumerar(repo_work, P_C_WORK_SHA)),
        "N_AUDITOR": (contar(repo_audit, P_C_AUDIT_SHA), enumerar(repo_audit, P_C_AUDIT_SHA)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-metodo", required=True)
    ap.add_argument("--repo-work", required=True)
    ap.add_argument("--repo-audit", required=True)
    ap.add_argument("--salida", default="salida.txt")
    args = ap.parse_args()

    lineas = []
    log = lineas.append
    fallos = []

    # -- E8/F9 identidad del candidato ---------------------------------------
    texto, blob = mod_candidato.leer(args.repo_work)
    cand = mod_candidato.Candidato(texto)
    coincide = blob == mod_candidato.CANDIDATE_BLOB_SHA
    log("E8 IDENTIDAD DEL CANDIDATO")
    log("  leido    %s" % blob)
    log("  congelado %s" % mod_candidato.CANDIDATE_BLOB_SHA)
    log("  coincide %s" % coincide)
    if not coincide:
        fallos.append(("F9", "-", "blob leido distinto del congelado"))
    log("")

    obligaciones = cand.obligaciones()
    ids_obligacion = [o[0] for o in obligaciones]
    conjunto_obligaciones = set(ids_obligacion)

    log("SUPERFICIE NORMATIVA EXTRAIDA DEL CANDIDATO")
    log("  obligaciones            %d" % len(obligaciones))
    log("  identificadores unicos  %d" % len(conjunto_obligaciones))
    log("  secciones numeradas     %s" % [s[0] for s in cand.secciones_numeradas()])
    log("  no mecanicas declaradas %s" % sorted(cand.no_mecanicas))
    log("  secciones mecanicas     %d" % len(cand.secciones_mecanicas()))
    log("")

    # -- autoridad ------------------------------------------------------------
    aut = mod_autoridad.Autoridad(args.repo_metodo)
    log("AUTORIDAD DE TRANSPORTE (derivada, no inventada)")
    log("  fuente %s:%s" % (mod_autoridad.TRANSPORT_AUTHORITY_SHA,
                            mod_autoridad.TRANSPORT_AUTHORITY_PATH))
    log("  campos %s" % ", ".join(aut.campos))
    log("  formas admitidas %s" % (aut.formas,))
    log("")

    ctx = {"autoridad": aut, "work_id": mod_corpus.WORK_ID,
           "sobre": mod_corpus.sobre, "salida": mod_corpus.salida}

    # -- E4/F5 secciones sin obligacion --------------------------------------
    huerfanas = cand.secciones_sin_obligacion()
    log("E4 SECCIONES CON OBLIGACION")
    log("  secciones mecanicas sin obligacion: %s" % (huerfanas or "ninguna"))
    if huerfanas:
        fallos.append(("F5", "-", "secciones sin obligacion: %s" % huerfanas))
    log("")

    # -- E5/F6 forma de las secciones ----------------------------------------
    violaciones = cand.violaciones_de_forma()
    log("E5 FORMA DE LAS SECCIONES MECANICAS")
    if violaciones:
        for numero, linea, detalle in violaciones:
            log("  VIOLACION seccion %s linea %d: %s" % (numero, linea, detalle))
        fallos.append(("F6", "-", "violaciones de forma: %d" % len(violaciones)))
    else:
        log("  sin violaciones")
    log("")

    # -- E1 casos -------------------------------------------------------------
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
            ok_real, det_real = comprobar(mod_estructurales.REAL, ctx)
            ok_mut, det_mut = comprobar(mutante(), ctx)
            ok = ok_real and not ok_mut
            detalle = "real=%s (%s) mutante=%s" % (ok_real, det_real, ok_mut)
            if ok_real and ok_mut:
                fallos.append(("F7", caso["id"],
                               "la comprobacion no falla sobre su mutante"))

        log("  %-5s %-5s %-26s%s %s" % ("OK" if ok else "FALLO", caso["id"], obl, neg, detalle))
        if not ok:
            fallos.append(("F1", caso["id"], detalle))
        if not ok and caso.get("negativo"):
            fallos.append(("N", caso["id"], "control %s no discriminado" % caso["negativo"]))
    log("")

    # -- E2/F2 y F4 identificadores emitidos ---------------------------------
    log("E2 ATRIBUCION DE RECHAZOS")
    ajenos = sorted(emitidos - conjunto_obligaciones)
    log("  identificadores emitidos por el mecanismo: %d" % len(emitidos))
    log("  ajenos al candidato: %s" % (ajenos or "ninguno"))
    if ajenos:
        fallos.append(("F2", "-", "identificadores ajenos: %s" % ajenos))
        fallos.append(("F4", "-", "reglas no respaldadas por el candidato: %s" % ajenos))
    log("")

    # -- E3/F3 cobertura ------------------------------------------------------
    log("E3 COBERTURA CONTRA EL CANDIDATO")
    sin_caso = sorted(conjunto_obligaciones - cubiertas)
    ajenas = sorted(cubiertas - conjunto_obligaciones)
    log("  obligaciones del candidato %d, ejercitadas %d"
        % (len(conjunto_obligaciones), len(cubiertas & conjunto_obligaciones)))
    log("  sin caso: %s" % (sin_caso or "ninguna"))
    log("  casos sobre obligaciones inexistentes: %s" % (ajenas or "ninguno"))
    if sin_caso:
        fallos.append(("F3", "-", "obligaciones sin caso: %s" % sin_caso))
    if ajenas:
        fallos.append(("F4", "-", "casos sobre obligaciones inexistentes: %s" % ajenas))
    log("")

    # -- E6/F7 y N12-N15 ------------------------------------------------------
    log("CONTROLES SOBRE EL PROPIO MECANISMO")
    c12 = mod_candidato.Candidato(mod_sinteticos.N12_OBLIGACION_SIN_CASO)
    faltan12 = {o[0] for o in c12.obligaciones()} - set(mod_sinteticos.N12_CASOS)
    log("  N12 obligacion sintetica sin caso -> F3 = %s (%s)"
        % (bool(faltan12), sorted(faltan12)))
    if not faltan12:
        fallos.append(("F7", "N12", "la cobertura no detecta una obligacion sin caso"))

    c13 = mod_candidato.Candidato(mod_sinteticos.N13_SECCION_SIN_OBLIGACION)
    huerf13 = c13.secciones_sin_obligacion()
    log("  N13 seccion sintetica sin obligacion -> F5 = %s (%s)" % (bool(huerf13), huerf13))
    if not huerf13:
        fallos.append(("F7", "N13", "la comprobacion de secciones no detecta una huerfana"))

    c14 = mod_candidato.Candidato(mod_sinteticos.N14_CONTENIDO_FUERA_DE_FORMA)
    viol14 = c14.violaciones_de_forma()
    log("  N14 contenido sintetico fuera de forma -> F6 = %s (%s)"
        % (bool(viol14), viol14))
    if not viol14:
        fallos.append(("F7", "N14", "la comprobacion de forma no detecta contenido colado"))

    detecta15 = mod_sinteticos.N15_BLOB_AJENO != mod_candidato.CANDIDATE_BLOB_SHA
    log("  N15 blob sintetico ajeno -> F9 = %s" % detecta15)
    if not detecta15:
        fallos.append(("F7", "N15", "la comprobacion de identidad no discrimina"))
    log("")

    log("CONTROLES NEGATIVOS DEL CORPUS")
    presentes = {c["negativo"] for c in mod_corpus.CASOS if c.get("negativo")}
    presentes |= {"N12", "N13", "N14", "N15"}
    faltan = [n for n in NEGATIVOS_EXIGIDOS if n not in presentes]
    log("  exigidos  %s" % NEGATIVOS_EXIGIDOS)
    log("  presentes %s" % sorted(presentes))
    if faltan:
        fallos.append(("F3", "-", "controles negativos ausentes: %s" % faltan))
    log("")

    # -- E7/F8 P-C ------------------------------------------------------------
    log("E7 P-C DERIVACION FUERA DEL ORQUESTADOR")
    log("  work  %s@%s" % (args.repo_work, P_C_WORK_SHA))
    log("  audit %s@%s" % (args.repo_audit, P_C_AUDIT_SHA))
    pc = derivar_p_c(args.repo_work, args.repo_audit)
    for nombre, (a, b) in sorted(pc.items()):
        log("  %-14s rev-list --count = %d   git log unico = %d   coincide = %s"
            % (nombre, a, b, a == b))
        if a != b:
            fallos.append(("F8", nombre, "%d != %d" % (a, b)))
    log("")

    veredicto = "EXITO" if not fallos else "FALLO"
    log("VEREDICTO=%s" % veredicto)
    for criterio, caso, detalle in fallos:
        log("  %s %s %s" % (criterio, caso, detalle))

    texto_salida = "\n".join(lineas) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto_salida)
    sys.stdout.write(texto_salida.encode("ascii", "replace").decode("ascii"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
