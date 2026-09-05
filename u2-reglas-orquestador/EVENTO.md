# EVENTO — U2 reglas del orquestador

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@b2cb76be7ba4b2e901bf89e7512cb81ae1d6ac37` y
`audit-chatgpt-i@d6dba9decf6091078fa1b7f4f49b044e59f4df02`.

Esa auditoría dio `D-09` por corregido y confirmó que `D-07` y `D-08` siguen corregidos.

No congeló el contrato por `D-10`: la bitácora estaba fijada dentro del directorio de un mecanismo
cuyo archivo ya contenía eventos de un contrato anterior, y `E12`/`F13` no definían si calificaban
el archivo físico completo o sólo los eventos de la identidad congelada.

Las auditorías anteriores de esta unidad corrigieron `D-01` a `D-09`.

## D-03: lo que hice mal

Ejecuté el mecanismo, observé una excepción, modifiqué el mecanismo y volví a ejecutarlo bajo el
mismo contrato. Lo declaré en la evidencia, pero declararlo no lo repara.

La interpretación del AUDITOR es correcta y no tengo nada que oponerle. La primera invocación ya
había empezado a ejercitar el mecanismo contra el candidato y produjo una observación: una
excepción en lugar del resultado que la comprobación en curso debía producir. Bajo `E1`/`F1`, y
sin tercera salida, esa observación se resuelve como fallo. Que el programa no llegara a escribir
la palabra `VEREDICTO` no la convierte en una no-corrida.

El razonamiento que me llevó ahí fue tratar la excepción como un problema de herramienta y no como
una observación de la corrida. Es exactamente la distinción que `§6.1` no admite, y el resultado
práctico es el que el AUDITOR nombra: ajustar el mecanismo a lo observado sin congelar un criterio
nuevo destruye la propiedad que el contrato previo existe para proteger.

Por eso el contrato que sigue lo dice de forma inequívoca, en lugar de dejarlo a la prudencia de
quien ejecuta.

## Qué hizo esta intervención

Corrigió `D-10` en el contrato propuesto. No tocó el candidato, que conserva su blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`, no ejecutó ninguna corrida y no escribió mecanismo
nuevo. `verificador/`, `verificacion-2/` y `verificacion-3/` quedan intactas. Las correcciones
aceptadas de `D-07`, `D-08` y `D-09` se conservan.

### D-10: qué califica un criterio sobre un archivo con historia

El contrato fijaba la bitácora dentro del directorio de un mecanismo, y ese archivo ya contenía un
`INICIO` y un `CIERRE` de un contrato anterior. `E12`/`F13` exigían «exactamente un `INICIO` y un
`CIERRE`» sin decir si contaban el archivo entero o sólo los eventos de la identidad congelada.
Leídos sobre el archivo físico, ya estaban incumplidos antes de correr.

La corrección tiene dos partes, y la segunda es la que importa.

**Dónde vive la bitácora.** Pasa a un path fijo de la unidad, por encima de los directorios de
mecanismo. Si cada contrato tuviera la suya dentro de su propio directorio, empezar una corrida
nueva bastaría con crear un directorio nuevo y la bitácora aparecería vacía: mover y reiniciar
serían indistinguibles, que es justo lo que `X4` existe para impedir. `E17`/`F19` y el control
`N20` lo vuelven exigible, porque una regla que sólo vive en la prosa no se comprueba.

**Qué se califica.** Todo criterio sobre la bitácora se evalúa exclusivamente sobre las líneas de
la identidad congelada. Las de otras identidades no se cuentan, y `E16`/`F18` exigen que estén
byte a byte al cerrar. Que el archivo tenga historia de contratos anteriores no es una anomalía:
es lo que un registro append-only compartido debe verse. La anomalía sería que esa historia
cambiara.

`verificacion-3/BITACORA.txt` no se migra ni se toca: es evidencia de aquella corrida bajo un
contrato agotado. Migrar sus marcas sería escribir en un registro hechos que no presenció, que es
la clase de reconstrucción que un append-only existe para no tener que creer. La bitácora de la
unidad empieza vacía con este contrato; es una transición única y queda declarada en el contrato
para que se vea.

### D-09: dos semánticas para la misma cosa

