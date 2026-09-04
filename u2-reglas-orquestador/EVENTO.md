# EVENTO — U2 reglas del orquestador

Describe el estado de la unidad. No acumula sus versiones anteriores: la historia vive en Git.

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@1c0613b14fc19fb06c2d590990360a2ffec9b1c5` y
`audit-chatgpt-i@937eb6c1e7158dc48875d77c913113b19280f6c7`.

Esa auditoría interpretó la corrida anterior contra el contrato congelado y la declaró FALLO por
`F3`, y detectó además un defecto de diseño bloqueante en el candidato.

## Qué hizo y por qué

Corrigió el candidato `REGLAS-ORQUESTADOR.md` respecto de los dos defectos y propone un contrato
previo nuevo para su nuevo blob. No ejecutó ninguna mitad de la nueva verificación y no escribió
código de mecanismo nuevo.

### D-01 — forma de la respuesta

El defecto era real y la evidencia lo certificaba al revés: el caso `C02` construía una salida con
dos bloques JSON, esperaba aceptación, y la corrida la marcaba correcta.

REVOLUTIONS §4.2 establece que el bloque final es el único bloque JSON de la respuesta y que no
existe contenido posterior. `CT-7` no tiene autoridad para relajar esa forma. Tomar el último
bloque es lícito precisamente porque la unicidad ya está garantizada; sin comprobarla, el
orquestador transporta un sobre que la autoridad declara mal formado.

`§2` del candidato pasa a comprobar la forma antes de extraer:

```text
X1  la salida contiene exactamente un bloque json
X2  no existe contenido posterior a ese bloque
X3  el bloque parsea como JSON
```

La sección referencia §4.2 como autoridad de la forma y describe la comprobación propia del
orquestador, sin redefinir el contrato. Se declara explícitamente que los espacios en blanco tras
el cierre del bloque no son contenido, porque esa frontera es la única ambigüedad material de
`X2` y dejarla implícita sería el tipo de vaguedad que `F4` existe para detectar.

### F3 — el denominador de la cobertura

Esta es la corrección de fondo, y el diagnóstico del AUDITOR es exacto: el `28/28` no demostraba
nada porque el denominador era la colección `REGLAS` escrita a mano dentro de `orquestador.py`.
Una regla del documento podía faltar simultáneamente en esa lista y en el corpus, y la
comprobación —que se comparaba consigo misma— seguía dando verde. Fue lo que ocurrió con la
secuencia de arranque externo de `§1.1`.

El candidato pasa a declarar su propio inventario de reglas mecánicas en `§13`: identificador,
sección de origen y enunciado, una por línea, en formato legible por máquina. El denominador de
la cobertura deja de vivir en el mecanismo y pasa a leerse del documento verificado.

Eso sólo mueve el problema si el inventario puede omitir una sección en silencio. Por eso `§13`
declara además que toda sección numerada aporta al menos una regla, salvo las que lista como no
mecánicas, y esa correspondencia también es comprobable leyendo el candidato.

El inventario resultante tiene 34 reglas sobre 17 secciones mecánicas, con `12` y `13`
declaradas no mecánicas.

### Sobre la evidencia de la corrida fallida

`verificador/` conserva el mecanismo, el corpus, la salida literal y la evidencia de la corrida
interpretada como FALLO. No se reescriben ni se borran: son evidencia previa de una corrida real
y su historia pertenece a la unidad.

No son un mecanismo válido para el candidato nuevo. El contrato bajo el que corrieron quedó
agotado, y el cambio de blob del candidato lo deja sin aplicación. El mecanismo de la próxima
corrida se construye después de que el AUDITOR congele el contrato que sigue.

---

## Contrato previo de verificación — PROPUESTO, NO EJECUTADO

Conforme a REVOLUTIONS §6.1 y `PLAN.md` §5.2. Ninguna mitad se ejecuta hasta que el AUDITOR lo
evalúe y lo congele.

El contrato anterior, propuesto en `work-claude-i@b2a7c472732e5da59b8c82da7278a0e66ed26e93` y
congelado en `audit-chatgpt-i@9679ca4ca6987a3706a0b06cebd3b03cce1dcc7a`, quedó agotado por su
corrida y no cubre este candidato.

### Candidato exacto

```text
repositorio  https://github.com/francogg89-ai/work-claude-i
path         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
blob         b77789d8293372aadc9dfe6f0f1080c889cf5143
```

### Propiedad que debe demostrarse

Que las reglas del candidato son mecánicamente aplicables y discriminantes, que su forma de
respuesta admitida coincide con la que la autoridad exige, y que la cobertura de la verificación
se mide contra el candidato y no contra el mecanismo.

```text
P-A  validación de forma del sobre, sucesión de turn_id y resolución de next_instance
P-B  frontera de DETENER, reanudación literal por CONTINUAR y transporte separado de directiva
P-C  la cadencia de relevo es derivable fuera del orquestador desde historias Git congeladas
P-D  la respuesta que el candidato hace aceptar y rechazar coincide con REVOLUTIONS §4.2:
     un único bloque json y sin contenido posterior
