# EVENTO — U3 método para constituir manifiestos

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@636a5d095574130b56c232da7958691f87234516` y
`audit-chatgpt-i@d67bde33a78ae1e86584933d1f42f69ba8f14379`.

Esa auditoría aprobó la corrida contractual de `U2` y cerró la unidad. La superficie aprobada es
`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`, blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`.

Autoridades aguas arriba de esta unidad: los contratos transversales cerrados en `U1`, la
superficie aprobada de `U2`, `PLAN.md` y el método autoritativo.

## Qué hizo esta intervención

Creó `u3-metodo-manifiestos/` y construyó el candidato `METODO-MANIFIESTOS.md`, documento
autoritativo de `CT-1`, `CT-2`, `CT-3`, `CT-4` y `CT-5` conforme a la asignación cerrada en `U1`.

Propone el contrato previo de la verificación discriminante que `PLAN.md` `D5` y `§5.1` asignan a
esta unidad. No ejecutó ninguna mitad y no escribió mecanismo.

`u2-reglas-orquestador/` no fue tocada.

### Las cinco autoridades que este documento recibe

```text
CT-1  cadena del sistema y frontera funcional entre los tres documentos
CT-2  contrato del paquete de constitucion
CT-3  politica periodica de relevo derivable
CT-4  descubrimiento de concurrencia y semantica de PROJECT.md
CT-5  fuentes auxiliares y no ampliacion de autoridad
```

`CT-6` es autoridad del `README.md` de la biblioteca y `CT-7` de `REGLAS-ORQUESTADOR.md`. Este
documento los referencia por repositorio, path y contrato, y no reproduce su texto normativo.

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

Resultado: 53 obligaciones sobre 8 secciones mecánicas, con `9` y `10` declaradas no mecánicas.

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
blob         296a2f5d9b70bd8890c5c832556fabc572fe2ede
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
          para P-C, dos repositorios reales sobre cortes congelados, y superficies declaradas
          dentro de la unidad
          un corpus de recorridos y de comparaciones definido dentro de la unidad, sin secretos
          insumos sinteticos para los controles negativos, nunca el candidato real
```

### Mecanismo

Un verificador determinista, sin modelo de lenguaje y sin red, en un directorio propio de este
contrato dentro de `u3-metodo-manifiestos/`.

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
E16  la evidencia preserva el resultado de X0 vinculacion por vinculacion, con el mapeo
     resolucion -> vinculaciones satisfechas, y todas resolvieron
E17  la traza externa de X0 cubre nominalmente cada vinculacion, sin invocacion que no sea sonda
     y sin apertura de archivo
E18  la traza interna de X0 no contiene llamadas a los modulos de la corrida
E19  el modulo del pre-vuelo no importa ningun modulo de la corrida
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
N9   una cadencia sintetica derivada por primer padre sobre una historia con merge debe diferir
     de la derivacion completa, y la derivacion completa es la correcta
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
- Que las 53 obligaciones agoten lo que `CT-1` a `CT-5` deben exigir es lectura del AUDITOR.

## Resultado

`u3-metodo-manifiestos/METODO-MANIFIESTOS.md`, candidato de `CT-1` a `CT-5`, blob
`296a2f5d9b70bd8890c5c832556fabc572fe2ede`, con 53 obligaciones sobre 8 secciones mecánicas; y
este contrato previo propuesto y no ejecutado.

## Necesidad humana detectada

Ninguna.
