# Evidencia — corrida única bajo el contrato congelado

Contrato congelado en `audit-chatgpt-i@856a0782cba7b331ee4f2178b7235553b1787c90`.
Candidato `u3-metodo-manifiestos/METODO-MANIFIESTOS.md`, blob
`f44f2a0797cde6f569cca6fe5397d45917680258`, leído del corte
`05041ddf0e7a687cc8ed1982a3d824570fe57710`.

## Resultado

```text
VEREDICTO=EXITO
terminacion = T1
codigo de retorno = 0
criterios de fallo activados = ninguno
controles que no discriminan = ninguno
E1 a E31 = SI
```

## Comando ejecutado

```text
directorio de trabajo
  C:\Franco_Metodos_AI\work-claude-i\u3-metodo-manifiestos\verificacion-2

comando
  python verificar.py --repo-work C:/Franco_Metodos_AI/work-claude-i
```

La salida literal está en `salida.txt`. Toda la evidencia estructurada, incluida cada travesía
observada, está en `evidencia.json`.

## X0, estrictamente antes de INICIO

```text
V1  local   05041ddf0e7a687cc8ed1982a3d824570fe57710   resuelve=True
V2  local   f44f2a0797cde6f569cca6fe5397d45917680258   resuelve=True
V3  local   636a5d095574130b56c232da7958691f87234516   resuelve=True
V4  local   5bd6b0f582c7970a7b8c6c838b9971a70df43dfc   resuelve=True
V5  remota  origin, refs/heads/main                    resuelve=True

estado EJECUTABLE   irresolubles ninguna
forma del resultado ['bool']  -- ningun campo donde un valor de referencia pueda viajar
```

### Cobertura nominal de la traza externa

Se mide sobre las cinco vinculaciones que el contrato declara, no sobre un conjunto derivado de
sus valores.

```text
cat-file -e 05041ddf...^{object}                satisface ['V1']
cat-file -e f44f2a07...^{object}                satisface ['V2']
cat-file -e 636a5d09...^{object}                satisface ['V3']
cat-file -e 5bd6b0f5...^{object}                satisface ['V4']
ls-remote --exit-code origin refs/heads/main    satisface ['V5']

declaradas 5   cubiertas 5   invocaciones que no son sonda 0   aperturas de archivo 0
ninguna sonda devolvio contenido
```

### Trazas del pre-vuelo

```text
traza interna, modulos entrados   contextlib, observador, prevuelo, sondas, subprocess
cruce con los modulos de la corrida   ninguno
importados al importar el pre-vuelo   prevuelo, sondas
imports declarados   prevuelo -> ['sondas']   sondas -> ['subprocess']
```

`observador` es el instrumento que observa la corrida, no parte de ella. `constantes` sólo
transporta literales. Los módulos de la corrida son `superficie`, `constituyente`, `corpus`,
`comprobaciones`, `registro`, `controles`, `corrida`, `bitacora` y `evaluadores`.

## La frontera de red

```text
R1  fase X0      ls-remote --exit-code origin refs/heads/main   -> booleano
R2  fase cuerpo  ls-remote origin refs/heads/main               -> valor vigente

interacciones remotas totales 2, cada una en su fase, ambas contra origin
```

## P-C

```text
P-C1  origin refs/heads/main -> 05041ddf0e7a687cc8ed1982a3d824570fe57710
      obtenida del remoto declarado, no de un clon local

P-C2  paths entre los cortes congelados
        u3-metodo-manifiestos/EVENTO.md
        u3-metodo-manifiestos/METODO-MANIFIESTOS.md

      superficie disjunta   u1-contratos-transversales/   interseccion 0   procede=True
      superficie solapada   u3-metodo-manifiestos/        interseccion 2   procede=False  rutea
```

## Cobertura del candidato

```text
obligaciones etiquetadas del candidato   56
obligaciones ejercitadas                 56
secciones numeradas                      10   no mecanicas declaradas por el documento  9 y 10
secciones mecanicas fuera de forma       0
casos de llamada                         36   con el resultado que su obligacion predice  36
comprobaciones estructurales             22   todas con superficie material declarada
```

Las secciones `9` y `10` presentan contenido entre el bloque y el primer `Nota.`, y `10` también
entre el encabezado y el bloque. Ambas están declaradas no mecánicas por el propio documento, y
`E5` sólo alcanza a las mecánicas.

## D-20, D-21 y D-22: la regla de alcance, observada

Cada comprobación declara la superficie material que lee. Las de documento leen la línea
etiquetada de una obligación con sus continuaciones; las de conducta leen una conducta nombrada.

Para cada comprobación de documento se construyeron dos variantes que alteran el documento **fuera
de esa superficie** y se comparó su observable con el del sujeto real:

```text
sin-ocurrencias-fuera   borra toda ocurrencia de los fragmentos que caiga fuera de la superficie
con-ruido-antes         inserta esos fragmentos, desordenados, antes de la superficie
```

