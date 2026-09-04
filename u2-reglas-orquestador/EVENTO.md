# EVENTO — U2 reglas del orquestador

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@8facccd089a651f9b097269b791ab33c895e725e` y
`audit-chatgpt-i@693498fc8ff681069cf3997ea7e3f8636826a2d3`.

Esa auditoría dio por corregidos `D-04` y `D-05`, reconoció que `X1`-`X3` cubren adecuadamente el
aborto, y no congeló el contrato por `D-06`: `X4` y `X5` no quedaban discriminados frente a
evidencia preexistente de una invocación del mismo mecanismo bajo el mismo contrato.

La auditoría anterior, `audit-chatgpt-i@b679065c468cd1ba3bc8289965ec0bdc1b1b7c0d`, había
interpretado la corrida contractual como FALLO y registrado `D-03`, `D-04` y `D-05`.

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

Corrigió `D-06` en el contrato propuesto. No tocó el candidato, que conserva su blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`, no ejecutó ninguna mitad de verificación y no escribió
`verificacion-3/`.

`D-06` era exacto: `X4` y `X5` estaban enunciados pero ninguna corrida los obligaba a demostrarse.
`E10` probaba el caso positivo y `N17` el aborto, y entre los dos quedaba abierto justamente el
escenario que produjo `D-03`: una invocación previa ya existente y un intento posterior bajo el
mismo contrato.

La corrección introduce una bitácora append-only que el mecanismo lee antes de empezar, y el
control `N18`, que exige demostrar que un reintento sobre una bitácora con marca previa se detiene
y no reemplaza el resultado anterior. Con eso `X4` y `X5` dejan de ser una declaración del
contrato y pasan a ser una propiedad que la corrida debe exhibir.

Las intervenciones anteriores de esta unidad corrigieron `D-04` en el candidato y la
verificabilidad de las dos propiedades de `D-05`.

`u2-reglas-orquestador/verificador/` y `u2-reglas-orquestador/verificacion-2/` no fueron tocadas:
son historia y evidencia de dos corridas ya interpretadas.

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
X1  antes del primer caso, el mecanismo lee la bitácora y anota en ella su marca de inicio
X2  una invocación que empezó y termina por excepción, aborto, interrupción, error de entorno o
    cualquier terminación distinta de la emisión del veredicto, es una ejecución observada
X3  esa observación se resuelve como FALLO. No existe tercera salida y no existe la categoría
    "no llegó a correr"
X4  esa ejecución agota el contrato. Si al leer la bitácora el mecanismo encuentra una marca de
    inicio previa para este mismo contrato, la invocación en curso es un reintento: se resuelve
    como FALLO, no evalúa los demás criterios como si fuera la corrida contractual, y no
    reemplaza el resultado anterior
X5  una corrida nueva exige un contrato nuevo, propuesto y congelado antes de ejecutarla. Una
    bitácora bajo otra identidad de contrato es una bitácora distinta
```

### La bitácora

```text
path       u2-reglas-orquestador/verificacion-3/BITACORA.txt
formato    una línea por evento, sólo se agrega, nunca se reescribe
identidad  cada línea lleva la identidad del contrato congelado y el blob del candidato
eventos    INICIO al abrir la corrida; CIERRE al emitir el veredicto
```

La bitácora es lo que convierte `X2`, `X4` y `X5` en hechos comprobables en lugar de
declaraciones de quien ejecutó.

```text
una invocación normal        deja INICIO y CIERRE
una invocación abortada      deja INICIO sin CIERRE
un reintento                 encuentra un INICIO previo y se detiene por X4
```

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

Un verificador determinista, sin modelo de lenguaje y sin red, en
`u2-reglas-orquestador/verificacion-3/`. `verificador/` y `verificacion-2/` no se modifican.

No declara catálogo propio de reglas: extrae del candidato las obligaciones y la estructura de sus
secciones, y de ahí obtiene el denominador.

Antes del primer caso lee la bitácora. Si encuentra una marca de inicio previa para este contrato,
se detiene por `X4` sin evaluar los demás criterios. Si no, anota su marca de inicio y, al emitir
el veredicto, su marca de cierre. La bitácora se preserva.

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
E11  al abrir, la bitácora no contenía ninguna marca de inicio previa para este contrato
E12  la bitácora preservada contiene exactamente un INICIO y un CIERRE, y su identidad de
     contrato y de candidato coincide con las congeladas
```

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
F11  la invocación empezó y terminó por excepción, aborto o interrupción, conforme a X2
F12  al abrir, la bitácora ya contenía una marca de inicio para este contrato: la invocación es
     un reintento conforme a X4 y no reemplaza el resultado anterior
