# EVENTO — U2 reglas del orquestador

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@3960b4865474daa0d53142cbf2e7cdc4236552c8` y
`audit-chatgpt-i@9f8512f1e7228fb81692c62b33414b11d974bd8d`.

Esa auditoría dio por corregido `D-01`, no congeló el contrato propuesto y devolvió `D-02` como
bloqueante: el inventario de `§13` podía representar una sección y a la vez omitir otras
obligaciones mecánicas de esa misma sección. Los ejemplos comprobados fueron `§8` y `§11`.

## Qué hizo y por qué

Reestructuró el candidato para que la omisión intrasección deje de ser posible, y propone un
contrato previo nuevo. No ejecutó ninguna mitad de verificación y no escribió mecanismo nuevo.

### El diagnóstico que hay que aceptar antes de corregir

El defecto no estaba en que el inventario estuviera incompleto. Estaba en que era **una lista
aparte del texto normativo**.

Cualquier lista paralela puede omitir una obligación, y ninguna comprobación que compare la lista
contra sí misma lo detecta. La corrección anterior movió esa lista del mecanismo al documento, lo
cual cerró la omisión de secciones enteras, pero conservó la forma que produce el problema: dos
superficies —el texto y su inventario— que deben coincidir y que nadie garantiza que coincidan.

Agregar una comprobación más sobre esa forma no resuelve nada. Mientras existan dos superficies,
existe una diferencia posible entre ellas.

### La corrección

Se elimina la lista paralela. Las obligaciones dejan de ser un resumen del texto y pasan a **ser**
el texto normativo.

Cada sección mecánica del candidato empieza ahora con un bloque de obligaciones etiquetadas, una
por línea, con identificador y enunciado. `§13` declara la convención completa:

```text
1  el bloque de obligaciones es la unica superficie normativa de una seccion mecanica
2  el conjunto de obligaciones del documento es el conjunto de esas lineas; no existe una segunda
   lista, ni en el documento ni en ninguna implementacion
3  una seccion mecanica tiene exactamente esta forma: encabezado, bloque de obligaciones y,
   opcionalmente, contenido libre a partir del primer marcador Nota.
4  cualquier contenido no vacio entre el encabezado y el bloque, o entre el bloque y el primer
   marcador Nota., es un defecto del documento
5  lo que sigue a un marcador Nota. explica y no obliga: una conducta que el documento pretenda
   exigir y que solo aparezca en una nota, no esta exigida por el documento
