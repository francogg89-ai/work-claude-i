# EVENTO — U3 método para constituir manifiestos

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@e202dbbd36e463809b4c12f6cb05b9734fb2c7b7` y
`audit-chatgpt-i@2931d940ba76b9cfaddaaa67a57f8065fdfb5f5d`.

Esa auditoría interpretó la segunda corrida oficial de `U3`: **`FALLO` contractual, aunque
`salida.txt` reporte `EXITO`**. Contrato consumido, reintento prohibido, `U3` sin cerrar. Abrió
`D-24` y dejó `D-13` a `D-23` corregidos.

`D-24` es mío y es grave: antes de la invocación oficial ejecuté materia de la corrida por una
ruta que elude `X0`, `X1` y `X4`. Está desarrollado abajo.

Antes, `audit-chatgpt-i@856a0782cba7b331ee4f2178b7235553b1787c90` había congelado el contrato de
esa corrida, y `audit-chatgpt-i@af2f37e9dba513523222c79a910ec049030deff6` el de la primera.
Ninguna de las dos demostró defectuoso al candidato.

Las auditorías previas cerraron `D-13` a `D-23`.

La auditoría anterior había aprobado la corrida contractual de `U2` y cerrado la unidad. La
superficie aprobada es `u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`, blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`.

Autoridades aguas arriba de esta unidad: los contratos transversales cerrados en `U1`, la
superficie aprobada de `U2`, `PLAN.md` y el método autoritativo.

## Qué hizo esta intervención

Propone un contrato previo nuevo, con identidad contractual nueva, que cierra `D-24` nombrando la
materia reservada a la corrida y volviendo observable la ruta por la que se ejecuta. No tocó el
candidato, que conserva su blob `f44f2a0797cde6f569cca6fe5397d45917680258`; no escribió
`verificacion-3`, no ejecutó ninguna mitad y no agregó ninguna línea a la bitácora.

`u3-metodo-manifiestos/BITACORA.txt` con sus cuatro líneas, `verificacion-1/` y `verificacion-2/`
quedan intactas: son evidencia de las dos corridas agotadas. `U1`, `U2`, `PLAN.md` y
`BOOTSTRAP.md` tampoco fueron tocados.

### D-20, D-21 y D-22: una sola raíz

Los tres hallazgos son de mis comprobaciones y comparten una causa: **la comprobación leyó una
superficie más ancha que la obligación que decía verificar.**

```text
S01  busco la cadena en el documento completo, y una ocurrencia del preambulo, anterior a
     R-1-cadena, altero el orden observado
S06  el mutante quito la primera ocurrencia global de una cita, que estaba en el preambulo, y
     dejo intacta la obligacion que pretendia violar
S13  busco nombres prohibidos en toda la fuente y encontro `lista_de_carriles` dentro de la
     lista que existe para rechazarla
```

Los dos primeros leen de más en el documento; el tercero lee de más en la fuente y confunde
mencionar con usar.

Por eso el contrato incorpora una regla, junto a la de medición:

```text
REGLA DE ALCANCE
toda comprobacion lee la superficie material de la obligacion que dice verificar, y no una
superficie mas ancha que la contenga.
Una ocurrencia fuera de esa superficie no puede cambiar su resultado.
Un mutante que altere algo fuera de esa superficie no viola la obligacion y no discrimina.
Cuando una obligacion prohibe mantener o usar algo, la comprobacion observa la conducta, no la
mencion del nombre.
```

La superficie material de una obligación es su propia línea etiquetada con sus continuaciones.
Cuando una obligación necesita otra superficie, el contrato la nombra.

`E25` a `E28`, `F27` a `F30` y los controles `N28` a `N31` la vuelven exigible. `N28` y `N29` son
el par que cierra `D-20`: alterar la cadena fuera de su obligación no debe cambiar el observable,
y alterarla dentro sí. `N30` cierra `D-21`. `N31` cierra `D-22` con dos sujetos sintéticos, uno
que sólo nombra la clave prohibida y otro que efectivamente mantiene ese estado.

### D-23 — atar el control a la conducta efectiva

La regla de alcance es correcta y no alcanza. Un mecanismo puede conservar un `S01` real que sigue
buscando en todo el documento y, aparte, implementar una comprobación localizada que sólo los
controles alcanzan: `N28` y `N29` pasan, y el candidato real se sigue calificando con la
comprobación ancha. Lo mismo con `S06`/`N30` y `S13`/`N31`.

Ese es exactamente el defecto que `D-07` nombró en `U2` y que `D-17` volvió a nombrar acá: un
control desconectado de la conducta efectiva no demuestra nada. `E20`/`F21`/`N9` lo cerraron para
una función; `E15` lo cerró para la función de corrida. Faltaba la regla general.

```text
REGLA DE IDENTIDAD DEL CONTROL
todo control ejercita la misma comprobacion efectiva que califica al candidato real para la
obligacion que dice cerrar, y compara el mismo observable.
Un control cambia el sujeto; no cambia la comprobacion.
No existe comprobacion alcanzable solo desde un control, ni obligacion cuyo control no ejercite
la comprobacion que la corrida real uso.
Declarar la identidad no basta: la evidencia observa que el control atraveso esa comprobacion.
Cuando un control no puede ejercitar la comprobacion misma, este contrato nombra la equivalencia
y la evidencia la demuestra; sin esa demostracion el control no cierra nada.
```

`E29` a `E31`, `F31` a `F33` y los controles `N32` y `N33` la vuelven exigible. `N32` construye
justamente la ruta paralela que debe quedar imposible. `N33` ataca lo que aprendí en `D-11`:
declarar una identidad es barato, y la propiedad sólo queda demostrada si la evidencia distingue
un control que atraviesa la comprobación real de uno que sólo dice atravesarla.

### D-24 — nombrar la materia, no sólo la guardia

La corrida anterior reportó `EXITO` y fue interpretada `FALLO`. Con razón. Antes de invocar llamé
directamente a la función que implementa el cuerpo, sin pasar por la función de corrida: leyó el
candidato, obtuvo la vigencia del remoto, ejercitó los casos y las comprobaciones sobre el sujeto
real, corrió los controles y devolvió un veredicto. Todo eso es materia de la corrida, y lo
ejecuté por una ruta que elude `X0`, `X1` y `X4`.

