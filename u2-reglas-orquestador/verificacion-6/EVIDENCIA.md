# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@e7894d2d65b0d35cadd04987420a15522a5ce93d:auditorias/f20c8bc8cbcb140a8aefc08f9dde02b56a26225c.md`.

## Resultado

```text
VEREDICTO=EXITO
código de retorno = 0
```

Ninguna condición de fallo se activó.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificacion-6

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

## Preparación del entorno, antes de invocar

Se sincronizaron los clones de `audit-chatgpt-i` y `revolutions-orchestra-ai` y se comprobó, con
operaciones Git ajenas al mecanismo, que las cinco vinculaciones congeladas resolvieran y que el
blob de la bitácora fuera el congelado `671123ea384675aa8e64ff79d8fdc8832ac00e28`. Recién
entonces se invocó.

Esa es la obligación de preparación que el contrato pone en quien ejecuta; `X0` es lo que la
vuelve comprobable.

## X0, estrictamente antes de INICIO

Las cinco vinculaciones nominales resolvieron:

```text
CANDIDATE_WORK_SHA        f20c8bc8cbcb140a8aefc08f9dde02b56a26225c   work    resuelve=True
CANDIDATE_BLOB_SHA        b871240fd38d28430fc86fc4b14f1b851dad1f10   work    resuelve=True
TRANSPORT_AUTHORITY_SHA   e05b24cc501ce839ffabee6d9666d069e056255c   metodo  resuelve=True
P_C_WORK_SHA              f20c8bc8cbcb140a8aefc08f9dde02b56a26225c   work    resuelve=True
P_C_AUDIT_SHA             5d7aa9c4a739b7fd908c894329739fe81c7cb61b   audit   resuelve=True
```

## E19 — cobertura nominal, con el mapeo preservado

```text
#1  git -C <work>    cat-file -e f20c8bc8...^{object}   satisface: CANDIDATE_WORK_SHA, P_C_WORK_SHA
#2  git -C <work>    cat-file -e b871240f...^{object}   satisface: CANDIDATE_BLOB_SHA
#3  git -C <metodo>  cat-file -e e05b24cc...^{object}   satisface: TRANSPORT_AUTHORITY_SHA
#4  git -C <work>    cat-file -e f20c8bc8...^{object}   satisface: CANDIDATE_WORK_SHA, P_C_WORK_SHA
#5  git -C <audit>   cat-file -e 5d7aa9c4...^{object}   satisface: P_C_AUDIT_SHA

vinculaciones nominales declaradas   5
cubiertas                            5
sin cubrir                           ninguna
invocaciones que no son sonda        0
aperturas de archivo                 0
E19                                  True
```

El mapeo declara qué vinculaciones satisface cada resolución. Las resoluciones `#1` y `#4` tienen
el mismo valor porque `CANDIDATE_WORK_SHA` y `P_C_WORK_SHA` apuntan al mismo objeto: cada una
satisface ambas vinculaciones, y la cobertura nominal es cinco de cinco.

Esa es la corrección de `D-12`. La evaluación anterior comparaba contra un conjunto de pares
`repositorio + SHA`, que colapsaba esas dos vinculaciones a una y activaba `F21` contra una
conducta correcta.

## Regla de medición, ejercitada

`cobertura_por_valor` se conserva en el mecanismo únicamente como contra-insumo de `N25`: es la
medición defectuosa, y existe para demostrar que la nominal discrimina. No se usa para evaluar la
corrida.

```text
N25  dos vinculaciones nominales distintas con el mismo repositorio y SHA
     medición nominal   2 cubiertas de 2 declaradas
     medición por valor 1
     discrimina         True
```

## Resultado contra el criterio congelado

```text
E1   84 casos, todos con el resultado que su obligación predice            SI
E2   13 identificadores emitidos, ninguno ajeno al candidato               SI
E3   83 obligaciones del candidato, 83 ejercitadas                         SI
E4   ninguna sección mecánica sin obligación                               SI
E5   ninguna sección mecánica viola su forma declarada                     SI
E6   toda comprobación estructural falla sobre su mutante                  SI
E7   el observable difiere entre real y mutante en las 36 comprobaciones   SI
E8   P-C: N_CONSTRUCTOR = 22, N_AUDITOR = 27, coincidentes                 SI
E9   el blob leído es exactamente el congelado                             SI
E10  INICIO y CIERRE preservados                                           SI
E11  no existía INICIO de esta identidad al abrir                          SI
E12  un INICIO y un CIERRE de la identidad congelada; 4 líneas ajenas      SI
E13  N17 y N18 atraviesan la misma correr() que la invocación real         SI
E14  N18 devuelve reintento sin anotar ni evaluar                          SI
E15  N17 resuelve su falla como F11 y deja INICIO y CIERRE                 SI
E16  las cuatro líneas ajenas quedaron byte a byte                         SI
E17  la ruta de la bitácora es la constante de unidad                      SI
E18  las cinco vinculaciones resolvieron, una por una                      SI
E19  cobertura nominal completa, con el mapeo preservado                   SI
E20  ninguna llamada interna de X0 alcanza módulos de la corrida           SI
E21  prevuelo importa sólo sondas; sondas importa sólo subprocess          SI

F1 a F23   ninguno ocurrió
```

