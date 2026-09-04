"""Corpus de casos del contrato previo congelado de U2.

Cada caso declara la regla del candidato que lo gobierna y el resultado normativo que esa
regla predice. El mecanismo no lee `esperado`: lo produce `verificar.py` y la comparacion
es posterior.

Los casos marcados con `negativo` son los controles negativos N1-N9 del contrato: su
aceptacion implica FALLO.
"""

import json

WORK_ID = "revolutions-orchestra-ai"
OTRO_WORK_ID = "otro-trabajo-ai"
REPO = "https://github.com/francogg89-ai/work-claude-i"
COMMIT = "0" * 40

BASE = {
    "protocol": "revolutions-hop/v1",
    "work_id": WORK_ID,
    "turn_id": 1,
    "actor": "AUDITOR",
    "repository": REPO,
    "commit": COMMIT,
    "next_actor": "CONSTRUCTOR",
    "next_instance": "fresh",
    "next_prompt": "prompt literal",
    "human_need": None,
    "unit": None,
    "final": False,
}

NECESIDAD = {
    "id": "H1",
    "type": "no_material",
    "request": "decision de dominio",
    "checkpoint": None,
    "guide_prompt": None,
    "expected_evidence": ["respuesta del humano"],
    "resume_actor": "AUDITOR",
}

PROMPT_ACENTOS = "linea uno\nlinea dos con acentos: intervención, auditoría\nlinea tres"
PROMPT_SECRETO = "usar TOKEN_FUDO → variable de entorno FUDO_TOKEN, sin resolverla"


def sobre(**cambios):
    s = dict(BASE)
    s.update(cambios)
    return s


def salida(s, prosa="El actor explica lo que hizo.\n\n"):
    """Salida de un actor: prosa y un unico bloque json final."""
    return prosa + "```json\n" + json.dumps(s, ensure_ascii=False, indent=2) + "\n```"


def salida_dos_bloques(s):
    """Un bloque json anterior que no es el sobre, y el sobre como ultimo bloque."""
    señuelo = '```json\n{"protocol": "otro/v9", "nota": "ejemplo de un documento"}\n```\n\n'
    return "Prosa.\n\n" + señuelo + "Mas prosa.\n\n```json\n" + \
        json.dumps(s, ensure_ascii=False, indent=2) + "\n```"