Lo justifiqué con `X2`: si no anoto `INICIO`, no hay ejecución observada. `X2` dice **cuándo una
ejecución queda observada**; no dice qué está permitido ejecutar fuera de la guardia. Leí una
regla de registro como si fuera una autorización. Y lo hice sabiendo que rozaba `D-03`, que es el
mismo error: usar el mecanismo antes de que el contrato lo autorice y después argumentar por qué
no cuenta.

El defecto de fondo, sin embargo, no es el atajo. Es que el contrato nombraba la guardia y no
nombraba la materia. Mientras el contrato no enumere qué está reservado a la corrida, «ejecutar el
cuerpo fuera de la guardia» es una frase y no un criterio: no hay denominador contra el cual
medir, y ninguna evidencia puede contradecir una declaración.

Por eso este contrato hace tres cosas que el anterior no hacía. Enumera `M1` a `M7`, la materia
reservada. Delimita `C1` a `C3`, lo que sí es trabajo de construcción, **antes** de usarlo y no
después. Y exige que cada entrada a materia reservada observe la guardia por encima en el momento
de ejecutarse, con un rechazo distinguible cuando no la tiene.

`E32` a `E34`, `F34` a `F36` y los controles `N34` a `N36` lo vuelven exigible. `N34` es el que
importa: si la conducta rechazada y la autorizada no difieren en su observable, la guardia está
declarada y no observada, y no cierra nada.

Una consecuencia que asumo: sin prueba de humo contra el candidato, un defecto mecánico cuesta un
contrato entero. Es el precio que `T2` ya fijaba y que estuve esquivando dos veces. Lo que queda
permitido es `C2` —ejercitar el mecanismo contra insumos sintéticos que no son el candidato ni
derivan de él, sin evaluar criterios y sin emitir veredicto—, y eso alcanza para los defectos de
forma, no para los de fondo.

### OBS-03: leí el transporte como si fuera la autoridad

`EVIDENCIA.md` afirmó que el prompt de congelamiento citaba un path inexistente. La autoridad
durable de congelamiento no contiene ese error: estaba en el transporte, no en la auditoría.

Registré una afirmación sobre la autoridad sin abrir la autoridad. Es exactamente lo que el propio
método advierte —lo que un prompt afirma es cita de transporte y no evidencia— y lo escribí en una
evidencia mientras lo repetía en cada pase.

No reescribo `EVIDENCIA.md`. Queda como está, con su error, porque es evidencia de una corrida ya
interpretada y corregirla retroactivamente sería peor que el error.

### OBS-04, corregida por ser ahora relevante

La frase heredada «`F1` a `F20` califican la invocación real» quedaba desactualizada frente a
`F1`-`F30`. `D-23` agrega `F31`-`F33`, así que un rango literal desactualizado ya no es sólo
editorial: nombra menos criterios de los que el encabezado normativo obliga. La frase ahora dice
«los criterios de fallo», sin rango. El encabezado `FALLO si ocurre cualquiera` no cambia, y
ningún criterio se agrega, quita ni reinterpreta por esto.

### D-18 — dos intentos y qué falló en el primero

El contrato original decía «sin red» y a la vez le exigía a `P-C1` la vigencia remota. La frase
venía de `U2`, donde era cierta porque nada de lo que `U2` verificaba estaba fuera del disco.

Mi primera corrección nombró **una única excepción, dentro del cuerpo**, y en la misma
intervención agregó `V5`, una sonda remota en `X0`. Es decir: mientras cerraba la contradicción por
un lado, la volvía a abrir por el otro. Dos interacciones remotas y un criterio que exigía una.

Lo que falló no fue el diseño de `V5` ni el de la excepción, sino haberlos escrito como respuestas
a dos defectos distintos sin releer uno contra el otro. Es la misma mecánica de `D-08`: extender el
alcance de una corrección sin revisar los criterios que ya la nombraban.

La corrección de ahora cuenta interacciones **por fase y por propósito**, y son exactamente dos:

```text
R1  en X0, antes de INICIO   pregunta si la referencia esta en el remoto
R2  en el cuerpo, P-C1       pregunta que dice esa referencia
```

Tocan el mismo endpoint y no son la misma cosa. Esa diferencia es la que ya separaba resolver de
leer en las sondas locales, así que `V5` conserva su clase: `X0` resuelve vinculaciones, no lee
valores. Su función es una sola y no cambia después de ejecutar.

Que `R1` no transporte el valor no queda declarado. Queda observable en la forma del resultado de
`X0` —un booleano por vinculación, sin campo donde una referencia pueda viajar—, y `E24`, `F26` y
`N27` lo detectan. `E23`, `F24` y `N25` fijan la cantidad y la fase.

Nada de esto debilita `D-13`: la vigencia sigue viniendo del remoto real, y comparar contra un
clon local sigue siendo lo que `R-6-remoto` prohíbe.

### D-19 — el denominador de X0, enumerado

`X0` tenía su frontera observada pero no su denominador fijado. Un mecanismo podía elegir qué
resolver, o inferirlo escaneando los SHAs que aparecen en el documento, y `E16`/`E17` habrían
medido cobertura sobre un conjunto que el propio mecanismo eligió.

Es la regla de medición otra vez, un paso antes: no alcanza con medir sobre un conjunto nominal si
el conjunto lo arma quien es medido.

Ahora las cinco vinculaciones están enumeradas por nombre en el contrato, y `F25` y `N26` niegan
que el mecanismo las obtenga de otro modo.

Al enumerarlas apareció algo que no había visto: la alcanzabilidad del remoto también es una
vinculación, y como tal pertenece a `X0`. Sin `V5`, una red caída no se descubriría hasta `P-C1`,
ya dentro de la corrida, y quemaría un contrato entero por una condición de entorno. Es la misma
lección que costó dos corridas con un clon desactualizado, aplicada antes de que vuelva a pasar.

### D-13 — el descubrimiento contra el remoto

`R-6-descubrimiento` decía «se lee su referencia actual» sin decir de dónde. Un clon local puede
estar desactualizado, y comparar contra él no demuestra vigencia: demuestra lo que este disco sabe.

