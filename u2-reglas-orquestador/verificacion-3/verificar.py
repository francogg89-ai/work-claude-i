"""Corrida única del contrato previo congelado de U2.

Congelado en audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0.

Regla de ejecución: la corrida empieza al anotar INICIO en la bitácora. Si ya existe un INICIO
para esta identidad de contrato, la invocación es un reintento, se resuelve por X4/F12 y no
reemplaza el resultado anterior. Cualquier excepción posterior a INICIO se resuelve como F11 y
no habilita corregir y reintentar.

Uso:
    python verificar.py --repo-metodo <ruta> --repo-work <ruta> --repo-audit <ruta>
"""

import argparse
import io
import os
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

P_C_WORK_SHA = "19d33fcb025f9d84736cd59f9e3ca6978ff4b48b"
P_C_AUDIT_SHA = "693498fc8ff681069cf3997ea7e3f8636826a2d3"

NEGATIVOS_EXIGIDOS = ["N%d" % i for i in range(1, 19)]


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
    return {
        "ok_real": ok_real, "obs_real": obs_real, "det_real": det_real,
        "ok_mut": ok_mut, "obs_mut": obs_mut, "det_mut": det_mut,
        "difiere": obs_real != obs_mut,
    }


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


def cuerpo(args, log, fallos):
    """Todo lo que ocurre después de INICIO. Cualquier excepción aquí es F11."""
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
                       % (r["ok_real"], r["ok_mut"], r["difiere"],
                          r["obs_real"], r["obs_mut"]))
            if r["ok_real"] and r["ok_mut"]:
                fallos.append(("F7", caso["id"], "la comprobacion no falla sobre su mutante"))
            if not r["difiere"]:
                fallos.append(("F8", caso["id"], "el observable no difiere entre real y mutante"))

        log("  %-5s %-5s %-26s%s %s" % ("OK" if ok else "FALLO", caso["id"], obl, neg, detalle))
        if not ok:
            fallos.append(("F1", caso["id"], detalle))
        if not ok and caso.get("negativo"):
            fallos.append(("N", caso["id"], "control %s no discriminado" % caso["negativo"]))
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
    ajenas = sorted(cubiertas - ids)
    log("  obligaciones %d, ejercitadas %d" % (len(ids), len(cubiertas & ids)))
    log("  sin caso: %s" % (sin_caso or "ninguna"))
    log("  casos sobre obligaciones inexistentes: %s" % (ajenas or "ninguno"))
    if sin_caso:
        fallos.append(("F3", "-", "obligaciones sin caso: %s" % sin_caso))
    if ajenas:
        fallos.append(("F4", "-", "casos sobre obligaciones inexistentes: %s" % ajenas))
    log("")

    log("CONTROLES SOBRE EL PROPIO MECANISMO")
    c12 = mod_candidato.Candidato(mod_sinteticos.N12_OBLIGACION_SIN_CASO)
    faltan12 = sorted({o[0] for o in c12.obligaciones()} - set(mod_sinteticos.N12_CASOS))
    log("  N12 obligacion sintetica sin caso -> F3 = %s (%s)" % (bool(faltan12), faltan12))
    if not faltan12:
        fallos.append(("F7", "N12", "la cobertura no detecta una obligacion sin caso"))

    c13 = mod_candidato.Candidato(mod_sinteticos.N13_SECCION_SIN_OBLIGACION)
    h13 = c13.secciones_sin_obligacion()
    log("  N13 seccion sintetica sin obligacion -> F5 = %s (%s)" % (bool(h13), h13))
    if not h13:
        fallos.append(("F7", "N13", "no se detecta una seccion huerfana"))

    c14 = mod_candidato.Candidato(mod_sinteticos.N14_CONTENIDO_FUERA_DE_FORMA)
    v14 = c14.violaciones_de_forma()
    log("  N14 contenido sintetico fuera de forma -> F6 = %s (%s)" % (bool(v14), v14))
    if not v14:
        fallos.append(("F7", "N14", "no se detecta contenido colado"))

    d15 = mod_sinteticos.N15_BLOB_AJENO != mod_candidato.CANDIDATE_BLOB_SHA
    log("  N15 blob sintetico ajeno -> F10 = %s" % d15)
    if not d15:
        fallos.append(("F7", "N15", "la comprobacion de identidad no discrimina"))

    r16 = evaluar_estructural(mod_estructurales.c_sintetica,
                              mod_estructurales.m_sintetico_inerte, ctx)
    detecta16 = not r16["difiere"]
    log("  N16 mutante sintetico inerte -> F8 = %s (obs_real=%s obs_mut=%s)"
        % (detecta16, r16["obs_real"], r16["obs_mut"]))
    if not detecta16:
        fallos.append(("F7", "N16", "no se detecta un mutante que no altera el observable"))

    for ruta in (mod_sinteticos.N17_BITACORA, mod_sinteticos.N18_BITACORA):
        if os.path.exists(ruta):
            os.remove(ruta)

    ident = dict(contrato=mod_sinteticos.CONTRATO_SINTETICO,
                 candidato=mod_sinteticos.CANDIDATO_SINTETICO)
    mod_bitacora.agregar("INICIO", ruta=mod_sinteticos.N17_BITACORA, **ident)
    try:
        raise RuntimeError("aborto sintetico despues de INICIO")
    except RuntimeError:
        pass
    lineas17 = mod_bitacora.leer(mod_sinteticos.N17_BITACORA)
    i17 = len(mod_bitacora.eventos(lineas17, "INICIO", **ident))
    c17 = len(mod_bitacora.eventos(lineas17, "CIERRE", **ident))
    detecta17 = i17 == 1 and c17 == 0
    log("  N17 invocacion sintetica abortada -> INICIO=%d CIERRE=%d observable = %s"
        % (i17, c17, detecta17))
    if not detecta17:
        fallos.append(("F7", "N17", "un aborto no queda observable en la bitacora"))

    mod_bitacora.agregar("INICIO", ruta=mod_sinteticos.N18_BITACORA, **ident)
    reintento = mod_bitacora.hay_inicio_previo(ruta=mod_sinteticos.N18_BITACORA, **ident)
    lineas18_antes = mod_bitacora.leer(mod_sinteticos.N18_BITACORA)
    log("  N18 segunda invocacion sobre bitacora con INICIO previo -> F12 = %s" % reintento)
    log("      la guardia se detiene sin anotar ni emitir veredicto: bitacora sin cambios = %s"
        % (mod_bitacora.leer(mod_sinteticos.N18_BITACORA) == lineas18_antes))
    if not reintento:
        fallos.append(("F7", "N18", "un reintento no es detectado"))
    log("")

    log("CONTROLES NEGATIVOS DEL CORPUS")
    presentes = {c["negativo"] for c in mod_corpus.CASOS if c.get("negativo")}
    presentes |= {"N12", "N13", "N14", "N15", "N16", "N17", "N18"}
    faltan = [n for n in NEGATIVOS_EXIGIDOS if n not in presentes]
    log("  exigidos  %s" % NEGATIVOS_EXIGIDOS)
    log("  presentes %s" % sorted(presentes))
    if faltan:
        fallos.append(("F3", "-", "controles negativos ausentes: %s" % faltan))
    log("")

    log("E8 P-C DERIVACION FUERA DEL ORQUESTADOR")
    log("  work  %s@%s" % (args.repo_work, P_C_WORK_SHA))
    log("  audit %s@%s" % (args.repo_audit, P_C_AUDIT_SHA))
    pc = derivar_p_c(args.repo_work, args.repo_audit)
    for nombre, (a, b) in sorted(pc.items()):
        log("  %-14s rev-list --count = %d   git log unico = %d   coincide = %s"
            % (nombre, a, b, a == b))
        if a != b:
            fallos.append(("F9", nombre, "%d != %d" % (a, b)))
    log("")


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

    log("REGLA DE EJECUCION")
    log("  contrato  %s" % mod_bitacora.CONTRATO)
    log("  candidato %s" % mod_bitacora.CANDIDATO)
    log("  bitacora  %s" % mod_bitacora.RUTA)

    if mod_bitacora.hay_inicio_previo():
        log("  X4 la bitacora ya contiene un INICIO para esta identidad de contrato")
        log("  esta invocacion es un reintento: no anota, no evalua y no reemplaza el resultado")
        log("")
        log("VEREDICTO=FALLO")
        log("  F12 - reintento bajo un contrato ya ejecutado")
        texto = "\n".join(lineas) + "\n"
        io.open("REINTENTO.txt", "w", encoding="utf-8", newline="\n").write(texto)
        sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
        return 1

    log("  E11 no existe INICIO previo para esta identidad")
    mod_bitacora.agregar("INICIO")
    log("  INICIO anotado antes del primer caso")
    log("")

    try:
        cuerpo(args, log, fallos)
    except Exception:
        log("")
        log("F11 EXCEPCION DESPUES DE INICIO")
        for l in traceback.format_exc().rstrip().split("\n"):
            log("  " + l)
        fallos.append(("F11", "-", "la corrida termino por excepcion despues de INICIO"))
        log("")

    mod_bitacora.agregar("CIERRE")
    ok_bit, det_bit = mod_bitacora.coherente()
    log("E12 BITACORA")
    for l in mod_bitacora.leer():
        log("  %s" % l)
    log("  coherente = %s (%s)" % (ok_bit, det_bit))
    if not ok_bit:
        fallos.append(("F13", "-", "bitacora incoherente: %s" % det_bit))
    log("")

    veredicto = "EXITO" if not fallos else "FALLO"
    log("VEREDICTO=%s" % veredicto)
    for criterio, caso, detalle in fallos:
        log("  %s %s %s" % (criterio, caso, detalle))

    texto = "\n".join(lineas) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
    sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
