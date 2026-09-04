# PLAN — Ecosistema de constitución y orquestación para REVOLUTIONS — ORCHESTRA

Describe cómo alcanzar el manifiesto de constitución
`manifiestos-trabajo-ai@bb985e6580fbb8208f141a2af7646815bd1f7cdc:manifiestos/revolutions-orchestra-ai/MANIFIESTO_TRABAJO.md`
bajo `revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c`.

No declara versión, aceptación, vigencia, apertura ni cierre de unidades: eso se deriva de Git
y del material de `audit-chatgpt-i` conforme al protocolo de derivación.

---

## 1. Resultado buscado

Tres documentos autoritativos, mutuamente coherentes, publicados en sus repositorios destino:

```text
metodo-manifiestos-ai      METODO-MANIFIESTOS.md
reglas-orquestador-ai      REGLAS-ORQUESTADOR.md
manifiestos-trabajo-ai     README.md + plantillas/ (sin alterar manifiestos/ ya publicado)
```

No son tres documentos independientes: son una sola especificación repartida en tres
superficies con interfaces explícitas entre sí y compatibles con el método autoritativo.

---

## 2. Unidades

Las unidades existen sólo donde hay una división real de materia y de dependencia. No se crean
por simetría con los tres repositorios destino: `U1` y `U5` existen porque resuelven problemas
que no pertenecen a ningún documento destino en particular.

```text
u1-contratos-transversales/     decisiones compartidas por los tres documentos
u2-reglas-orquestador/          REGLAS-ORQUESTADOR.md
u3-metodo-manifiestos/          METODO-MANIFIESTOS.md
u4-biblioteca-manifiestos/      README.md y plantillas de manifiestos-trabajo-ai
u5-verificacion-y-promocion/    verificación cruzada, ejemplo end-to-end, promoción, informe
```

Cada unidad contiene su `EVENTO.md` y sus materiales fundamentales. Una intervención toca el
directorio de una sola unidad, o la raíz cuando es previa a toda unidad.

### 2.1. Por qué U1 es una unidad y no un cuarto documento

`U1` no produce texto para copiar dentro de los tres documentos destino. Produce la asignación de
autoridad de `D7`: qué documento es la única fuente normativa de cada contrato transversal y cómo
los demás lo referencian.

Decidir esa asignación antes de escribir tres documentos protege una propiedad material: una
contradicción detectada tarde obligaría a corregir tres superficies en lugar de una, y una regla
escrita dos veces obligaría a mantener sincronizadas dos superficies para siempre.

`U1` es materia de trabajo y no se promueve a ningún repositorio destino. Si sobreviviera como
documento publicado sería una cuarta autoridad que repite reglas, exactamente lo que el
manifiesto excluye en sus secciones 20 y 21.

### 2.2. Mapeo de promoción

```text
u2-reglas-orquestador/REGLAS-ORQUESTADOR.md
    -> reglas-orquestador-ai : REGLAS-ORQUESTADOR.md

u3-metodo-manifiestos/METODO-MANIFIESTOS.md
    -> metodo-manifiestos-ai : METODO-MANIFIESTOS.md

u4-biblioteca-manifiestos/README.md
    -> manifiestos-trabajo-ai : README.md

u4-biblioteca-manifiestos/plantillas/MANIFIESTO_TRABAJO.md
    -> manifiestos-trabajo-ai : plantillas/MANIFIESTO_TRABAJO.md

u4-biblioteca-manifiestos/plantillas/PROJECT.md
    -> manifiestos-trabajo-ai : plantillas/PROJECT.md
```

`u1-contratos-transversales/` y `u5-verificacion-y-promocion/` no tienen destino: son materia de
trabajo y evidencia.

`manifiestos/revolutions-orchestra-ai/MANIFIESTO_TRABAJO.md` no se toca. La promoción a
`manifiestos-trabajo-ai` agrega paths y no modifica los existentes.

---

## 3. Dependencias y secuencia

```text
U1 --> U2 --> U3 --> U4 --> U5
```

- `U1` precede a todo: asigna, conforme a `D7`, la autoridad normativa única de cada contrato
  transversal y las relaciones de referencia entre documentos. No ordena repetir el texto
  normativo en varios destinos. `U2`, `U3` y `U4` dependen de esa asignación, y no unas de otras
  por su contenido.
- `U2` sigue a `U1` porque es la superficie más cerrada y mecánica, y fija el contorno exacto
  del paquete de constitución que `U3` debe producir.
