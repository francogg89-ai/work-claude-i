"""Comprobaciones estructurales y de documento, con su observable y su mutante.

Cada comprobacion se ejercita dos veces: contra el sujeto real, donde debe pasar, y contra un
mutante que viola la obligacion leida, donde debe fallar. El observable debe diferir entre ambos:
si no difiere, el mutante no esta violando la propiedad que la comprobacion lee.
"""

import inspect
import re

import casos
import metodo

ACCIONES_DE_EJECUCION = {"IMPLEMENTAR", "DESPLEGAR", "EJECUTAR_TRABAJO", "ESCRIBIR_CODIGO"}
ACCIONES_DE_DECISION = {"DECIDIR_UNIDAD", "DECIDIR_NECESIDAD", "APROBAR_ENTREGA",
                        "OTORGAR_PERMISO", "DECLARAR_VEREDICTO"}
ACCIONES_DE_RELEVO = {"DECIDIR_RELEVO", "CONTAR_ENTREGAS", "DERIVAR_CADENCIA_EN_TRANSPORTE"}
ACCIONES_DE_MODELO = {"ELEGIR_MODELO", "SELECCIONAR_RUNTIME", "FIJAR_REGLAS_DE_COSTO"}

ESTADO_DE_EJECUCION = {"unidad_actual", "ultima_entrega", "ultimo_auditor", "estado_del_loop",
                       "work_sha_vigente", "audit_sha_vigente"}


def _normalizar(texto):
    """El texto del candidato envuelve lineas: la busqueda de enunciados normaliza espacios."""
    return " ".join(texto.split())


def sujeto_real(texto):
    return {"acciones": set(metodo.ACCIONES), "texto": texto,
            "plano": _normalizar(texto), "fuente": inspect.getsource(metodo),
            "politica_relevo": metodo.politica_relevo,
            "descubrir": metodo.descubrir,
            "constituir": metodo.constituir}


def mutante(base, **cambios):
    s = dict(base)
    s.update(cambios)
    return s


# -- comprobaciones -----------------------------------------------------------

def c_cadena(s, ctx):
    orden = ["metodo-manifiestos-ai produce", "manifiestos-trabajo-ai",
             "el paquete de constitucion inicia", "reglas-orquestador-ai transporta",
             "revolutions-orchestra-ai gobierna"]
    t = s["plano"]
    posiciones = [t.find(x) for x in orden]
    ok = all(p >= 0 for p in posiciones) and posiciones == sorted(posiciones)
    return ok, repr(posiciones), "posiciones de la cadena = %s" % posiciones


def c_referencias(s, ctx):
    t = s["plano"]
    exigidos = ["CT-6", "manifiestos-trabajo-ai : README.md",
                "CT-7", "reglas-orquestador-ai : REGLAS-ORQUESTADOR.md"]
    faltan = [x for x in exigidos if x not in t]
    return not faltan, repr(faltan), "referencias ausentes = %s" % faltan


def c_sin_sha_ajeno(s, ctx):
    """R-1-sin-sha y R-8-no-circular: el candidato no congela SHAs de documentos citados."""
    hallados = sorted(set(re.findall(r"\b[0-9a-f]{40}\b", s["plano"])))
    return not hallados, repr(hallados), "SHAs congelados en el candidato = %s" % hallados


def c_estado_del_paquete(s, ctx):
    paquete = s["constituir"](casos.RESPUESTAS_COMPLETAS)[0] or {}
    cruce = sorted(set(paquete) & ESTADO_DE_EJECUCION)
    return not cruce, repr(cruce), "estado de ejecucion en el paquete = %s" % cruce


def c_pregunta_explicita(s, ctx):
    """R-5-pregunta: no hay politica por defecto; sin eleccion explicita se rechaza."""
    obs = s["politica_relevo"](None)[1]
    return obs == "R-5-opciones", repr(obs), "politica sin eleccion -> %s" % obs