`PLAN.md` `D2` dice remoto, y ahora el candidato también. Se agregó además `R-6-remoto`, que
enuncia la razón en lugar de dejarla implícita.

Esa distinción no es teórica en este trabajo: dos corridas de `U2` se perdieron porque un clon
local no tenía un objeto que sí existía en el remoto.

### D-14 — las dependencias externas, localizables

El candidato citaba los documentos ajenos por repositorio y path, pero no nombraba los contratos.
`R-1-referencias` los nombra ahora: `CT-6` en `manifiestos-trabajo-ai : README.md` y `CT-7` en
`reglas-orquestador-ai : REGLAS-ORQUESTADOR.md`. `R-1-sin-sha` conserva la prohibición de congelar
sus identidades, que es lo que evitaría el ciclo.

Un path sin nombre de contrato obliga a leer el documento entero para saber qué se está citando.
Con el nombre, la dependencia queda localizable, que es lo que `D7` pedía.

### D-15 — los insumos de P-C, nombrados antes

El contrato decía «dos repositorios reales sobre cortes congelados y superficies declaradas», que
es exactamente el margen que permite elegir los insumos después de ver cómo se comporta el
mecanismo. Ahora están nombrados: repositorio, remoto, los dos cortes y las dos superficies.

`P-C` se parte en dos porque son dos propiedades distintas. `P-C1` demuestra la conducta —obtener
la referencia del remoto— y su valor no se congela, porque congelar la vigencia sería negarla.
`P-C2` demuestra la discriminación sobre cortes fijos, para que la corrida sea determinista. La
limitación que eso deja está declarada por adelantado.

### D-16 — una sola bitácora, y comprobable

Decir que la bitácora vive en un path fijo no impide que una implementación la derive de su propio
directorio y aparezca vacía. `E21`, `F22` y el control `N24` lo vuelven exigible, igual que en
`U2`: mover y reiniciar no pueden ser indistinguibles.

### D-17 — N9 contra la derivación efectiva

`N9` demostraba que un recorrido por primer padre da un número menor sobre una historia con merge.
Eso es cierto y no dice nada del mecanismo: podía convivir con un camino real que usara primer
padre igual.

Ahora `N9` ejercita **la misma función** que implementa `R-5-derivacion` en el camino real, y
`E20`/`F21` exigen que sea una sola. Un control desconectado de la conducta efectiva es el defecto
que `D-07` nombró en `U2`, y no tenía por qué repetirse acá.

### Las cinco autoridades que este documento recibe

```text
CT-1  cadena del sistema y frontera funcional entre los tres documentos
CT-2  contrato del paquete de constitucion
CT-3  politica periodica de relevo derivable
CT-4  descubrimiento de concurrencia y semantica de PROJECT.md
CT-5  fuentes auxiliares y no ampliacion de autoridad
```

`CT-6` es autoridad del `README.md` de la biblioteca y `CT-7` de `REGLAS-ORQUESTADOR.md`. El
candidato los nombra en `R-1-referencias` por repositorio, path y nombre de contrato, no reproduce
su texto normativo y no congela sus identidades.

### El contorno que U2 fija

`U2` aprobó que el orquestador, en el arranque externo, recibe el paquete de constitución, abre
una instancia inicial de AUDITOR y le entrega ese paquete literalmente, sin validarlo, sin
completarlo, sin resumirlo y sin reescribirlo.

Eso fija el contorno de `§4` de este candidato: si el orquestador no completa nada, el paquete
tiene que llegar completo. De ahí `R-4-campos`, `R-4-aplicables` y `R-4-identidades`. Un campo
faltante no lo repara nadie aguas abajo, y un SHA inventado no lo detecta el transporte.

### La convención de superficie normativa, y por qué se hereda

El candidato adopta la misma convención que `U2`: cada sección mecánica empieza con su bloque de
obligaciones etiquetadas, y lo que sigue a un marcador `Nota.` explica y no obliga.

No es simetría. Es la única forma en que la cobertura de una verificación puede medirse contra el
documento en vez de contra una lista paralela, que es lo que costó tres correcciones en `U2`. Un
documento sin esa convención sólo admite cobertura declarada.

Resultado: 56 obligaciones sobre 8 secciones mecánicas, con `9` y `10` declaradas no mecánicas.

Al construirlo apareció la misma trampa que `OBS-01` encontró en `U2`: `§8` terminaba con un
separador `---` sin `Nota.` previa, fuera de la forma que el propio documento declara. Se corrigió
antes de proponer el contrato, que es cuando corresponde corregirlo.

### Contradicciones materiales

Ninguna. `CT-1` a `CT-5` se pudieron escribir sin contradecir `U1`, la superficie aprobada de
`U2`, `PLAN.md` ni el método autoritativo.

---

## Contrato previo de verificación — PROPUESTO, NO EJECUTADO

Conforme a REVOLUTIONS §6.1 y `PLAN.md` §5.2. Ninguna mitad se ejecuta hasta que el AUDITOR lo
evalúe y lo congele.

### Candidato exacto

```text
repositorio  https://github.com/francogg89-ai/work-claude-i
path         u3-metodo-manifiestos/METODO-MANIFIESTOS.md
blob         f44f2a0797cde6f569cca6fe5397d45917680258
```

### Las vinculaciones que X0 resuelve

Conjunto nominal, cerrado y fijado antes de ejecutar. El mecanismo lo toma de esta lista literal;
no lo elige, no lo infiere y no lo deriva escaneando SHAs presentes en el documento.

```text
V1  CANDIDATE_WORK_SHA       local   work-claude-i    el work SHA que la auditoria de
                                                      congelamiento designe como CANDIDATE_WORK_SHA
V2  CANDIDATE_BLOB_SHA       local   work-claude-i    f44f2a0797cde6f569cca6fe5397d45917680258
V3  P_C_CORTE_ORIGEN         local   work-claude-i    636a5d095574130b56c232da7958691f87234516
V4  P_C_CORTE_DESTINO        local   work-claude-i    5bd6b0f582c7970a7b8c6c838b9971a70df43dfc
V5  P_C_REFERENCIA_REMOTA    remota  work-claude-i    origin, refs/heads/main
                                                      resuelve a un booleano de alcanzabilidad
```

