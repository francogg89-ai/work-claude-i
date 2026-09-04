"""Corrida unica del contrato previo congelado de U2.

Congelado en audit-chatgpt-i@9679ca4ca6987a3706a0b06cebd3b03cce1dcc7a.

El mecanismo produce su resultado y la comparacion contra el resultado normativo esperado
es posterior. Evalua E1-E4, F1-F5 y los controles negativos N1-N9. No existe tercera salida.

Uso:
    python verificar.py --repo-metodo <ruta> --repo-work <ruta> --repo-audit <ruta>
"""

import argparse
import inspect
import io
import re
import subprocess
import sys

import autoridad as mod_autoridad
import corpus as mod_corpus
import orquestador as mod_orquestador

P_C_WORK_SHA = "b2a7c472732e5da59b8c82da7278a0e66ed26e93"
P_C_AUDIT_SHA = "3e27c9af3e71767f4898c6607659c84ab010aa4a"

NEGATIVOS_EXIGIDOS = {"N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9"}


def ejecutar_caso(caso, aut):
    orq = mod_orquestador.Orquestador(
        mod_corpus.WORK_ID, aut,
        instancias=caso["inicio"].get("instancias"),
        ultimo_turn_id=caso["inicio"].get("ultimo_turn_id", 0),
    )
    traza = []
    for op in caso["ops"]:
        nombre = op[0]
        if nombre == "recibir":
            traza.extend(orq.recibir(op[1]))
        elif nombre == "despachar":
            traza.extend(orq.despachar())
        elif nombre == "detener":
            traza.extend(orq.detener())
        elif nombre == "continuar":
            traza.extend(orq.continuar(op[1]))
        else:
            raise RuntimeError("operacion no declarada por el candidato: %s" % nombre)
    return orq, traza


def estructural(nombre, orq, traza):
    """Devuelve (ok, detalle) para los casos que no se expresan como traza de sobres."""
    if nombre == "reporte_sin_reparacion":
        if len(traza) != 1:
            return False, "el reporte no es una unica accion"
        accion = traza[0]
        if accion[0] != "DETENER_REPORTAR" or len(accion) != 2:
            return False, "el reporte no tiene la forma (DETENER_REPORTAR, regla)"
        if accion[1] not in mod_orquestador.REGLAS:
            return False, "la regla reportada no esta declarada"
        return True, "reporte = %s, sin sobre reparado" % (accion,)

    if nombre == "sin_cadencia_ni_git":
        fuente = inspect.getsource(mod_orquestador)
        importaciones = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", fuente, re.M))
        prohibidas = {"subprocess", "socket", "urllib", "http", "requests", "os"}
        cruce = importaciones & prohibidas
        if cruce:
            return False, "el orquestador importa %s" % sorted(cruce)
        nombres = [n for n, _ in inspect.getmembers(mod_orquestador.Orquestador)]
        nombres += [n for n in dir(mod_orquestador) if not n.startswith("__")]
        patron = re.compile(r"cadencia|relevo|count|conteo|git|rev_list", re.I)
        sospechosos = [n for n in nombres if patron.search(n) and n != "REGLAS"]
        if sospechosos:
            return False, "el orquestador expone %s" % sorted(sospechosos)
        return True, "sin importaciones de Git/red y sin miembros de conteo o cadencia"

    if nombre == "estado_solo_admitido":
        claves = set(orq.estado_efimero().keys())
        prohibidos = {
            "current_unit", "approved_work_sha", "latest_audit", "relay_pending",
            "work_status", "constructor_count", "auditor_count",
        }
        if claves != mod_orquestador.ESTADO_ADMITIDO:
            return False, "estado efimero = %s" % sorted(claves)
        if claves & prohibidos:
            return False, "estado paralelo presente"
        return True, "estado efimero = %s" % sorted(claves)

    raise RuntimeError("comprobacion estructural no declarada: %s" % nombre)