## Controles

`N1`-`N11` están presentes en el corpus y ninguno fue aceptado. Los catorce controles sobre el
propio mecanismo discriminaron:

```text
N12  obligación sintética sin caso                    -> F3 detectado
N13  sección sintética sin obligación                 -> F5 detectado
N14  contenido sintético fuera de forma               -> F6 detectado
N15  blob sintético ajeno                             -> F10 detectado
N16  mutante sintético inerte                         -> F8 detectado
N17  aborto capturado atravesando correr()            -> T2, F11, INICIO y CIERRE
N18  reintento atravesando la misma correr()          -> reintento, sin anotar ni evaluar
N19  historia ajena alterada                          -> F18 detectado
N20  ruta derivada del propio directorio              -> F19 detectado
N21  vinculación sintética irresoluble                -> NO_EJECUTABLE detectado
N22  X0 sintético que lee el candidato                -> F21 detectado, traza externa difiere
N23  X0 sintético que ejecuta en memoria              -> F22 detectado en ('corpus','sobre'),
                                                         traza interna difiere, sin interacción
                                                         externa adicional
N24  pre-vuelo sintético que importa la corrida       -> F23 detectado
N25  dos vinculaciones con el mismo repo y SHA        -> nominal 2, por valor 1, discrimina
```

## Trazas de X0

```text
externa   5 procesos, todos sondas de resolubilidad, 0 aperturas de archivo
interna   módulos llamados: __main__, abc, collections.abc, contextlib, instrumentacion,
          os, prevuelo, sondas, subprocess
          llamadas a módulos de la corrida: ninguna
imports   prevuelo -> sondas ; sondas -> subprocess ; cruce con la corrida: ninguno
```

`E20` se evalúa bajo la interpretación durable congelada: la frontera es el conjunto cerrado de
módulos de corrida. Los frames de la biblioteca estándar aparecen porque toda sonda Git pasa por
`subprocess`.

## Bitácora de la unidad

```text
INICIO audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240f...
CIERRE audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240f...
INICIO audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59 b871240f...
CIERRE audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59 b871240f...
INICIO audit-chatgpt-i@e7894d2d65b0d35cadd04987420a15522a5ce93d b871240f...
CIERRE audit-chatgpt-i@e7894d2d65b0d35cadd04987420a15522a5ce93d b871240f...
```

Un `INICIO` y un `CIERRE` de la identidad congelada; las cuatro líneas de los dos contratos
agotados intactas.

## Archivos del mecanismo

```text
prevuelo.py        X0: resolubilidad y nada más; importa sólo su ayudante de sondeo
sondas.py          la sonda: cat-file -e, resuelve sin devolver contenido
instrumentacion.py intercepción externa (procesos, archivos) e interna (llamadas)
candidato.py       lee el candidato del commit congelado y extrae su superficie normativa
autoridad.py       campos, tipos y formas admitidas desde la autoridad congelada
orquestador.py     implementa las obligaciones del candidato
estructurales.py   36 comprobaciones estructurales, su observable y su mutante
corpus.py          84 casos con su obligación y su resultado normativo esperado
sinteticos.py      insumos sintéticos de N12-N25
bitacora.py        bitácora append-only de la unidad, calificada por identidad
verificar.py       X0, cobertura nominal, correr() con la guardia X4, E1-E21, F1-F23, N1-N25
salida.txt         salida literal de la corrida
```

`prevuelo.py` no contiene lógica de casos copiada. Las evidencias de las cinco corridas
anteriores siguen intactas en `verificador/`, `verificacion-2/` a `verificacion-5/`.

## Limitaciones

Las que el contrato congelado declara, sin agregados:

- el corpus es finito;
- el verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo;
- `P-C` corre sobre historias cortas y lineales;
- `P-B` verifica las transiciones declaradas, no una interrupción concurrente real;
- `P-E` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería;
- `P-F` demuestra que cada mutante altera el observable que su comprobación lee;
- `P-G` observa interacciones externas, llamadas internas e importaciones; no observa lógica de
  la corrida copiada en línea dentro del pre-vuelo;
- la bitácora hace auditable la cantidad de invocaciones siempre que se preserve.