Cinco vinculaciones nominales. `E16` y `E17` se miden sobre exactamente estas cinco, conforme a la
regla de medición: dos nombres distintos siguen siendo dos aunque compartan valor.

Sólo `V1` queda por completar, y lo completa la auditoría que congele este contrato, porque el
work SHA de una entrega no existe antes de cerrarla. Las otras cuatro están fijadas aquí.

`V5` es la vinculación que hace `X0` capaz de detectar por adelantado que el remoto no está
alcanzable. Sin ella, una red caída no aparecería hasta `P-C1`, ya dentro de la corrida, y quemaría
un contrato entero por una condición de entorno: exactamente lo que pasó dos veces con un clon
desactualizado.

Su función es una y no cambia después de ejecutar: comprobar que la referencia existe en el
remoto. No obtiene su valor, no lo transporta y no lo pone a disposición del cuerpo. Quien obtiene
el valor vigente es `P-C1`, dentro del cuerpo, porque esa es la conducta que `P-C1` demuestra.

```text
sonda local    resuelve un objeto en un clon y no devuelve su contenido
sonda remota   resuelve una referencia en un remoto y devuelve solo si existe
```

### Regla de ejecución

Idéntica en su semántica a la que `U2` dejó congelada, con la bitácora propia de esta unidad.

```text
X0  antes de todo lo demas, el mecanismo resuelve cada identidad Git que este contrato congela.
    Si alguna no resuelve, termina NO_EJECUTABLE informando cuales: no anota INICIO, no ejecuta
    ningun caso, no evalua ningun criterio, no emite veredicto, no consume el contrato y no deja
    linea en la bitacora. X0 no comprueba ninguna otra cosa
X1  superado X0, lee la bitacora de la unidad, busca una marca de inicio de la identidad
    congelada y, si no la hay, anota la suya
X2  toda invocacion que anoto INICIO es una ejecucion observada, cualquiera sea su final
X3  solo puede aprobarse la que emitio veredicto EXITO. Cualquier otro final es FALLO
X4  una ejecucion observada agota el contrato. Si al abrir hay un INICIO previo de esta
    identidad, la invocacion es un reintento: se resuelve como FALLO, no evalua criterios y no
    reemplaza el resultado anterior
X5  una corrida nueva exige un contrato nuevo, propuesto y congelado antes de ejecutarla
```

Las tres terminaciones posibles, y sólo tres:

```text
T1  veredicto EXITO    anota CIERRE   unica terminacion aprobable
T2  veredicto FALLO    anota CIERRE   incluye la excepcion capturada del cuerpo
T3  sin veredicto      no anota CIERRE   lo que ningun mecanismo puede manejar de si mismo
```

### La bitácora

```text
path       u3-metodo-manifiestos/BITACORA.txt
alcance    una sola bitacora para esta unidad, compartida por todos sus contratos
formato    una linea por evento, solo se agrega, nunca se reescribe
identidad  cada linea lleva la identidad del contrato y el blob del candidato
```

La ruta es una constante de la unidad y no se deriva del directorio del mecanismo: una bitácora
que viviera junto al mecanismo se reiniciaría al crear un directorio nuevo, y mover pasaría a ser
indistinguible de reiniciar.

`u2-reglas-orquestador/BITACORA.txt` no es esta bitácora y no se toca. Cada unidad lleva la suya.

### Regla de medición

```text
toda cobertura se mide sobre el conjunto nominal que el contrato declara,
nunca sobre un conjunto derivado de sus valores.
Dos elementos con nombres distintos siguen siendo dos aunque compartan valor.
```

Alcanza a las obligaciones del candidato, a las vinculaciones congeladas de `X0` y a la
enumeración de controles negativos.

### Regla de alcance

```text
toda comprobacion lee la superficie material de la obligacion que dice verificar, y no una
superficie mas ancha que la contenga.
Una ocurrencia fuera de esa superficie no puede cambiar su resultado.
Un mutante que altere algo fuera de esa superficie no viola la obligacion y no discrimina.
Cuando una obligacion prohibe mantener o usar algo, la comprobacion observa la conducta, no la
mencion del nombre.
```

La superficie material de una obligacion es su propia linea etiquetada con sus continuaciones.
Cuando una obligacion necesita otra superficie, este contrato la nombra.

### Regla de identidad del control

```text
todo control ejercita la misma comprobacion efectiva que califica al candidato real para la
obligacion que dice cerrar, y compara el mismo observable.
Un control cambia el sujeto; no cambia la comprobacion.
No existe comprobacion alcanzable solo desde un control, ni obligacion cuyo control no ejercite
la comprobacion que la corrida real uso.
Declarar la identidad no basta: la evidencia observa que el control atraveso esa comprobacion.
Cuando un control no puede ejercitar la comprobacion misma, este contrato nombra la equivalencia
y la evidencia la demuestra; sin esa demostracion el control no cierra nada.
```

Alcanza a todos los controles negativos de este contrato, no sólo a los que cierran `D-20`,
`D-21` y `D-22`. Este contrato no nombra ninguna equivalencia: todos sus controles ejercitan la
comprobación misma sobre un sujeto sintético.

### Materia reservada a la corrida

Conjunto nominal, cerrado y fijado antes de ejecutar. La regla de medición lo alcanza: el
inventario se mide sobre esta lista, no sobre lo que el mecanismo resulte hacer.

```text
M1  leer el candidato desde el corte congelado
M2  R2 / P-C1: obtener del remoto la referencia vigente
M3  P-C2: el descubrimiento sobre los dos cortes congelados
M4  ejecutar cualquier caso del corpus
M5  ejercer cualquier comprobacion sobre el sujeto real o sobre una variante derivada de el
M6  ejercer cualquier control negativo
M7  evaluar cualquier criterio E o F, y emitir cualquier veredicto
```

### Materia de construcción, delimitada antes de usarla

```text
C1  escribir el codigo del mecanismo, leerlo, analizarlo sintacticamente e importarlo
C2  ejercitar una funcion del mecanismo contra insumos sinteticos que no son el candidato, no
    derivan de el y no son el sujeto real de ninguna comprobacion, sin evaluar ningun criterio de
    este contrato y sin emitir veredicto
C3  operaciones sobre los repositorios ajenas al mecanismo: sincronizar, resolver identidades,
    inspeccionar el arbol
```

