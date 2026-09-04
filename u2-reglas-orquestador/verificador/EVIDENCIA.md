# Evidencia — corrida única bajo contrato congelado

Contrato congelado en
`audit-chatgpt-i@9679ca4ca6987a3706a0b06cebd3b03cce1dcc7a:auditorias/b2a7c472732e5da59b8c82da7278a0e66ed26e93.md`.

Candidato congelado
`work-claude-i@b2a7c472732e5da59b8c82da7278a0e66ed26e93:u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`,
blob `49ad9e04a6ea2f04e4ec6f1f0efd2c5adf51f367`.

El candidato no fue modificado por esta intervención: su blob sigue siendo el congelado.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificador

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

Una sola corrida. El contrato queda agotado al producir este resultado.

## Parámetros relevantes

```text
TRANSPORT_AUTHORITY   revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c
                      metodo/REVOLUTIONS.md
P_C_WORK_SHA          b2a7c472732e5da59b8c82da7278a0e66ed26e93
P_C_AUDIT_SHA         3e27c9af3e71767f4898c6607659c84ab010aa4a
```

Los tres repositorios se leyeron por ruta local. Las rutas son parámetros de la corrida, no
identidades: las identidades son los SHAs de arriba, y el AUDITOR puede reejecutar el mecanismo
sobre sus propios clones apuntando a esos mismos SHAs.

El verificador operó sobre SHAs exactos y en ningún punto sobre `HEAD` ni sobre una referencia
móvil.

## Código de retorno

```text
0
```

El mecanismo devuelve `0` sólo cuando no se registró ninguna condición de fallo, y `1` en
cualquier otro caso.

## Salida

La salida literal e íntegra está en `salida.txt`, preservada sin edición.

Resumen de lo que esa salida contiene:

```text
autoridad derivada    12 campos, con su conjunto de tipos admitidos por campo,
                      y las tres formas admitidas, extraídas de la fuente congelada
casos                 34 casos, todos con resultado idéntico al normativo esperado
E2                    todos los rechazos citan una regla declarada
E3                    28 reglas declaradas, 28 ejercitadas
controles negativos   N1-N9 exigidos, N1-N9 presentes, ninguno aceptado
P-C                   N_CONSTRUCTOR = 5, N_AUDITOR = 7, coincidentes por dos derivaciones
VEREDICTO             EXITO
```

## Qué significa "derivación independiente" en P-C

`E4` exige que `P-C` reproduzca los números de la derivación Git independiente de `D1`.

`D1` deriva con `git rev-list --count <corte>`. La segunda derivación usa un camino distinto,
`git log --format=%H <corte>`, y deduplica en el verificador antes de contar. Son dos caminos
distintos sobre el mismo conjunto alcanzable, y coincidieron en ambos repositorios.

## Archivos del mecanismo

```text
autoridad.py    obtiene campos, tipos y formas admitidas desde la fuente congelada
orquestador.py  implementa las reglas declaradas por el candidato; no importa Git ni red
corpus.py       34 casos, cada uno con su regla y su resultado normativo esperado
verificar.py    ejecuta, compara después de producir, y evalúa E1-E4, F1-F5 y N1-N9
salida.txt      salida literal de la corrida
```

`orquestador.py` no conoce el resultado esperado de ningún caso: `corpus.py` lo declara y
`verificar.py` compara después de que el mecanismo produjo el suyo.

## Limitaciones

Son las que el contrato congelado declara, sin agregados:

- el corpus es finito: demuestra que las reglas discriminan sobre los casos declarados, no que
  ninguna entrada imaginable las eluda;
- el verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo; una corrida local no demuestra que un orquestador desplegado se comporte así;
- `P-C` corrió sobre dos historias actualmente cortas y lineales: demuestra que la derivación
  produce el número correcto sobre ellas, no que se comporte igual sobre una topología con
  merges;
- `P-B` verificó las transiciones declaradas, no el comportamiento de un proceso real bajo una
  interrupción concurrente.