`X2` y la sección de bitácora describían una invocación abortada como la que termina sin veredicto
y deja `INICIO` sin `CIERRE`. `E15` y `N17` exigían que la falla se capturara, se resolviera como
`F11` y dejara `INICIO` y `CIERRE`. Las dos cosas no pueden regir a la vez, y el contrato no decía
cuál mandaba.

El origen es el mismo que el de `D-08`: arrastré la redacción original de `X2` —escrita cuando el
aborto era el incidente de `D-03`, una excepción que efectivamente mató la invocación— y después
diseñé un mecanismo que captura sus propias excepciones, sin volver a `X2` a decidir cuál de las
dos conductas es la contractual.

La corrección elige una y sólo una: el mecanismo captura lo que puede capturar. Una excepción del
cuerpo se registra como `F11` con su traza, se resuelve dentro del veredicto y se anota `CIERRE`.
Una falla observada produce un resultado, no un vacío, porque un resultado es mejor evidencia que
una ausencia.

`INICIO` sin `CIERRE` deja de ser la conducta esperada de una falla y pasa a nombrar lo único que
ningún mecanismo puede manejar de sí mismo: que el proceso sea terminado antes de poder escribir.
Eso el mecanismo no lo produce, lo sufre, y su firma la lee el AUDITOR en la bitácora preservada.

`E12`/`F13` ya exigen un `INICIO` y un `CIERRE` en la entrega, de modo que una bitácora con
`INICIO` colgado es `F13` y no una corrida aprobable.

### D-08: la contradicción anterior

`F14` decía que un control falla si «no atraviesa la función de corrida real, **o** su invocación
sintética evaluó criterios o modificó su bitácora en lugar de detenerse».

La primera cláusula vale para los dos controles. La segunda vale sólo para `N18`, y describe
exactamente lo que `N17` **debe** hacer: anotar `INICIO`, ejecutar el cuerpo y dejar su bitácora
sintética escrita. Un mismo enunciado exigía y prohibía la misma conducta según el control, y el
criterio no distinguía cuál era cuál.

El error viene de haber escrito `F14` pensando en `N18` y haberlo redactado para «los controles»
en plural, después de extender el tratamiento a `N17`. Extender el alcance de una corrección sin
revisar los criterios que ya la nombraban es cómo se fabrica una contradicción interna.

La corrección separa las tres exigencias en criterios distintos: la que comparten ambos controles,
la que sólo aplica al reintento y la que sólo aplica al aborto. Cada uno queda con un criterio de
fallo propio, y ninguna conducta esperada activa el fallo de otra.

### D-07 y por qué el control era falso

`N18` creaba una bitácora sintética con `INICIO` y llamaba a `hay_inicio_previo()`. Eso comprueba
que la función sabe leer una bitácora. No comprueba nada sobre la conducta que `X4` exige.

La guardia real vivía en `main()`, como un retorno temprano que el control nunca ejercitaba.
Borrar ese retorno habría dejado `N18` en verde y el mecanismo habría aceptado un reintento.

Es el mismo defecto que `E6` y `E7` fueron creados para cerrar, un nivel más arriba: una
comprobación que no atraviesa la decisión que dice comprobar no puede fallar cuando esa decisión
se rompe, y por lo tanto no demuestra nada. Que el observable de una comprobación difiera no
alcanza si la comprobación no toca el camino que gobierna la conducta real.

### La corrección

La decisión de `X4` deja de vivir en `main()` y pasa a una única función de corrida que ambos
caminos atraviesan:

```text
correr(identidad, ruta de bitácora, ...)
    1  aplica la guardia X4 leyendo esa bitácora
    2  si hay INICIO previo, devuelve el resultado de reintento sin anotar y sin evaluar criterios
    3  si no, anota INICIO, ejecuta el cuerpo, anota CIERRE y devuelve el resultado

main()  invoca correr con la identidad y la bitácora reales
N18     invoca la misma correr con una identidad sintética, sobre una bitácora sintética que ya
        contiene INICIO
```

Si alguien borra o rompe la guardia, `N18` deja de recibir el resultado de reintento: la
invocación sintética evalúa criterios y modifica su bitácora, y el control falla. Esa es la
propiedad que `D-07` pedía y que la versión anterior no tenía.

