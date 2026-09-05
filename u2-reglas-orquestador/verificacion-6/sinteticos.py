"""Insumos sintéticos de los controles N12-N20.

Nunca se aplican al candidato real ni a la bitácora real de la unidad.
"""

BASE = """# DOCUMENTO SINTETICO

# 1. Seccion mecanica

```text
R-1-alfa                 obligacion alfa
R-1-beta                 obligacion beta
```

Nota. Explicación que no obliga.

# 2. Superficie normativa

```text
SECCIONES_NO_MECANICAS   2
```
"""

# N12: la obligación R-1-beta existe y ningún caso la ejercita.
N12_OBLIGACION_SIN_CASO = BASE
N12_CASOS = ["R-1-alfa"]

# N13: la sección 3 es mecánica y no aporta ninguna obligación.
N13_SECCION_SIN_OBLIGACION = BASE.replace(
    "# 2. Superficie normativa",
    "# 3. Seccion mecanica sin obligaciones\n\nNota. Sólo prosa.\n\n# 2. Superficie normativa",
)

# N14: contenido no vacío entre el encabezado de una sección mecánica y su bloque.
N14_CONTENIDO_FUERA_DE_FORMA = BASE.replace(
    "# 1. Seccion mecanica\n\n```text",
    "# 1. Seccion mecanica\n\nTexto colado antes del bloque de obligaciones.\n\n```text",
)

# N15: identidad de blob que no coincide con la congelada.
N15_BLOB_AJENO = "0" * 40

# N17-N20 usan bitácoras e identidades sintéticas.
N17_BITACORA = "BITACORA_N17.txt"
N18_BITACORA = "BITACORA_N18.txt"
N19_BITACORA = "BITACORA_N19.txt"

IDENT_SINTETICA = {"contrato": "contrato-sintetico", "candidato": "1" * 40}
IDENT_AJENA = {"contrato": "contrato-ajeno", "candidato": "2" * 40}

# N20: fuente de un módulo de bitácora que deriva su ruta del propio directorio.
N20_FUENTE_DERIVADA = (
    "import os\n"
    "RUTA_RELATIVA = os.path.join(os.path.dirname(__file__), \"BITACORA.txt\")\n"
)


# N24: fuente de un modulo de pre-vuelo que importa un modulo de la corrida.
N24_FUENTE_IMPORTADORA = (
    "import sondas\n"
    "import corpus\n"
    "\n"
    "def ejecutar(identidades):\n"
    "    return corpus.CASOS\n"
)


# N25: dos vinculaciones nominales distintas que comparten repositorio y SHA.
N25_VINCULACIONES = [
    ("VINCULACION_ALFA", "C:/Franco_Metodos_AI/work-claude-i",
     "b871240fd38d28430fc86fc4b14f1b851dad1f10"),
    ("VINCULACION_BETA", "C:/Franco_Metodos_AI/work-claude-i",
     "b871240fd38d28430fc86fc4b14f1b851dad1f10"),
]