- `U3` sigue a `U2` porque `metodo-manifiestos-ai` produce lo que el orquestador consume en el
  arranque externo.
- `U4` sigue a `U3` porque la biblioteca guarda exactamente lo que ese método publica.
- `U5` sigue a las tres porque la verificación cruzada exige las tres superficies materiales.

Las dependencias son de contrato, no de calendario. Una corrección en `U1` obliga a revisar el
impacto en `U2`, `U3` y `U4`; ese impacto se trata como cambio de plan si altera secuencia,
criterios de terminación o decisiones técnicas.

---

## 4. Decisiones técnicas

### D1. Política periódica de relevo derivable desde Git

El manifiesto exige cadencia periódica sin contadores vivos, con la propiedad `10, 20, 30...` y
no `10 desde el último relevo`.

Hechos Git que cuentan:

```text
entrega autoritativa del CONSTRUCTOR   = un commit de work-*  alcanzable desde el corte
intervención autoritativa del AUDITOR  = un commit de audit-* alcanzable desde el corte
```

La equivalencia es exacta por `P1` y `P2`: una intervención principal es un commit autoritativo y
todo commit de `work-*` es una entrega. No existen commits de control, de modo que el conjunto
contable no necesita ningún filtro que los excluya.

Ese conjunto es el de los commits alcanzables desde el corte. La derivación cuenta ese conjunto,
no un recorrido sobre él:

```text
N_CONSTRUCTOR = git -C <work>  rev-list --count <corte-work>
N_AUDITOR     = git -C <audit> rev-list --count <corte-audit>

corresponde relevo cuando  N % <cadencia> == 0
```

`rev-list --count` sin filtros cuenta cada commit alcanzable exactamente una vez, cualquiera sea
la topología de la historia.

No se usa `--first-parent`: ese recorrido omite los commits alcanzables por los padres
secundarios de un merge, que `P2` también declara entregas, de modo que ante una historia válida
con merges produciría un número menor que el conjunto normativo. La cadencia dejaría de
corresponder a las intervenciones autoritativas reales, y ningún invariante del método garantiza
que ambas cuentas coincidan.

Tampoco se filtra por path ni se leen mensajes de commit: no existe convención de commits que
sostenga tal filtro y ninguna operación del protocolo de derivación los lee.

Propiedades que esto satisface:

- no persiste estado mutable: `CONSTRUCTOR_COUNT` y `AUDITOR_COUNT` no existen;
- la cadencia es absoluta sobre múltiplos, de modo que un relevo manual no la reinicia;
- el contador conceptual pertenece al trabajo y no a la instancia que ocupa el rol;
- las intervenciones auditoras con `human_need`, las que preservan una decisión humana y la que
  emite `final=true` cuentan igual que cualquier otra, porque todas son commits de `audit-*`;
  no hace falta `relay_pending` ni una taxonomía de intervenciones;
- el commit de bootstrap de cada actor es su primera intervención autoritativa y cuenta como
  tal, lo que hace la regla uniforme y sin excepciones;
- la derivación no supone linealidad ni ausencia de merges, de modo que no depende de una
  propiedad de la historia que este plan no puede garantizar;
- el resultado es un hecho ligado a un corte exacto y no una verdad presente que envejezca: dos
  actores que lo derivan sobre el mismo SHA obtienen el mismo número;
- el ORQUESTADOR no la evalúa: la deriva el actor con autoridad, y el orquestador sólo ejecuta
  `next_instance`.

La cadencia concreta es política inicial de ejecución y llega por constitución al bootstrap. No
pertenece al manifiesto salvo que el humano la considere parte material de su intención. Esta
corrida no aplica cadencia automática; el diseño sí debe definirla y dejarla verificable.

### D2. Descubrimiento de modificaciones concurrentes sin estado central

El manifiesto excluye un `EVENT.md` central, la lista viva de carriles y el registro redundante
de mutaciones, y exige poder descubrir y verificar modificaciones materiales pertinentes de
otros trabajos sobre el mismo proyecto.

Mecanismo: los repositorios compartidos son su propia fuente. `PROJECT.md` declara superficies
estables como `repositorio + conjunto de paths`, y la constitución declara qué superficie puede
afectar este trabajo. Antes de una mutación material sobre una superficie compartida:

