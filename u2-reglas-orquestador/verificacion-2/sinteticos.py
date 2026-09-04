"""Insumos sintéticos de los controles N12-N15.

Nunca se aplican al candidato real: existen para demostrar que las comprobaciones de cobertura,
de sección, de forma y de identidad pueden fallar.
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
