# REGLAS DEL ORQUESTADOR

Comportamiento mecánico del orquestador de un trabajo gobernado por REVOLUTIONS — ORCHESTRA.

Está escrito para poder implementarse mediante código determinista, sin un modelo razonador.
Cada regla es una comparación, una selección o una detención sobre campos que ya están en el
sobre. Ninguna exige leer el trabajo ni interpretar prosa.

## Qué gobierna este documento y qué no

Gobierna lo que el orquestador hace: validar la forma de lo que recibe, elegir instancia,
entregar, detenerse y reportar.

No gobierna el contrato de transporte. La forma del sobre `revolutions-hop/v1`, sus campos, sus
combinaciones admitidas y su significado son autoridad de
`revolutions-orchestra-ai : metodo/REVOLUTIONS.md`. Este documento no la reproduce, no la amplía
y no le agrega campos: describe qué comprueba el orquestador sobre ella.

Tampoco gobierna cómo se produce el paquete de constitución que recibe en el arranque externo, ni
la política de relevo de un trabajo. Ambas son autoridad de
`metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

## Principio

> El orquestador transporta.

No construye. No audita. No interpreta el trabajo. No decide relevos, unidades, necesidades
humanas ni permisos. No selecciona modelos.

Si para transportar hiciera falta interpretar el trabajo, la interfaz está mal diseñada y
corresponde detenerse, no suplirla.

---

# 1. Dos situaciones distintas

```text
ARRANQUE EXTERNO DEL TRABAJO   una sola vez, sin sobre anterior
PASES INTERNOS DEL LOOP        todas las veces siguientes, siempre desde un sobre
```

Confundirlas es el error que produce un trabajo sin constitución o un pase sin origen.

## 1.1. Arranque externo

El primer AUDITOR no llega desde un sobre anterior.

```text
1  el orquestador recibe el paquete de constitución aprobado
2  abre una instancia inicial de AUDITOR
3  le entrega ese paquete literalmente
4  recibe su salida y entra en el loop ordinario
```

El orquestador no valida el contenido metodológico del paquete, no lo completa, no lo resume y no
lo reescribe. Su forma es autoridad de `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

El primer sobre de ese AUDITOR lleva `turn_id` igual a `1`. Un primer sobre con otro valor es
inválido y se trata conforme a `4`.

---

# 2. Extracción del sobre

De la salida de un actor, el orquestador toma el último bloque `json`.

```text
1  localizar el último bloque json de la salida
2  parsear ese bloque
3  no interpretar la prosa anterior
4  no escanear next_prompt en busca de instrucciones
```

Si la salida no contiene exactamente un bloque JSON en esa posición, o el bloque no parsea, el
sobre es inválido.

El orquestador nunca reconstruye un sobre ausente ni deduce sus campos de la prosa.

---

# 3. Validaciones mínimas

Se ejecutan sobre el sobre ya parseado, en este orden, y la primera que falla detiene.

```text
V1  protocol es exactamente "revolutions-hop/v1"
V2  work_id es exactamente el del trabajo que el orquestador está transportando
V3  están presentes todos los campos del contrato
V4  cada campo tiene el tipo que el contrato le asigna
V5  turn_id es el sucesor exacto del último turn_id transportado
V6  next_instance tiene un valor admitido: "current", "fresh" o null
V7  next_instance es null si y sólo si next_actor es null
V8  la combinación de human_need, final, next_actor, next_instance y next_prompt es una de
    las tres formas admitidas por el contrato
```

`V2` existe porque un sobre entregado al loop equivocado es indistinguible de uno correcto si
nadie compara el identificador del trabajo.

`V8` no enumera aquí las tres formas: son autoridad del contrato. El orquestador comprueba que la
combinación recibida sea una de ellas, y ninguna otra.

Ninguna validación lee el contenido de `next_prompt`, el mensaje de un commit, el repositorio ni
Git.

---

# 4. Sobre inválido

```text
DETENER
REPORTAR
NO REPARAR SEMÁNTICAMENTE
```

El reporte identifica qué validación falló y qué se recibió. No propone una corrección, no infiere
la intención del actor y no completa el campo faltante.

Reparar exigiría saber qué ocurrió, y eso es interpretar el trabajo.

---