```text
1  tomar el corte constitutivo de ese repositorio, congelado en el bootstrap
2  leer la referencia actual del mismo repositorio en su remoto
3  git diff --name-only <corte> <referencia actual>
4  intersectar los paths modificados con la superficie propia declarada
5  intersección vacía      -> compatibilidad demostrable, procede
   intersección no vacía   -> compatibilidad no demostrable: no procede por presunción
```

No requiere saber qué otros trabajos existen ni consultar un registro: lo que otro trabajo
modificó ya está demostrado por el repositorio compartido. El `PROJECT_SHA` del bootstrap sigue
siendo identidad de origen y no se reescribe por haber consultado la vigencia.

Ante intersección no vacía el CONSTRUCTOR preserva y entrega; el AUDITOR determina si el
conflicto se resuelve técnicamente o si existe NECESIDAD DEL HUMANO.

### D3. Punto de extensión para fuentes auxiliares

Las fuentes auxiliares de lecciones, incidentes, experimentos y skills viajan dentro de
`SOURCE_REPOS`, con repositorio, identidad exacta y función declarada, y son de sólo lectura. No
se modifica `revolutions-hop/v1` y no se agrega ningún campo al sobre.

La regla que el diseño debe dejar explícita:

> una skill puede explicar cómo realizar una acción; nunca autoriza por sí misma a realizarla.

Las capacidades se siguen derivando de la constitución más las decisiones humanas posteriores,
según `P7` y `D6` del método. Este trabajo no diseña la taxonomía de skills.

### D4. Vía exacta de promoción final y su verificación

REVOLUTIONS impide estructuralmente que el CONSTRUCTOR escriba en los tres repositorios destino,
y esa frontera no es delegable. La promoción se prepara como material exacto y se rutea:

```text
1  el material destino vive en work-claude-i con su forma final
2  U5 produce la tabla de promoción: por cada archivo, path de origen, path de destino,
   repositorio de destino y SHA de blob exacto
3  U5 produce u5-verificacion-y-promocion/CHECKPOINT_HUMANO.md, autocontenido, con el prompt
   listo para un agente externo, sin secretos
4  el CONSTRUCTOR cierra su intervención y entrega; no declara que la necesidad es real
5  el AUDITOR comprueba si es humana, si es material y si el checkpoint alcanza; si corresponde,
   detiene el loop con una necesidad de tipo material
6  resuelta la promoción, la evidencia que vuelve es FINAL_SHA, PATHS y BLOB_SHAS por repositorio
```

Verificación independiente de la promoción: el SHA de blob de Git es función del contenido y no
del repositorio. Para cada archivo promovido, el blob publicado en el `main` del destino debe ser
idéntico al blob del mismo contenido en `work-claude-i` al `WORK_SHA` declarado. Eso hace la
promoción exacta y comprobable byte a byte desde GitHub, sin confiar en el reporte de nadie, y
satisface la relectura exigida antes del cierre definitivo.

`.gitattributes` fija `* text=auto eol=lf` desde el commit raíz para que esa identidad de blob no
dependa de la plataforma local.

### D5. Verificación ejecutable dentro de la unidad que produce lo verificado

El manifiesto pide que `reglas-orquestador-ai` pueda implementarse mediante código determinista
sin un LLM razonador, y que las pruebas observen exactamente las reglas declaradas y no una
aproximación narrativa.

Regla de ubicación: cada unidad construye y ejecuta la verificación discriminante de su propia
materia. Ninguna unidad depende, para poder cerrarse, de material que este plan ubique en una
unidad posterior.

```text
U2  construye y ejecuta el verificador determinista de las reglas del orquestador:
    forma del sobre, combinaciones human_need/final, sucesión exacta de turn_id,
    valores admitidos de next_instance, transiciones de DETENER y CONTINUAR, y la
    cadencia de D1 evaluada contra las historias Git reales de work-claude-i y
    audit-chatgpt-i

U3  ejercita el descubrimiento de concurrencia de D2 con operaciones Git reales sobre
    superficies declaradas, incluido un solapamiento material no resuelto

U5  ejercita la verificación cruzada del manifiesto sobre las tres superficies ya
    construidas, y la identidad de blob del mapeo de promoción
```

El verificador de `U2` es evidencia y vive únicamente en `work-claude-i`, bajo
`u2-reglas-orquestador/`. No se promueve: el manifiesto restringe cada repositorio destino a su
documento autoritativo más lo materialmente necesario, y una implementación de referencia
publicada competiría con el documento como fuente de verdad.