`N17` recibe el mismo tratamiento, aunque la auditoría no lo señaló. Tenía exactamente la misma
debilidad: simulaba la firma de un aborto en vez de atravesar el manejo real de excepciones. Ahora
invoca la misma `correr` con una falla inyectada y comprueba el camino que el mecanismo usa de
verdad. Corregir sólo lo señalado y dejar en pie a su gemelo habría sido cuestión de tiempo.

### D-04 — forma de `§10.1`

La sección llevaba un separador `---` después de su bloque de obligaciones y sin `Nota.` previa, lo
que su propia `§13` declara defecto.

Se corrigió agregando a `§10.1` la nota que le faltaba. El separador queda en la zona libre y la
sección recupera su forma. No se tocó `§13`: la regla funcionó, detectó una inconsistencia real
del documento, y relajarla para acomodar el defecto habría sido redefinir el criterio después del
resultado.

Comprobación de forma sobre el candidato corregido: ninguna violación.

### D-05 — verificabilidad de dos propiedades

El AUDITOR fue preciso al separar las cosas: el sujeto real se comportó conforme a
`R-9.1-frontera` y `R-9.3-no-en-json`. Lo que falló fue la evidencia discriminante.

Pero el defecto no era sólo del mutante. Las dos obligaciones estaban redactadas de un modo que
hacía difícil construir una violación observable, y eso sí es materia del candidato:

```text
antes  R-9.1-frontera    la frontera preferida de detencion es un sobre valido del CONSTRUCTOR
                         hacia el AUDITOR todavia no entregado
```

`preferida` no es una conducta: es una preferencia. Una obligación que no nombra una conducta
observable no puede violarse de forma observable, y cualquier mutante contra ella es una apuesta.
Ahora enuncia qué hace el orquestador en ese punto: conserva el sobre y no lo entrega.

```text
antes  R-9.3-no-en-json  la directiva no se agrega al JSON del sobre
```

No decía **cuándo** se observa. Mi comprobación miró el sobre antes de que la directiva se
emitiera, y por construcción no podía ver la violación. Ahora la obligación fija la ventana de
observación: en ningún momento del transporte, y el sobre observado después de emitir la directiva
es idéntico al recibido.

El candidato conserva 83 obligaciones sobre 17 secciones mecánicas.

---

## Contrato previo de verificación — PROPUESTO, NO EJECUTADO

Conforme a REVOLUTIONS §6.1 y `PLAN.md` §5.2. Ninguna mitad se ejecuta hasta que el AUDITOR lo
evalúe y lo congele.

### Candidato exacto

```text
repositorio  https://github.com/francogg89-ai/work-claude-i
path         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
blob         b871240fd38d28430fc86fc4b14f1b851dad1f10
```

### Regla de ejecución

Esta regla gobierna sobre cualquier otra lectura del contrato.

```text
X1  antes del primer caso, el mecanismo lee la bitácora de la unidad, busca en ella una marca de
    inicio de la identidad congelada y, si no la hay, anota la suya
X2  toda invocación que anotó INICIO es una ejecución observada, cualquiera sea su final
X3  una invocación observada sólo puede aprobarse si emitió veredicto EXITO. Cualquier otro
    final es FALLO. No existe tercera salida ni la categoría "no llegó a correr"
X4  una ejecución observada agota el contrato. Si al leer la bitácora el mecanismo encuentra una
    marca de inicio previa para este mismo contrato, la invocación en curso es un reintento: se
    resuelve como FALLO, no evalúa los demás criterios como si fuera la corrida contractual, y no
    reemplaza el resultado anterior
X5  una corrida nueva exige un contrato nuevo, propuesto y congelado antes de ejecutarla. Una
    bitácora bajo otra identidad de contrato es una bitácora distinta
```

### Las tres terminaciones posibles, y sólo tres

```text
T1  veredicto EXITO                            anota CIERRE   única terminación aprobable
T2  veredicto FALLO                            anota CIERRE   incluye F11: falla capturada
T3  terminación sin veredicto                  no anota CIERRE
```

`T2` es la semántica del fallo dentro de la corrida. El mecanismo captura cualquier excepción del
cuerpo, la registra como `F11` con su traza, la resuelve dentro del veredicto y anota `CIERRE`.
Una falla observada produce un resultado, no un vacío.

