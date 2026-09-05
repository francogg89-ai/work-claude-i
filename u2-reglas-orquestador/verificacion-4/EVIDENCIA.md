# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933:auditorias/7292639ddc2706a12c86d244b2a7352a8025b733.md`.

## Resultado

```text
VEREDICTO=FALLO
código de retorno = 1
criterio activado = F11
```

Una única condición de fallo. Su causa está identificada abajo y no es un defecto del candidato.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificacion-4

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

## Qué falló, y de quién es el defecto

`P-C` ejecuta operaciones Git de sólo lectura sobre los SHAs congelados. La derivación sobre
`audit-chatgpt-i@d6dba9decf6091078fa1b7f4f49b044e59f4df02` abortó:

```text
git -C C:/Franco_Metodos_AI/audit-chatgpt-i rev-list --count d6dba9decf6091078fa1b7f4f49b044e59f4df02
  returned non-zero exit status 128
```

El clon local de `audit-chatgpt-i` no contenía ese objeto: el corte congelado para `P-C` es
posterior al último `fetch` de ese repositorio en esta máquina.

El defecto es de preparación de la corrida, y es mío. Antes de anotar `INICIO` debí sincronizar
los tres clones que la corrida lee, no sólo los dos que había tocado en esta intervención. No es
un defecto de `REGLAS-ORQUESTADOR.md`, ni del contrato, ni del mecanismo.

No se corrigió ni se reintentó. La ejecución fue observada, se resolvió como `FALLO` conforme a
`T2`/`F11`, y el contrato queda agotado. Sincronizar el clon y volver a invocar produciría una
segunda invocación bajo la misma identidad, que es exactamente lo que `X4` prohíbe y lo que el
incidente `D-03` estableció que no se hace.

## Lo que sí quedó demostrado antes de la falla

La excepción se produjo en `P-C`, que es lo último que el cuerpo evalúa. Todo lo anterior se
ejecutó y quedó preservado en `salida.txt`:

```text
E9   blob leido = b871240fd38d28430fc86fc4b14f1b851dad1f10 = congelado        SI
E4   ninguna sección mecánica sin obligación                                  SI
E5   ninguna sección mecánica viola su forma declarada                        SI
E1   84 casos, 84 con el resultado que su obligación predice, 0 discrepantes  SI
E2   13 identificadores emitidos, ninguno ajeno al candidato                  SI
E3   83 obligaciones del candidato, 83 ejercitadas                            SI
E6   toda comprobación estructural falla sobre su mutante                     SI
E7   el observable difiere entre real y mutante en las 36 comprobaciones      SI
E8   P-C                                                                      NO EVALUADO
```

Eso no convierte la corrida en aprobable: el éxito exige `E1`-`E17` simultáneamente y `F11`
ocurrió. Se registra para que el AUDITOR sepa qué quedó ejercitado y qué no.

## La regla de ejecución funcionó

Esta corrida es la primera que ejercita la maquinaria de `X1`-`X5` contra una falla real, y se
comportó como el contrato exige:

```text
T2   la excepción fue capturada, registrada con su traza y resuelta en el veredicto
     no hubo T3: la invocación no murió en silencio
CIERRE anotado al emitir el veredicto, que es FALLO
E12  la bitácora tiene un INICIO y un CIERRE de la identidad congelada
E16  no había líneas de otras identidades, y ninguna fue alterada
```

Contenido preservado de `u2-reglas-orquestador/BITACORA.txt`:

```text
INICIO audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240fd38d28430fc86fc4b14f1b851dad1f10
CIERRE audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240fd38d28430fc86fc4b14f1b851dad1f10
```

Una falla observada produjo un resultado, no un vacío. Esa era la razón de elegir `T2` sobre `T3`
al cerrar `D-09`, y esta corrida lo muestra funcionando.

## Regla de ejecución observada

```text
bitácora de la unidad antes de la corrida   no existía
ruta resuelta                               C:/Franco_Metodos_AI/work-claude-i/
                                            u2-reglas-orquestador/BITACORA.txt
X4 reintento detectado                      no: no había INICIO de esta identidad
INICIO anotado                              antes del primer caso
CIERRE anotado                              al emitir el veredicto FALLO
```

