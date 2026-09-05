"""Corpus de casos. Cada caso declara la obligación del candidato que lo gobierna.

El mecanismo no lee `esperado`: lo produce, y la comparación es posterior.

Los casos estructurales delegan en `estructurales.py`, donde cada comprobación viene con el
mutante sintético que debe hacerla fallar.
"""

import json

WORK_ID = "revolutions-orchestra-ai"
REPO = "https://github.com/francogg89-ai/work-claude-i"

BASE = {
    "protocol": "revolutions-hop/v1",
    "work_id": WORK_ID,
    "turn_id": 1,
    "actor": "AUDITOR",
    "repository": REPO,
    "commit": "0" * 40,
    "next_actor": "CONSTRUCTOR",
    "next_instance": "fresh",
    "next_prompt": "prompt literal",
    "human_need": None,
    "unit": None,
    "final": False,
}

NECESIDAD = {
    "id": "H1", "type": "no_material", "request": "decision de dominio",
    "checkpoint": None, "guide_prompt": None,
    "expected_evidence": ["respuesta del humano"], "resume_actor": "AUDITOR",
}

PROMPT_ACENTOS = "línea uno\nlínea dos con acentos: intervención, auditoría\nlínea tres"
PROMPT_SECRETO = "usar TOKEN_FUDO → variable de entorno FUDO_TOKEN, sin resolverla"
PAQUETE = "ARRANQUE EXTERNO\nWORK_ID=revolutions-orchestra-ai\nCARRIL=I\n"


def sobre(**cambios):
    s = dict(BASE)
    s.update(cambios)
    return s


def salida(s, prosa="El actor explica lo que hizo.\n\n"):
    return prosa + "```json\n" + json.dumps(s, ensure_ascii=False, indent=2) + "\n```\n"


def salida_dos_bloques(s):
    señuelo = '```json\n{"nota": "ejemplo de un documento"}\n```\n\n'
    return "Prosa.\n\n" + señuelo + "```json\n" + \
        json.dumps(s, ensure_ascii=False, indent=2) + "\n```\n"


def salida_con_posterior(s):
    return salida(s) + "\nUna coda que la autoridad no admite.\n"


def _t(id_, obl, ops, esperado, negativo=None):
    return {"id": id_, "obligacion": obl, "tipo": "traza", "inicio": {},
            "ops": ops, "esperado": esperado, "negativo": negativo}


def _ti(id_, obl, inicio, ops, esperado, negativo=None):
    c = _t(id_, obl, ops, esperado, negativo)
    c["inicio"] = inicio
    return c


def _e(id_, obl, negativo=None):
    return {"id": id_, "obligacion": obl, "tipo": "estructural", "negativo": negativo}


C = "CONSTRUCTOR"
A = "AUDITOR"
INST_C = {"instancias": {C: "C#1"}}
INST_A = {"instancias": {A: "A#1"}}