```text
S01  documento:R-1-cadena         observable identico en las dos variantes
S02  documento:R-1-no-sustituye   observable identico en las dos variantes
S03  documento:R-1-no-amplia      observable identico en las dos variantes
S06  documento:R-1-referencias    observable identico en las dos variantes
S18  documento:R-8-no-reemplaza   observable identico en las dos variantes
```

Ésas son exactamente las dos operaciones que hicieron fallar a la corrida anterior: `S01` leía
posiciones sobre el documento entero y una ocurrencia del preámbulo alteraba el orden; el mutante
de `S06` quitaba la primera ocurrencia global, que estaba en el preámbulo. Con la superficie
acotada, ninguna de las dos cambia el observable.

`D-22` se cierra por conducta. `S13` no busca `EVENT.md`, `lista_de_carriles` ni
`registro_central` en la fuente: invoca el descubrimiento dos veces con las mismas entradas y
observa si quedó estado del otro lado —globales mutables y celdas de clausura— y si abrió algún
archivo.

```text
N31  sujeto que solo nombra las claves prohibidas para rechazarlas   pasa
     sujeto que efectivamente mantiene ese estado                    falla
     misma comprobacion en ambos: ('comprobaciones.py', 'c_S13', 167)
```

## D-23: la atadura entre control y conducta efectiva, observada

Toda invocación de una comprobación —la que califica al candidato y la de cualquier control— pasa
por el mismo despachador, que observa con `sys.settrace` en qué bloque de código entró. Esa
entrada, y no la etiqueta, es la identidad que queda registrada.

```text
registros de travesia   59   calificacion 55   control 4
fallos de atadura       ninguno
```

Los cuatro controles que ejercen una comprobación atraviesan la misma que calificó al candidato:

```text
N28  S01  R-1-cadena        sujeto cadena-alterada-fuera   ('comprobaciones.py','c_S01',79)  ok=True
N29  S01  R-1-cadena        sujeto cadena-alterada-dentro  ('comprobaciones.py','c_S01',79)  ok=False
N31  S13  R-6-sin-registro  sujeto solo-nombra             ('comprobaciones.py','c_S13',167) ok=True
N31  S13  R-6-sin-registro  sujeto mantiene-estado         ('comprobaciones.py','c_S13',167) ok=False
```

`N28` y `N29` sólo juntos demuestran que `S01` lee su superficie:

```text
observable real                    [25, 56, 130, 165, 200]
alterada FUERA de la obligacion    [25, 56, 130, 165, 200]   identico
alterada DENTRO de la obligacion   [-1, 40, 114, 149, 184]   distinto
```

`N32` y `N33` demuestran que el criterio sabe fallar, con registros sintéticos:

```text
N32  calificacion S01 -> c_S01 ; control S01-localizada -> c_S01_localizada, alcanzable solo
     desde el control                                        -> F31 y F32, identidades distintas
N33  control que declara S01 y atraviesa c_S02               -> F31, F32, F33
     control que declara S01 y atraviesa c_S01               -> ningun fallo
```

La misma atadura vale fuera de las comprobaciones:

```text
E20  la derivacion que ejercita N9 y la del camino real son la misma funcion
     ('constituyente.py', 'derivar_cadencia', 181)
E15  N16 y N17 atraviesan la misma funcion de corrida que la invocacion real
     ('corrida.py', 'correr', 20)
```

Este contrato no nombra ninguna equivalencia y ninguna se invocó: los cuatro controles ejercen la
comprobación misma sobre un sujeto sintético.

## Discriminación de los mutantes

Cada comprobación se ejerció sobre su sujeto real y sobre su mutante. Las 22 fallaron sobre el
mutante, en las 22 el observable difirió, y en las 22 el mutante alteró la superficie que esa
comprobación lee —no algo fuera de ella.

## Los 33 controles

```text
N1   paquete sin campo aplicable                -> R-4-campos
N2   identidad Git abreviada                    -> R-4-identidades
N3   secreto en lugar de su referencia          -> R-4-sin-secretos
N4   trabajo aislado con PROJECT_SHA            -> R-4-project
N5   interseccion no vacia que procede          -> F11
N6   interseccion vacia que no procede          -> F11
N7   PROJECT.md con ultimo SHA / lista carriles -> R-6-prohibido en los dos
N8   politica de relevo con contador persistido -> R-5-sin-contadores
N9   historia sintetica con merge               -> efectiva 5, primer padre 3, difieren
N10  fuente auxiliar que amplia capacidad       -> R-7-no-autoriza
N11  obligacion sintetica sin caso              -> F3
N12  seccion sintetica sin obligacion           -> F5
N13  contenido sintetico fuera de forma         -> F6
N14  blob sintetico ajeno                       -> F12
N15  mutante que no altera su observable        -> F8
N16  falla inyectada en la misma correr()       -> T2, F13, INICIO y CIERRE sinteticos
N17  reintento sobre la misma correr()          -> REINTENTO, sin anotar y sin evaluar
N18  bitacora con lineas ajenas alteradas       -> F15
N19  vinculacion sintetica irresoluble          -> NO_EJECUTABLE
N20  X0 sintetico que abre el candidato         -> F18, traza externa distinta
N21  X0 sintetico que entra a un modulo         -> F19, traza interna distinta
N22  pre-vuelo que importa la corrida           -> F20
N23  dos vinculaciones con el mismo valor       -> nominal 2, por valor 1
N24  ruta de bitacora derivada del mecanismo    -> F22
N25  tercera interaccion de red                 -> F24, la traza la distingue de la real
N26  conjunto distinto de V1-V5                 -> F25
N27  X0 que transporta el valor de la referencia-> F26, forma distinta de la real
N28  cadena alterada FUERA de la obligacion     -> observable identico
N29  cadena alterada DENTRO de la obligacion    -> observable distinto
N30  mutante que altera fuera de la superficie  -> F29, aunque el observable difiera
N31  solo nombra pasa, mantiene estado falla    -> misma comprobacion en ambos sujetos
N32  ruta paralela control / calificacion       -> F31 y F32
N33  identidad declarada y no atravesada        -> F33; el que si la atraviesa, ninguno
```