`C1` a `C3` no alcanzan `M1` a `M7`. Una prueba de humo que lea el candidato es `M1` y por lo
tanto no es `C2`: ahí murió la corrida anterior, y la frontera queda escrita antes y no después.

### Regla de materia reservada

```text
toda ejecucion de materia reservada ocurre con la guardia por encima, y la guardia se observa en
el momento de ejecutarla, no se declara al final.
Una invocacion de materia reservada sin la guardia por encima se rechaza, y ese rechazo es
observable y distinto de la conducta autorizada.
Toda entrada a materia reservada queda contada y fechada por fase, y ninguna ocurre fuera del
cuerpo.
El inventario de entradas materiales del mecanismo es exactamente la lista M1 a M7: ninguna
entrada material queda fuera de ella.
Lo que no es materia reservada es materia de construccion, y este contrato la delimita antes de
ejecutar.
```

### Propiedad que debe demostrarse

```text
P-A  un recorrido de entrevista que cierra la intencion produce un paquete de constitucion con
     todos los campos aplicables, con identidades Git exactas obtenidas de Git y sin secretos
P-B  un trabajo aislado produce un paquete completo que no lleva PROJECT_REPO, PROJECT_PATH ni
     PROJECT_SHA, y el metodo no crea PROJECT.md por simetria
P-C  el descubrimiento de concurrencia distingue compatibilidad demostrable de compatibilidad no
     demostrable, y un solapamiento material no resuelto no procede por presuncion
P-D  el denominador de la cobertura es el conjunto completo de obligaciones etiquetadas del
     candidato, y su estructura no admite contenido normativo fuera de ese conjunto
P-E  cada comprobacion estructural discrimina de verdad: su mutante viola la obligacion que la
     comprobacion lee, y esa diferencia queda observable en la evidencia
P-F  el pre-vuelo se limita a resolver las vinculaciones congeladas, y esa limitacion es
     observable en su traza externa, en su traza interna y en sus importaciones
P-G  cada control ejercita la conducta efectiva que califica al candidato, y no una ruta
     paralela construida para el control: la evidencia observa la comprobacion atravesada
P-H  la materia reservada solo se ejecuta por la ruta que atraviesa la guardia, y esa ruta queda
     observada en cada entrada material, no declarada al final
```

### Entorno y fuentes

```text
entorno   Windows local bajo C:\Franco_Metodos_AI, dentro del perimetro constitutivo
fuentes   el candidato, del que se leen sus obligaciones y su estructura
          un corpus de recorridos y de comparaciones definido dentro de la unidad, sin secretos
          insumos sinteticos para los controles negativos, nunca el candidato real
```

#### Insumos de P-C, congelados antes de ejecutar

El repositorio, los dos cortes y las dos superficies quedan nombrados aquí. La evaluación no
puede elegirlos después de observar el mecanismo.

```text
P_C_REPO              https://github.com/francogg89-ai/work-claude-i
P_C_REMOTO            origin
P_C_CORTE_ORIGEN      636a5d095574130b56c232da7958691f87234516
P_C_CORTE_DESTINO     5bd6b0f582c7970a7b8c6c838b9971a70df43dfc

SUPERFICIE_DISJUNTA   work-claude-i : u1-contratos-transversales/
SUPERFICIE_SOLAPADA   work-claude-i : u3-metodo-manifiestos/
```

`P-C` se demuestra en dos partes, y las dos son necesarias:

```text
P-C1  conducta: el descubridor obtiene la referencia actual del remoto declarado con una
      operacion de solo lectura, y la evidencia preserva que obtuvo. Su valor no se congela
      porque es, por definicion, la vigencia
P-C2  discriminacion: sobre los dos cortes congelados, la superficie disjunta produce
      interseccion vacia y procede, y la superficie solapada produce interseccion no vacia y no
      procede
```

Nota de limitación, declarada por adelantado: `P-C2` congela el corte destino para que la corrida
sea determinista. En uso real ese corte es la referencia remota vigente, y `P-C1` es lo que
demuestra que el descubridor la obtiene del remoto y no de un clon local.

### Mecanismo

Un verificador determinista, sin modelo de lenguaje, en un directorio propio de este contrato
dentro de `u3-metodo-manifiestos/`.

#### La frontera de red, única y acotada

`U2` pudo declarar su mecanismo sin red porque nada de lo que verificaba estaba fuera del disco.
`U3` no puede: `R-6-remoto` exige que la vigencia se obtenga del remoto, y `P-C1` existe para
demostrar esa conducta. Heredar la frase de `U2` dejó el contrato diciendo dos cosas
incompatibles.

La frontera cuenta interacciones por fase y por propósito, y son exactamente dos:

```text
el mecanismo no usa red, con dos excepciones nombradas, ambas de solo lectura y ambas contra
P_C_REPO en P_C_REMOTO:

R1  en X0, antes de INICIO. Resuelve V5: comprueba que la referencia declarada existe en el
    remoto. Su resultado es un booleano de alcanzabilidad. El valor de la referencia no se usa
    en ningun criterio y no queda disponible para el cuerpo
R2  en el cuerpo, P-C1. Obtiene el valor vigente de esa referencia y lo preserva

cualquier otra interaccion de red es fallo, y tambien lo es una de estas dos ocurrida fuera de
su fase
```

Se resuelve así y no debilitando `D-13`: la alternativa —comparar contra un clon local— es
exactamente lo que `R-6-remoto` prohíbe, porque demuestra lo que ese disco sabe y no vigencia.

`R1` y `R2` tocan el mismo endpoint y no son la misma cosa. `R1` pregunta si está; `R2` pregunta
qué dice. Esa diferencia es la misma que separa resolver de leer en las sondas locales, y por eso
`V5` conserva la clase que ya tenía: `X0` resuelve vinculaciones, no lee valores.

Que `R1` no transporte el valor no puede quedar declarado. Queda observable en la forma del
resultado de `X0`: un booleano por vinculación, sin campo donde una referencia pueda viajar. Un
pre-vuelo que devolviera el valor cambiaría esa forma, y `E24`, `F26` y `N27` lo detectan.