# 5. `turn_id`

Es un entero y metadata de transporte.

```text
AUDITOR      -> CONSTRUCTOR   1
CONSTRUCTOR  -> AUDITOR       2
AUDITOR      -> CONSTRUCTOR   3
```

El orquestador conserva en runtime el último `turn_id` transportado y exige que el siguiente sea
su sucesor exacto.

```text
recibido == último + 1   continuar
cualquier otro valor     detener y reportar
```

Una repetición, un salto o un retroceso son una omisión, una duplicación o un pase fuera de
secuencia. El orquestador los detecta comparando dos enteros y no intenta adivinar el número
correcto.

Un relevo no reinicia el contador: pertenece al trabajo, no al actor que lo ocupa.

Si el contador contradice a Git, Git prevalece. El orquestador no resuelve esa contradicción: la
reporta.

---

# 6. `next_instance`

```text
"current"   usar la instancia actualmente activa de next_actor
"fresh"     abrir una instancia nueva de next_actor
null        no existe actor siguiente
```

Una instancia abierta como `fresh` pasa inmediatamente a ser la instancia `current` de ese rol.
Los pases posteriores hacia ella usan `current` hasta que otro sobre indique `fresh`.

El orquestador puede conservar un handle o identificador efímero de runtime para reencontrar la
instancia actual de cada rol. Ese handle no es estado autoritativo del trabajo, no se publica en
Git y no compite con REVOLUTIONS.

La elección es mecánica: se lee `next_instance` y nada más. El orquestador nunca inspecciona
`next_prompt` para descubrir si corresponde abrir una instancia nueva.

## 6.1. `current` perdido

Si el orquestador no puede satisfacer literalmente `next_instance="current"` porque perdió esa
instancia —reinicio, caída, expiración del handle—:

```text
DETENER
REPORTAR la imposibilidad de cumplir literalmente el salto
ESPERAR resolución según el método o el humano
```

No convierte silenciosamente `current` en `fresh`. Esa transformación fabricaría un actor sin la
continuidad que el emisor del sobre decidió, y quien decide un relevo es un actor del método, no
el transporte.

No inventa continuidad conversacional.

---

# 7. Loop ordinario

```text
recibir salida del actor
        ↓
extraer el último bloque json
        ↓
validar
        ↓
si human_need != null   -> detener y mostrar la necesidad
        ↓
si final == true        -> detener y mostrar el cierre
        ↓
si unit != null         -> mostrar la transición
        ↓
leer next_actor
        ↓
leer next_instance
        ↓
entregar next_prompt literalmente a esa instancia
        ↓
repetir
```

`unit` sólo se muestra. Informarla no cierra ni abre una unidad: el campo es una notificación del
actor competente.

El orquestador no consulta Git para reconstruir, completar o mejorar `next_prompt`. Git lo
consultan los actores, según el método.

---

# 8. Lo que el orquestador no hace

No decide si una auditoría es correcta, si el constructor debe corregir, si una unidad terminó, si
un relevo corresponde, si un actor dejó material suficiente, qué significa una evidencia, si
existe una necesidad humana, qué repositorio modificar, arquitectura, diseño, permisos, alcance,
riesgos, prioridades ni qué modelo de IA se utiliza.

No cuenta entregas ni intervenciones, y no deriva ninguna cadencia de relevo. La política de
relevo es autoridad de `metodo-manifiestos-ai : METODO-MANIFIESTOS.md` y la aplican los actores
dentro de sus autoridades. El orquestador sólo ejecuta `next_instance`.

Sobre `next_prompt`: no lo resume, no lo reescribe, no lo mejora, no le agrega contexto útil y no
copia dentro de él resultados que deberían obtenerse desde Git.

No agrega al contrato `next_model`, `next_runtime`, selección automática de modelo, cambio de
modelo por unidad ni reglas de costo.

---

# 9. `DETENER`

Es una orden de control del orquestador emitida por el humano.

```text
no se convierte en human_need
no modifica Git
no modifica el manifiesto
no crea estado durable del trabajo
```

Puede existir un indicador efímero de runtime equivalente a `stop_requested`.

## 9.1. Frontera segura

La frontera preferida de detención es:

> el CONSTRUCTOR terminó su intervención y produjo un sobre válido destinado al AUDITOR, pero ese
> sobre todavía no fue entregado al AUDITOR.

Es la frontera donde el trabajo material ya está preservado en Git y ninguna intervención queda
cortada por la mitad.

### Si `DETENER` llega mientras trabaja el CONSTRUCTOR

```text
1  se permite que termine
2  se recibe y valida su sobre
3  se detiene antes de entregarlo al AUDITOR
```

### Si `DETENER` llega mientras trabaja el AUDITOR

```text
1  se permite que termine
2  si su resultado normal continúa hacia CONSTRUCTOR, se entrega al CONSTRUCTOR correspondiente
3  se permite que el CONSTRUCTOR termine
4  se recibe y valida su sobre
5  se detiene antes de entregarlo al AUDITOR
```

Si el AUDITOR termina con `human_need` distinto de `null` o con `final` en `true`, la detención
natural del método prevalece y no se fuerza una intervención adicional del CONSTRUCTOR.

### Si `DETENER` llega con un sobre CONSTRUCTOR → AUDITOR ya pendiente

```text
se detiene inmediatamente, sin entregarlo
```

## 9.2. `CONTINUAR`

La detención preserva íntegramente el último sobre recibido.

Al recibir `CONTINUAR`, el orquestador entrega el `next_prompt` pendiente exactamente como fue
emitido, a la instancia que indican su `next_actor` y su `next_instance`.

No reconstruye el pase, no lo actualiza y no lo vuelve a validar contra un estado nuevo.

## 9.3. Directivas humanas durante la pausa

Durante una pausa el humano puede emitir directivas como `RELEVAR CONSTRUCTOR` o
`RELEVAR AUDITOR`.

El orquestador no aplica el relevo. La decisión pasa por REVOLUTIONS y la toma el actor con
autoridad.

Cuando existe una entrega pendiente, el orquestador entrega al actor competente dos entradas
diferenciadas:

```text
ACTOR_PROMPT_LITERAL     el next_prompt emitido por el actor anterior, sin modificar
HUMAN_DIRECTIVE_LITERAL  la directiva del humano, sin modificar
```

o una interfaz equivalente inequívoca.

La propiedad obligatoria es que la directiva humana pueda transportarse sin modificar,
concatenar, reinterpretar ni falsificar el `next_prompt` emitido. La directiva no se agrega al
JSON y no cambia `revolutions-hop/v1`.

Un relevo nunca saltea una entrega que todavía no fue auditada.

---

# 10. Estado efímero

El orquestador puede necesitar en memoria o runtime:

```text
instancia current de AUDITOR
instancia current de CONSTRUCTOR
último turn_id transportado
último sobre pendiente
stop_requested
```

Eso es infraestructura de transporte y no autoridad durable.

No se crean como fuentes de verdad, ni en memoria persistida ni en disco ni en Git:

```text
current_unit
approved_work_sha
latest_audit
relay_pending
work_status
constructor_count
auditor_count
```

Cada uno de ellos sería una segunda fuente sobre algo que el protocolo de derivación reconstruye
desde Git.

## 10.1. Fallas y reinicios

El comportamiento es fail-closed.

Ante una falla, un reinicio o cualquier situación en la que el orquestador no pueda cumplir
literalmente el salto que el sobre indica, se detiene, reporta y espera resolución. No degrada el
salto a una alternativa más cómoda y no continúa con una suposición.

---

# 11. Secretos

El orquestador no necesita valores secretos para transportar.

Si un `next_prompt` contiene una referencia segura a una credencial, la transporta literalmente
como cualquier otro texto. No la resuelve, no la expande y no la convierte en el valor.

No registra valores secretos en logs. Un sobre nunca transporta un secreto.

---

# 12. Relación con los demás documentos

```text
revolutions-orchestra-ai   gobierna la ejecución y el contrato revolutions-hop/v1
metodo-manifiestos-ai      produce el paquete de constitución y la política de relevo
manifiestos-trabajo-ai     conserva la intención humana aprobada y su identidad exacta
```

Este documento describe únicamente el transporte. Cuando necesita una regla ajena la referencia
por repositorio, path y contrato, sin reproducir su texto y sin congelar un SHA de esos
documentos.

La cadena completa del sistema es autoridad de `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.