def c_remoto(s, ctx):
    fuente = inspect.getsource(metodo.referencia_remota) if hasattr(
        metodo, "referencia_remota") else ""
    fuente = s.get("fuente_remota", fuente)
    usa = "ls-remote" in fuente and "remoto" in fuente
    return usa, repr(("ls-remote" in fuente, "remoto" in fuente)), "fuente = %s" % usa


def c_sin_registro_central(s, ctx):
    patron = re.compile(r"EVENT\.md|lista_de_carriles|registro_central", re.I)
    hallados = sorted(set(patron.findall(s["fuente"])))
    return not hallados, repr(hallados), "registro central = %s" % hallados


def c_descubrir_puro(s, ctx):
    """R-6-sha-constitutivo: consultar la vigencia no muta el corte constitutivo."""
    paths = ["a/x.md", "b/y.md"]
    superficie = {"repo": "r", "paths": ("a/",)}
    antes = (list(paths), dict(superficie))
    s["descubrir"](paths, superficie)
    despues = (list(paths), dict(superficie))
    return antes == despues, repr(despues), "entradas sin mutar = %s" % (antes == despues)


def c_sin_campos_de_transporte(s, ctx):
    prohibidos = ["next_model", "next_runtime", "revolutions-hop/v2"]
    hallados = [p for p in prohibidos if p in s["fuente"]]
    return not hallados, repr(hallados), "campos agregados = %s" % hallados


def c_capacidades_derivadas(s, ctx):
    t = s["plano"]
    exigidos = ["las capacidades se derivan de la constitucion",
                "no las amplia"]
    faltan = [x for x in exigidos if x not in t]
    return not faltan, repr(faltan), "enunciados ausentes = %s" % faltan


def c_texto(fragmentos):
    def f(s, ctx):
        faltan = [x for x in fragmentos if x not in s["plano"]]
        return not faltan, repr(faltan), "fragmentos ausentes = %s" % faltan
    return f


def c_sin_acciones(prohibidas):
    def f(s, ctx):
        cruce = sorted(set(s["acciones"]) & set(prohibidas))
        return not cruce, repr(cruce), "acciones prohibidas = %s" % cruce
    return f


def c_con_acciones(exigidas):
    def f(s, ctx):
        faltan = sorted(set(exigidas) - set(s["acciones"]))
        return not faltan, repr(faltan), "acciones faltantes = %s" % faltan
    return f


# -- mutantes -----------------------------------------------------------------

def m_texto_sin(base, fragmento):
    return lambda: mutante(base, plano=base["plano"].replace(fragmento, "", 1))


def m_texto_con(base, extra):
    return lambda: mutante(base, plano=base["plano"] + extra)


def m_politica_con_default(base):
    def politica(eleccion, persiste_contador=False):
        return {"politica": eleccion or "cada_n", "vive_en": "constitucion"}, None
    return lambda: mutante(base, politica_relevo=politica)


def m_descubrir_muta(base):
    def descubrir(paths, superficie):
        paths.append("colado/por/el/mecanismo.md")
        return metodo.descubrir(paths, superficie)
    return lambda: mutante(base, descubrir=descubrir)


def m_constituir_con_estado(base):
    def constituir(respuestas):
        paquete, rechazo = metodo.constituir(respuestas)
        if paquete is not None:
            paquete = dict(paquete, unidad_actual="U3", ultima_entrega="abc")
        return paquete, rechazo
    return lambda: mutante(base, constituir=constituir)


def m_acciones_mas(base, extra):
    return lambda: mutante(base, acciones=set(base["acciones"]) | set(extra))


def m_acciones_menos(base, quitar):
    return lambda: mutante(base, acciones=set(base["acciones"]) - set(quitar))


def m_fuente_con(base, extra):
    return lambda: mutante(base, fuente=base["fuente"] + extra)