def derivar_p_c(repo_work, repo_audit):
    """Dos derivaciones independientes del mismo conjunto contable, por repositorio."""
    def contar(repo, sha):
        salida = subprocess.run(
            ["git", "-C", repo, "rev-list", "--count", sha],
            check=True, stdout=subprocess.PIPE).stdout.decode().strip()
        return int(salida)

    def enumerar(repo, sha):
        # Camino distinto: git log en lugar de rev-list, y deduplicacion propia.
        salida = subprocess.run(
            ["git", "-C", repo, "log", "--format=%H", sha],
            check=True, stdout=subprocess.PIPE).stdout.decode().split()
        return len(set(salida))

    return {
        "N_CONSTRUCTOR": (contar(repo_work, P_C_WORK_SHA),
                          enumerar(repo_work, P_C_WORK_SHA)),
        "N_AUDITOR": (contar(repo_audit, P_C_AUDIT_SHA),
                      enumerar(repo_audit, P_C_AUDIT_SHA)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-metodo", required=True)
    ap.add_argument("--repo-work", required=True)
    ap.add_argument("--repo-audit", required=True)
    ap.add_argument("--salida", default="salida.txt")
    args = ap.parse_args()

    linea = []
    def log(texto=""):
        linea.append(texto)

    aut = mod_autoridad.Autoridad(args.repo_metodo)
    log("AUTORIDAD DE TRANSPORTE (derivada, no inventada)")
    log("  fuente  %s@%s:%s" % ("revolutions-orchestra-ai",
                                mod_autoridad.TRANSPORT_AUTHORITY_SHA,
                                mod_autoridad.TRANSPORT_AUTHORITY_PATH))
    log("  campos  %s" % ", ".join(aut.campos))
    for campo in aut.campos:
        log("    %-14s %s" % (campo, "|".join(sorted(aut.tipos[campo]))))
    log("  formas admitidas (necesidad, final, trio_null)")
    for f in aut.formas:
        log("    %s" % (f,))
    log()

    fallos = []
    log("CASOS")
    for caso in mod_corpus.CASOS:
        orq, traza = ejecutar_caso(caso, aut)
        producido = [tuple(a) for a in traza]
        esperado = [tuple(a) for a in caso["esperado"]]

        if "estructural" in caso:
            ok, detalle = estructural(caso["estructural"], orq, producido)
            if producido != esperado:
                ok = False
                detalle = "traza %s != esperado %s" % (producido, esperado)
        else:
            ok = producido == esperado
            detalle = "" if ok else "producido %s != esperado %s" % (producido, esperado)

        marca = "OK  " if ok else "FALLO"
        neg = " [%s]" % caso["negativo"] if caso["negativo"] else ""
        log("  %s %-5s %-28s%s %s" % (marca, caso["id"], caso["regla"], neg, detalle))
        if not ok:
            fallos.append(("F1", caso["id"], detalle))
        if not ok and caso["negativo"]:
            fallos.append(("N", caso["id"], "control negativo %s no rechazado" % caso["negativo"]))
    log()

    log("E2 atribucion de rechazos")
    for caso in mod_corpus.CASOS:
        for accion in caso["esperado"]:
            if accion[0] == "DETENER_REPORTAR":
                if accion[1] not in mod_orquestador.REGLAS:
                    fallos.append(("F2", caso["id"], "regla no declarada: %s" % accion[1]))
    log("  todos los rechazos citan una regla declarada: %s"
        % (not [f for f in fallos if f[0] == "F2"]))
    log()

    log("E3 cobertura de reglas")
    cubiertas = {c["regla"] for c in mod_corpus.CASOS}
    faltantes = sorted(set(mod_orquestador.REGLAS) - cubiertas)
    sobrantes = sorted(cubiertas - set(mod_orquestador.REGLAS))
    log("  reglas declaradas %d, reglas ejercitadas %d" % (len(mod_orquestador.REGLAS), len(cubiertas)))
    if faltantes:
        fallos.append(("F3", "-", "reglas sin caso: %s" % faltantes))
        log("  sin caso: %s" % faltantes)
    if sobrantes:
        fallos.append(("F4", "-", "casos que invocan reglas no declaradas: %s" % sobrantes))
        log("  no declaradas: %s" % sobrantes)
    log()

    log("CONTROLES NEGATIVOS")
    presentes = {c["negativo"] for c in mod_corpus.CASOS if c["negativo"]}
    faltan_neg = sorted(NEGATIVOS_EXIGIDOS - presentes)
    log("  exigidos %s" % sorted(NEGATIVOS_EXIGIDOS))
    log("  presentes %s" % sorted(presentes))
    if faltan_neg:
        fallos.append(("F3", "-", "controles negativos ausentes: %s" % faltan_neg))
    log()

    log("P-C derivacion de cadencia fuera del orquestador")
    log("  work  %s@%s" % (args.repo_work, P_C_WORK_SHA))
    log("  audit %s@%s" % (args.repo_audit, P_C_AUDIT_SHA))
    pc = derivar_p_c(args.repo_work, args.repo_audit)
    for nombre, (por_count, por_enumeracion) in sorted(pc.items()):
        coincide = por_count == por_enumeracion
        log("  %-14s rev-list --count = %d   enumeracion unica = %d   coincide = %s"
            % (nombre, por_count, por_enumeracion, coincide))
        if not coincide:
            fallos.append(("F5", nombre, "%d != %d" % (por_count, por_enumeracion)))
    log()

    veredicto = "EXITO" if not fallos else "FALLO"
    log("VEREDICTO=%s" % veredicto)
    if fallos:
        for criterio, caso, detalle in fallos:
            log("  %s %s %s" % (criterio, caso, detalle))

    texto = "\n".join(linea) + "\n"
    io.open(args.salida, "w", encoding="utf-8", newline="\n").write(texto)
    sys.stdout.write(texto.encode("ascii", "replace").decode("ascii"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
