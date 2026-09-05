"""Insumos sinteticos de los controles sobre el propio mecanismo.

Nunca se aplican al candidato real ni a la bitacora real de la unidad.
"""

BASE = """# DOCUMENTO SINTETICO

# 1. Seccion mecanica

```text
R-1-alfa                 obligacion alfa
R-1-beta                 obligacion beta
```

Nota. Explicacion que no obliga.

# 2. Superficie normativa

```text
SECCIONES_NO_MECANICAS   2
```
"""

N11_OBLIGACION_SIN_CASO = BASE
N11_CASOS = ["R-1-alfa"]

N12_SECCION_SIN_OBLIGACION = BASE.replace(
    "# 2. Superficie normativa",
    "# 3. Seccion mecanica sin obligaciones\n\nNota. Solo prosa.\n\n# 2. Superficie normativa")

N13_CONTENIDO_FUERA_DE_FORMA = BASE.replace(
    "# 1. Seccion mecanica\n\n```text",
    "# 1. Seccion mecanica\n\nTexto colado antes del bloque.\n\n```text")

N14_BLOB_AJENO = "0" * 40

N16_BITACORA = "BITACORA_N16.txt"
N17_BITACORA = "BITACORA_N17.txt"
N18_BITACORA = "BITACORA_N18.txt"

IDENT_SINTETICA = {"contrato": "contrato-sintetico", "candidato": "1" * 40}
IDENT_AJENA = {"contrato": "contrato-ajeno", "candidato": "2" * 40}

N22_FUENTE_IMPORTADORA = (
    "import sondas\n"
    "import casos\n"
    "\n"
    "def ejecutar(v):\n"
    "    return casos.CASOS_LLAMADA\n"
)

N24_FUENTE_DERIVADA = (
    "import os\n"
    "RUTA_RELATIVA = os.path.join(os.path.dirname(__file__), \"BITACORA.txt\")\n"
)
