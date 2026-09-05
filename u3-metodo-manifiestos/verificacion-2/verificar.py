"""Verificador de U3, contrato audit-chatgpt-i@856a0782cba7b331ee4f2178b7235553b1787c90.

Se ejecuta una vez. Orden estricto: `X0` antes de todo lo demas; despues `X1`, y el cuerpo dentro
de la unica funcion de corrida donde vive `X4`.

```text
uso   python verificar.py --repo-work <ruta del clon de work-claude-i>
```

EXITO exige `E1` a `E31` simultaneamente. Un criterio de fallo activado lo impide; un control que
no discrimina tambien, porque el `E` que ese control demuestra queda sin demostrar, y `X3` no
admite tercera salida.
"""

import ast
import io
import json
import os
import subprocess
import sys

import constantes
import observador

NOMINALES = constantes.NOMBRES_VINCULACIONES
AQUI = os.path.dirname(os.path.abspath(__file__))


class Tee(object):
    def __init__(self, destino):
        self.destino = destino
        self.buffer = []

    def escribir(self, texto=""):
        self.buffer.append(texto)
        try:
            sys.stdout.write(texto + "\n")
        except UnicodeEncodeError:
            sys.stdout.write(texto.encode("ascii", "replace").decode("ascii") + "\n")

    def volcar(self):
        io.open(self.destino, "w", encoding="utf-8", newline="\n").write(
            "\n".join(self.buffer) + "\n")


