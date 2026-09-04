# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@fd356b9369cf5bd80a9a15a6695453f2e191dcfe:auditorias/5f5e2ee8e9bcc7f471cabcd0ecd865ff5cfa0a39.md`.

## Resultado

```text
VEREDICTO=FALLO
código de retorno = 1
```

Tres condiciones de fallo se activaron: `F6` una vez y `F7`/`F1` en dos comprobaciones
estructurales. El detalle y su atribución están más abajo.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificacion-2

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

## Invocación abortada previa, declarada

Antes de la corrida que produjo este resultado hubo una invocación que abortó con
`UnicodeEncodeError` dentro de un mutante, sin producir veredicto, sin escribir `salida.txt` y sin
evaluar ningún criterio. La causa fue que el sustituto de `open` usado por las comprobaciones de
ausencia de escritura delegaba en el `open` real; el mutante intentó escribir un texto con
caracteres no representables en la codificación por defecto de la consola.

Esa invocación dejó en el directorio tres archivos creados por mutantes —
`handle_persistido.tmp`, `detencion_durable.tmp` y `orquestador.log` — a las `17:15:02`. El
sustituto fue corregido a las `17:15:12` para devolver un objeto en memoria, y la corrida que
produjo `salida.txt` a las `17:15:19` no escribió ningún archivo fuera de su propia salida. Los
tres archivos fueron eliminados por ser residuo de mutantes y no evidencia.

Se declara porque el AUDITOR debe poder juzgar si esa invocación abortada afecta la condición de
corrida única, y ocultarla sería falsear la procedencia de la evidencia.

## Parámetros relevantes

```text
CANDIDATE_WORK_SHA     5f5e2ee8e9bcc7f471cabcd0ecd865ff5cfa0a39
CANDIDATE_PATH         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
CANDIDATE_BLOB_SHA     4cfc8f88ead6a1466f61522496605b6c89ed4057
TRANSPORT_AUTHORITY    revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c
                       metodo/REVOLUTIONS.md
P_C_WORK_SHA           5f5e2ee8e9bcc7f471cabcd0ecd865ff5cfa0a39
P_C_AUDIT_SHA          9f8512f1e7228fb81692c62b33414b11d974bd8d
```

El candidato se leyó desde Git en su commit congelado, no desde el disco. Ninguna operación usó
`HEAD` ni una referencia móvil.

## Identidad del candidato leída

```text
leido     4cfc8f88ead6a1466f61522496605b6c89ed4057
congelado 4cfc8f88ead6a1466f61522496605b6c89ed4057
coincide  True
```

## Conjunto de obligaciones extraído

```text
obligaciones            83
identificadores unicos  83
secciones numeradas     1 1.1 2 3 4 5 6 6.1 7 8 9 9.1 9.2 9.3 10 10.1 11 12 13
no mecanicas declaradas 12 13
secciones mecanicas     17
```

El denominador no proviene del mecanismo: se extrae del candidato leído en su blob congelado.

## Relación obligación → caso

`salida.txt` lista los 84 casos, cada uno con la obligación que lo gobierna. Las 83 obligaciones
del candidato quedan cubiertas; ningún caso invoca una obligación inexistente.

## Resultado contra el criterio congelado

```text
E1  84 casos ejecutados; 82 con el resultado que su obligación predice, 2 discrepantes   NO
E2  13 identificadores emitidos por el mecanismo, ninguno ajeno al candidato             SI
E3  83 obligaciones del candidato, 83 ejercitadas, ninguna sin caso                      SI
E4  ninguna sección mecánica sin obligación                                              SI
E5  una violación de forma en la sección 10.1                                            NO
E6  dos comprobaciones estructurales no fallaron sobre su mutante                        NO
E7  P-C coincidente por dos derivaciones sobre los SHAs congelados                       SI
E8  el blob leído es exactamente el congelado                                            SI

F1  ocurrió: S24 y S28
F2  no ocurrió
F3  no ocurrió
F4  no ocurrió
F5  no ocurrió
F6  ocurrió: sección 10.1, línea 335
F7  ocurrió: S24 y S28
F8  no ocurrió
F9  no ocurrió
```

## Los tres hallazgos, con su atribución