`T3` es lo que el mecanismo no puede manejar por definición: una terminación del proceso que le
impide escribir. No la produce el mecanismo, la sufre. Su firma es un `INICIO` sin `CIERRE`, y esa
asimetría la lee el AUDITOR en la bitácora preservada, no el mecanismo mientras corre.

Esta es la corrección de `D-09`. Las versiones anteriores describían `T3` en la regla de ejecución
y exigían `T2` en `N17`, sin decir cuál regía. Rige `T2` para todo lo que el mecanismo puede
capturar, y `T3` sólo nombra lo que ningún mecanismo puede capturar de sí mismo.

`CIERRE` se anota al emitir veredicto, sea `EXITO` o `FALLO`. No significa que la corrida haya
salido bien: significa que terminó diciendo qué pasó.

### La bitácora

```text
path       u2-reglas-orquestador/BITACORA.txt
alcance    una sola bitácora para la unidad, compartida por todos los contratos
formato    una línea por evento, sólo se agrega, nunca se reescribe
identidad  cada línea lleva la identidad del contrato y el blob del candidato
eventos    INICIO al abrir la corrida; CIERRE al emitir el veredicto, sea EXITO o FALLO
```

La bitácora es lo que convierte `X2`, `X4` y `X5` en hechos comprobables en lugar de
declaraciones de quien ejecutó.

```text
T1 y T2   una invocación que emitió veredicto     deja INICIO y CIERRE
T3        una terminación sin veredicto           deja INICIO sin CIERRE
reintento encuentra un INICIO previo de su identidad, se detiene por X4 sin anotar nada
```

#### Por qué la bitácora pertenece a la unidad y no al mecanismo

Esta es la corrección de `D-10`, y la decisión de fondo es dónde vive el archivo.

Si cada contrato tuviera su bitácora dentro del directorio de su propio mecanismo, empezar una
corrida nueva bastaría con crear un directorio nuevo, y la bitácora aparecería vacía. Un registro
que se reinicia al moverse no registra nada: mover y reiniciar serían indistinguibles, que es
exactamente la propiedad que `X4` existe para impedir.

Por eso la bitácora es una sola, vive en un path fijo de la unidad, por encima de los directorios
de mecanismo, y no se mueve ni se recrea junto a ellos. El mecanismo de cada contrato vive en su
directorio; la bitácora no.

#### Cómo se califica sobre un archivo que ya tiene historia

Ninguna línea de otra identidad de contrato se cuenta, se borra, se reescribe ni se
reinterpreta. Todo criterio sobre la bitácora se evalúa **exclusivamente sobre las líneas cuya
identidad de contrato y blob de candidato coinciden con los congelados**.

```text
líneas de la identidad congelada   se cuentan y se califican
líneas de otra identidad           se conservan byte a byte y no se cuentan
```

Que el archivo contenga historia de contratos anteriores no es una anomalía: es lo que un
registro append-only compartido debe verse. Lo que sí sería una anomalía es que esa historia
cambiara.

#### La transición, dicha explícitamente

`u2-reglas-orquestador/verificacion-3/BITACORA.txt` no es esta bitácora. Es evidencia de aquella
corrida, bajo un contrato agotado, y queda donde está sin modificarse.

Sus marcas no se migran a la bitácora de la unidad. Migrarlas sería escribir en un registro
hechos que ese registro no presenció, que es la clase de reconstrucción que un append-only
existe para no tener que creer.

La bitácora de la unidad empieza vacía con este contrato. Es una transición única y queda
declarada aquí para que se vea: de aquí en adelante el path no cambia, y cualquier corrida futura
de esta unidad encuentra en él todo lo que ocurrió antes.

La bitácora se preserva en Git junto con la evidencia. Su contenido es parte del delta que el
AUDITOR inspecciona, de modo que la cantidad de invocaciones deja de ser algo que el CONSTRUCTOR
informe y pasa a ser algo que el AUDITOR lee.

Esta es la corrección de `D-06`. La versión anterior de esta regla probaba el caso positivo y el
aborto, pero no el reintento: un mecanismo podía escribir su marca, abortar, ser corregido y
volver a invocarse sin que nada lo detectara, que es exactamente lo que ocurrió en la corrida
interpretada como `D-03`.

### Propiedad que debe demostrarse

