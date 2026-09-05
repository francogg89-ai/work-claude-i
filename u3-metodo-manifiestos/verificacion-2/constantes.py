"""Valores literales del contrato congelado. Ningun modulo los infiere.

Identidad contractual: audit-chatgpt-i@856a0782cba7b331ee4f2178b7235553b1787c90.
`prevuelo.py` no importa este modulo: recibe la lista de vinculaciones como argumento.
"""

IDENTIDAD_CONTRATO = "audit-chatgpt-i@856a0782cba7b331ee4f2178b7235553b1787c90"

CANDIDATE_WORK_SHA = "05041ddf0e7a687cc8ed1982a3d824570fe57710"
CANDIDATE_PATH = "u3-metodo-manifiestos/METODO-MANIFIESTOS.md"
CANDIDATE_BLOB_SHA = "f44f2a0797cde6f569cca6fe5397d45917680258"

# Constante de la unidad. No se deriva del directorio del mecanismo.
BITACORA_PATH_UNIDAD = "u3-metodo-manifiestos/BITACORA.txt"

P_C_REPO = "https://github.com/francogg89-ai/work-claude-i"
P_C_REMOTO = "origin"
P_C_CORTE_ORIGEN = "636a5d095574130b56c232da7958691f87234516"
P_C_CORTE_DESTINO = "5bd6b0f582c7970a7b8c6c838b9971a70df43dfc"
P_C_REFERENCIA = "refs/heads/main"

SUPERFICIE_DISJUNTA = {"repo": "work-claude-i", "paths": ("u1-contratos-transversales/",)}
SUPERFICIE_SOLAPADA = {"repo": "work-claude-i", "paths": ("u3-metodo-manifiestos/",)}


def vinculaciones(repo_work):
    """Lista literal y cerrada. Cinco vinculaciones nominales, en su orden congelado."""
    return [
        ("V1", "local", repo_work, CANDIDATE_WORK_SHA),
        ("V2", "local", repo_work, CANDIDATE_BLOB_SHA),
        ("V3", "local", repo_work, P_C_CORTE_ORIGEN),
        ("V4", "local", repo_work, P_C_CORTE_DESTINO),
        ("V5", "remota", repo_work, P_C_REMOTO, P_C_REFERENCIA),
    ]


NOMBRES_VINCULACIONES = ("V1", "V2", "V3", "V4", "V5")

# Los modulos que implementan o ejercitan al candidato. `observador` no esta: es el instrumento
# que observa la corrida, no parte de ella, y `constantes` solo transporta literales.
MODULOS_DE_LA_CORRIDA = (
    "superficie", "constituyente", "corpus", "comprobaciones", "registro", "controles",
    "corrida", "bitacora", "evaluadores",
)