CASOS = [
    # -- 1.1 arranque externo -------------------------------------------------
    _t("T01", "R-1.1-recibe-paquete", [("arranque", PAQUETE)],
       [("ENTREGAR_PAQUETE", A, "AUDITOR#externo", PAQUETE)]),
    _t("T02", "R-1.1-abre-auditor", [("arranque", PAQUETE)],
       [("ENTREGAR_PAQUETE", A, "AUDITOR#externo", PAQUETE)]),
    _t("T03", "R-1.1-entrega-paquete", [("arranque", PAQUETE)],
       [("ENTREGAR_PAQUETE", A, "AUDITOR#externo", PAQUETE)]),
    _t("T04", "R-1.1-entra-al-loop",
       [("arranque", PAQUETE), ("recibir", salida(sobre(turn_id=1)))],
       [("ENTREGAR_PAQUETE", A, "AUDITOR#externo", PAQUETE), ("RECIBIDO",)]),
    _t("T05", "R-1.1-primer-turn-id", [("recibir", salida(sobre(turn_id=5)))],
       [("DETENER_REPORTAR", "R-1.1-primer-turn-id")]),

    # -- 2 forma de la respuesta ---------------------------------------------
    _t("T06", "R-2-unicidad", [("recibir", salida_dos_bloques(sobre()))],
       [("DETENER_REPORTAR", "R-2-unicidad")], negativo="N10"),
    _t("T07", "R-2-sin-posterior", [("recibir", salida_con_posterior(sobre()))],
       [("DETENER_REPORTAR", "R-2-sin-posterior")], negativo="N11"),
    _t("T08", "R-2-parseo", [("recibir", "Una salida sin ningun bloque json.")],
       [("DETENER_REPORTAR", "R-2-parseo")]),
    _t("T09", "R-2-toma-el-bloque", [("recibir", salida(sobre()))], [("RECIBIDO",)]),
    _t("T10", "R-2-no-prosa",
       [("recibir", salida(sobre(), prosa='Prosa que menciona protocol y turn_id 99.\n\n'))],
       [("RECIBIDO",)]),

    # -- 3 validaciones -------------------------------------------------------
    _ti("T11", "R-3-orden", {"ultimo_turn_id": 6},
        [("recibir", salida(sobre(protocol="otro", turn_id=99)))],
        [("DETENER_REPORTAR", "R-V1")]),
    _t("T12", "R-V1", [("recibir", salida(sobre(protocol="revolutions-hop/v2")))],
       [("DETENER_REPORTAR", "R-V1")], negativo="N7"),
    _t("T13", "R-V2", [("recibir", salida(sobre(work_id="otro-trabajo-ai")))],
       [("DETENER_REPORTAR", "R-V2")], negativo="N6"),
    _t("T14", "R-V3",
       [("recibir", salida({k: v for k, v in BASE.items() if k != "unit"}))],
       [("DETENER_REPORTAR", "R-V3")]),
    _t("T15", "R-V4", [("recibir", salida(sobre(turn_id="1")))],
       [("DETENER_REPORTAR", "R-V4")]),
    _ti("T16", "R-V5", {"ultimo_turn_id": 6}, [("recibir", salida(sobre(turn_id=6)))],
        [("DETENER_REPORTAR", "R-V5")], negativo="N3"),
    _t("T17", "R-V6", [("recibir", salida(sobre(next_instance="nueva")))],
       [("DETENER_REPORTAR", "R-V6")], negativo="N5"),
    _t("T18", "R-V7", [("recibir", salida(sobre(next_actor=None, next_instance="fresh")))],
       [("DETENER_REPORTAR", "R-V7")], negativo="N4"),
    _t("T19", "R-V8", [("recibir", salida(sobre(human_need=NECESIDAD)))],
       [("DETENER_REPORTAR", "R-V8")], negativo="N1"),
    _t("T20", "R-V8", [("recibir", salida(sobre(human_need=NECESIDAD, final=True,
                                                next_actor=None, next_instance=None,
                                                next_prompt=None)))],
       [("DETENER_REPORTAR", "R-V8")], negativo="N2"),

    # -- 4 sobre invalido -----------------------------------------------------
    _t("T21", "R-4-detiene", [("recibir", salida(sobre(protocol="otro")))],
       [("DETENER_REPORTAR", "R-V1")]),
    _t("T22", "R-4-reporte", [("recibir", salida(sobre(work_id="ajeno")))],
       [("DETENER_REPORTAR", "R-V2")]),

    # -- 5 turn_id ------------------------------------------------------------
    _ti("T23", "R-5-sucesor", {"ultimo_turn_id": 6},
        [("recibir", salida(sobre(turn_id=7)))], [("RECIBIDO",)]),
    _ti("T24", "R-5-otro-detiene", {"ultimo_turn_id": 6},
        [("recibir", salida(sobre(turn_id=5)))],
        [("DETENER_REPORTAR", "R-V5")], negativo="N3"),
    _ti("T25", "R-5-no-reinicio", dict(INST_C, ultimo_turn_id=20),
        [("recibir", salida(sobre(turn_id=1, next_instance="fresh")))],
        [("DETENER_REPORTAR", "R-V5")], negativo="N3"),

    # -- 6 next_instance ------------------------------------------------------
    _ti("T26", "R-6-current", dict(INST_C, ultimo_turn_id=4),
        [("recibir", salida(sobre(turn_id=5, next_instance="current"))), ("despachar",)],
        [("RECIBIDO",), ("ENTREGAR", C, "C#1", "prompt literal")]),
    _t("T27", "R-6-fresh",
       [("recibir", salida(sobre(turn_id=1, next_instance="fresh"))), ("despachar",)],
       [("RECIBIDO",), ("ENTREGAR", C, "CONSTRUCTOR#t1", "prompt literal")]),
    _ti("T28", "R-6-null", {"ultimo_turn_id": 32},
        [("recibir", salida(sobre(turn_id=33, final=True, next_actor=None,
                                  next_instance=None, next_prompt=None))), ("despachar",)],
        [("RECIBIDO",), ("MOSTRAR_CIERRE",)]),
    _ti("T29", "R-6-fresh-a-current", dict(INST_A, ultimo_turn_id=0),
        [("recibir", salida(sobre(turn_id=1, next_instance="fresh"))), ("despachar",),
         ("recibir", salida(sobre(turn_id=2, actor=C, next_actor=A,
                                  next_instance="current"))), ("despachar",),
         ("recibir", salida(sobre(turn_id=3, next_instance="current",
                                  next_prompt="segundo pase"))), ("despachar",)],
        [("RECIBIDO",), ("ENTREGAR", C, "CONSTRUCTOR#t1", "prompt literal"),
         ("RECIBIDO",), ("ENTREGAR", A, "A#1", "prompt literal"),
         ("RECIBIDO",), ("ENTREGAR", C, "CONSTRUCTOR#t1", "segundo pase")]),
    _ti("T30", "R-6-solo-next-instance", dict(INST_C, ultimo_turn_id=4),
        [("recibir", salida(sobre(turn_id=5, next_instance="current",
                                  next_prompt="abri una instancia fresh"))), ("despachar",)],
        [("RECIBIDO",), ("ENTREGAR", C, "C#1", "abri una instancia fresh")]),
    _ti("T31", "R-6.1-detiene", {"ultimo_turn_id": 4},
        [("recibir", salida(sobre(turn_id=5, next_instance="current"))), ("despachar",)],
        [("RECIBIDO",), ("DETENER_REPORTAR", "R-6.1-detiene")], negativo="N8"),

    # -- 7 loop ---------------------------------------------------------------
    _ti("T32", "R-7-necesidad", {"ultimo_turn_id": 24},
        [("recibir", salida(sobre(turn_id=25, human_need=NECESIDAD, next_actor=None,
                                  next_instance=None, next_prompt=None))), ("despachar",)],
        [("RECIBIDO",), ("MOSTRAR_NECESIDAD",)]),
    _ti("T33", "R-7-final", {"ultimo_turn_id": 32},
        [("recibir", salida(sobre(turn_id=33, final=True, next_actor=None,
                                  next_instance=None, next_prompt=None))), ("despachar",)],
        [("RECIBIDO",), ("MOSTRAR_CIERRE",)]),
    _ti("T34", "R-7-unit", dict(INST_C, ultimo_turn_id=10),
        [("recibir", salida(sobre(turn_id=11, next_instance="current",
                                  unit="unidad 2 terminada; inicio unidad 3"))),
         ("despachar",)],
        [("RECIBIDO",), ("MOSTRAR_UNIDAD", "unidad 2 terminada; inicio unidad 3"),
         ("ENTREGAR", C, "C#1", "prompt literal")]),
    _ti("T35", "R-7-orden", dict(INST_C, ultimo_turn_id=10),
        [("recibir", salida(sobre(turn_id=11, next_instance="current",
                                  unit="u2 -> u3"))), ("despachar",)],
        [("RECIBIDO",), ("MOSTRAR_UNIDAD", "u2 -> u3"),
         ("ENTREGAR", C, "C#1", "prompt literal")]),
    _ti("T36", "R-7-entrega-literal", dict(INST_C, ultimo_turn_id=2),
        [("recibir", salida(sobre(turn_id=3, next_instance="current",
                                  next_prompt=PROMPT_ACENTOS))), ("despachar",)],
        [("RECIBIDO",), ("ENTREGAR", C, "C#1", PROMPT_ACENTOS)]),

    # -- 9.1 DETENER ----------------------------------------------------------
    _ti("T37", "R-9.1-constructor-1", dict(INST_A, ultimo_turn_id=5),
        [("detener",), ("recibir", salida(sobre(turn_id=6, actor=C, next_actor=A,
                                                next_instance="current")))],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",)]),
    _ti("T38", "R-9.1-constructor-2", dict(INST_A, ultimo_turn_id=5),
        [("detener",), ("recibir", salida(sobre(turn_id=6, actor=C, next_actor=A,
                                                next_instance="current",
                                                protocol="otro")))],
        [("PAUSA_SOLICITADA",), ("DETENER_REPORTAR", "R-V1")]),
    _ti("T39", "R-9.1-constructor-3", dict(INST_A, ultimo_turn_id=5),
        [("detener",), ("recibir", salida(sobre(turn_id=6, actor=C, next_actor=A,
                                                next_instance="current"))),
         ("despachar",)],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",)]),
    _ti("T40", "R-9.1-auditor-1", dict(INST_C, ultimo_turn_id=6),
        [("detener",), ("recibir", salida(sobre(turn_id=7, next_instance="current")))],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",)]),
    _ti("T41", "R-9.1-auditor-2", dict(INST_C, ultimo_turn_id=6),
        [("detener",), ("recibir", salida(sobre(turn_id=7, next_instance="current",
                                                next_prompt="proxima accion material"))),
         ("despachar",)],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",),
         ("ENTREGAR", C, "C#1", "proxima accion material")]),
    _ti("T42", "R-9.1-auditor-3", {"instancias": {C: "C#1", A: "A#1"}, "ultimo_turn_id": 6},
        [("detener",), ("recibir", salida(sobre(turn_id=7, next_instance="current"))),
         ("despachar",),
         ("recibir", salida(sobre(turn_id=8, actor=C, next_actor=A,
                                  next_instance="current"))), ("despachar",)],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",), ("ENTREGAR", C, "C#1", "prompt literal"),
         ("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",)]),
    _ti("T43", "R-9.1-natural", dict(INST_C, ultimo_turn_id=6),
        [("detener",), ("recibir", salida(sobre(turn_id=7, human_need=NECESIDAD,
                                                next_actor=None, next_instance=None,
                                                next_prompt=None))), ("despachar",)],
        [("PAUSA_SOLICITADA",), ("RECIBIDO",), ("MOSTRAR_NECESIDAD",)]),
    _ti("T44", "R-9.1-pendiente", dict(INST_A, ultimo_turn_id=7),
        [("recibir", salida(sobre(turn_id=8, actor=C, next_actor=A,
                                  next_instance="current"))), ("detener",)],
        [("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",)], negativo="N9"),

    # -- 9.2 CONTINUAR --------------------------------------------------------
    _ti("T45", "R-9.2-preserva", dict(INST_A, ultimo_turn_id=7),
        [("recibir", salida(sobre(turn_id=8, actor=C, next_actor=A,
                                  next_instance="current", next_prompt=PROMPT_ACENTOS))),
         ("detener",), ("continuar", None)],
        [("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",),
         ("ENTREGAR", A, "A#1", PROMPT_ACENTOS)]),
    _ti("T46", "R-9.2-literal", dict(INST_A, ultimo_turn_id=7),
        [("recibir", salida(sobre(turn_id=8, actor=C, next_actor=A,
                                  next_instance="current", next_prompt=PROMPT_ACENTOS))),
         ("detener",), ("continuar", None)],
        [("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",),
         ("ENTREGAR", A, "A#1", PROMPT_ACENTOS)]),

    # -- 9.3 directiva --------------------------------------------------------
    _ti("T47", "R-9.3-canal-separado", dict(INST_A, ultimo_turn_id=7),
        [("recibir", salida(sobre(turn_id=8, actor=C, next_actor=A,
                                  next_instance="current", next_prompt=PROMPT_ACENTOS))),
         ("detener",), ("continuar", "RELEVAR AUDITOR")],
        [("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",),
         ("ENTREGAR", A, "A#1", PROMPT_ACENTOS),
         ("ENTREGAR_DIRECTIVA", "RELEVAR AUDITOR")]),

    # -- 11 secretos ----------------------------------------------------------
    _ti("T48", "R-11-literal", dict(INST_C, ultimo_turn_id=12),
        [("recibir", salida(sobre(turn_id=13, next_instance="current",
                                  next_prompt=PROMPT_SECRETO))), ("despachar",)],
        [("RECIBIDO",), ("ENTREGAR", C, "C#1", PROMPT_SECRETO)]),

    # -- estructurales --------------------------------------------------------
    _e("S01", "R-1-dos-caminos"),
    _e("S02", "R-1.1-no-interpreta"),
    _e("S03", "R-2-no-escanear-prompt"),
    _e("S04", "R-2-no-reconstruye"),
    _e("S05", "R-3-no-lee-fuentes"),
    _e("S06", "R-4-no-repara"),
    _e("S07", "R-5-no-adivina"),
    _e("S08", "R-5-git-prevalece"),
    _e("S09", "R-6-handle-efimero"),
    _e("S10", "R-6.1-no-degrada", negativo="N8"),
    _e("S11", "R-6.1-no-inventa", negativo="N8"),
    _e("S12", "R-7-unit-no-decide"),
    _e("S13", "R-7-no-consulta-git"),
    _e("S14", "R-8-no-decide"),
    _e("S15", "R-8-no-elige-modelo"),
    _e("S16", "R-8-no-cadencia"),
    _e("S17", "R-8-no-toca-prompt"),
    _e("S18", "R-8-no-copia-git"),
    _e("S19", "R-8-no-extiende"),
    _e("S20", "R-9-no-necesidad"),
    _e("S21", "R-9-no-git"),
    _e("S22", "R-9-no-durable"),
    _e("S23", "R-9-flag-efimero"),
    _e("S24", "R-9.1-frontera"),
    _e("S25", "R-9.2-no-reconstruye"),
    _e("S26", "R-9.3-no-aplica-relevo"),
    _e("S27", "R-9.3-no-modifica"),
    _e("S28", "R-9.3-no-en-json"),
    _e("S29", "R-9.3-no-saltea"),
    _e("S30", "R-10-estado-admitido"),
    _e("S31", "R-10-no-paralelo"),
    _e("S32", "R-10.1-fail-closed"),
    _e("S33", "R-10.1-no-degrada"),
    _e("S34", "R-11-no-necesita"),
    _e("S35", "R-11-no-resuelve"),
    _e("S36", "R-11-no-logs"),
]
