# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59:auditorias/f2429c2be622c305d4cfd6cebcd00837ea3ed42d.md`.

## Resultado

```text
VEREDICTO=FALLO
código de retorno = 1
criterio activado = F21
```

Una única condición de fallo. Su causa está identificada abajo y no es un defecto del candidato ni
de la conducta de `X0`.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u2-reglas-orquestador\verificacion-5

comando
  python verificar.py \
    --repo-metodo C:/Franco_Metodos_AI/revolutions-orchestra-ai \
    --repo-work   C:/Franco_Metodos_AI/work-claude-i \
    --repo-audit  C:/Franco_Metodos_AI/audit-chatgpt-i
```

## X0, estrictamente antes de INICIO

Las cinco identidades congeladas resolvieron:

```text
CANDIDATE_WORK_SHA        f2429c2be622c305d4cfd6cebcd00837ea3ed42d   work    resuelve=True
CANDIDATE_BLOB_SHA        b871240fd38d28430fc86fc4b14f1b851dad1f10   work    resuelve=True
TRANSPORT_AUTHORITY_SHA   e05b24cc501ce839ffabee6d9666d069e056255c   metodo  resuelve=True
P_C_WORK_SHA              f2429c2be622c305d4cfd6cebcd00837ea3ed42d   work    resuelve=True
P_C_AUDIT_SHA             063cb3ac7edaa9a1457708a17be1789a862f6bd9   audit   resuelve=True
```

Antes de invocar la corrida se comprobó, con operaciones Git ajenas al mecanismo, que las cinco
resolvieran. `P_C_AUDIT_SHA` no resolvía: era la misma condición que mató la corrida anterior, y
esta vez apareció antes de tocar nada. Se sincronizó el clon de `audit-chatgpt-i` y recién
entonces se invocó. Esa es la obligación de preparación que el contrato pone en quien ejecuta, y
`X0` es lo que la vuelve comprobable.

## El fallo, y de quién es

`F21` se activó por la evaluación de `E19`, no por la conducta de `X0`.

La traza externa interceptada de `X0` es:

```text
git -C <work>    cat-file -e f2429c2be622c305d4cfd6cebcd00837ea3ed42d^{object}   sonda
git -C <work>    cat-file -e b871240fd38d28430fc86fc4b14f1b851dad1f10^{object}   sonda
git -C <metodo>  cat-file -e e05b24cc501ce839ffabee6d9666d069e056255c^{object}   sonda
git -C <work>    cat-file -e f2429c2be622c305d4cfd6cebcd00837ea3ed42d^{object}   sonda
git -C <audit>   cat-file -e 063cb3ac7edaa9a1457708a17be1789a862f6bd9^{object}   sonda

aperturas de archivo: 0
invocaciones que no son sonda: 0
```

Cinco sondas, una por identidad congelada, ninguna otra invocación externa, ningún archivo
abierto. Ninguna sonda devuelve contenido: `cat-file -e` informa por código de retorno.

El defecto está en cómo mi comprobación contó. `CANDIDATE_WORK_SHA` y `P_C_WORK_SHA` son dos
identidades congeladas distintas **con el mismo valor en el mismo repositorio**. Mi comprobación
comparó las cinco sondas contra un conjunto de pares `(repositorio, sha)`, que deduplica y queda
en cuatro:

```text
sondas=5  identidades=4  ->  E19=False
```

El contrato dice «exactamente una sonda de resolubilidad por identidad congelada». Las identidades
son cinco. Contarlas por valor en lugar de por identidad convirtió una conducta correcta en un
fallo.

Es un defecto del mecanismo de comprobación, del mismo linaje que los que ya costaron dos rondas:
la comprobación calificó algo distinto de lo que el criterio nombra.

No se corrigió ni se reintentó. La ejecución fue observada, se resolvió como `FALLO` y el contrato
queda agotado.

## Lo que sí quedó demostrado

El fallo ocurrió en la evaluación de `E19`, que es lo primero que el cuerpo evalúa. Todo lo demás
se ejecutó igual y quedó preservado en `salida.txt`:

```text
E18  las cinco identidades congeladas resolvieron, identidad por identidad          SI
E20  ninguna llamada interna de X0 alcanza modulos de la corrida                    SI
E21  prevuelo importa solo sondas; sondas importa solo subprocess                   SI
E9   blob leido = b871240fd38d28430fc86fc4b14f1b851dad1f10 = congelado              SI
E4   ninguna seccion mecanica sin obligacion                                        SI
E5   ninguna seccion mecanica viola su forma declarada                              SI
E1   84 casos, 84 con el resultado que su obligacion predice, 0 discrepantes        SI
E2   13 identificadores emitidos, ninguno ajeno al candidato                        SI
E3   83 obligaciones del candidato, 83 ejercitadas                                  SI
E6   toda comprobacion estructural falla sobre su mutante                           SI
E7   el observable difiere entre real y mutante en las 36 comprobaciones            SI
E8   P-C: N_CONSTRUCTOR = 20, N_AUDITOR = 25, coincidentes                          SI
E12  un INICIO y un CIERRE de la identidad congelada                                SI
E16  las dos lineas ajenas quedaron byte a byte                                     SI
E19  la evaluacion conto identidades por valor y no por identidad                   NO
```

`E16` se ejercitó por primera vez sobre historia real: la bitácora ya contenía el `INICIO` y el
`CIERRE` del contrato anterior, y quedaron intactos.

## Sobre la lectura de E20

`E20` dice «toda llamada pertenece al módulo del pre-vuelo o a su ayudante de sondeo: ninguna
pertenece a los módulos de la corrida ni a su cuerpo».

La traza interna registra necesariamente frames de la biblioteca estándar, porque toda sonda Git
pasa por `subprocess`:

```text
modulos llamados: __main__, abc, collections.abc, contextlib, instrumentacion, os,
                  prevuelo, sondas, subprocess