La ruta es la constante de unidad, resuelta contra `--repo-work`. `agregar` falla cerrado si el
directorio no existe, para que una ruta mal resuelta no escriba la bitácora en otro lugar en
silencio.

## Controles sobre el propio mecanismo

Los nueve se ejecutaron antes de `P-C` y discriminaron:

```text
N12  obligación sintética sin caso                 -> F3 detectado
N13  sección sintética sin obligación              -> F5 detectado
N14  contenido sintético fuera de forma            -> F6 detectado
N15  blob sintético ajeno                          -> F10 detectado
N16  mutante sintético que no altera el observable -> F8 detectado
N17  aborto capturado atravesando correr()         -> ruta=corrida, F11, veredicto FALLO,
                                                      bitácora sintética con INICIO y CIERRE
N18  reintento atravesando la misma correr()       -> ruta=reintento, criterios no evaluados,
                                                      bitácora sintética sin cambios
N19  historia ajena                                -> intacta detectada, alterada detectada
N20  ruta derivada del propio directorio           -> F19 detectado
```

`N17` y `N18` atravesaron `correr()`, la misma función que la invocación real. `N17` obtuvo `F11`
sobre su bitácora sintética y `N18` el resultado de reintento sobre la suya: son sus éxitos, no
fallos de la corrida, conforme a la acotación de alcance del contrato.

`N1`-`N11` están presentes en el corpus y ninguno fue aceptado.

## Parámetros relevantes

```text
CANDIDATE_WORK_SHA     7292639ddc2706a12c86d244b2a7352a8025b733
CANDIDATE_PATH         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
CANDIDATE_BLOB_SHA     b871240fd38d28430fc86fc4b14f1b851dad1f10
TRANSPORT_AUTHORITY    revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c
P_C_WORK_SHA           7292639ddc2706a12c86d244b2a7352a8025b733
P_C_AUDIT_SHA          d6dba9decf6091078fa1b7f4f49b044e59f4df02
BITACORA_PATH          u2-reglas-orquestador/BITACORA.txt
```

## Trabajo previo a INICIO, declarado

Antes de invocar la corrida se ejecutó una prueba de humo que sólo importó los módulos, ejercitó
insumos sintéticos y comprobó que la bitácora de la unidad no existía. No leyó el candidato, no
ejecutó ningún caso del corpus y no ejercitó ninguna comprobación estructural sobre el sujeto
real.

Esa prueba no incluyó las operaciones Git de `P-C`. Si las hubiera incluido, el clon
desactualizado habría aparecido antes de `INICIO` y esta corrida no se habría gastado. Es la
lección concreta de este fallo.

## Archivos del mecanismo

```text
candidato.py      lee el candidato del commit congelado y extrae su superficie normativa
autoridad.py      obtiene campos, tipos y formas admitidas desde la autoridad congelada
orquestador.py    implementa las obligaciones del candidato; no importa Git ni red
estructurales.py  36 comprobaciones estructurales, su observable y su mutante
corpus.py         84 casos, cada uno con su obligación y su resultado normativo esperado
sinteticos.py     insumos sintéticos de N12-N20
bitacora.py       bitácora append-only de la unidad, calificada por identidad
verificar.py      correr() único, guardia X4 compartida, E1-E17, F1-F19, N1-N20
salida.txt        salida literal de la corrida
```

Las evidencias de las tres corridas anteriores siguen intactas en `verificador/`,
`verificacion-2/` y `verificacion-3/`. `verificacion-3/BITACORA.txt` no fue leída ni modificada.

## Limitaciones

Las que el contrato congelado declara, sin agregados:

- el corpus es finito;
- el verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo;
- `P-C` corre sobre historias cortas y lineales —en esta corrida no llegó a correr—;
- `P-B` verifica las transiciones declaradas, no una interrupción concurrente real;
- `P-E` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería;
- `P-F` demuestra que cada mutante altera el observable que su comprobación lee, no que ese
  observable sea el más adecuado;
- la bitácora hace auditable la cantidad de invocaciones siempre que se preserve.