### D6. Tratamiento de contradicciones entre manifiesto y método

Si un requisito del manifiesto contradice materialmente al método autoritativo, se elige la
solución mínima que conserve las autoridades de REVOLUTIONS y no cree una segunda fuente de
verdad. La contradicción y la decisión adoptada se explican en el `EVENTO.md` de la unidad donde
aparecen. No se modifica `revolutions-orchestra-ai`.

### D7. Autoridad única por contrato transversal

Un contrato transversal se escribe en un solo documento. Los demás lo referencian por
`repositorio + path + nombre del contrato`, sin reproducir su texto normativo y sin congelar un
SHA del documento citado, para no crear dependencias SHA circulares entre documentos que se citan
mutuamente.

```text
contrato de transporte revolutions-hop/v1
    autoridad: revolutions-orchestra-ai — método autoritativo, que no se redefine ni se amplía

mecánica del orquestador: validaciones mínimas, next_instance, turn_id, loop ordinario,
DETENER, CONTINUAR, directivas humanas durante la pausa, estado efímero, fail-closed
    autoridad: reglas-orquestador-ai : REGLAS-ORQUESTADOR.md

política periódica de relevo derivable de D1 y su llegada a la constitución
    autoridad: metodo-manifiestos-ai : METODO-MANIFIESTOS.md

descubrimiento de concurrencia de D2 y semántica de PROJECT.md
    autoridad: metodo-manifiestos-ai : METODO-MANIFIESTOS.md

admisión de fuentes auxiliares y regla de que una skill no autoriza, de D3
    autoridad: metodo-manifiestos-ai : METODO-MANIFIESTOS.md

estructura de paths de la biblioteca y reglas de creación y modificación
    autoridad: manifiestos-trabajo-ai : README.md
```

Una regla que describe el comportamiento propio del orquestador pertenece a
`REGLAS-ORQUESTADOR.md` aunque hable de una política ajena. Que el orquestador no evalúa la
cadencia ni decide relevos es comportamiento del orquestador; la política de relevo sigue
viviendo en `METODO-MANIFIESTOS.md`. Esa frontera es lo que distingue referenciar de duplicar.

---

## 5. Verificaciones

### 5.1. Por unidad

- `U1`: cada contrato transversal responde qué información irreducible conserva o qué propiedad
  material protege, y tiene exactamente un documento asignado como autoridad; los que no
  responden no existen.
- `U2`: el verificador construido en la propia unidad ejercita las validaciones mínimas,
  `next_instance`, `turn_id`, el loop ordinario, DETENER y CONTINUAR contra entradas explícitas
  —incluidas las que deben ser rechazadas— y la cadencia de `D1` contra historias Git reales.
- `U3`: recorrido de la entrevista sobre un caso que produce constitución completa y sobre un
  caso aislado que no necesita `PROJECT.md`; y ejercicio del descubrimiento de concurrencia de
  `D2`, incluido un solapamiento material que no debe resolverse por presunción.
- `U4`: la estructura de paths y las reglas de creación y modificación se comprueban contra el
  contenido real ya publicado en `manifiestos-trabajo-ai`.
- `U5`: los treinta y cuatro puntos de verificación cruzada del manifiesto, cada uno contra la
  superficie concreta que lo satisface, y la identidad de blob de cada archivo del mapeo de
  promoción.

### 5.2. Contrato previo

Toda verificación discriminante se propone en el `EVENTO.md` de su unidad antes de ejecutarse:
candidato exacto, propiedad a demostrar, entorno o fuente, mecanismo, criterio de éxito, criterio
de fallo, control negativo y limitaciones conocidas. No se ejecuta ninguna mitad hasta que el
AUDITOR la congele. El criterio no se redefine después de observar el resultado.

Las verificaciones ubicadas por `D5` y las tres pruebas obligatorias del manifiesto son
discriminantes y requieren ese contrato.

### 5.3. Evidencia preservada

De cada verificación ejecutada se preserva el comando o acción, los parámetros no sensibles
relevantes, la salida, el código de retorno y las limitaciones conocidas. Un resultado local no
demuestra una propiedad que sólo puede verificarse en el entorno real, y decirlo es parte de la
entrega.

---

## 6. Criterios de terminación

### 6.1. Por unidad

- `U1`: los contratos transversales están escritos, cada uno justifica su existencia, y ninguno
  duplica una regla que REVOLUTIONS ya fija.
