# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0:auditorias/19d33fcb025f9d84736cd59f9e3ca6978ff4b48b.md`.

## Resultado

```text
VEREDICTO=EXITO
código de retorno = 0
```

Ningún criterio de fallo se activó.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificacion-3

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

## Regla de ejecución

```text
BITACORA.txt antes de la corrida   no existía
X4 reintento detectado             no: no había INICIO previo para esta identidad
INICIO anotado                     antes del primer caso
CIERRE anotado                     al emitir el veredicto
```

Contenido preservado de `BITACORA.txt`:

```text
INICIO audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0 b871240fd38d28430fc86fc4b14f1b851dad1f10
CIERRE audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0 b871240fd38d28430fc86fc4b14f1b851dad1f10
```

Exactamente un INICIO y un CIERRE de esta identidad, sin líneas ajenas.

El cuerpo de la corrida está envuelto de modo que cualquier excepción posterior a `INICIO` se
registra como `F11` y se resuelve en el veredicto en lugar de abortar. Ninguna se produjo.

## Trabajo previo a INICIO, declarado

Antes de invocar la corrida se ejecutó una prueba de humo que hizo únicamente esto:

```text
importar los ocho módulos del mecanismo
ejercitar los insumos sintéticos N12, N13, N14, N17 y N18
comprobar que BITACORA.txt no existía
borrar las bitácoras sintéticas que esa prueba creó
```

No leyó el candidato, no ejecutó ningún caso del corpus, no ejercitó ninguna comprobación
estructural sobre el sujeto real y no tocó `BITACORA.txt`.

Se declara porque la frontera de la corrida es `INICIO` y el AUDITOR debe poder juzgar qué ocurrió
antes de ella sin depender de que se lo cuenten después.

## Parámetros relevantes

```text
CANDIDATE_WORK_SHA     19d33fcb025f9d84736cd59f9e3ca6978ff4b48b
CANDIDATE_PATH         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
CANDIDATE_BLOB_SHA     b871240fd38d28430fc86fc4b14f1b851dad1f10
TRANSPORT_AUTHORITY    revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c
                       metodo/REVOLUTIONS.md
P_C_WORK_SHA           19d33fcb025f9d84736cd59f9e3ca6978ff4b48b
P_C_AUDIT_SHA          693498fc8ff681069cf3997ea7e3f8636826a2d3
```

El candidato se leyó desde Git en su commit congelado. Ninguna operación usó `HEAD`.

## Identidad del candidato leída

```text
leido     b871240fd38d28430fc86fc4b14f1b851dad1f10
congelado b871240fd38d28430fc86fc4b14f1b851dad1f10
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

## Relación obligación → caso

`salida.txt` lista los 84 casos, cada uno con la obligación que lo gobierna, su resultado y —para
los estructurales— el observable del sujeto real y el de su mutante.

```text
casos con resultado OK      84
casos con resultado FALLO    0
obligaciones sin caso        ninguna
casos sobre obligaciones inexistentes  ninguno
```

## Resultado contra el criterio congelado

```text
E1   84 casos, todos con el resultado que su obligación predice            SI
E2   13 identificadores emitidos, ninguno ajeno al candidato               SI
E3   83 obligaciones, 83 ejercitadas                                       SI
E4   ninguna sección mecánica sin obligación                               SI
E5   ninguna sección mecánica viola su forma declarada                     SI
E6   toda comprobación estructural falla sobre su mutante                  SI
E7   el observable difiere entre real y mutante en las 36 comprobaciones   SI
E8   P-C: N_CONSTRUCTOR = 11, N_AUDITOR = 14, coincidentes                 SI
E9   el blob leído es exactamente el congelado                             SI
E10  INICIO y CIERRE preservados                                           SI
E11  no existía INICIO previo para esta identidad                          SI
E12  la bitácora tiene un INICIO y un CIERRE, sin líneas ajenas            SI