F13  la bitácora preservada no contiene exactamente un INICIO y un CIERRE, o su identidad de
     contrato o de candidato no coincide con las congeladas
```

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
N17  una invocación sintética que anota su marca de inicio y termina por excepción debe dejar en
     su bitácora sintética un INICIO sin CIERRE, y quedar registrada como ejecución observada
     conforme a X2
N18  sobre una bitácora sintética que ya contiene un INICIO para el mismo contrato, una segunda
     invocación debe detenerse por X4 y resolver F12, sin evaluar los demás criterios y sin
     emitir un veredicto que reemplace al anterior. Si en cambio continúa y produce un resultado
     normal, la detección de reintento no discrimina y la corrida es FALLO
```

`N16` reproduce sintéticamente el defecto de `S24` y `S28` y obliga al mecanismo a demostrar que
lo detecta.

`N17` y `N18` son las dos mitades del defecto `D-03`, y sólo juntas lo cubren. `N17` demuestra que
una invocación abortada queda observable en lugar de desaparecer. `N18` demuestra lo que faltaba:
que un reintento sobre esa evidencia es detectado y no puede sustituir el resultado anterior. Sin
`N18`, `X4` y `X5` eran una promesa del contrato que ninguna corrida obligaba a cumplir.

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

## Corrida bajo el contrato congelado

Se ejecutó una única corrida contra el candidato y el criterio congelados en
`audit-chatgpt-i@c1586576249d37070a8f2fb9ecaa1d3740e522b0`. Ni el candidato ni este evento fueron
modificados antes de producir el resultado.

El mecanismo, su corpus, sus insumos sintéticos, la bitácora, la salida literal y la evidencia
están en `u2-reglas-orquestador/verificacion-3/`. `verificador/` y `verificacion-2/` quedaron
intactas.

```text
código de retorno   0
VEREDICTO           EXITO
```

### Regla de ejecución

```text
BITACORA.txt antes de la corrida   no existía
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
los insumos sintéticos y comprobó que `BITACORA.txt` no existía. No leyó el candidato, no ejecutó
ningún caso del corpus y no ejercitó ninguna comprobación estructural sobre el sujeto real.
`EVIDENCIA.md` la declara en detalle. La frontera de la corrida es `INICIO`, y qué ocurrió antes
de ella debe poder juzgarlo el AUDITOR sin depender de que se lo cuenten después.

## Limitaciones de esta entrega

- El candidato no cambió, pero ninguna evidencia anterior lo cubre: las dos corridas ya
  interpretadas corrieron contra blobs distintos y bajo contratos agotados.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA.
- Las dos obligaciones reformuladas cambian su enunciado, no la conducta que exigen. Que la nueva
  redacción sea fiel a esa conducta es lectura del AUDITOR.
- La corrida demuestra que el candidato es aplicable y que sus obligaciones discriminan sobre el
  corpus declarado. No demuestra que el candidato exija todo lo que `CT-7` debería exigir: esa
  suficiencia sustantiva es lectura del AUDITOR.

## Resultado

La corrida única bajo el contrato congelado, con veredicto `EXITO`, su mecanismo, su corpus, sus
insumos sintéticos, su bitácora, su salida literal y su evidencia.

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md` conserva sin cambios el blob congelado
`b871240fd38d28430fc86fc4b14f1b851dad1f10`.

## Necesidad humana detectada

Ninguna.