- `U2`: `REGLAS-ORQUESTADOR.md` cubre arranque externo, contrato de transporte, validaciones
  mínimas, `next_instance`, `turn_id`, loop ordinario, lo que el orquestador no hace, DETENER,
  CONTINUAR, directivas humanas durante la pausa, estado efímero y comportamiento fail-closed;
  y el verificador construido en esta misma unidad ejercita esas reglas.
- `U3`: `METODO-MANIFIESTOS.md` lleva una idea informal hasta manifiesto, constitución y paquete
  de arranque, con cierre humano explícito, y sin decidir durante la ejecución lo que corresponde
  al CONSTRUCTOR, al AUDITOR o al HUMANO.
- `U4`: `README.md` explica qué guarda y qué no guarda la biblioteca, su estructura de paths, sus
  reglas de creación y modificación, el rol de Git, `PROJECT.md` opcional y su relación con
  `metodo-manifiestos-ai` y con REVOLUTIONS; las plantillas existen sólo si aportan utilidad real.
- `U5`: la verificación cruzada está ejecutada punto por punto, el ejemplo end-to-end es
  completo, la tabla de promoción es exacta y el checkpoint alcanza para un agente externo.

### 6.2. Del trabajo

El trabajo alcanza el manifiesto cuando los tres documentos están publicados en el `main` de sus
repositorios destino, el contenido publicado fue releído desde GitHub y coincide por identidad de
blob con el material de `work-claude-i`, y el informe final del manifiesto está producido con
`FINAL_SHA`, `PATHS` y `BLOB_SHAS` por repositorio. Declarar terminado el trabajo es un veredicto
del AUDITOR.

---

## 7. Riesgos

- **Sobrearquitectura.** Tres documentos que repiten las mismas reglas producirían dobles fuentes
  de verdad. Mitigación: `D7` asigna a cada contrato transversal un único documento autoritativo
  y los demás lo referencian; `U1` decide esa asignación y no se publica.
- **Unidad que no puede cerrarse con su propio material.** Un criterio de terminación que
  dependiera de una unidad posterior haría inauditable el cierre en el momento que corresponde.
  Mitigación: la regla de ubicación de `D5`.
- **Contradicción manifiesto/método detectada tarde.** Mitigación: `D6` y el orden `U1` primero.
- **Ampliación ficticia del perímetro en la promoción.** Escribir en un repositorio destino sería
  un cambio de intención disfrazado de conveniencia. Mitigación: `D4` rutea la promoción por el
  mecanismo de necesidad humana material del método.
- **Dependencia SHA circular.** Los tres repositorios destino son salidas de este trabajo y no
  pueden ser autoridades constitutivas con un SHA previo a su construcción. Mitigación: los
  documentos declaran dependencias por repositorio, path y contrato; las ejecuciones concretas
  congelan SHAs disponibles al constituir.
- **Verificación narrativa.** Las pruebas obligatorias exigen observar las reglas declaradas.
  Mitigación: `D5` y los contratos previos de `5.2`.
- **Información indispensable atrapada en `_info_local`.** Esa carpeta no es autoridad, puede
  desaparecer y su contenido no es reconstruible desde ninguna fuente durable. Mitigación: nada
  indispensable sobrevive sólo allí; todo lo necesario para continuar o auditar vive en Git antes
  de entregar.
- **Divergencia de normalización de fin de línea.** Rompería la verificación por identidad de
  blob. Mitigación: `.gitattributes` desde el commit raíz.

---

## 8. Intervenciones humanas previsibles

Anticiparlas permite planificar; no las habilita por adelantado. Cuando llegue el momento, el
AUDITOR comprueba primero si siguen siendo necesarias.

1. **Decisión humana sobre este plan.** Se conserva en `audit-chatgpt-i` ligada al SHA exacto al
   que se refiere. El mismo SHA puede pasar de revisión a esa decisión sin modificarse.
2. **Promoción final a los tres repositorios destino.** Necesidad material previsible, con
   checkpoint conforme a `D4`. Puede dejar de serlo si el humano provee otra vía compatible con
   las fronteras estructurales de los roles.
3. **Cadencia concreta de relevo periódico**, si el humano decide aplicarla a corridas futuras.
   Es política inicial de ejecución y llega por constitución, no por este plan.

Ninguna decisión técnica se traslada al humano para evitar resolverla.