llamadas a modulos de la corrida: ninguna
```

Leída al pie de la letra, la primera cláusula no la satisface ninguna implementación capaz de
sondear, y el criterio sería imposible por construcción. Se aplicó la cláusula operativa —la que
nombra el conjunto cerrado de módulos de la corrida—, que sí es mecánica y sí discrimina.

Se declara porque es una imprecisión de mi propia redacción del contrato, y la lectura correcta
corresponde al AUDITOR. `F22`, que es el criterio de fallo, no tiene esa ambigüedad y no ocurrió.

## Controles sobre el propio mecanismo

Los trece se ejecutaron y discriminaron:

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
N21  identidad sintética irresoluble                  -> NO_EJECUTABLE detectado
N22  X0 sintético que lee el candidato                -> F21 detectado, traza externa difiere
N23  X0 sintético que ejecuta en memoria un caso      -> F22 detectado, traza interna difiere,
                                                         sin interacción externa adicional
N24  pre-vuelo sintético que importa la corrida       -> F23 detectado
```

`N23` es el que cerraba el punto ciego de `D-11`: ejercitó un `X0` que no abre archivos ni invoca
procesos adicionales y que sin embargo ejecuta un caso del corpus en memoria. Su traza interna lo
delató y difirió de la del `X0` real. `N1`-`N11` están presentes en el corpus y ninguno fue
aceptado.

## Bitácora de la unidad

```text
INICIO audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240fd38d28430fc86fc4b14f1b851dad1f10
CIERRE audit-chatgpt-i@e9d0e9f7f52661b3271ea6cb1840015c944d2933 b871240fd38d28430fc86fc4b14f1b851dad1f10
INICIO audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59 b871240fd38d28430fc86fc4b14f1b851dad1f10
CIERRE audit-chatgpt-i@32c65a5d82b4f274ecd2fd82aefd30602da80c59 b871240fd38d28430fc86fc4b14f1b851dad1f10
```

Un `INICIO` y un `CIERRE` de la identidad congelada; las dos líneas del contrato anterior
intactas. `verificacion-3/BITACORA.txt` no fue leída ni modificada.

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
sinteticos.py      insumos sintéticos de N12-N24
bitacora.py        bitácora append-only de la unidad, calificada por identidad
verificar.py       X0, correr() único con la guardia X4, E1-E21, F1-F23, N1-N24
salida.txt         salida literal de la corrida
```

La fuente completa del pre-vuelo se preserva para inspeccionar el residuo declarado: la traza
interna observa llamadas, no código en línea. `prevuelo.py` no contiene lógica de casos copiada.

Las evidencias de las cuatro corridas anteriores siguen intactas en `verificador/`,
`verificacion-2/`, `verificacion-3/` y `verificacion-4/`.

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