```

### Entorno y fuentes relevantes

```text
entorno   Windows local bajo C:\Franco_Metodos_AI, dentro del perímetro constitutivo
fuentes   el inventario de reglas y las secciones del candidato, leídos del candidato mismo
          la autoridad de transporte, en su identidad congelada, para campos, tipos, formas
          admitidas y forma de respuesta
          para P-C, las historias Git de work-claude-i y audit-chatgpt-i sobre el corte que el
          AUDITOR congele
          un corpus de sobres y secuencias definido dentro de la unidad, sin sobres reales del
          loop y sin secretos
```

### Mecanismo

Un verificador determinista, sin modelo de lenguaje y sin red, dentro de
`u2-reglas-orquestador/`, que implemente únicamente las reglas del inventario del candidato y use
la autoridad exacta cuando el candidato la referencia.

El mecanismo no declara su propio catálogo de reglas: lee `§13` del candidato y las secciones
numeradas del candidato, y de ahí obtiene tanto el denominador de la cobertura como la
correspondencia sección–regla.

Antes de cualquier comparación comprueba que el candidato que está leyendo es exactamente el blob
congelado.

Para `P-C` ejecuta las operaciones Git de sólo lectura de `D1` sobre los SHAs congelados, por dos
caminos distintos.

Se ejecuta una vez. Un contrato se agota al producir su resultado.

### Criterio discriminante de éxito

ÉXITO si y sólo si simultáneamente:

```text
E1  cada caso produce el resultado que su regla predice
E2  cada rechazo cita un identificador presente en el inventario del candidato
E3  toda regla del inventario leído del candidato tiene al menos un caso que la ejercita
E4  toda sección numerada del candidato aporta al menos una regla del inventario, o está
    declarada no mecánica por el propio candidato
E5  P-C reproduce los mismos números por dos derivaciones Git distintas sobre los SHAs congelados
E6  el candidato leído por el mecanismo es exactamente el blob congelado
```

### Criterio discriminante de fallo

FALLO si ocurre cualquiera:

```text
F1  algún caso difiere del resultado que su regla predice
F2  algún rechazo cita un identificador ausente del inventario del candidato
F3  alguna regla del inventario queda sin caso
F4  el mecanismo necesita una regla que ni el inventario ni una referencia autoritativa
    explícita del candidato respaldan
F5  alguna sección numerada del candidato queda sin representación y sin declararse no mecánica
F6  P-C difiere entre sus dos derivaciones
F7  el blob leído no es el congelado
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

`N10` y `N11` son los controles que el contrato anterior no tenía y cuya ausencia permitió que el
defecto `D-01` fuera certificado como correcto.

Además, dos controles sobre el propio mecanismo de cobertura, ejecutados contra insumos
sintéticos y nunca contra el candidato real:

```text
N12  un inventario sintético con una regla sin caso debe producir F3.
     Si la corrida no lo detecta, la comprobación de cobertura no discrimina.
N13  un candidato sintético con una sección numerada ausente del inventario y no declarada
     no mecánica debe producir F5.
```

`N12` y `N13` existen porque el defecto anterior no estuvo en el candidato sino en la
comprobación: un control de cobertura que se compara consigo mismo no puede fallar, y por lo tanto
no demuestra nada. Un control que no puede fallar no discrimina, y estos dos obligan al mecanismo
de cobertura a demostrar que sí puede.

### Limitaciones conocidas

- El corpus es finito: demuestra que las reglas discriminan sobre los casos declarados, no que
  ninguna entrada imaginable las eluda.
- El verificador es evidencia local y no la implementación de referencia de un orquestador
  productivo. Una corrida local no demuestra que un orquestador desplegado se comporte así.
- `P-C` corre sobre historias cortas y lineales: demuestra que la derivación produce el número
  correcto sobre ellas, no que se comporte igual sobre una topología con merges.
- `P-B` verifica las transiciones declaradas, no el comportamiento de un proceso real bajo una
  interrupción concurrente.
- `E4` detecta que una sección quedó sin regla. No demuestra que la regla declarada agote el
  contenido normativo de su sección: esa suficiencia es lectura del AUDITOR sobre el candidato, y
  ningún mecanismo de este contrato la sustituye.

---

## Qué verificó esta intervención

Nada. Corrige el candidato y propone el contrato.

## Limitaciones de esta entrega

- El candidato cambió de blob, por lo que ninguna evidencia anterior lo cubre.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA.
- El inventario de `§13` es una superficie nueva del candidato. Que esté completo respecto de las
  secciones es comprobable; que cada enunciado capture bien su sección es lectura del AUDITOR.

## Resultado

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md` corregido, blob
`b77789d8293372aadc9dfe6f0f1080c889cf5143`, y este contrato previo propuesto y no ejecutado.

## Necesidad humana detectada

Ninguna.