```text
P-A  validación de forma del sobre, sucesión de turn_id y resolución de next_instance
P-B  frontera de DETENER, reanudación literal por CONTINUAR y transporte separado de directiva
P-C  la cadencia de relevo es derivable fuera del orquestador desde historias Git congeladas
P-D  la respuesta que el candidato hace aceptar y rechazar coincide con REVOLUTIONS §4.2
P-E  el denominador de la cobertura es el conjunto completo de obligaciones etiquetadas del
     candidato, y su estructura no admite contenido normativo fuera de ese conjunto
P-F  cada comprobación estructural discrimina de verdad: su mutante viola la obligación que la
     comprobación lee, y esa diferencia queda observable en la evidencia
```

### Entorno y fuentes relevantes

```text
entorno   Windows local bajo C:\Franco_Metodos_AI, dentro del perímetro constitutivo
fuentes   el candidato, del que se leen obligaciones, secciones y declaración de no mecánicas
          la autoridad de transporte en su identidad congelada
          para P-C, las historias Git sobre el corte que el AUDITOR congele
          un corpus de sobres y secuencias definido dentro de la unidad, sin sobres reales
          insumos sintéticos para los controles negativos, nunca el candidato real
```

### Mecanismo

Un verificador determinista, sin modelo de lenguaje y sin red, en un directorio propio de este
contrato dentro de `u2-reglas-orquestador/`. `verificador/`, `verificacion-2/` y `verificacion-3/`
no se modifican: son evidencia de corridas ya interpretadas.

La ruta de la bitácora es una constante de la unidad y no se deriva del directorio del mecanismo.
El mecanismo cambia de directorio con cada contrato; la bitácora no cambia de lugar nunca.

No declara catálogo propio de reglas: extrae del candidato las obligaciones y la estructura de sus
secciones, y de ahí obtiene el denominador.

Toda invocación —la real y las sintéticas de los controles— atraviesa una única función de
corrida, parametrizada por identidad de contrato y ruta de bitácora. Esa función contiene la
guardia `X4`: si encuentra una marca de inicio previa, devuelve el resultado de reintento sin
anotar nada y sin evaluar los demás criterios; si no, anota `INICIO`, ejecuta el cuerpo, anota
`CIERRE` y devuelve el resultado.

La guardia no vive en el punto de entrada del programa ni se comprueba consultando por separado
una función auxiliar. Vive en el camino que ambas invocaciones recorren, de modo que romperla haga
fallar el control.

Las invocaciones sintéticas de los controles no re-ejecutan los controles: exercitan la guardia y
la regla de ejecución, no el conjunto de controles. Esa acotación es parte del mecanismo y se
declara aquí para que no se confunda con una excepción al criterio.

Antes de comparar comprueba que el candidato que lee es el blob congelado.

Cada comprobación estructural registra el valor del observable que lee, para el sujeto real y para
su mutante, y ambos valores se preservan en la evidencia.

Para `P-C` ejecuta operaciones Git de sólo lectura sobre los SHAs congelados, por dos caminos.

### Criterio discriminante de éxito

ÉXITO si y sólo si simultáneamente:

```text
E1   cada caso produce el resultado que su obligación predice
E2   cada rechazo cita un identificador de obligación presente en el candidato
E3   toda obligación etiquetada del candidato tiene al menos un caso que la ejercita
E4   toda sección numerada aporta al menos una obligación, o está declarada no mecánica
E5   toda sección mecánica respeta la forma que el candidato declara
E6   toda comprobación estructural falla sobre su mutante
E7   para toda comprobación estructural, el observable leído difiere entre sujeto real y
     mutante, y ambos valores quedan preservados
E8   P-C reproduce los mismos números por dos derivaciones Git distintas
E9   el candidato leído es exactamente el blob congelado
E10  la corrida preserva su marca de inicio y su marca de cierre
E11  al abrir, la bitácora de la unidad no contenía ninguna marca de inicio de la identidad
     congelada
E12  la bitácora preservada contiene exactamente un INICIO y un CIERRE de la identidad
     congelada; las líneas de otras identidades no se cuentan
E16  las líneas de otras identidades presentes al abrir están, byte a byte, al cerrar: ninguna
     fue borrada, alterada ni reordenada
E17  la ruta de la bitácora es la constante fija de la unidad, y el mecanismo no la deriva de su
     propio directorio ni usa ninguna otra
E13  los controles de reintento y de aborto atraviesan la misma función de corrida que la
     invocación real, y observan su decisión efectiva y no una función auxiliar consultada aparte
E14  el control de reintento devuelve el resultado de reintento: no anota en su bitácora
     sintética y no evalúa los demás criterios
E15  el control de aborto anota INICIO en su bitácora sintética, ejecuta el cuerpo con la falla
     inyectada, la resuelve como F11 con su traza, anota CIERRE, y deja esa bitácora con un
     INICIO y un CIERRE
```