def construir(texto):
    """Devuelve [(id, obligacion, comprobar, mutante, negativo)] con el sujeto real ligado."""
    base = sujeto_real(texto)
    cadena_frag = "reglas-orquestador-ai transporta"
    return [
        ("S01", "R-1-cadena", c_cadena, m_texto_sin(base, cadena_frag), None),
        ("S02", "R-1-no-sustituye", c_texto(["ninguno de esos documentos sustituye a otro"]),
         m_texto_sin(base, "ninguno de esos documentos sustituye a otro"), None),
        ("S03", "R-1-no-amplia", c_texto(["ninguno amplia las autoridades de REVOLUTIONS"]),
         m_texto_sin(base, "ninguno amplia las autoridades de REVOLUTIONS"), None),
        ("S04", "R-1-no-ejecuta", c_sin_acciones(ACCIONES_DE_EJECUCION),
         m_acciones_mas(base, {"EJECUTAR_TRABAJO"}), None),
        ("S05", "R-1-no-decide", c_sin_acciones(ACCIONES_DE_DECISION),
         m_acciones_mas(base, {"DECIDIR_UNIDAD"}), None),
        ("S06", "R-1-referencias", c_referencias,
         m_texto_sin(base, "manifiestos-trabajo-ai : README.md"), None),
        ("S07", "R-1-sin-sha", c_sin_sha_ajeno, m_texto_con(base, "\n" + "e" * 40 + "\n"),
         None),
        ("S08", "R-2-alternativas", c_con_acciones({"PROPONER"}),
         m_acciones_menos(base, {"PROPONER"}), None),
        ("S09", "R-3-puede", c_con_acciones({"ENTREVISTAR", "PROPONER", "REDACTAR",
                                             "SENALAR_CONTRADICCION", "SUGERIR"}),
         m_acciones_menos(base, {"SUGERIR"}), None),
        ("S10", "R-5-pregunta", c_pregunta_explicita,
         m_politica_con_default(base), None),
        ("S11", "R-5-no-orquestador", c_sin_acciones(ACCIONES_DE_RELEVO),
         m_acciones_mas(base, {"DECIDIR_RELEVO"}), None),
        ("S12", "R-6-remoto", c_remoto,
         lambda: mutante(base, fuente_remota="def f(): return rev_parse(local)"), None),
        ("S13", "R-6-sin-registro", c_sin_registro_central,
         m_fuente_con(base, "\nEVENT_MD_CENTRAL = 'EVENT.md'\n"), None),
        ("S14", "R-6-sha-constitutivo", c_descubrir_puro,
         m_descubrir_muta(base), None),
        ("S15", "R-7-capacidades", c_capacidades_derivadas,
         m_texto_sin(base, "las capacidades se derivan de la constitucion"), None),
        ("S16", "R-7-sin-campos", c_sin_campos_de_transporte,
         m_fuente_con(base, "\nCAMPO_EXTRA = 'next_model'\n"), None),
        ("S17", "R-8-no-ejecuta", c_sin_acciones(ACCIONES_DE_EJECUCION),
         m_acciones_mas(base, {"DESPLEGAR"}), None),
        ("S18", "R-8-no-reemplaza", c_texto(["no reemplaza a REVOLUTIONS"]),
         m_texto_sin(base, "no reemplaza a REVOLUTIONS"), None),
        ("S19", "R-8-no-decide", c_sin_acciones(ACCIONES_DE_DECISION),
         m_acciones_mas(base, {"DECLARAR_VEREDICTO"}), None),
        ("S20", "R-8-no-estado", c_estado_del_paquete,
         m_constituir_con_estado(base), None),
        ("S21", "R-8-no-circular", c_sin_sha_ajeno,
         m_texto_con(base, "\n" + "f" * 40 + "\n"), None),
        ("S22", "R-8-no-modelo", c_sin_acciones(ACCIONES_DE_MODELO),
         m_acciones_mas(base, {"ELEGIR_MODELO"}), None),
    ]