El log de la historia sintética de `N9` y sus dos conteos están en `N9_HISTORIA.txt`.

## La bitácora de la unidad

```text
ruta   C:\Franco_Metodos_AI\work-claude-i\u3-metodo-manifiestos\BITACORA.txt
       compuesta con la raiz del repositorio y la constante de la unidad, no con el directorio
       del mecanismo

ajena    INICIO audit-chatgpt-i@af2f37e9... f44f2a07...
ajena    CIERRE audit-chatgpt-i@af2f37e9... f44f2a07...
propia   INICIO audit-chatgpt-i@856a0782... f44f2a07...
propia   CIERRE audit-chatgpt-i@856a0782... f44f2a07...
```

Al abrir no había `INICIO` de esta identidad. Las dos líneas de la identidad anterior no se
cuentan y quedaron byte a byte. `u2-reglas-orquestador/BITACORA.txt` no fue leída ni modificada.

## Trabajo previo a INICIO, declarado

Durante la construcción del mecanismo se ejercitó el analizador de superficie contra el texto del
candidato, para desarrollarlo. Después, y antes de invocar, se corrió una prueba de humo que llamó
al cuerpo **directamente**, fuera de `corrida.correr()`: no anotó `INICIO`, no escribió ninguna
línea en la bitácora de la unidad, no emitió veredicto y no evaluó los criterios de la corrida.
Su propósito fue no quemar un contrato por un defecto mecánico. También se ejercitaron en seco los
evaluadores de `X0` con operaciones ajenas al mecanismo.

Ninguna de esas invocaciones anotó `INICIO`, y por `X2` ninguna es una ejecución observada. Se
declara porque el AUDITOR debe poder verlo, no porque el contrato lo permita implícitamente.

## Archivos del mecanismo

```text
sondas.py          sonda local (cat-file -e) y sonda remota (ls-remote --exit-code)
prevuelo.py        X0: resuelve la lista literal que recibe; no importa la corrida
constantes.py      los literales del contrato congelado
observador.py      intercepcion externa, interna y de travesia
superficie.py      lee el candidato, extrae superficies y construye variantes fuera de superficie
constituyente.py   implementa las obligaciones del candidato; unica funcion de derivacion
corpus.py          36 casos de llamada con sus entradas explicitas
comprobaciones.py  22 comprobaciones, cada una una funcion propia: su bloque de codigo es su
                   identidad
registro.py        registro de comprobaciones y unico despachador que observa la travesia
evaluadores.py     evaluadores puros de cada criterio, alimentables con insumo sintetico
controles.py       los 33 controles negativos
corrida.py         unica funcion de corrida; aqui vive la guardia X4
bitacora.py        bitacora append-only en la constante fija de la unidad
verificar.py       X0, orquestacion, criterios E1-E31 y salida
salida.txt         salida literal de la corrida
evidencia.json     evidencia estructurada completa
N9_HISTORIA.txt    log de la historia sintetica con merge y sus dos conteos
```

## Limitaciones conocidas

Las que el contrato congelado declara, sin agregados:

- el corpus es finito: demuestra que las obligaciones discriminan sobre los casos declarados, no
  que ninguna entrada imaginable las eluda;
- el constituyente es evidencia local y no la implementación de referencia de un agente de
  constitución;
- `P-A` y `P-B` ejercitan recorridos definidos dentro de la unidad, no una conversación real;
- `P-D` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería: esa suficiencia es lectura del AUDITOR;
- `P-E` demuestra que cada mutante altera el observable que su comprobación lee, no que ese
  observable sea el más adecuado para la obligación;
- `P-F` observa interacciones externas, llamadas internas e importaciones; no observa lógica de
  la corrida copiada en línea dentro del pre-vuelo;
- `P-G` observa la comprobación atravesada; demuestra que control y calificación son la misma, no
  que esa comprobación sea la mejor posible para su obligación;
- la bitácora hace auditable la cantidad de invocaciones siempre que se preserve.