`E14` y `E15` describen conductas opuestas porque los dos controles demuestran cosas opuestas.
`N18` demuestra que una invocación prohibida se detiene antes de empezar; `N17` demuestra que una
invocación que sí empezó resuelve su falla dentro del veredicto en lugar de desaparecer. Exigirle
a `N17` que «se detenga sin modificar su bitácora» sería exigirle que no demuestre nada.

Ningún control sintético toca `BITACORA.txt`. Cada uno usa su propia bitácora, bajo una identidad
de contrato sintética.

`E7` es la lección de `S24` y `S28`. Bajo el contrato anterior una comprobación podía fallar sobre
su mutante por razones ajenas a la obligación; exigir que el observable difiera obliga a que el
mutante viole la propiedad leída y no otra cosa.

### Criterio discriminante de fallo

FALLO si ocurre cualquiera:

```text
F1   algún caso difiere del resultado que su obligación predice
F2   algún rechazo cita un identificador ausente del candidato
F3   alguna obligación etiquetada queda sin caso
F4   el mecanismo necesita una regla que ni las obligaciones del candidato ni una referencia
     autoritativa explícita del candidato respaldan
F5   alguna sección numerada queda sin obligación y sin declararse no mecánica
F6   alguna sección mecánica viola su forma declarada
F7   alguna comprobación estructural no falla sobre su mutante
F8   el observable de alguna comprobación estructural no difiere entre real y mutante
F9   P-C difiere entre sus dos derivaciones
F10  el blob leído no es el congelado
F11  el cuerpo de la corrida produjo una excepción: se captura, se registra con su traza y se
     resuelve dentro del veredicto conforme a T2
F12  al abrir, la bitácora ya contenía una marca de inicio de la identidad congelada: la
     invocación es un reintento conforme a X4 y no reemplaza el resultado anterior
F13  la bitácora preservada no contiene exactamente un INICIO y un CIERRE de la identidad
     congelada
F18  alguna línea de otra identidad presente al abrir fue borrada, alterada o reordenada
F19  la ruta de la bitácora no es la constante fija de la unidad, o el mecanismo la deriva de su
     propio directorio
F14  el control de reintento o el de aborto no atraviesa la función de corrida real, u observa
     una función auxiliar consultada aparte en lugar de su decisión efectiva
F15  el control de reintento anotó en su bitácora sintética o evaluó los demás criterios en lugar
     de devolver el resultado de reintento
F16  el control de aborto no resolvió su falla inyectada como F11, o no dejó en su bitácora
     sintética un INICIO y un CIERRE
F17  algún control sintético leyó o modificó BITACORA.txt en lugar de su bitácora sintética
```

`F15` y `F16` son excluyentes por construcción: cada uno nombra a un único control y ninguna
conducta esperada de uno activa el fallo del otro.

### Alcance de los criterios frente a las invocaciones sintéticas

`F1` a `F13` califican a la **invocación real**. `F11` y `F12`, en particular, describen lo que le
ocurre a la corrida contractual.

Los resultados que producen las invocaciones sintéticas de `N17` y `N18` son observaciones de esos
controles y no fallos de la corrida real. Que `N17` obtenga `F11` sobre su bitácora sintética y que
`N18` obtenga el resultado de reintento sobre la suya es precisamente lo que deben demostrar: es
su éxito, no el fracaso de la corrida.

Lo que sí activa un fallo de la corrida real es que esos controles no exhiban la conducta
esperada, y eso lo dicen `F14`, `F15`, `F16` y `F17`.

Sin esta acotación, `N17` cumpliendo `E15` haría FALLAR la corrida por `F11`, que es la misma
forma de contradicción que `D-08` señaló un nivel más abajo.