### F6 — defecto del candidato

```text
VIOLACION seccion 10.1 linea 335: contenido no vacio entre el bloque y la primera Nota.: '---'
```

Es exactamente `OBS-01`. La sección `10.1` termina su bloque de obligaciones y a continuación
lleva un separador Markdown `---` sin marcador `Nota.` previo.

El candidato declara defecto a cualquier contenido no vacío en esa zona. Una línea `---` es
contenido no vacío. El mecanismo aplicó la regla declarada sin necesitar completarla, de modo que
`F6` ocurre y `F4` no.

La lectura alternativa —tratar `---` como separador tipográfico y no como contenido— habría
exigido una regla que el candidato no declara ni obtiene por referencia autoritativa, y habría
activado `F4`. Ninguna lectura del criterio congelado conduce a ÉXITO sobre este blob.

### F7 y F1 en S24 — defecto del mecanismo, no del candidato

La comprobación de `R-9.1-frontera` pasó sobre el sujeto real y **también** sobre su mutante.

El mutante `m_entrega_en_pausa` reemplaza `detener` por una llamada a `despachar` con
`stop_requested` ya activo. Como el candidato exige justamente pausar en esa situación, el mutante
reproduce la conducta correcta en lugar de violarla. La comprobación no quedó demostrada como
capaz de fallar.

El defecto está en el mutante, no en el candidato ni en la conducta observada: el sujeto real
pausó y preservó el sobre pendiente, que es lo que la obligación exige.

### F7 y F1 en S28 — defecto del mecanismo, no del candidato

La comprobación de `R-9.3-no-en-json` pasó sobre el sujeto real y **también** sobre su mutante.

La comprobación toma una copia del sobre pendiente **antes** de emitir la directiva, y el mutante
`m_directiva_en_json` inyecta la directiva **después**. La copia observada nunca contiene la
mutación, de modo que la comprobación no puede detectarla.

El defecto está en el orden de observación de la comprobación. La conducta del sujeto real fue
correcta: la directiva viajó por su canal y no dentro del sobre.

## Controles negativos

```text
exigidos  N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 N13 N14 N15
presentes N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 N13 N14 N15
```

Ninguno de `N1`-`N11` fue aceptado por el mecanismo.

Los cuatro controles sobre el propio mecanismo discriminaron:

```text
N12  obligación sintética sin caso        -> F3 detectado (R-1-beta)
N13  sección sintética sin obligación     -> F5 detectado (sección 3)
N14  contenido sintético fuera de forma   -> F6 detectado (sección 1, línea 5)
N15  blob sintético ajeno                 -> F9 detectado
```

`E6` los generaliza a toda comprobación estructural, y es exactamente ese criterio el que
descubrió los defectos de `S24` y `S28`. Bajo el contrato anterior, esas dos comprobaciones
habrían entrado en la evidencia como verdes sin demostrar nada.

## P-C

```text
N_CONSTRUCTOR  rev-list --count = 8   git log unico = 8   coincide = True
N_AUDITOR      rev-list --count = 10  git log unico = 10  coincide = True
```

Dos caminos Git distintos sobre los SHAs congelados, coincidentes.

## Archivos del mecanismo

```text
candidato.py      lee el candidato del commit congelado y extrae su superficie normativa
autoridad.py      obtiene campos, tipos y formas admitidas desde la autoridad congelada
orquestador.py    implementa las obligaciones del candidato; no importa Git ni red
estructurales.py  comprobaciones estructurales y sus mutantes
corpus.py         84 casos, cada uno con su obligación y su resultado normativo esperado
sinteticos.py     insumos sintéticos de N12-N15
verificar.py      ejecuta, compara después de producir, y evalúa E1-E8, F1-F9, N1-N15
salida.txt        salida literal de la corrida
```

La evidencia de la corrida anterior, bajo un contrato distinto y un candidato distinto, sigue en
`u2-reglas-orquestador/verificador/` sin modificación.

## Limitaciones

Son las que el contrato congelado declara, sin agregados:

- el corpus es finito;
- el verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo;
- `P-C` corrió sobre historias cortas y lineales;
- `P-B` verificó las transiciones declaradas, no una interrupción concurrente real;
- `P-E` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería.
