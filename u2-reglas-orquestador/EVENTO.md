# EVENTO — U2 reglas del orquestador

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@67f0d8f3d8e768e4c1c17cef49c6aeda669884cf` y
`audit-chatgpt-i@0ae8d8525c7ac0f6b84f547af44a1d00dfb59b03`.

La auditoría aplicable cerró `U1`, aceptó como cambio local la ampliación a siete contratos
transversales, y dejó una observación no bloqueante sobre verificación previa.

## Observación D-01 de la auditoría de U1

Acepto la clasificación. La corrida de encabezados de `U1` era discriminante —mecanismo,
propiedad, resultado que podía pasar o fallar, y control negativo explícito— y por lo tanto debió
proponerse y congelarse antes de ejecutarse.

Su resultado queda excluido de la evidencia y no es precedente. Esta unidad propone su contrato
antes de tocar el mecanismo: al cerrar esta intervención no existe ninguna mitad ejecutada, ni
código del verificador escrito, ni corrida parcial, ni resultado observado.

## Qué hizo y por qué

Produjo el candidato `u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`, documento autoritativo de
`CT-7` conforme a la asignación cerrada en `U1`.

Cada regla quedó redactada como una comparación, una selección o una detención sobre campos ya
presentes en el sobre, para que el manifiesto pueda cumplirse: que el documento sea implementable
por código determinista sin un modelo razonador.

### Frontera deliberada respecto del contrato de transporte

El documento no reproduce el contrato `revolutions-hop/v1`. Esa es la decisión de diseño que más
condiciona su redacción, y merece quedar explícita porque la línea es fina.

Las validaciones `V1`–`V8` describen **qué comprueba el orquestador**, que es comportamiento
propio del orquestador. La forma del sobre, sus campos y sus tres combinaciones admitidas siguen
siendo autoridad de REVOLUTIONS §4.1, y por eso `V8` no las enumera: exige que la combinación
recibida sea una de las que el contrato admite, sin copiarlas.

Si `V8` las hubiera enumerado, cualquier evolución futura del contrato dejaría dos superficies
que habría que sincronizar, que es la propiedad que `D7` protege.

La misma frontera se aplicó a la cadencia de relevo: el documento declara que el orquestador no
cuenta, no deriva y no decide relevos —comportamiento propio— y referencia `CT-3` para la
política, que pertenece a `METODO-MANIFIESTOS.md`.

---

## Contrato previo de verificación — PROPUESTO, NO EJECUTADO

Conforme a REVOLUTIONS §6.1 y `PLAN.md` §5.2. Ninguna mitad se ejecuta hasta que el AUDITOR lo
evalúe y lo congele. Si lo devuelve por insuficiente, se propone uno nuevo; no se ejecuta el
mecanismo mientras tanto.

### Candidato exacto

```text
repositorio  https://github.com/francogg89-ai/work-claude-i
path         u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
blob         49ad9e04a6ea2f04e4ec6f1f0efd2c5adf51f367
```

El commit que contiene ese blob es el que esta intervención cierra. La identidad del blob se
declara aquí porque es la única que puede escribirse dentro del commit que la crea.

### Propiedad que debe demostrarse

Que las reglas del candidato son mecánicamente aplicables y discriminantes: que una
implementación determinista que sólo aplique lo que el documento declara acepta exactamente los
casos que el documento declara válidos, rechaza exactamente los que declara inválidos, y atribuye
cada rechazo a una regla concreta del documento.

La propiedad tiene tres partes, que se demuestran juntas:

```text
P-A  validación de forma, sucesión de turn_id y resolución de next_instance
P-B  frontera de DETENER, reanudación literal por CONTINUAR y transporte de directiva humana
P-C  la cadencia de relevo es derivable fuera del orquestador desde historias Git reales
```

`P-C` no verifica la política de relevo, que pertenece a `CT-3`. Verifica lo que el candidato
afirma: que la derivación existe fuera del orquestador y que el orquestador no la necesita para
transportar.

### Entorno y fuentes relevantes

```text
entorno   Windows local bajo C:\Franco_Metodos_AI, dentro del perímetro constitutivo
fuentes   para P-A y P-B: un corpus de sobres y secuencias definido dentro de la unidad,
          sin sobres reales del loop y sin secretos
          para P-C: las historias Git reales de work-claude-i y audit-chatgpt-i, sobre el
          corte exacto que el AUDITOR congele junto con este contrato
