# EVENTO — U2 reglas del orquestador

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@6c8630ad5144c9de44b172139314c3d5b90a35d1` y
`audit-chatgpt-i@b679065c468cd1ba3bc8289965ec0bdc1b1b7c0d`.

Esa auditoría interpretó la corrida contractual como FALLO y registró tres defectos: `D-03` por
violación de la condición de corrida única, `D-04` por la forma de `§10.1` del candidato, y `D-05`
por dos comprobaciones estructurales sin capacidad demostrada de fallar.

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

Corrigió `D-04` en el candidato, corrigió la verificabilidad de las dos propiedades de `D-05`, y
propone un contrato previo nuevo. No ejecutó ninguna mitad de verificación y no escribió mecanismo
nuevo.

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
X1  la corrida empieza cuando el mecanismo escribe su marca de inicio, antes del primer caso
X2  una invocación que empezó y termina por excepción, aborto, interrupción, error de entorno o
    cualquier terminación distinta de la emisión del veredicto, es una ejecución observada
X3  esa observación se resuelve como FALLO. No existe tercera salida y no existe la categoría
    "no llegó a correr"
X4  esa ejecución agota el contrato. Corregir el mecanismo y volver a invocarlo bajo el mismo
    contrato no produce una corrida válida y no reemplaza el resultado
X5  una corrida nueva exige un contrato nuevo, propuesto y congelado antes de ejecutarla
```

La marca de inicio existe para que `X2` sea comprobable y no dependa de que quien ejecutó lo
declare. Una invocación abortada deja su marca de inicio sin marca de cierre, y esa asimetría es
la evidencia.

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

Escribe su marca de inicio antes del primer caso y su marca de cierre al emitir el veredicto.
Ambas se preservan.

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
E10  la corrida preserva su marca de inicio y su marca de cierre, y no existe evidencia de una
     invocación anterior de este mecanismo bajo este contrato
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
N17  una invocación sintética que escribe su marca de inicio y termina por excepción debe
     quedar registrada como ejecución observada conforme a X2
```

`N16` reproduce sintéticamente el defecto de `S24` y `S28` y obliga al mecanismo a demostrar que
lo detecta. `N17` hace lo mismo con el defecto `D-03`: obliga a demostrar que una invocación
abortada es observable en la evidencia y no queda como si no hubiera ocurrido.

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

---

## Qué verificó esta intervención

Nada. Corrige el candidato y propone el contrato.

## Limitaciones de esta entrega

- El candidato cambió de blob, por lo que ninguna evidencia anterior lo cubre.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA.
- Las dos obligaciones reformuladas cambian su enunciado, no la conducta que exigen. Que la nueva
  redacción sea fiel a esa conducta es lectura del AUDITOR.

## Resultado

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md` corregido, blob
`b871240fd38d28430fc86fc4b14f1b851dad1f10`, con la forma de `§10.1` restaurada y las obligaciones
`R-9.1-frontera` y `R-9.3-no-en-json` reformuladas para ser observables; y este contrato previo
propuesto y no ejecutado.

## Necesidad humana detectada

Ninguna.