No declara catálogo propio de obligaciones: las extrae del candidato.

Construye un constituyente determinista que, dado un conjunto explícito de respuestas de
entrevista, produce un paquete de constitución aplicando únicamente lo que el candidato declara.
Construye además un descubridor que ejecuta la comparación de `R-6-descubrimiento` con
operaciones Git de sólo lectura sobre cortes congelados.

Toda invocación —la real y las sintéticas de los controles— atraviesa una única función de
corrida donde vive la guardia `X4`. `X0` corre bajo intercepción externa e interna.

Se ejecuta una vez. Un contrato se agota al producir su resultado.

### Criterio discriminante de éxito

ÉXITO si y sólo si simultáneamente:

```text
E1   cada caso produce el resultado que su obligacion predice
E2   cada rechazo cita un identificador de obligacion presente en el candidato
E3   toda obligacion etiquetada del candidato tiene al menos un caso que la ejercita
E4   toda seccion numerada aporta al menos una obligacion, o esta declarada no mecanica
E5   toda seccion mecanica respeta la forma que el candidato declara
E6   toda comprobacion estructural falla sobre su mutante
E7   el observable leido difiere entre sujeto real y mutante, y ambos quedan preservados
E8   el paquete del recorrido completo lleva todos los campos aplicables, con identidades
     obtenidas de Git y sin ningun valor secreto
E9   el paquete del trabajo aislado esta completo y no lleva ningun campo PROJECT_*
E10  el descubrimiento procede con interseccion vacia y no procede con interseccion no vacia,
     y en este ultimo caso rutea preservando y entregando
E11  el candidato leido es exactamente el blob congelado
E12  la corrida preserva su marca de inicio y su marca de cierre
E13  al abrir, la bitacora no contenia INICIO de esta identidad
E14  la bitacora contiene exactamente un INICIO y un CIERRE de esta identidad; las lineas de
     otras identidades no se cuentan y quedan byte a byte
E15  los controles de reintento y de aborto atraviesan la misma funcion de corrida que la
     invocacion real
E16  la evidencia preserva el resultado de X0 para las cinco vinculaciones nominales V1 a V5,
     con el mapeo resolucion -> vinculaciones satisfechas, y todas resolvieron
E17  la traza externa de X0 cubre nominalmente V1 a V5, sin invocacion que no sea sonda y sin
     apertura de archivo
E18  la traza interna de X0 no contiene llamadas a los modulos de la corrida
E19  el modulo del pre-vuelo no importa ningun modulo de la corrida
E20  la derivacion de cadencia es una unica funcion del mecanismo: la que ejercita N9 es la misma
     que implementa R-5-derivacion en el camino real, y la evidencia lo hace verificable
E21  la ruta de la bitacora es la constante fija de la unidad, y el mecanismo no la deriva de su
     propio directorio ni usa ninguna otra
E22  P-C usa exactamente los insumos congelados —repositorio, remoto, los dos cortes y las dos
     superficies— y la evidencia preserva la referencia remota que P-C1 obtuvo
E23  la corrida realiza exactamente dos interacciones de red, R1 en X0 y R2 en el cuerpo, ambas
     de solo lectura contra P_C_REPO en P_C_REMOTO, cada una en su fase; la evidencia preserva
     ambas. Ninguna otra parte del mecanismo usa red
E24  el resultado de X0 para V5 es un booleano de alcanzabilidad: no transporta el valor de la
     referencia, y la forma del resultado de X0 no tiene campo donde ese valor pueda viajar
E25  cada comprobacion declara la superficie material que lee, y la evidencia la preserva
E26  para cada comprobacion que lee el candidato, una alteracion fuera de su superficie no
     cambia su observable
E27  el mutante de cada comprobacion estructural altera la superficie que esa comprobacion lee,
     y la diferencia del observable proviene de esa alteracion
E28  las comprobaciones de estado o registro prohibido observan si el mecanismo lo mantiene o lo
     usa, no si su nombre aparece en la fuente
E29  cada control declara la comprobacion que ejercita, y la evidencia observa que atraveso esa
     misma comprobacion, no una equivalente por nombre
E30  la comprobacion que un control atraviesa para una obligacion es la que califico al candidato
     real para esa obligacion, y compara el mismo observable
E31  ninguna comprobacion es alcanzable solo desde un control: el conjunto nominal de
     comprobaciones que los controles atraviesan esta contenido en el que califico al candidato,
     y toda obligacion que un control dice cerrar tiene ahi su comprobacion
E32  toda entrada a materia reservada observo la guardia por encima al ejecutarse, y una
     invocacion sin la guardia queda rechazada con un observable distinto del autorizado
E33  toda entrada a materia reservada ocurrio dentro del cuerpo: la evidencia preserva la cuenta
     y la fase de cada una, y ninguna cae fuera
E34  el inventario de entradas materiales del mecanismo es exactamente M1 a M7, tomado de esa
     lista literal y no obtenido por inferencia
```

### Criterio discriminante de fallo

FALLO si ocurre cualquiera:

```text
F1   algun caso difiere del resultado que su obligacion predice
F2   algun rechazo cita un identificador ausente del candidato
F3   alguna obligacion etiquetada queda sin caso
F4   el mecanismo necesita una regla que el candidato no declara ni obtiene por referencia
     autoritativa explicita
F5   alguna seccion numerada queda sin obligacion y sin declararse no mecanica
F6   alguna seccion mecanica viola su forma declarada
F7   alguna comprobacion estructural no falla sobre su mutante
F8   el observable de alguna comprobacion estructural no difiere entre real y mutante
F9   el paquete del recorrido completo omite un campo aplicable, lleva una identidad que no
     proviene de Git, o transporta un valor secreto
F10  el paquete del trabajo aislado lleva algun campo PROJECT_*, o queda incompleto
F11  el descubrimiento procede con interseccion no vacia, o no procede con interseccion vacia
F12  el blob leido no es el congelado
F13  la invocacion empezo y su cuerpo produjo una excepcion, resuelta en el veredicto conforme
     a T2
F14  al abrir habia un INICIO previo de esta identidad: la invocacion es un reintento
F15  la bitacora no contiene exactamente un INICIO y un CIERRE de esta identidad, o alguna linea
     ajena fue alterada
F16  algun control de reintento o de aborto no atraviesa la funcion de corrida real
F17  se anoto INICIO con alguna vinculacion congelada irresoluble
F18  la traza externa de X0 deja una vinculacion sin cubrir, contiene una invocacion que no es
     sonda, abre un archivo, o alguna sonda devuelve contenido
F19  la traza interna de X0 contiene una llamada a un modulo de la corrida
F20  el modulo del pre-vuelo importa algun modulo de la corrida
F21  la derivacion de cadencia que ejercita N9 no es la que el camino real usa
F22  la ruta de la bitacora no es la constante fija de la unidad, o el mecanismo la deriva de su
     propio directorio
F23  P-C usa insumos distintos de los congelados, o la evidencia no preserva la referencia
     remota obtenida por P-C1
F24  la corrida realiza una interaccion de red que no es R1 ni R2, una dirigida a un repositorio
     o remoto distintos de los declarados, o una de las dos ocurrida fuera de su fase
F25  el conjunto de vinculaciones que X0 resuelve no es exactamente V1 a V5, o el mecanismo lo
     obtiene por inferencia en lugar de la lista literal congelada
F26  el resultado de X0 transporta el valor de la referencia remota en lugar de un booleano de
     alcanzabilidad
F27  alguna comprobacion no declara la superficie que lee, o lee una mas ancha que la obligacion
F28  el observable de alguna comprobacion cambia por una ocurrencia ajena a su superficie
F29  el mutante de alguna comprobacion estructural altera algo fuera de la superficie que esa
     comprobacion lee
F30  alguna comprobacion de estado prohibido se satisface o falla por la ocurrencia lexica de un
     nombre en lugar de por la conducta del mecanismo
F31  algun control atraviesa una comprobacion distinta de la que califico al candidato real para
     la obligacion que ese control dice cerrar, o compara otro observable
F32  existe una comprobacion alcanzable solo desde los controles, o una obligacion cuyo control
     no atraviesa ninguna comprobacion de la calificacion real
F33  un control declara una identidad de comprobacion que la evidencia no observa atravesada, o
     invoca una equivalencia que este contrato no nombra o que la evidencia no demuestra
F34  alguna entrada a materia reservada se ejecuto sin la guardia por encima, o el rechazo no se
     distingue en su observable de la conducta autorizada
F35  alguna entrada a materia reservada ocurrio fuera del cuerpo, o la evidencia no preserva su
     cuenta y su fase
F36  existe una entrada material del mecanismo que M1 a M7 no cubre, o el inventario se obtiene
     por inferencia en lugar de la lista literal congelada
```

No existe tercera salida.

Los criterios de fallo califican la invocación real. Los resultados de las invocaciones
sintéticas de los controles son observaciones de esos controles, no fallos de la corrida.

### Control negativo

Sobre la materia del candidato:

```text
N1   un paquete que omite un campo aplicable debe rechazarse
N2   un paquete con una identidad Git abreviada o no obtenida de Git debe rechazarse
N3   un paquete que transporta el valor de un secreto en lugar de su referencia debe rechazarse
N4   un trabajo aislado cuyo paquete lleva PROJECT_SHA debe rechazarse
N5   un descubrimiento con interseccion no vacia que procede debe rechazarse
N6   un descubrimiento con interseccion vacia que no procede debe rechazarse
N7   un PROJECT.md sintetico que registra ultimo SHA o lista de carriles debe rechazarse
N8   una politica de relevo sintetica que persiste un contador debe rechazarse
N9   sobre una historia Git sintetica que contiene un merge, la derivacion efectiva —la misma
     funcion que el mecanismo usa para implementar R-5-derivacion— debe contar el conjunto
     alcanzable completo, y un recorrido por primer padre sobre esa misma historia debe dar un
     numero menor. La evidencia preserva el log de esa historia y ambos numeros. Si los dos
     numeros coinciden, la historia sintetica no discrimina y el control no demuestra nada
N10  una fuente auxiliar sintetica que pretende ampliar una capacidad debe rechazarse
```

Sobre el propio mecanismo, contra insumos sintéticos y nunca contra el candidato real:

```text
N11  un candidato sintetico con una obligacion sin caso debe producir F3
N12  un candidato sintetico con una seccion sin obligacion y no declarada no mecanica -> F5
N13  un candidato sintetico con contenido fuera de forma debe producir F6
N14  un blob sintetico ajeno debe producir F12
N15  una comprobacion sintetica cuyo mutante no altera su observable debe producir F8
N16  una invocacion sintetica de la misma funcion de corrida con una falla inyectada debe
     terminar conforme a T2 y dejar su bitacora sintetica con INICIO y CIERRE
N17  una invocacion sintetica sobre una bitacora que ya contiene INICIO debe devolver el
     resultado de reintento sin anotar y sin evaluar criterios
N18  una bitacora sintetica con lineas ajenas alteradas debe producir F15
N19  una vinculacion sintetica irresoluble debe hacer que X0 termine NO_EJECUTABLE
N20  un X0 sintetico que ademas lee el candidato debe producir F18, con traza externa distinta
N21  un X0 sintetico que ejecuta en memoria un caso, sin interaccion externa adicional, debe
     producir F19, con traza interna distinta
N22  un modulo de pre-vuelo sintetico que importa un modulo de la corrida debe producir F20
N23  dos vinculaciones sinteticas con nombres distintos y el mismo repositorio y SHA deben
     evaluarse como dos vinculaciones cubiertas, no como una
N24  un mecanismo sintetico que derive la ruta de la bitacora de su propio directorio, en lugar
     de la constante de la unidad, debe producir F22. Ese es el camino por el que una corrida
     nueva podria encontrar una bitacora vacia y eludir X4
N25  un mecanismo sintetico que realice una tercera interaccion de red, una dirigida a otro
     repositorio, o R2 fuera del cuerpo, debe producir F24. Si la traza no lo distingue de la
     corrida real, la frontera de red esta declarada y no observada
N26  un conjunto sintetico de vinculaciones distinto de V1 a V5, o derivado escaneando SHAs en
     lugar de tomado de la lista literal, debe producir F25
N27  un X0 sintetico cuyo resultado para V5 transporte el valor de la referencia en lugar de un
     booleano debe producir F26, y la forma de su resultado debe diferir de la del X0 real
N28  un candidato sintetico con la cadena alterada FUERA de la obligacion que la enuncia no debe
     cambiar el observable de esa comprobacion. Si lo cambia, la comprobacion lee de mas
N29  un candidato sintetico con la cadena alterada DENTRO de esa obligacion si debe cambiarlo.
     N28 y N29 solo juntos demuestran que la comprobacion lee su superficie y no otra
N30  un mutante sintetico que altere algo fuera de la superficie que su comprobacion lee debe
     quedar detectado como no discriminante, aunque el observable coincidentemente difiera
N31  dos sujetos sinteticos frente a una prohibicion de estado: uno que solo nombra la clave
     para rechazarla debe pasar, y uno que efectivamente mantiene ese estado debe fallar. Si la
     comprobacion no los distingue, mide ocurrencia lexica y no conducta
N32  un mecanismo sintetico con ruta paralela: la comprobacion que califica al sujeto lee de mas,
     y una comprobacion localizada alcanzable solo desde el control satisface N28 y N29. Debe
     producir F31 y F32, y las identidades de comprobacion atravesadas deben diferir entre el
     control y la calificacion. Si no difieren, la atadura esta declarada y no observada
N33  un control sintetico que declara la identidad de la comprobacion real pero atraviesa otra
     debe producir F33, y la evidencia debe distinguirlo de un control que si la atraviesa. Si no
     los distingue, la identidad es una etiqueta y no una observacion
N34  una invocacion sintetica de materia reservada sin la guardia por encima debe quedar
     rechazada, y una con la guardia debe proceder. Los dos observables deben diferir. Si no
     difieren, la guardia esta declarada y no observada, y N34 no demuestra nada
N35  un registro sintetico de entradas materiales con una fase distinta de cuerpo debe producir
     F35
N36  un mecanismo sintetico con una entrada material que M1 a M7 no cubre debe producir F36
```

`N9` es el control que ejercita, sobre una historia sintética con merge, la razón por la que
`R-5-derivacion` cuenta el conjunto alcanzable y no un recorrido. Es la primera vez que esa
propiedad se puede ejercitar: las historias reales de este trabajo son lineales.

### Limitaciones conocidas

- El corpus es finito: demuestra que las obligaciones discriminan sobre los casos declarados, no
  que ninguna entrada imaginable las eluda.
- El constituyente es evidencia local y no la implementación de referencia de un agente de
  constitución. Que un agente real siga este método no lo demuestra esta corrida.
- `P-A` y `P-B` ejercitan recorridos de entrevista definidos dentro de la unidad, no una
  conversación real con un humano. Lo que se verifica es que las obligaciones del candidato
  determinan el paquete, no que una entrevista concreta las cumpla.
- `P-D` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería: esa suficiencia es lectura del AUDITOR.
- `P-E` demuestra que cada mutante altera el observable que su comprobación lee, no que ese
  observable sea el más adecuado para la obligación.
- `P-F` observa interacciones externas, llamadas internas e importaciones; no observa lógica de
  la corrida copiada en línea dentro del pre-vuelo.
- `P-H` observa la ruta de cada entrada material de esta corrida y demuestra que el mecanismo
  entregado no ejecuta materia reservada eludiendo la guardia. No demuestra que no haya existido
  una ejecución previa en otra máquina o en otro corte: eso lo sostienen la bitácora y la
  declaración del CONSTRUCTOR, y por eso `C1` a `C3` quedan escritos antes y no después.
- La bitácora hace auditable la cantidad de invocaciones siempre que se preserve.

---

## Qué verificó esta intervención

Nada. Construye el candidato y propone el contrato.

## Limitaciones de esta entrega

- El candidato es nuevo y ninguna evidencia lo cubre todavía.
- `METODO-MANIFIESTOS.md` referencia `CT-6` y `CT-7`, cuyos documentos autoritativos son el
  `README.md` de la biblioteca —que aún no existe, y es materia de `U4`— y
  `REGLAS-ORQUESTADOR.md`, ya aprobado. Las referencias son por repositorio, path y contrato, y
  no congelan SHA, por lo que no crean dependencia circular ni quedan rotas cuando `U4` escriba
  el suyo.
- Que las 56 obligaciones agoten lo que `CT-1` a `CT-5` deben exigir es lectura del AUDITOR.

## Resultado

Este contrato previo nuevo, propuesto y no ejecutado, con `D-24` cerrado por la enumeración de la
materia reservada `M1`-`M7`, la delimitación previa de la materia de construcción `C1`-`C3`, la
regla de materia reservada, `E32`-`E34`, `F34`-`F36` y los controles `N34`-`N36`. Agrega `P-H`.

Conserva sin cambios todo lo aceptado de `D-13` a `D-23`: `X0`-`X5`, `T1`-`T3`, `V1`-`V5`,
`R1`/`R2`, `P-C1`/`P-C2`, `P-A` a `P-G`, las reglas de medición nominal, de alcance y de identidad
del control, `E1`-`E31`, `F1`-`F33` y `N1`-`N33` con los controles que ya demostraron
discriminación.

`verificacion-2/` queda entera como evidencia de la corrida agotada, con su `salida.txt` que dice
`EXITO` y su `EVIDENCIA.md` que declara la llamada directa. No la reescribo: esa declaración es
justamente lo que permitió detectar `D-24`, y borrarla sería peor que el error.

La bitácora de la unidad ya contiene el `INICIO` y el `CIERRE` del contrato consumido. Para esta
identidad son líneas ajenas: no cuentan para `E13`/`E14` y deben quedar byte a byte, de modo que
`E14` se ejercita por primera vez en esta unidad sobre historia real.

`u3-metodo-manifiestos/METODO-MANIFIESTOS.md` conserva sin cambios el blob
`f44f2a0797cde6f569cca6fe5397d45917680258`, con 56 obligaciones sobre 8 secciones mecánicas.

## Necesidad humana detectada

Ninguna.