No existe tercera salida. Toda observación de la corrida cae en éxito o fallo.

### Control negativo

```text
N1   human_need distinto de null junto con next_prompt distinto de null
N2   final en true junto con human_need distinto de null
N3   turn_id repetido, salteado o retrocedido
N4   next_instance "fresh" con next_actor null
N5   next_instance fuera de {"current", "fresh", null}
N6   work_id ajeno al trabajo transportado
N7   protocol distinto de "revolutions-hop/v1"
N8   instancia current perdida: debe detener y nunca degradar a fresh
N9   DETENER con sobre CONSTRUCTOR → AUDITOR ya pendiente: debe detener sin entregarlo
N10  salida con más de un bloque json: debe rechazarse
N11  contenido no vacío posterior al bloque json: debe rechazarse
```

Sobre el propio mecanismo, contra insumos sintéticos y nunca contra el candidato real:

```text
N12  un candidato sintético con una obligación etiquetada sin caso debe producir F3
N13  un candidato sintético con una sección sin obligación y no declarada no mecánica -> F5
N14  un candidato sintético con contenido fuera de forma debe producir F6
N15  un blob sintético ajeno debe producir F10
N16  una comprobación sintética cuyo mutante no altera el observable que ella lee debe producir
     F8, y si además pasa sobre ese mutante, F7
N17  una invocación sintética de la misma función de corrida, con una falla inyectada en el
     cuerpo, debe terminar conforme a T2: capturar la falla, registrarla como F11 con su traza,
     emitir veredicto FALLO y dejar su bitácora sintética con INICIO y CIERRE. Si en cambio la
     falla se propaga sin resolverse en el veredicto, el mecanismo produce T3 donde el contrato
     exige T2, y el control no discrimina
N18  una invocación sintética de la misma función de corrida, sobre una bitácora sintética que ya
     contiene un INICIO para esa identidad, debe devolver el resultado de reintento: sin anotar
     nada, sin evaluar los demás criterios y sin emitir un veredicto que reemplace al anterior.
     Si en cambio evalúa criterios o modifica su bitácora, la guardia X4 no discrimina
N19  sobre una bitácora sintética que contiene líneas de otra identidad, una invocación sintética
     debe dejarlas byte a byte. Una variante que las borre o las altere debe producir F18; si la
     comprobación no lo detecta, no discrimina
N20  un mecanismo sintético que derive la ruta de la bitácora de su propio directorio, en lugar
     de la constante de la unidad, debe producir F19. Ese es el camino por el que una corrida
     nueva podría encontrar una bitácora vacía y eludir X4
```

`N16` reproduce sintéticamente el defecto de `S24` y `S28` y obliga al mecanismo a demostrar que
lo detecta.

`N17` y `N18` son las dos mitades del defecto `D-03`, y ahora atraviesan el camino real. Un
control que consulta una función auxiliar por separado comprueba que esa función existe; no
comprueba la conducta. Si la guardia se borra del camino que gobierna una invocación, `N18` debe
enterarse, y sólo se entera si lo recorre.

Esa es la corrección de `D-07`, y `E13`/`F14` la vuelven exigible en lugar de dejarla a la forma
que tenga el mecanismo.

Las conductas que cada uno debe exhibir son opuestas y quedan en criterios separados: `E14`/`F15`
para el reintento, que se detiene antes de anotar; `E15`/`F16` para el aborto, que anota, ejecuta
y cierra. Esa separación es la corrección de `D-08`.

### Limitaciones conocidas

- El corpus es finito.
- El verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo.
- `P-C` corre sobre historias cortas y lineales.
- `P-B` verifica las transiciones declaradas, no una interrupción concurrente real.
- `P-E` demuestra que el denominador cubre todo lo que el candidato exige, no que el candidato
  exija todo lo que debería.
- `P-F` demuestra que cada mutante altera el observable que su comprobación lee. No demuestra que
  ese observable sea el más adecuado para la obligación: esa elección es lectura del AUDITOR.