# Cada caso: id, regla, negativo, ops, esperado.
# ops se ejecutan en orden sobre un Orquestador construido con `inicio`.
CASOS = [
    {
        "id": "C01", "regla": "R-1.1-primer-turn-id", "negativo": None,
        "inicio": {},
        "ops": [("recibir", salida(sobre(turn_id=5)))],
        "esperado": [("DETENER_REPORTAR", "R-1.1-primer-turn-id")],
    },
    {
        "id": "C02", "regla": "R-2-ultimo-bloque", "negativo": None,
        "inicio": {},
        "ops": [("recibir", salida_dos_bloques(sobre()))],
        "esperado": [("RECIBIDO",)],
    },
    {
        "id": "C03", "regla": "R-2-no-parsea", "negativo": None,
        "inicio": {},
        "ops": [("recibir", "Una salida sin ningun bloque json.")],
        "esperado": [("DETENER_REPORTAR", "R-2-no-parsea")],
    },
    {
        "id": "C04", "regla": "R-2-no-escanear-prompt", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 4},
        "ops": [
            ("recibir", salida(sobre(turn_id=5, next_instance="current",
                                     next_prompt="abri una instancia fresh nueva ahora"))),
            ("despachar",),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#1",
             "abri una instancia fresh nueva ahora"),
        ],
    },
    {
        "id": "C05", "regla": "R-V1", "negativo": "N7",
        "inicio": {},
        "ops": [("recibir", salida(sobre(protocol="revolutions-hop/v2")))],
        "esperado": [("DETENER_REPORTAR", "R-V1")],
    },
    {
        "id": "C06", "regla": "R-V2", "negativo": "N6",
        "inicio": {},
        "ops": [("recibir", salida(sobre(work_id=OTRO_WORK_ID)))],
        "esperado": [("DETENER_REPORTAR", "R-V2")],
    },
    {
        "id": "C07", "regla": "R-V3", "negativo": None,
        "inicio": {},
        "ops": [("recibir", salida({k: v for k, v in BASE.items() if k != "unit"}))],
        "esperado": [("DETENER_REPORTAR", "R-V3")],
    },
    {
        "id": "C08", "regla": "R-V4", "negativo": None,
        "inicio": {},
        "ops": [("recibir", salida(sobre(turn_id="1")))],
        "esperado": [("DETENER_REPORTAR", "R-V4")],
    },
    {
        "id": "C09a", "regla": "R-V5", "negativo": "N3",
        "inicio": {"ultimo_turn_id": 6},
        "ops": [("recibir", salida(sobre(turn_id=6)))],
        "esperado": [("DETENER_REPORTAR", "R-V5")],
    },
    {
        "id": "C09b", "regla": "R-V5", "negativo": "N3",
        "inicio": {"ultimo_turn_id": 6},
        "ops": [("recibir", salida(sobre(turn_id=9)))],
        "esperado": [("DETENER_REPORTAR", "R-V5")],
    },
    {
        "id": "C09c", "regla": "R-V5", "negativo": "N3",
        "inicio": {"ultimo_turn_id": 6},
        "ops": [("recibir", salida(sobre(turn_id=5)))],
        "esperado": [("DETENER_REPORTAR", "R-V5")],
    },
    {
        "id": "C10", "regla": "R-V6", "negativo": "N5",
        "inicio": {},
        "ops": [("recibir", salida(sobre(next_instance="nueva")))],
        "esperado": [("DETENER_REPORTAR", "R-V6")],
    },
    {
        "id": "C11", "regla": "R-V7", "negativo": "N4",
        "inicio": {},
        "ops": [("recibir", salida(sobre(next_actor=None, next_instance="fresh")))],
        "esperado": [("DETENER_REPORTAR", "R-V7")],
    },
    {
        "id": "C12", "regla": "R-V8", "negativo": "N1",
        "inicio": {},
        "ops": [("recibir", salida(sobre(human_need=NECESIDAD)))],
        "esperado": [("DETENER_REPORTAR", "R-V8")],
    },
    {
        "id": "C13", "regla": "R-V8", "negativo": "N2",
        "inicio": {},
        "ops": [("recibir", salida(sobre(human_need=NECESIDAD, final=True,
                                         next_actor=None, next_instance=None,
                                         next_prompt=None)))],
        "esperado": [("DETENER_REPORTAR", "R-V8")],
    },
    {
        "id": "C14", "regla": "R-4-reporte", "negativo": None,
        "inicio": {},
        "ops": [("recibir", salida(sobre(protocol="otro")))],
        "esperado": [("DETENER_REPORTAR", "R-V1")],
        "estructural": "reporte_sin_reparacion",
    },
    {
        "id": "C15a", "regla": "R-5-no-reinicio", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 20},
        "ops": [("recibir", salida(sobre(turn_id=21, next_instance="fresh")))],
        "esperado": [("RECIBIDO",)],
    },
    {
        "id": "C15b", "regla": "R-5-no-reinicio", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 20},
        "ops": [("recibir", salida(sobre(turn_id=1, next_instance="fresh")))],
        "esperado": [("DETENER_REPORTAR", "R-V5")],
    },
    {
        "id": "C16", "regla": "R-6-resolucion", "negativo": None,
        "inicio": {"ultimo_turn_id": 0},
        "ops": [("recibir", salida(sobre(turn_id=1, next_instance="fresh"))), ("despachar",)],
        "esperado": [
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#t1", "prompt literal"),
        ],
    },
    {
        "id": "C17", "regla": "R-6-fresh-a-current", "negativo": None,
        "inicio": {"instancias": {"AUDITOR": "AUDITOR#0"}, "ultimo_turn_id": 0},
        "ops": [
            ("recibir", salida(sobre(turn_id=1, next_instance="fresh"))), ("despachar",),
            ("recibir", salida(sobre(turn_id=2, actor="CONSTRUCTOR",
                                     next_actor="AUDITOR", next_instance="current"))),
            ("despachar",),
            ("recibir", salida(sobre(turn_id=3, next_instance="current",
                                     next_prompt="segundo pase"))),
            ("despachar",),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#t1", "prompt literal"),
            ("RECIBIDO",),
            ("ENTREGAR", "AUDITOR", "AUDITOR#0", "prompt literal"),
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#t1", "segundo pase"),
        ],
    },
    {
        "id": "C18", "regla": "R-6.1-fail-closed", "negativo": "N8",
        "inicio": {"ultimo_turn_id": 4},
        "ops": [
            ("recibir", salida(sobre(turn_id=5, next_instance="current"))),
            ("despachar",),
        ],
        "esperado": [("RECIBIDO",), ("DETENER_REPORTAR", "R-6.1-fail-closed")],
    },
    {
        "id": "C19", "regla": "R-7-orden", "negativo": None,
        "inicio": {"ultimo_turn_id": 24},
        "ops": [
            ("recibir", salida(sobre(turn_id=25, human_need=NECESIDAD, next_actor=None,
                                     next_instance=None, next_prompt=None))),
            ("despachar",),
        ],
        "esperado": [("RECIBIDO",), ("MOSTRAR_NECESIDAD",)],
    },
    {
        "id": "C20", "regla": "R-7-orden", "negativo": None,
        "inicio": {"ultimo_turn_id": 32},
        "ops": [
            ("recibir", salida(sobre(turn_id=33, final=True, next_actor=None,
                                     next_instance=None, next_prompt=None))),
            ("despachar",),
        ],
        "esperado": [("RECIBIDO",), ("MOSTRAR_CIERRE",)],
    },
    {
        "id": "C21", "regla": "R-7-orden", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 10},
        "ops": [
            ("recibir", salida(sobre(turn_id=11, next_instance="current",
                                     unit="unidad 2 terminada; inicio unidad 3"))),
            ("despachar",),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("MOSTRAR_UNIDAD", "unidad 2 terminada; inicio unidad 3"),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#1", "prompt literal"),
        ],
    },
    {
        "id": "C22", "regla": "R-7-entrega-literal", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 2},
        "ops": [
            ("recibir", salida(sobre(turn_id=3, next_instance="current",
                                     next_prompt=PROMPT_ACENTOS))),
            ("despachar",),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#1", PROMPT_ACENTOS),
        ],
    },
    {
        "id": "C23", "regla": "R-8-no-cadencia", "negativo": None,
        "inicio": {},
        "ops": [],
        "esperado": [],
        "estructural": "sin_cadencia_ni_git",
    },
    {
        "id": "C24", "regla": "R-9.1-detener-constructor", "negativo": None,
        "inicio": {"instancias": {"AUDITOR": "AUDITOR#1"}, "ultimo_turn_id": 5},
        "ops": [
            ("detener",),
            ("recibir", salida(sobre(turn_id=6, actor="CONSTRUCTOR",
                                     next_actor="AUDITOR", next_instance="current"))),
            ("despachar",),
        ],
        "esperado": [("PAUSA_SOLICITADA",), ("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",)],
    },
    {
        "id": "C25", "regla": "R-9.1-detener-auditor", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 6},
        "ops": [
            ("detener",),
            ("recibir", salida(sobre(turn_id=7, next_instance="current",
                                     next_prompt="proxima accion material"))),
            ("despachar",),
        ],
        "esperado": [
            ("PAUSA_SOLICITADA",),
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#1", "proxima accion material"),
        ],
    },
    {
        "id": "C26", "regla": "R-9.1-detencion-natural", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 6},
        "ops": [
            ("detener",),
            ("recibir", salida(sobre(turn_id=7, human_need=NECESIDAD, next_actor=None,
                                     next_instance=None, next_prompt=None))),
            ("despachar",),
        ],
        "esperado": [("PAUSA_SOLICITADA",), ("RECIBIDO",), ("MOSTRAR_NECESIDAD",)],
    },
    {
        "id": "C27", "regla": "R-9.1-pendiente", "negativo": "N9",
        "inicio": {"instancias": {"AUDITOR": "AUDITOR#1"}, "ultimo_turn_id": 7},
        "ops": [
            ("recibir", salida(sobre(turn_id=8, actor="CONSTRUCTOR",
                                     next_actor="AUDITOR", next_instance="current"))),
            ("detener",),
        ],
        "esperado": [("RECIBIDO",), ("PAUSA_SIN_ENTREGAR",)],
    },
    {
        "id": "C28", "regla": "R-9.2-continuar-literal", "negativo": None,
        "inicio": {"instancias": {"AUDITOR": "AUDITOR#1"}, "ultimo_turn_id": 7},
        "ops": [
            ("recibir", salida(sobre(turn_id=8, actor="CONSTRUCTOR", next_actor="AUDITOR",
                                     next_instance="current",
                                     next_prompt=PROMPT_ACENTOS))),
            ("detener",),
            ("continuar", None),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("PAUSA_SIN_ENTREGAR",),
            ("ENTREGAR", "AUDITOR", "AUDITOR#1", PROMPT_ACENTOS),
        ],
    },
    {
        "id": "C29", "regla": "R-9.3-canal-separado", "negativo": None,
        "inicio": {"instancias": {"AUDITOR": "AUDITOR#1"}, "ultimo_turn_id": 7},
        "ops": [
            ("recibir", salida(sobre(turn_id=8, actor="CONSTRUCTOR", next_actor="AUDITOR",
                                     next_instance="current",
                                     next_prompt=PROMPT_ACENTOS))),
            ("detener",),
            ("continuar", "RELEVAR AUDITOR"),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("PAUSA_SIN_ENTREGAR",),
            ("ENTREGAR", "AUDITOR", "AUDITOR#1", PROMPT_ACENTOS),
            ("ENTREGAR_DIRECTIVA", "RELEVAR AUDITOR"),
        ],
    },
    {
        "id": "C30", "regla": "R-10-estado-efimero", "negativo": None,
        "inicio": {},
        "ops": [],
        "esperado": [],
        "estructural": "estado_solo_admitido",
    },
    {
        "id": "C31", "regla": "R-11-secreto-literal", "negativo": None,
        "inicio": {"instancias": {"CONSTRUCTOR": "CONSTRUCTOR#1"}, "ultimo_turn_id": 12},
        "ops": [
            ("recibir", salida(sobre(turn_id=13, next_instance="current",
                                     next_prompt=PROMPT_SECRETO))),
            ("despachar",),
        ],
        "esperado": [
            ("RECIBIDO",),
            ("ENTREGAR", "CONSTRUCTOR", "CONSTRUCTOR#1", PROMPT_SECRETO),
        ],
    },
]