```

El corpus se construye dentro de la unidad y se publica con la corrida, para que el AUDITOR pueda
reejecutar el mecanismo sobre las mismas entradas.

### Mecanismo

Un verificador determinista, sin modelo de lenguaje y sin red, ubicado en
`u2-reglas-orquestador/`. Implementa únicamente lo que el documento declara: `V1`–`V8`, la regla
de sucesión de `§5`, la resolución de `§6` incluido el fail-closed de `§6.1`, y las transiciones
de `§9`. Para `P-C` invoca las operaciones Git de sólo lectura que `D1` del plan define.

Cada caso del corpus declara la regla del documento que lo gobierna y el resultado que el
documento predice. El verificador no conoce el resultado esperado: lo produce, y la comparación es
posterior.

Se ejecuta una vez. Un contrato se agota al producir su resultado; una corrida nueva necesita un
contrato nuevo.

### Criterio discriminante de éxito

Se satisface si y sólo si se cumplen las cuatro condiciones:

```text
E1  para cada caso del corpus, el resultado producido es idéntico al que el documento predice
E2  cada rechazo cita la regla concreta del candidato que lo produjo
E3  toda regla mecánica del candidato tiene al menos un caso que la ejercita
E4  P-C reproduce, sobre el corte congelado, los mismos números que las operaciones Git
    de D1 producen ejecutadas de forma independiente
```

`E3` existe porque un corpus que sólo ejercita las reglas cómodas no demuestra que el documento
sea aplicable: demuestra que una parte lo es.

### Criterio discriminante de fallo

Se declara fallo si ocurre cualquiera de estas condiciones:

```text
F1  algún caso produce un resultado distinto del que el documento predice
F2  algún rechazo no puede atribuirse a una regla declarada del candidato
F3  alguna regla mecánica del candidato queda sin caso que la ejercite
F4  el mecanismo necesita, para decidir un caso, una regla que el candidato no declara
F5  P-C no reproduce los números de la derivación independiente
```

`F4` es el criterio que detecta el defecto más probable de este documento: una regla escrita con
suficiente ambigüedad como para que la implementación deba completarla por su cuenta. Si eso
ocurre, el defecto está en el candidato, no en el mecanismo.

Toda observación de la corrida se resuelve dentro de estos criterios. No existe una tercera
categoría ni salida por limitación del escenario.

### Control negativo

La propiedad podría satisfacerse por accidente: un verificador que aceptara todo produciría `E1`
sobre un corpus compuesto sólo por casos válidos.

Por eso el corpus incluye casos que el mecanismo **debe** rechazar, y su aceptación es fallo:

```text
N1  human_need distinto de null junto con next_prompt distinto de null
N2  final en true junto con human_need distinto de null
N3  turn_id repetido, salteado o retrocedido respecto del último transportado
N4  next_instance "fresh" con next_actor null
N5  next_instance con un valor fuera de {"current", "fresh", null}
N6  work_id que no corresponde al trabajo transportado
N7  protocol distinto de "revolutions-hop/v1"
N8  instancia current perdida: el mecanismo debe detenerse y no degradar el salto a fresh
N9  DETENER con un sobre CONSTRUCTOR -> AUDITOR ya pendiente: debe detener sin entregarlo
```

`N8` es el control negativo más importante del conjunto. Es la única condición en la que un
orquestador defectuoso podría continuar funcionando de forma aparentemente correcta mientras
fabrica un actor que ningún actor del método decidió.

Si el mecanismo acepta cualquiera de `N1`–`N9`, la corrida es fallo aunque todos los casos
positivos pasen.

### Limitaciones conocidas

- El corpus es finito. Demuestra que las reglas discriminan sobre los casos declarados, no que
  ninguna entrada imaginable las eluda.
- El mecanismo implementa el candidato; no es la implementación de referencia de un orquestador
  real ni se promueve a `reglas-orquestador-ai`. Una corrida local no demuestra que un
  orquestador desplegado se comporte así, y decirlo es parte de la entrega.
- `P-C` se apoya en dos historias Git que en este corte son cortas y lineales. Demuestra que la
  derivación produce el número correcto sobre ellas, no que se comporte igual sobre una historia
  con merges: esa propiedad la sostiene la definición de `D1`, que cuenta el conjunto alcanzable
  completo, y no esta corrida.
- `P-B` verifica las transiciones declaradas, no el comportamiento de un proceso real bajo una
  interrupción concurrente.

---

## Qué verificó esta intervención

Nada. Esta intervención construye el candidato y propone el contrato.

La revisión de que el documento cubre las obligaciones de `CT-7` es lectura de diseño y
corresponde al AUDITOR, que tiene acceso directo al candidato y a las fuentes.

## Limitaciones de esta entrega

- El texto normativo de `CT-7` queda escrito, pero su suficiencia operacional no está demostrada
  hasta que la corrida bajo contrato congelado la ejercite.
- `REGLAS-ORQUESTADOR.md` referencia `CT-1`, `CT-2` y `CT-3`, cuyos documentos autoritativos
  todavía no existen. Las referencias son por repositorio, path y contrato, y no congelan SHA,
  por lo que no crean dependencia circular ni quedan rotas cuando esos documentos se escriban.

## Resultado

`u2-reglas-orquestador/REGLAS-ORQUESTADOR.md`, candidato de `CT-7`, y este contrato previo
propuesto y no ejecutado.

## Necesidad humana detectada

Ninguna.