```

El punto 5 es el que cierra `D-02`. La completitud del denominador deja de ser una afirmación
empírica sobre el documento —que alguien tendría que verificar sección por sección— y pasa a ser
una propiedad de su estructura: **fuera del bloque etiquetado no hay lugar donde una obligación
pueda existir**, porque el documento declara que ahí no obliga.

El punto 4 impide la vía de escape obvia: colar contenido normativo entre el encabezado y el
bloque, o antes de la primera nota.

Resultado sobre el candidato: 83 obligaciones etiquetadas sobre 17 secciones mecánicas, con `12` y
`13` declaradas no mecánicas. Las secciones que `D-02` señaló quedaron desagregadas: `§8` pasó de
una obligación a seis, y `§11` de una a cuatro, incluida la prohibición de registrar valores
secretos en logs.

La corrección de `D-01` se conserva: `§2` mantiene unicidad del bloque, ausencia de contenido
posterior y parseo válido, con REVOLUTIONS §4.2 como autoridad de la forma.

### Lo que este cambio no resuelve, dicho sin adorno

Una conducta que debería ser obligación puede haber quedado redactada como nota. Eso es un juicio
de redacción y ningún mecanismo de este contrato lo detecta.

La diferencia con la situación anterior es material: antes, una obligación omitida del inventario
seguía siendo exigida por el texto y el denominador quedaba incompleto sin que nadie lo notara.
Ahora, lo que quedó en una nota no obliga a nadie, por declaración del propio documento. El
denominador es completo respecto de lo que el documento exige; lo que puede fallar es que el
documento exija menos de lo que debería, y eso es lectura del AUDITOR sobre el candidato.

### Sobre la evidencia de la corrida fallida

`verificador/` conserva sin modificación el mecanismo, el corpus, la salida y la evidencia de la
corrida interpretada como FALLO. No son un mecanismo válido para este candidato: su contrato está
agotado y el blob cambió dos veces desde entonces.

---

## Contrato previo de verificación — PROPUESTO, NO EJECUTADO

Conforme a REVOLUTIONS §6.1 y `PLAN.md` §5.2. Ninguna mitad se ejecuta hasta que el AUDITOR lo
evalúe y lo congele.

### Candidato exacto

```text
repositorio  https://github.com/francogg89-ai/work-claude-i
path         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
blob         4cfc8f88ead6a1466f61522496605b6c89ed4057
```

### Propiedad que debe demostrarse

Que las reglas del candidato son mecánicamente aplicables y discriminantes, que su forma de
respuesta admitida coincide con la que la autoridad exige, y que la cobertura de la verificación
se mide contra la totalidad de la superficie normativa del candidato.

```text
P-A  validación de forma del sobre, sucesión de turn_id y resolución de next_instance
P-B  frontera de DETENER, reanudación literal por CONTINUAR y transporte separado de directiva
P-C  la cadencia de relevo es derivable fuera del orquestador desde historias Git congeladas
P-D  la respuesta que el candidato hace aceptar y rechazar coincide con REVOLUTIONS §4.2:
     un único bloque json y sin contenido posterior
P-E  el denominador de la cobertura es el conjunto completo de obligaciones etiquetadas del
     candidato, y la estructura del candidato no admite contenido normativo fuera de ese conjunto
```

### Entorno y fuentes relevantes

```text
entorno   Windows local bajo C:\Franco_Metodos_AI, dentro del perímetro constitutivo
fuentes   el candidato mismo, del que se leen sus obligaciones etiquetadas, sus secciones
          numeradas y su declaración de secciones no mecánicas
          la autoridad de transporte, en su identidad congelada, para campos, tipos, formas
          admitidas y forma de respuesta
          para P-C, las historias Git de work-claude-i y audit-chatgpt-i sobre el corte que el
          AUDITOR congele
          un corpus de sobres y secuencias definido dentro de la unidad, sin sobres reales del
          loop y sin secretos
          insumos sintéticos para los controles negativos, nunca el candidato real
```

### Mecanismo

Un verificador determinista, sin modelo de lenguaje y sin red, dentro de
`u2-reglas-orquestador/`, que implemente únicamente las obligaciones del candidato y use la
autoridad exacta cuando el candidato la referencia.

El mecanismo no declara ningún catálogo propio de reglas. Extrae del candidato el conjunto de
obligaciones etiquetadas y la estructura de sus secciones, y de ahí obtiene el denominador de la
cobertura.

Antes de cualquier comparación comprueba que el candidato que lee es exactamente el blob
congelado.

Un caso puede ser de traza —un escenario de sobres y órdenes cuya secuencia de acciones se
compara con la que la obligación predice— o estructural —una afirmación sobre el mecanismo o
sobre el documento—. Todo caso estructural declara además el insumo sintético que debe hacerlo
fallar.

Para `P-C` ejecuta las operaciones Git de sólo lectura de `D1` sobre los SHAs congelados, por dos
caminos distintos.

Se ejecuta una vez. Un contrato se agota al producir su resultado.

### Criterio discriminante de éxito

ÉXITO si y sólo si simultáneamente:

```text
E1  cada caso produce el resultado que su obligación predice
E2  cada rechazo cita un identificador de obligación presente en el candidato
E3  toda obligación etiquetada del candidato tiene al menos un caso que la ejercita
E4  toda sección numerada del candidato aporta al menos una obligación, o está declarada no
    mecánica por el propio candidato
