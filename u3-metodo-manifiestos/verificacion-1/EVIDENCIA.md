# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en
`audit-chatgpt-i@af2f37e9dba513523222c79a910ec049030deff6:auditorias/25a6e890351a5f402867dd6343bf80c041dd8cfc.md`.

## Resultado

```text
VEREDICTO=FALLO
código de retorno = 1
criterios activados = F1 (S01, S06, S13), F7 (S06), F8 (S06)
```

Los tres hallazgos son defectos de mis comprobaciones. Ninguno es un defecto del candidato. El
detalle y su atribución están abajo.

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u3-metodo-manifiestos\verificacion-1

comando
  python verificar.py --repo-work C:/Franco_Metodos_AI/work-claude-i
```

## Nota de transporte

El prompt de congelamiento citó `CANDIDATE_PATH=u3-metodo-manifiestos/METODO-MANIFIESTAS.md`. Ese
path no existe. El blob congelado `f44f2a0797cde6f569cca6fe5397d45917680258` resuelve en Git en
`u3-metodo-manifiestos/METODO-MANIFIESTOS.md`, comprobado con `git ls-tree -r` sobre
`25a6e890351a5f402867dd6343bf80c041dd8cfc`. La corrida usó ese path. Se declara porque la
identidad la fija el blob, no la cita, y el AUDITOR debe poder ver la discrepancia.

## X0, estrictamente antes de INICIO

```text
V1  local   25a6e890351a5f402867dd6343bf80c041dd8cfc          resuelve=True
V2  local   f44f2a0797cde6f569cca6fe5397d45917680258          resuelve=True
V3  local   636a5d095574130b56c232da7958691f87234516          resuelve=True
V4  local   5bd6b0f582c7970a7b8c6c838b9971a70df43dfc          resuelve=True
V5  remota  ('origin', 'refs/heads/main')                     resuelve=True

irresolubles: ninguna
forma del resultado: sólo booleanos = True
```

Antes de invocar se sincronizaron los clones y se comprobó, con operaciones ajenas al mecanismo,
que las cinco vinculaciones resolvieran.

### Cobertura nominal de la traza externa

```text
#1  cat-file -e 25a6e890...   satisface: V1
#2  cat-file -e f44f2a07...   satisface: V2
#3  cat-file -e 636a5d09...   satisface: V3
#4  cat-file -e 5bd6b0f5...   satisface: V4
#5  ls-remote --exit-code origin refs/heads/main   satisface: V5

declaradas 5  cubiertas 5  sin cubrir ninguna  invocaciones que no son sonda 0  archivos 0
```

### Frontera de red

```text
R1  en X0, 1 interaccion: ls-remote --exit-code origin refs/heads/main
    devuelve solo si existe; el resultado de X0 para V5 es un booleano
R2  en el cuerpo, P-C1: origin refs/heads/main -> 25a6e890351a5f402867dd6343bf80c041dd8cfc
```

Dos interacciones, cada una en su fase, ambas contra el repositorio y remoto declarados.

### Traza interna e imports

```text
llamadas a modulos de la corrida: ninguna
prevuelo importa ['sondas']   sondas importa ['subprocess']   cruce con la corrida: ninguno
```

## P-C2, sobre los cortes congelados

```text
paths modificados 636a5d09..5bd6b0f5
  u3-metodo-manifiestos/EVENTO.md
  u3-metodo-manifiestos/METODO-MANIFIESTOS.md

superficie disjunta   interseccion vacia       procede=True   ruteo=False
superficie solapada   interseccion 2 paths     procede=False  ruteo=True
```

## Los tres hallazgos, y de quién son

Los tres comparten una raíz: **la comprobación leyó un alcance más ancho que la propiedad que
verificaba.**

### S01 — R-1-cadena: el alcance de la búsqueda

```text
posiciones = [1273, 1080, 1378, 1413, 1448]
```

La comprobación busca los cinco eslabones de la cadena en el documento completo y exige que
aparezcan en orden. `manifiestos-trabajo-ai` aparece en la posición 1080, en el preámbulo —«la
identidad de publicación son autoridad de `manifiestos-trabajo-ai : README.md`»—, antes de la
obligación `R-1-cadena`, que empieza en 1273.

Dentro de la obligación el orden es correcto: `1273 → 1378 → 1413 → 1448`. Lo que falló es que la
comprobación buscó en todo el documento en lugar de en el enunciado de la obligación que dice
verificar.

### S06 — R-1-referencias: el mutante removió otra ocurrencia

```text
real=True  mutante=True  difiere=False
```

El mutante quita la primera ocurrencia de `manifiestos-trabajo-ai : README.md`. Esa primera
ocurrencia es la del preámbulo, no la de `R-1-referencias`, que queda intacta. La comprobación
sigue encontrando la cadena y el observable no cambia.

`E7` lo detectó exactamente para lo que fue creado: un mutante que no altera el observable que su
comprobación lee no demuestra nada. El defecto es del mutante, y su origen es el mismo que el de
`S01` —trabajar sobre el documento entero cuando la propiedad vive en una obligación.

### S13 — R-6-sin-registro: nombrar una prohibición no es implementarla

```text
hallados = ['lista_de_carriles']
```

La comprobación busca `EVENT.md`, `lista_de_carriles` o `registro_central` en la fuente de
`metodo.py`. Los encuentra porque `PROJECT_PROHIBIDO` **enumera esas claves para rechazarlas**: la
prohibición nombra lo prohibido.

La comprobación confundió mencionar con usar. El mecanismo no mantiene ningún registro central;
declara cuáles no puede haber, que es lo que la obligación exige.

## Resto del criterio congelado

El fallo ocurrió en tres casos estructurales. Todo lo demás se ejecutó y quedó preservado:

```text
casos ejecutados      58     con el resultado que su obligacion predice  55
E2   identificadores emitidos, ninguno ajeno al candidato                SI
E3   56 obligaciones del candidato, 56 ejercitadas                       SI
E5   ninguna seccion mecanica viola su forma declarada                   SI
E11  blob leido = f44f2a07... = congelado                                SI
E12  un INICIO y un CIERRE de la identidad congelada                     SI
E13  no existia INICIO previo de esta identidad                          SI
E14  la bitacora no tenia lineas ajenas y no se altero ninguna           SI
E16  las cinco vinculaciones resolvieron, con su forma booleana          SI
E17  cobertura nominal 5 de 5, sin no-sondas y sin archivos              SI
E18  ninguna llamada interna de X0 alcanza la corrida                    SI
E19  el pre-vuelo no importa modulos de la corrida                       SI
E23  dos interacciones de red, R1 en X0 y R2 en el cuerpo                SI
E24  el resultado de X0 para V5 es booleano                              SI
E1   3 casos difirieron                                                  NO
E6   S06 no fallo sobre su mutante                                       NO
E7   el observable de S06 no difirio                                     NO
```

## Controles

`N1` a `N10` sobre la materia del candidato están presentes en el corpus y ninguno fue aceptado.
Los diecisiete sobre el propio mecanismo discriminaron:

```text
N9   historia sintetica con merge: derivacion efectiva = 5, primer padre = 3, difieren
     el log de esa historia esta en N9_HISTORIA.txt