F1 a F13   ninguno ocurrió
```

## Las dos comprobaciones que el contrato anterior no discriminaba

`S24` y `S28` fueron las que activaron `F7` en la corrida anterior. Con las obligaciones
reformuladas y `E7` exigiendo que el observable difiera, ahora discriminan:

```text
S24  R-9.1-frontera
     obs_real = (entregado=False, conservado=True)
     obs_mut  = (entregado=True,  conservado=False)

S28  R-9.3-no-en-json
     obs_real = (sobre identico al recibido=True,  contiene la directiva=False)
     obs_mut  = (sobre identico al recibido=False, contiene la directiva=True)
```

El mutante de `S24` ahora entrega el sobre pendiente en lugar de reproducir la pausa correcta. El
de `S28` es observado por una sonda instalada en `despachar`, que ve el sobre en el instante en que
el orquestador lo usa y no una copia tomada antes de la mutación.

## Controles negativos

```text
exigidos  N1 a N18
presentes N1 a N18
```

`N1`-`N11` fueron rechazados por el mecanismo. Los siete controles sobre el propio mecanismo
discriminaron:

```text
N12  obligación sintética sin caso                    -> F3 detectado
N13  sección sintética sin obligación                 -> F5 detectado
N14  contenido sintético fuera de forma               -> F6 detectado
N15  blob sintético ajeno                             -> F10 detectado
N16  mutante sintético que no altera el observable    -> F8 detectado
N17  invocación sintética abortada tras INICIO        -> INICIO=1 CIERRE=0, observable
N18  bitácora sintética con INICIO previo             -> F12 detectado, sin anotar ni emitir
```

`N16` reproduce el defecto de `S24` y `S28` de la corrida anterior y demuestra que ahora se
detecta. `N17` y `N18` son las dos mitades de `D-03`: la primera demuestra que un aborto queda
observable, la segunda que un reintento se detiene y no reemplaza el resultado anterior.

Las bitácoras sintéticas `BITACORA_N17.txt` y `BITACORA_N18.txt` se preservan como evidencia de
esos dos controles. Son archivos distintos de `BITACORA.txt` y llevan una identidad de contrato
sintética.

## P-C

```text
N_CONSTRUCTOR  rev-list --count = 11  git log unico = 11  coincide = True
N_AUDITOR      rev-list --count = 14  git log unico = 14  coincide = True
```

Dos caminos Git distintos sobre los SHAs congelados, coincidentes.

## Archivos del mecanismo

```text
candidato.py      lee el candidato del commit congelado y extrae su superficie normativa
autoridad.py      obtiene campos, tipos y formas admitidas desde la autoridad congelada
orquestador.py    implementa las obligaciones del candidato; no importa Git ni red
estructurales.py  36 comprobaciones estructurales, su observable y su mutante
corpus.py         84 casos, cada uno con su obligación y su resultado normativo esperado
sinteticos.py     insumos sintéticos de N12-N18
bitacora.py       bitácora append-only: INICIO, CIERRE, detección de reintento
verificar.py      ejecuta una vez, compara después de producir, y evalúa E1-E12, F1-F13, N1-N18
salida.txt        salida literal de la corrida
BITACORA.txt      bitácora de esta corrida
```

Las evidencias de las dos corridas anteriores siguen intactas en
`u2-reglas-orquestador/verificador/` y `u2-reglas-orquestador/verificacion-2/`.

## Limitaciones

Son las que el contrato congelado declara, sin agregados:

- el corpus es finito;
- el verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo;
- `P-C` corrió sobre historias cortas y lineales;
- `P-B` verificó las transiciones declaradas, no una interrupción concurrente real;
- `P-E` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería;
- `P-F` demuestra que cada mutante altera el observable que su comprobación lee, no que ese
  observable sea el más adecuado para la obligación;
- la bitácora hace auditable la cantidad de invocaciones siempre que se preserve; la supresión
  deliberada no produce una corrida aprobable sino una entrega defectuosa por `F13`.