E5  toda sección mecánica del candidato respeta su forma declarada: no existe contenido no vacío
    entre el encabezado y el bloque de obligaciones, ni entre el bloque y el primer marcador Nota.
E6  toda comprobación estructural demuestra que puede fallar: se ejercita contra su insumo
    sintético y falla sobre él
E7  P-C reproduce los mismos números por dos derivaciones Git distintas sobre los SHAs congelados
E8  el candidato leído por el mecanismo es exactamente el blob congelado
```

### Criterio discriminante de fallo

FALLO si ocurre cualquiera:

```text
F1  algún caso difiere del resultado que su obligación predice
F2  algún rechazo cita un identificador ausente del candidato
F3  alguna obligación etiquetada queda sin caso
F4  el mecanismo necesita una regla que ni las obligaciones del candidato ni una referencia
    autoritativa explícita del candidato respaldan
F5  alguna sección numerada queda sin obligación y sin declararse no mecánica
F6  alguna sección mecánica viola su forma declarada
F7  alguna comprobación estructural no falla sobre su insumo sintético
F8  P-C difiere entre sus dos derivaciones
F9  el blob leído no es el congelado
```

No existe tercera salida. Toda observación de la corrida cae en éxito o fallo.

### Control negativo

El corpus incluye casos que el mecanismo **debe** rechazar. Su aceptación implica FALLO.

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

Controles sobre el propio mecanismo de cobertura, ejecutados contra insumos sintéticos y nunca
contra el candidato real:

```text
N12  un candidato sintético con una obligación etiquetada sin caso debe producir F3
N13  un candidato sintético con una sección numerada sin obligación y no declarada no mecánica
     debe producir F5
N14  un candidato sintético con contenido no vacío entre el encabezado de una sección mecánica y
     su bloque de obligaciones debe producir F6
N15  un candidato sintético cuyo blob no coincide con el congelado debe producir F9
```

`E6` generaliza lo que `N12`-`N15` ejemplifican: ninguna comprobación estructural entra en la
evidencia sin haber demostrado que puede fallar.

Ese criterio es la lección de las dos corridas anteriores. La primera declaró `28/28` con un
control de cobertura que se comparaba consigo mismo; la segunda propuso un control de secciones
que no podía detectar una omisión dentro de una sección. En ambos casos el problema no fue el
candidato sino una comprobación incapaz de fallar. `E6` la obliga a demostrarlo antes de contar
como evidencia.

### Limitaciones conocidas

- El corpus es finito: demuestra que las obligaciones discriminan sobre los casos declarados, no
  que ninguna entrada imaginable las eluda.
- El verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo. Una corrida local no demuestra que un orquestador desplegado se comporte así.
- `P-C` corre sobre historias cortas y lineales: demuestra que la derivación produce el número
  correcto sobre ellas, no que se comporte igual sobre una topología con merges.
- `P-B` verifica las transiciones declaradas, no el comportamiento de un proceso real bajo una
  interrupción concurrente.
- `P-E` demuestra que el denominador cubre todo lo que el candidato **exige**. No demuestra que el
  candidato exija todo lo que debería: una conducta redactada como nota en lugar de como
  obligación no obliga, y detectar esa decisión de redacción es lectura del AUDITOR sobre el
  candidato. Ningún mecanismo de este contrato la sustituye.

---

## Qué verificó esta intervención

Nada. Reestructura el candidato y propone el contrato.

## Limitaciones de esta entrega

- El candidato cambió de blob, por lo que ninguna evidencia anterior lo cubre.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA.
- La desagregación de obligaciones aumentó la superficie del candidato de forma material. Que
  cada enunciado sea fiel a la conducta que describe es lectura del AUDITOR.

## Resultado

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md` reestructurado, blob
`4cfc8f88ead6a1466f61522496605b6c89ed4057`, con 83 obligaciones etiquetadas sobre 17 secciones
mecánicas, y este contrato previo propuesto y no ejecutado.

## Necesidad humana detectada

Ninguna.