N11  obligacion sintetica sin caso              -> F3 detectado
N12  seccion sintetica sin obligacion           -> F5 detectado
N13  contenido sintetico fuera de forma         -> F6 detectado
N14  blob sintetico ajeno                       -> F12 detectado
N15  mutante sintetico inerte                   -> F8 detectado
N16  aborto capturado atravesando correr()      -> T2, F13, INICIO y CIERRE
N17  reintento atravesando la misma correr()    -> reintento, sin anotar ni evaluar
N18  historia ajena alterada                    -> F15 detectado
N19  vinculacion sintetica irresoluble          -> NO_EJECUTABLE detectado
N20  X0 sintetico que lee el candidato          -> F18 detectado, traza externa difiere
N21  X0 sintetico que ejecuta en memoria        -> F19 detectado, traza interna difiere
N22  pre-vuelo sintetico que importa la corrida -> F20 detectado
N23  dos vinculaciones con el mismo valor       -> nominal 2, por valor 1, discrimina
N24  ruta derivada del propio directorio        -> F22 detectado
N25  interaccion de red adicional fuera de fase -> F24 detectado
N26  conjunto distinto de V1-V5                 -> F25 detectado
N27  X0 que transporta el valor de la referencia-> F26 detectado
```

`N9` es la primera vez que la derivación de cadencia se ejercita donde la diferencia importa: la
función efectiva —la misma que implementa `R-5-derivacion`— cuenta 5 sobre una historia con merge,
y un recorrido por primer padre cuenta 3.

## Bitácora de la unidad

```text
INICIO audit-chatgpt-i@af2f37e9dba513523222c79a910ec049030deff6 f44f2a07...
CIERRE audit-chatgpt-i@af2f37e9dba513523222c79a910ec049030deff6 f44f2a07...
```

Primera corrida de esta unidad: un `INICIO`, un `CIERRE`, sin líneas ajenas.
`u2-reglas-orquestador/BITACORA.txt` no fue leída ni modificada.

## Trabajo previo a INICIO, declarado

Una prueba de humo que importó los módulos, ejercitó los insumos sintéticos y comprobó que la
bitácora de la unidad no existía. No leyó el candidato, no ejecutó ningún caso del corpus y no
ejercitó ninguna comprobación estructural sobre el sujeto real.

## Archivos del mecanismo

```text
prevuelo.py        X0: resolubilidad de V1-V5, resultado booleano
sondas.py          sonda local (cat-file -e) y sonda remota (ls-remote --exit-code)
instrumentacion.py intercepcion externa e interna
candidato.py       lee el candidato del commit congelado y extrae su superficie normativa
metodo.py          implementa las obligaciones del candidato; unica funcion de derivacion
casos.py           36 casos de llamada con sus entradas explicitas
estructurales.py   22 comprobaciones estructurales, su observable y su mutante
sinteticos.py      insumos sinteticos de los controles
bitacora.py        bitacora append-only de la unidad
verificar.py       X0, correr() con la guardia X4, criterios y controles
salida.txt         salida literal de la corrida
N9_HISTORIA.txt    log y conteos de la historia sintetica con merge
```

## Limitaciones

Las que el contrato congelado declara, sin agregados:

- el corpus es finito;
- el constituyente es evidencia local y no la implementación de referencia de un agente de
  constitución;
- `P-A` y `P-B` ejercitan recorridos definidos dentro de la unidad, no una conversación real;
- `P-D` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería;
- `P-E` demuestra que cada mutante altera el observable que su comprobación lee;
- `P-F` observa interacciones externas, llamadas internas e importaciones;
- `P-C2` congela el corte destino para que la corrida sea determinista; `P-C1` es lo que demuestra
  que la vigencia se obtiene del remoto;
- la bitácora hace auditable la cantidad de invocaciones siempre que se preserve.