- La bitácora hace auditable la cantidad de invocaciones **siempre que se preserve**. Un
  CONSTRUCTOR que la borrara antes de cerrar su commit no dejaría rastro en el árbol de trabajo.
  Lo que el mecanismo cierra es la posibilidad de reintentar sin darse cuenta y la de reintentar
  sin que quede escrito; lo que no puede cerrar es la supresión deliberada de la evidencia. Ese
  residuo lo cubre `E12`, que exige la bitácora completa y coherente en la entrega: una entrega
  con veredicto y sin bitácora es FALLO por `F13`, de modo que borrarla no produce una corrida
  aprobable sino una entrega defectuosa.

---

---

## La corrida anterior, no aprobada

Se ejecutó una única corrida contra el candidato y el criterio congelados en
`audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0`, y el mecanismo emitió `EXITO`. El
AUDITOR no lo aprobó por `D-07`, y ese contrato quedó agotado.

Lo que sigue es el registro de esa corrida, no un resultado vigente. Su mecanismo, corpus,
insumos sintéticos, bitácora, salida literal y evidencia se conservan sin modificación en
`u2-reglas-orquestador/verificacion-3/`, junto con `verificador/` y `verificacion-2/`.

```text
código de retorno   0
VEREDICTO           EXITO
```

### Regla de ejecución

```text
su bitácora antes de la corrida     no existía
INICIO                             anotado antes del primer caso
CIERRE                             anotado al emitir el veredicto
coherencia                         un INICIO y un CIERRE, sin líneas ajenas
```

### Resultado contra el criterio congelado

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
E12  bitácora coherente                                                    SI

F1 a F13   ninguno ocurrió
N1 a N18   todos presentes; N1-N11 rechazados, N12-N18 discriminaron
```

### Las dos comprobaciones que antes no discriminaban

`S24` y `S28` habían activado `F7` en la corrida anterior. Con las obligaciones reformuladas y
`E7` exigiendo que el observable difiera, ahora discriminan:

```text
S24  obs_real = (entregado False, conservado True)   obs_mut = (True, False)
S28  obs_real = (identico True, contiene False)      obs_mut = (False, True)
```

`N16` reproduce sintéticamente ese defecto y demuestra que el mecanismo lo detecta; `N17` y `N18`
hacen lo mismo con las dos mitades de `D-03`.

### Trabajo previo a INICIO, declarado

Antes de invocar la corrida se ejecutó una prueba de humo que sólo importó los módulos, ejercitó
los insumos sintéticos y comprobó que la bitácora de aquella corrida no existía. No leyó el candidato, no ejecutó
ningún caso del corpus y no ejercitó ninguna comprobación estructural sobre el sujeto real.
`EVIDENCIA.md` la declara en detalle. La frontera de la corrida es `INICIO`, y qué ocurrió antes
de ella debe poder juzgarlo el AUDITOR sin depender de que se lo cuenten después.

## Limitaciones de esta entrega

- El candidato no cambió, pero ninguna evidencia anterior lo cubre: las tres corridas ya
  interpretadas corrieron bajo contratos agotados, y la última no fue aprobada.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA.
- Que el candidato exija todo lo que `CT-7` debería exigir es lectura del AUDITOR: ningún
  mecanismo de este contrato la sustituye.
- `E13` exige que los controles atraviesen la función de corrida real. No demuestra que esa
  función sea el único camino posible hacia una ejecución: un mecanismo futuro que abriera un
  segundo camino quedaría fuera de lo que el control recorre. Lo que el criterio cierra es la
  desconexión entre el control y la decisión que dice comprobar.

## Resultado

Este contrato previo, propuesto y no ejecutado, con:

```text
D-07  cerrado por E13/F14 y por N17 y N18 atravesando la misma función de corrida
D-08  cerrado separando en E14/F15 y E15/F16 las conductas opuestas de cada control
D-09  cerrado eligiendo T2 como semántica contractual de la falla: el mecanismo captura lo que
      puede capturar, y T3 nombra sólo lo que ningún mecanismo puede manejar de sí mismo
D-10  cerrado llevando la bitácora a un path fijo de la unidad y calificando todo criterio
      exclusivamente sobre las líneas de la identidad congelada, con E16/F18 protegiendo la
      historia y E17/F19 más N20 impidiendo el reinicio por mudanza
```

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md` conserva sin cambios el blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`. `verificador/`, `verificacion-2/` y `verificacion-3/`
quedan intactas como historia y evidencia de tres corridas ya interpretadas.

## Necesidad humana detectada

Ninguna.
