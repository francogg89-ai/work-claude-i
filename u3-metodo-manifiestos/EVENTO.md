# EVENTO — U3 método para constituir manifiestos

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@7f5c3aeb124c89a09f7ed846529c49e01ce432c3` y
`audit-chatgpt-i@26193e0fdccfc657e4019e189c325473a29614ce`.

Esa auditoría cerró `D-13` a `D-17` y dio el candidato por aceptable. No congeló el contrato:
abrió `D-18`, por la contradicción entre declarar el mecanismo sin red y exigirle a `P-C1` la
vigencia remota, y `D-19`, porque el conjunto de vinculaciones que `X0` resuelve no estaba
enumerado.

La auditoría anterior había aprobado la corrida contractual de `U2` y cerrado la unidad. La
superficie aprobada es `u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`, blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`.

Autoridades aguas arriba de esta unidad: los contratos transversales cerrados en `U1`, la
superficie aprobada de `U2`, `PLAN.md` y el método autoritativo.

## Qué hizo esta intervención

Corrigió `D-18` y `D-19`, los dos en el contrato propuesto. No tocó el candidato, que conserva su
blob `f44f2a0797cde6f569cca6fe5397d45917680258`; no ejecutó ninguna mitad, no creó la bitácora y no
escribió mecanismo. `U1`, `U2`, `PLAN.md` y `BOOTSTRAP.md` no fueron tocados.

### D-18 — la contradicción que heredé

El contrato declaraba el mecanismo «sin red» y a la vez le exigía a `P-C1` obtener la vigencia del
remoto. Las dos cosas no pueden regir juntas.

El origen es reconocible: copié la frase de `U2`, donde era cierta. `U2` verificaba un documento y
dos historias locales, y no tenía nada que consultar afuera. `U3` verifica una conducta que por
definición ocurre contra un remoto. Heredar una frontera sin volver a preguntarse si sigue siendo
la frontera correcta es la misma forma de error que produjo `D-08` y `D-09`.

La corrección no debilita `D-13`. Comparar contra un clon local sería exactamente lo que
`R-6-remoto` prohíbe. Lo que hace es nombrar una única excepción y acotarla: una operación de sólo
lectura contra el repositorio y el remoto declarados, una sola vez, dentro del cuerpo, registrada
en la traza. Cualquier otra interacción de red es fallo, y `E23`, `F24` y `N25` lo vuelven
observable en lugar de declarado.

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
```

Cinco vinculaciones nominales. `E16` y `E17` se miden sobre exactamente estas cinco, conforme a la
regla de medición: dos nombres distintos siguen siendo dos aunque compartan valor.

Sólo `V1` queda por completar, y lo completa la auditoría que congele este contrato, porque el
work SHA de una entrega no existe antes de cerrarla. Las otras cuatro están fijadas aquí.

`V5` es la vinculación que hace `X0` capaz de detectar por adelantado que el remoto no está
alcanzable. Sin ella, una red caída no aparecería hasta `P-C1`, ya dentro de la corrida, y quemaría
un contrato entero por una condición de entorno: exactamente lo que pasó dos veces con un clon
desactualizado.

```text
sonda local    resuelve un objeto en un clon y no devuelve su contenido
sonda remota   resuelve una referencia en un remoto y no devuelve contenido
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

La frontera queda así, y es una sola:

```text
el mecanismo no usa red, con una unica excepcion nombrada
esa excepcion es la consulta de P-C1: una operacion de solo lectura contra P_C_REPO en
P_C_REMOTO, que devuelve una referencia y no contenido
ocurre una sola vez, dentro del cuerpo de la corrida
queda registrada en la traza y su resultado se preserva
cualquier otra interaccion de red es fallo
```

Se resuelve por excepción nombrada y no debilitando `D-13`: la alternativa —comparar contra un
clon local— es exactamente lo que `R-6-remoto` prohíbe, porque demuestra lo que ese disco sabe y
no vigencia.

`X0` conserva su frontera propia. Su vinculación remota se resuelve con una sonda que devuelve una
referencia y no contenido, igual que las locales resuelven un objeto sin devolverlo.

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
E23  la corrida realiza exactamente una interaccion de red, la de P-C1, dirigida a P_C_REPO en
     P_C_REMOTO, y la evidencia la preserva. Ninguna otra parte del mecanismo usa red
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
F24  la corrida realiza una interaccion de red distinta de la de P-C1, o dirigida a un
     repositorio o remoto distintos de los declarados
F25  el conjunto de vinculaciones que X0 resuelve no es exactamente V1 a V5, o el mecanismo lo
     obtiene por inferencia en lugar de la lista literal congelada
```

No existe tercera salida.

`F1` a `F20` califican la invocación real. Los resultados de las invocaciones sintéticas de los
controles son observaciones de esos controles, no fallos de la corrida.

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
N25  un mecanismo sintetico que realice una segunda interaccion de red, o una dirigida a otro
     repositorio, debe producir F24. Si la traza no lo distingue de la corrida real, la frontera
     de red esta declarada y no observada
N26  un conjunto sintetico de vinculaciones distinto de V1 a V5, o derivado escaneando SHAs en
     lugar de tomado de la lista literal, debe producir F25
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

Este contrato previo, corregido, propuesto y no ejecutado, con `D-18` cerrado por una frontera de
red única y acotada —`E23`, `F24`, `N25`— y `D-19` cerrado enumerando las cinco vinculaciones que
`X0` resuelve, con `F25` y `N26` negando que el mecanismo las obtenga de otro modo.

`u3-metodo-manifiestos/METODO-MANIFIESTOS.md` conserva sin cambios el blob
`f44f2a0797cde6f569cca6fe5397d45917680258`, con 56 obligaciones sobre 8 secciones mecánicas.

## Necesidad humana detectada

Ninguna.