def imports_declarados(path):
    arbol = ast.parse(io.open(path, encoding="utf-8").read())
    nombres = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres.update(a.name.split(".")[0] for a in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            nombres.add(nodo.module.split(".")[0])
    return sorted(nombres)


def git(repo, *args):
    proceso = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
    return proceso.stdout


def mapear_cobertura(invocaciones, vinculaciones):
    """Cobertura NOMINAL: cada vinculacion declarada, satisfecha por su propia resolucion."""
    mapeo, satisfechas = [], []
    for inv in invocaciones:
        cubre = []
        for v in vinculaciones:
            if v[1] == "local" and any(v[3] in a for a in inv["argv"]):
                cubre.append(v[0])
            elif v[1] == "remota" and v[3] in inv["argv"] and v[4] in inv["argv"]:
                cubre.append(v[0])
        mapeo.append({"argv": inv["argv"], "satisface": cubre})
        satisfechas.extend(cubre)
    return mapeo, satisfechas


# -- X0 y orquestacion --------------------------------------------------------

def main(argv):
    repo_work = None
    for i, a in enumerate(argv):
        if a == "--repo-work" and i + 1 < len(argv):
            repo_work = os.path.abspath(argv[i + 1])
    if repo_work is None:
        repo_work = os.path.abspath(os.path.join(AQUI, "..", ".."))

    out = Tee(os.path.join(AQUI, "salida.txt"))
    out.escribir("VERIFICACION U3")
    out.escribir("contrato   %s" % constantes.IDENTIDAD_CONTRATO)
    out.escribir("repo-work  %s" % repo_work)
    out.escribir("")

    externa = observador.Externa()
    externa.activar()
    externa.fase = "X0"
    externa.vigilar_archivos(True)

    modulos_antes = set(sys.modules)
    import prevuelo
    delta_import = sorted(set(sys.modules) - modulos_antes)

    vinculaciones = constantes.vinculaciones(repo_work)
    with observador.Interna() as interna:
        estado, resuelto = prevuelo.resolver(vinculaciones)

    invocaciones_x0 = externa.de_fase("X0")
    aperturas_x0 = [a for a in externa.aperturas if a["fase"] == "X0"]
    mapeo, satisfechas = mapear_cobertura(invocaciones_x0, vinculaciones)

    out.escribir("X0, estrictamente antes de INICIO")
    for nombre in NOMINALES:
        out.escribir("  %-4s resuelve=%s" % (nombre, resuelto.get(nombre)))
    out.escribir("  estado %s   irresolubles %s"
                 % (estado, prevuelo.irresolubles(resuelto) or "ninguna"))
    out.escribir("  forma del resultado  %s"
                 % sorted({type(v).__name__ for v in resuelto.values()}))
    out.escribir("  cobertura nominal")
    for m in mapeo:
        out.escribir("    %-58s satisface %s" % (" ".join(m["argv"][3:]), m["satisface"]))
    out.escribir("  invocaciones que no son sonda  %d"
                 % sum(1 for i in invocaciones_x0 if i["clase"] == "no-sonda"))
    out.escribir("  aperturas de archivo en X0     %d" % len(aperturas_x0))
    out.escribir("  traza interna, modulos         %s" % interna.modulos())
    out.escribir("  importados por el pre-vuelo    %s" % delta_import)
    out.escribir("")

    x0 = {"estado": estado, "resuelto": dict(resuelto), "mapeo": mapeo,
          "satisfechas": satisfechas, "invocaciones": invocaciones_x0,
          "aperturas": aperturas_x0, "modulos_internos": interna.modulos(),
          "delta_import": delta_import,
          "imports_prevuelo": imports_declarados(os.path.join(AQUI, "prevuelo.py")),
          "imports_sondas": imports_declarados(os.path.join(AQUI, "sondas.py"))}

    if estado != prevuelo.EJECUTABLE:
        out.escribir("RESULTADO  NO_EJECUTABLE")
        out.escribir("no se anota INICIO, no se ejecuta el cuerpo, el contrato no se consume")
        externa.desactivar()
        escribir_evidencia({"x0": x0, "estado": "NO_EJECUTABLE"})
        out.volcar()
        return 2

    externa.fase = "cuerpo"

    import bitacora
    import constituyente
    import controles
    import corpus
    import corrida
    import evaluadores as EV
    import registro
    import superficie

    ruta_bitacora = bitacora.ruta_de_unidad(repo_work, constantes.BITACORA_PATH_UNIDAD)
    previas = bitacora.leer(ruta_bitacora)
    habia_inicio = bitacora.tiene_inicio(previas, constantes.IDENTIDAD_CONTRATO)
    out.escribir("bitacora   %s" % ruta_bitacora)
    out.escribir("  INICIO previo de esta identidad  %s" % habia_inicio)
    out.escribir("  lineas ajenas antes              %d"
                 % len(bitacora.ajenas(previas, constantes.IDENTIDAD_CONTRATO)))
    out.escribir("")

    caja = {}
    modulos = {"bitacora": bitacora, "constituyente": constituyente, "controles": controles,
               "corpus": corpus, "EV": EV, "registro": registro, "superficie": superficie}

    def cuerpo():
        return ejecutar_cuerpo(repo_work, externa, out, caja, modulos)

    resultado = corrida.correr(ruta_bitacora, constantes.IDENTIDAD_CONTRATO,
                               constantes.CANDIDATE_BLOB_SHA, cuerpo)

    lineas_despues = bitacora.leer(ruta_bitacora)
    propias = bitacora.propias(lineas_despues, constantes.IDENTIDAD_CONTRATO)
    ajenas = bitacora.ajenas(lineas_despues, constantes.IDENTIDAD_CONTRATO)

    fallos = EV.fusionar(
        dict(resultado["criterios"]),
        caja.get("fallos", {}),
        EV.evaluar_bitacora(resultado["ajenas_antes"], ajenas, propias,
                            constantes.IDENTIDAD_CONTRATO),
        EV.evaluar_ruta_bitacora(ruta_bitacora, repo_work,
                                 constantes.BITACORA_PATH_UNIDAD, AQUI),
        EV.evaluar_frontera(externa.invocaciones, constantes.P_C_REMOTO),
        EV.evaluar_traza_externa(invocaciones_x0, aperturas_x0, NOMINALES, satisfechas),
        EV.evaluar_traza_interna(interna.modulos(), constantes.MODULOS_DE_LA_CORRIDA),
        EV.evaluar_imports(x0["imports_prevuelo"] + x0["imports_sondas"] + delta_import,
                           constantes.MODULOS_DE_LA_CORRIDA),
        EV.evaluar_conjunto_x0([v[0] for v in vinculaciones], NOMINALES),
        EV.evaluar_forma_x0(resuelto))
    if habia_inicio:
        fallos.setdefault("F14", []).append(True)

    externa.desactivar()

    no_discriminan = [c["id"] for c in caja.get("evidencia", {}).get("controles", [])
                      if not c["discrimina"]]
    criterios_e = evaluar_exito(fallos, resultado, habia_inicio, resuelto, caja, no_discriminan)
    sin_demostrar = sorted(k for k, v in criterios_e.items() if not v)

    veredicto = "EXITO" if (not fallos and not no_discriminan and not sin_demostrar
                            and resultado["veredicto"] == "EXITO") else "FALLO"

    imprimir_resumen(out, veredicto, fallos, resultado, externa, criterios_e,
                     no_discriminan, propias, ajenas)

    evidencia = {"x0": x0, "resultado": serializar(
                     {k: v for k, v in resultado.items() if k != "datos"}),
                 "veredicto": veredicto, "fallos": serializar(fallos),
                 "criterios_de_exito": criterios_e,
                 "controles_que_no_discriminan": no_discriminan,
                 "frontera": externa.invocaciones,
                 "bitacora": {"ruta": ruta_bitacora,
                              "ajenas_antes": resultado["ajenas_antes"],
                              "propias_despues": propias, "ajenas_despues": ajenas}}
    evidencia.update(caja.get("evidencia", {}))
    escribir_evidencia(evidencia)
    out.volcar()
    return 0 if veredicto == "EXITO" else 1


# -- el cuerpo ----------------------------------------------------------------

def ejecutar_cuerpo(repo_work, externa, out, caja, M):
    bitacora, C, controles = M["bitacora"], M["constituyente"], M["controles"]
    corpus, EV, registro, superficie = M["corpus"], M["EV"], M["registro"], M["superficie"]

    externa.vigilar_archivos(True)
    fallos, evidencia = {}, {}

    # -- E11: el candidato leido es exactamente el blob congelado ------------
    ref = "%s:%s" % (constantes.CANDIDATE_WORK_SHA, constantes.CANDIDATE_PATH)
    blob_leido = git(repo_work, "rev-parse", ref).decode().strip()
    texto = git(repo_work, "show", ref).decode("utf-8")
    fallos = EV.fusionar(fallos, EV.evaluar_blob(blob_leido, constantes.CANDIDATE_BLOB_SHA))
    out.escribir("candidato  %s" % constantes.CANDIDATE_PATH)
    out.escribir("  blob leido  %s" % blob_leido)

    documento = superficie.Documento(texto)
    obligaciones = sorted(documento.obligaciones)
    out.escribir("  obligaciones %d   secciones %d   no mecanicas %s"
                 % (len(obligaciones), len(documento.secciones),
                    sorted(documento.no_mecanicas)))
    if documento.ambiguas:
        fallos.setdefault("F27", []).append(("superficie no unica", documento.ambiguas))

    con_obligaciones = {n for n, s in documento.secciones.items() if s.obligaciones}
    fallos = EV.fusionar(fallos,
                         EV.evaluar_secciones(documento.secciones, documento.no_mecanicas,
                                              con_obligaciones),
                         EV.evaluar_forma_secciones(documento.defectos_de_forma,
                                                    documento.no_mecanicas))

    # -- P-C1: R2, unica interaccion de red del cuerpo -----------------------
    vigencia = C.vigencia_remota(repo_work, constantes.P_C_REMOTO, constantes.P_C_REFERENCIA)
    registro_vigencia = [i for i in externa.invocaciones
                         if i["fase"] == "cuerpo" and i["remota"]][-1]
    if not vigencia:
        fallos.setdefault("F23", []).append(("P-C1 no obtuvo la referencia remota",))
    out.escribir("")
    out.escribir("P-C1  %s %s -> %s" % (constantes.P_C_REMOTO, constantes.P_C_REFERENCIA,
                                        vigencia))

    # -- P-C2 ----------------------------------------------------------------
    paths = C.paths_modificados(repo_work, constantes.P_C_CORTE_ORIGEN,
                                constantes.P_C_CORTE_DESTINO)
    solapado = C.descubrir(paths, constantes.SUPERFICIE_SOLAPADA)
    disjunto = C.descubrir(paths, constantes.SUPERFICIE_DISJUNTA)
    fallos = EV.fusionar(fallos, EV.evaluar_descubrimiento(solapado, disjunto))
    out.escribir("P-C2  paths entre los cortes congelados %s" % paths)
    out.escribir("      solapada  procede=%s ruteo=%s interseccion=%d"
                 % (solapado["procede"], solapado["ruteo"] is not None,
                    len(solapado["interseccion"])))
    out.escribir("      disjunta  procede=%s interseccion=%d"
                 % (disjunto["procede"], len(disjunto["interseccion"])))

    # -- P-A y P-B: E8 y E9 ---------------------------------------------------
    completo, _ = C.constituir(corpus.CON_PROJECT)
    aislado, _ = C.constituir(corpus.AISLADO)
    faltantes = [c for c in C.CAMPOS_OBLIGATORIOS if c not in (completo or {})]
    secretos = [k for k, v in (completo or {}).items() if C.VALOR_SECRETO.search(str(v))]
    if completo is None or faltantes or secretos:
        fallos.setdefault("F9", []).append((faltantes, secretos))
    project_en_aislado = [c for c in C.CAMPOS_PROJECT if c in (aislado or {})]
    if aislado is None or project_en_aislado or \
            [c for c in C.CAMPOS_OBLIGATORIOS if c not in (aislado or {})]:
        fallos.setdefault("F10", []).append(project_en_aislado)
    out.escribir("P-A   paquete completo   campos %d   secretos %d"
                 % (len(completo or {}), len(secretos)))
    out.escribir("P-B   trabajo aislado    campos PROJECT_* %d" % len(project_en_aislado))

    # -- casos de llamada: E1, E2 --------------------------------------------
    ctx_casos = {"repo": repo_work, "V1": constantes.CANDIDATE_WORK_SHA,
                 "V3": constantes.P_C_CORTE_ORIGEN, "V4": constantes.P_C_CORTE_DESTINO,
                 "superficie_solapada": constantes.SUPERFICIE_SOLAPADA,
                 "superficie_disjunta": constantes.SUPERFICIE_DISJUNTA}
    resultados_casos = []
    for caso in corpus.casos():
        obtenido = caso.invocar(ctx_casos)
        coincide = obtenido == caso.predice
        resultados_casos.append({"id": caso.id, "obligacion": caso.obligacion,
                                 "obtenido": repr(obtenido), "predice": repr(caso.predice),
                                 "coincide": coincide})
        if not coincide:
            fallos.setdefault("F1", []).append((caso.id, repr(obtenido), repr(caso.predice)))
        if isinstance(obtenido, str) and obtenido.startswith("R-") \
                and obtenido not in documento.obligaciones:
            fallos.setdefault("F2", []).append((caso.id, obtenido))
    out.escribir("")
    out.escribir("casos de llamada  %d   con el resultado que su obligacion predice  %d"
                 % (len(resultados_casos), sum(1 for r in resultados_casos if r["coincide"])))

    # -- comprobaciones: E6, E7, E25, E26, E27 -------------------------------
    sujeto_conducta = registro.sujeto_conducta(registro_vigencia)
    ctx_comp = registro.contexto(externa.aperturas, constantes.P_C_REMOTO, registro_vigencia,
                                 corpus.CON_PROJECT)
    ctx_comp["sujeto_conducta"] = sujeto_conducta

    comps = registro.comprobaciones()
    por_sid = {c.sid: c for c in comps}
    identidades = {c.sid: observador.clave(c.fn.__code__) for c in comps}

    registros, items_alcance, items_discriminacion = [], [], []
    for comp in comps:
        if comp.tipo == "documento":
            sujeto = documento.sujeto()
            mutante = comp.mutacion(documento, comp.clave)
            variantes = {
                "sin-ocurrencias-fuera": superficie.sin_ocurrencias_fuera(
                    documento, comp.clave, comp.fragmentos),
                "con-ruido-antes": superficie.con_ruido_antes(
                    documento, comp.clave, comp.fragmentos)}
        else:
            sujeto = sujeto_conducta
            mutante = comp.mutacion(sujeto_conducta)
            variantes = {}

        real = registro.ejercer(comp, sujeto, ctx_comp, EV.CALIFICACION)
        mut = registro.ejercer(comp, mutante, ctx_comp, EV.CALIFICACION, etiqueta="mutante")
        registros.extend([real, mut])
        if not real["ok"]:
            fallos.setdefault("F1", []).append((comp.sid, "fallo sobre el sujeto real",
                                                real["observable"]))
        obs_variantes = {}
        for nombre in sorted(variantes):
            r = registro.ejercer(comp, variantes[nombre], ctx_comp, EV.CALIFICACION,
                                 etiqueta=nombre)
            registros.append(r)
            obs_variantes[nombre] = r["observable"]
        items_alcance.append({"sid": comp.sid, "superficie": comp.superficie_declarada(),
                              "tipo": comp.tipo, "obligacion": comp.clave,
                              "observable": real["observable"], "variantes": obs_variantes})
        items_discriminacion.append({
            "sid": comp.sid, "ok_mutante": mut["ok"],
            "obs_real": real["observable"], "obs_mutante": mut["observable"],
            "extracto_real": repr(registro.extracto(comp, sujeto)),
            "extracto_mutante": repr(registro.extracto(comp, mutante))})

    fallos = EV.fusionar(fallos,
                         EV.evaluar_alcance(items_alcance, set(documento.obligaciones)),
                         EV.evaluar_discriminacion(items_discriminacion))
    out.escribir("comprobaciones    %d   todas con superficie material declarada  %s"
                 % (len(comps), all(i["superficie"] for i in items_alcance)))

    # -- E3 -------------------------------------------------------------------
    ejercitadas = {c.obligacion for c in corpus.casos()} | {c.obligacion for c in comps}
    fallos = EV.fusionar(fallos, EV.evaluar_cobertura(obligaciones, ejercitadas))
    out.escribir("cobertura         %d obligaciones del candidato, %d ejercitadas"
                 % (len(obligaciones), len(ejercitadas & set(obligaciones))))

    # -- controles ------------------------------------------------------------
    ctx_ctrl = {"repo": repo_work, "disjunto": disjunto, "solapado": solapado,
                "dir_evidencia": AQUI, "blob_congelado": constantes.CANDIDATE_BLOB_SHA,
                "nominales": NOMINALES, "modulos_corrida": constantes.MODULOS_DE_LA_CORRIDA,
                "sha_repetido": constantes.P_C_CORTE_ORIGEN, "raiz": repo_work,
                "constante_bitacora": constantes.BITACORA_PATH_UNIDAD, "dir_mecanismo": AQUI,
                "remoto": constantes.P_C_REMOTO}
    resultados_controles = controles.sobre_la_materia(ctx_ctrl)
    resultados_controles += controles.sobre_los_criterios(ctx_ctrl)
    sobre_comp, registros_control, real_s01 = controles.sobre_las_comprobaciones(
        documento, ctx_comp, por_sid)
    resultados_controles += sobre_comp
    registros.append(real_s01)
    registros.extend(registros_control)
    out.escribir("controles         %d   discriminan %d"
                 % (len(resultados_controles),
                    sum(1 for c in resultados_controles if c["discrimina"])))

    # -- E20/F21 y E15/F16 ----------------------------------------------------
    identidad_derivacion = observador.clave(C.derivar_cadencia.__code__)
    if identidad_derivacion != ctx_ctrl.get("n9", {}).get("identidad_derivacion"):
        fallos.setdefault("F21", []).append(
            (identidad_derivacion, ctx_ctrl.get("n9", {}).get("identidad_derivacion")))

    import corrida
    identidad_correr = observador.clave(corrida.correr.__code__)
    for nombre, identidad in sorted(ctx_ctrl.get("identidad_corrida", {}).items()):
        if identidad != identidad_correr:
            fallos.setdefault("F16", []).append((nombre, identidad, identidad_correr))

    # -- E28/F30: conducta y no ocurrencia lexica -----------------------------
    n31 = [c for c in resultados_controles if c["id"] == "N31"]
    if n31 and not n31[0]["discrimina"]:
        fallos.setdefault("F30", []).append(n31[0]["obtenido"])

    # -- E29, E30, E31 / F31, F32, F33 ---------------------------------------
    atadura = EV.evaluar_atadura(registros, identidades)
    fallos = EV.fusionar(fallos, atadura)
    out.escribir("atadura           registros de travesia %d   fallos %s"
                 % (len(registros), sorted(atadura) or "ninguno"))

    evidencia.update({
        "casos": resultados_casos, "alcance": items_alcance,
        "discriminacion": items_discriminacion, "controles": resultados_controles,
        "registros_de_travesia": registros,
        "identidades_registradas": {k: list(v) for k, v in sorted(identidades.items())},
        "identidad_derivacion": list(identidad_derivacion),
        "identidad_correr": list(identidad_correr),
        "n9": ctx_ctrl.get("n9"), "identidad_corrida": ctx_ctrl.get("identidad_corrida"),
        "p_c": {"repo": constantes.P_C_REPO, "remoto": constantes.P_C_REMOTO,
                "referencia": constantes.P_C_REFERENCIA, "vigencia_obtenida": vigencia,
                "corte_origen": constantes.P_C_CORTE_ORIGEN,
                "corte_destino": constantes.P_C_CORTE_DESTINO, "paths": paths,
                "solapado": solapado, "disjunto": disjunto},
        "paquetes": {"completo": sorted(completo or {}), "aislado": sorted(aislado or {})},
        "cobertura": {"obligaciones": obligaciones,
                      "ejercitadas": sorted(ejercitadas & set(obligaciones))}})

    caja["fallos"] = fallos
    caja["evidencia"] = evidencia
    return ("EXITO" if not fallos else "FALLO"), None


# -- criterios de exito, uno por uno -----------------------------------------

def evaluar_exito(fallos, resultado, habia_inicio, resuelto, caja, no_discriminan):
    ev = caja.get("evidencia", {})
    sin = lambda *cs: not any(c in fallos for c in cs)
    control = lambda ident: ident not in no_discriminan
    alcance = ev.get("alcance", [])
    return {
        "E1": sin("F1"), "E2": sin("F2"), "E3": sin("F3"), "E4": sin("F5"), "E5": sin("F6"),
        "E6": sin("F7"), "E7": sin("F8"),
        "E8": sin("F9"), "E9": sin("F10"), "E10": sin("F11"), "E11": sin("F12"),
        "E12": bool(resultado["anoto_inicio"] and resultado["anoto_cierre"]),
        "E13": not habia_inicio, "E14": sin("F15"),
        "E15": sin("F16") and control("N16") and control("N17"),
        "E16": all(resuelto.values()) and len(resuelto) == len(NOMINALES),
        "E17": sin("F18"), "E18": sin("F19"), "E19": sin("F20"),
        "E20": sin("F21") and control("N9"), "E21": sin("F22") and control("N24"),
        "E22": sin("F23"), "E23": sin("F24") and control("N25"),
        "E24": sin("F26") and control("N27"),
        "E25": bool(alcance) and all(i["superficie"] for i in alcance) and sin("F27"),
        "E26": sin("F28") and control("N28") and control("N29"),
        "E27": sin("F29") and control("N30"),
        "E28": sin("F30") and control("N31"),
        "E29": sin("F33") and control("N33"),
        "E30": sin("F31") and control("N32"),
        "E31": sin("F32") and control("N32"),
    }


# -- salida -------------------------------------------------------------------

def serializar(objeto):
    return json.loads(json.dumps(objeto, default=repr))


def escribir_evidencia(evidencia):
    io.open(os.path.join(AQUI, "evidencia.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(serializar(evidencia), ensure_ascii=False, indent=1, sort_keys=True))


def imprimir_resumen(out, veredicto, fallos, resultado, externa, criterios_e,
                     no_discriminan, propias, ajenas):
    out.escribir("")
    out.escribir("frontera de red")
    for i in externa.invocaciones:
        if i["remota"]:
            out.escribir("  %-7s %s" % (i["fase"], " ".join(i["argv"][3:])))
    out.escribir("  interacciones remotas totales  %d"
                 % sum(1 for i in externa.invocaciones if i["remota"]))
    out.escribir("")
    out.escribir("bitacora de la unidad")
    for l in ajenas:
        out.escribir("  ajena    %s" % l)
    for l in propias:
        out.escribir("  propia   %s" % l)
    out.escribir("")
    out.escribir("criterios de exito")
    linea = []
    for k in sorted(criterios_e, key=lambda x: int(x[1:])):
        linea.append("%s=%s" % (k, "SI" if criterios_e[k] else "NO"))
        if len(linea) == 6:
            out.escribir("  " + "  ".join(linea))
            linea = []
    if linea:
        out.escribir("  " + "  ".join(linea))
    out.escribir("")
    out.escribir("terminacion  %s" % resultado["terminacion"])
    out.escribir("criterios de fallo activados  %s" % (sorted(fallos) or "ninguno"))
    for codigo in sorted(fallos):
        for detalle in fallos[codigo][:8]:
            out.escribir("    %s  %s" % (codigo, repr(detalle)[:200]))
    out.escribir("controles que no discriminan  %s" % (no_discriminan or "ninguno"))
    out.escribir("")
    out.escribir("VEREDICTO=%s" % veredicto)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
