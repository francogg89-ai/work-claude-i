# Contratos transversales

Asignación de autoridad normativa única y relaciones de referencia entre los tres documentos
destino, conforme a `PLAN.md` §2.1 y `D7`.

## Qué es y qué no es este documento

Es materia de trabajo. No se promueve a ningún repositorio destino y no es autoridad sobre
ninguna regla.

No contiene el texto normativo de ningún contrato. Cada contrato se escribe una sola vez, en el
documento que esta asignación le da como autoridad, durante la unidad correspondiente. Escribirlo
aquí y copiarlo después crearía dentro de `work-claude-i` una segunda superficie que habría que
mantener sincronizada, que es la propiedad que `D7` protege.

Lo que sí fija, por contrato:

- qué información irreducible conserva o qué propiedad material protege;
- qué documento es su única autoridad normativa;
- qué obligaciones debe satisfacer ese documento al escribirlo;
- qué dicen los demás documentos cuando necesitan la regla;
- qué no redefine, porque ya es autoridad de REVOLUTIONS.

## Regla de referencia

Un documento que necesita una regla ajena la referencia por `repositorio + path + nombre del
contrato`. No reproduce su texto normativo y no congela un SHA del documento citado.

La restricción sobre el SHA existe porque los tres documentos se citan mutuamente: congelar
identidades exactas entre ellos produciría el ciclo `A contiene el SHA de B` y `B contiene el SHA
de A` que el manifiesto excluye. Las ejecuciones concretas sí congelan los SHAs disponibles al
constituir; los documentos metodológicos declaran dependencias por repositorio, path y contrato.

Una regla que describe el comportamiento propio de un documento le pertenece aunque hable de una
materia ajena. Que el ORQUESTADOR no evalúa la cadencia de relevo es comportamiento del
ORQUESTADOR y pertenece a `REGLAS-ORQUESTADOR.md`; la política de relevo sigue perteneciendo a
`METODO-MANIFIESTOS.md`. Esa frontera es la que distingue referenciar de duplicar.

---

## CT-1 — Cadena del sistema y frontera funcional entre los tres documentos

**Qué conserva.** Ninguno de los tres repositorios puede inferir por sí mismo su lugar en la
cadena ni dónde termina su competencia. REVOLUTIONS gobierna la ejecución y no describe esta
arquitectura, porque estos tres documentos no existían cuando se definió.

**Autoridad.** `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

Es el único documento que necesita conocer la cadena completa para producir un paquete de
constitución: parte de una intención informal y debe terminar en algo que el ORQUESTADOR pueda
consumir sin interpretar.

**Obligaciones del documento autoritativo.** Expresar la cadena `metodo-manifiestos-ai` produce →
`manifiestos-trabajo-ai` congela intención y vínculo con proyecto → paquete de constitución
inicia → `reglas-orquestador-ai` transporta → `revolutions-orchestra-ai` gobierna la ejecución.
Declarar que ninguno sustituye a otro y que ninguno amplía las autoridades de REVOLUTIONS.

**Referencia de los demás.** `REGLAS-ORQUESTADOR.md` y el `README.md` de la biblioteca declaran su
propia función y sus propios límites —lo cual es autodescripción, no duplicación— y referencian
`CT-1` para la cadena completa.

**No redefine.** Las autoridades de REVOLUTIONS §5, la separación estructural de escritura de
`§5.1` del método ni los archivos de rol.

---

## CT-2 — Contrato del paquete de constitución

**Qué conserva.** El primer AUDITOR de un trabajo no llega desde un sobre anterior: recibe un
paquete de constitución y todavía no existe ningún `BOOTSTRAP.md`. REVOLUTIONS §2.6 fija qué
hechos preserva ese bootstrap, pero no la forma del paquete que permite construirlo. Sin este
contrato, cada arranque externo inventaría su propia forma.

**Autoridad.** `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

Es el documento que produce el paquete; la forma pertenece a quien la produce.

**Obligaciones del documento autoritativo.** Fijar el conjunto de campos aplicables —`WORK_ID`,
carril, identidad exacta del método, identidad exacta del manifiesto, identidad exacta de
`PROJECT.md` cuando exista, repositorio de trabajo, repositorio de auditoría, repositorios fuente,
raíz local, paths locales, entornos, capacidades por actor, referencias seguras a credenciales y
políticas iniciales de ejecución—, cuáles son obligatorios y cuáles sólo cuando aplican, y que
ningún valor secreto viaja en el paquete: viaja la referencia segura, nunca el valor.

**Referencia de los demás.** `REGLAS-ORQUESTADOR.md` declara que en el arranque externo recibe el
paquete y abre una instancia inicial de AUDITOR sin interpretarlo ni completarlo, y referencia
`CT-2` para su forma.

**No redefine.** REVOLUTIONS §2.6, que sigue siendo la autoridad sobre qué registra el bootstrap.
El paquete es la entrada; el bootstrap es el hecho durable que el AUDITOR construye con ella.

---

## CT-3 — Política periódica de relevo derivable

**Qué conserva.** La cadencia debe ser derivable de hechos Git y no persistirse como estado
mutable. REVOLUTIONS define quién decide un relevo y cómo se ejecuta, pero no una política
periódica: es una política inicial de ejecución que el humano elige.

**Autoridad.** `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

Es quien pregunta al humano qué política quiere y la lleva a la constitución.

**Obligaciones del documento autoritativo.** Definir inequívocamente qué hecho Git cuenta como
entrega del CONSTRUCTOR y cuál como intervención del AUDITOR; que el conjunto contable es el de
commits alcanzables desde el corte exacto y se cuenta completo, sin recorrido por primer padre,
sin filtro por path y sin leer mensajes de commit; que la cadencia opera sobre múltiplos absolutos
de modo que un relevo manual no la reinicia; que el contador conceptual pertenece al trabajo y no
a la instancia; que las intervenciones auditoras con necesidad humana, las que preservan una
decisión humana y la que cierra el trabajo cuentan como cualquier otra; y que no existe
`relay_pending` ni contador persistido.

**Referencia de los demás.** `REGLAS-ORQUESTADOR.md` declara, como regla propia, que el
ORQUESTADOR no cuenta, no deriva y no decide relevos, y que ejecuta literalmente
`next_instance`; referencia `CT-3` para la política.

**No redefine.** REVOLUTIONS §12.2 y §12.3, que fijan la mecánica del relevo de cada rol y quién
tiene autoridad para disponerlo.

---

## CT-4 — Descubrimiento de concurrencia y semántica de `PROJECT.md`

**Qué conserva.** Dos trabajos sobre un mismo proyecto no pueden inferir la compatibilidad de sus
perímetros materiales, y el manifiesto excluye resolverlo con un registro central, una lista viva
de carriles o un `EVENT.md` que replique lo que los repositorios ya demuestran.

**Autoridad.** `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

Es quien cierra con el humano si el trabajo puede coexistir con otros y con qué precisión.

**Obligaciones del documento autoritativo.** Definir `PROJECT.md` como contrato estable de
vinculación y no como base viva; qué puede contener y qué no puede registrar; cómo se declara una
superficie como `repositorio + conjunto de paths`; y el procedimiento de comprobación previo a una
mutación material sobre superficie compartida: comparar el corte constitutivo congelado en el
bootstrap contra la referencia actual del mismo repositorio, intersectar los paths modificados con
la superficie propia declarada, y no proceder por presunción cuando la intersección no es vacía.
Debe dejar explícito que consultar la vigencia no reescribe el `PROJECT_SHA` constitutivo, y que
un trabajo aislado no necesita `PROJECT.md`.

**Referencia de los demás.** El `README.md` de la biblioteca declara `PROJECT.md` como path
opcional junto al manifiesto y sus reglas de creación y modificación, y referencia `CT-4` para su
semántica.

**No redefine.** REVOLUTIONS §9, que fija el tratamiento del drift y de la concurrencia material,
ni el circuito CONSTRUCTOR detecta → preserva y entrega → AUDITOR determina.

---

## CT-5 — Fuentes auxiliares y no ampliación de autoridad

**Qué conserva.** Una fuente de lecciones, incidentes, experimentos o skills puede ser
materialmente útil sin que su existencia amplíe permisos. Esa distinción no es inferible del
hecho de que un repositorio esté declarado en la constitución.

**Autoridad.** `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`.

Es quien determina si una fuente auxiliar es útil para una ejecución y cómo localizarla de forma
exacta sin cargar indiscriminadamente su contenido.

**Obligaciones del documento autoritativo.** Declarar que las fuentes auxiliares viajan dentro de
`SOURCE_REPOS` con repositorio, identidad exacta y función, que son de sólo lectura, y la regla
explícita de que una skill puede explicar cómo realizar una acción y nunca autoriza por sí misma a
realizarla. Las capacidades se siguen derivando de la constitución más las decisiones humanas
posteriores.

**Referencia de los demás.** `REGLAS-ORQUESTADOR.md` no necesita conocer la distinción: transporta
`next_prompt` literalmente y no interpreta su contenido. El `README.md` de la biblioteca declara
que no guarda fuentes auxiliares.

**No redefine.** REVOLUTIONS §5.2, autoridad sobre delegación de capacidades y su derivación, ni
el contrato `revolutions-hop/v1`, al que no se le agrega ningún campo.

---

## CT-6 — Identidad de publicación y estructura de la biblioteca

**Qué conserva.** La identidad de constitución de un manifiesto es `repositorio + path + commit
SHA exacto`. Ni el método que publica ni el trabajo que se constituye pueden inferir la estructura
de paths ni las reglas de modificación de la biblioteca.

**Autoridad.** `manifiestos-trabajo-ai : README.md`.

La estructura de un repositorio pertenece a ese repositorio.

**Obligaciones del documento autoritativo.** Declarar qué guarda y qué no guarda; la estructura
`manifiestos/<WORK_ID>/MANIFIESTO_TRABAJO.md` con `PROJECT.md` opcional; que la identidad de
constitución usa el commit SHA y que el blob SHA puede informarse adicionalmente para
verificación; que una modificación posterior toca el mismo path, produce un commit nuevo, no
reescribe la historia y no crea variantes renombradas; que la ejecución ya constituida conserva su
SHA de origen; que no guarda estado de ejecución ni auditorías ni planes ni bootstraps; y que las
plantillas, si existen, quedan identificadas como tales y no se confunden con trabajos reales.

**Referencia de los demás.** `METODO-MANIFIESTOS.md` publica en esa estructura y congela las
identidades exactas resultantes, y referencia `CT-6` en lugar de redefinirla.

**No redefine.** REVOLUTIONS §2.1, autoridad sobre qué es un manifiesto y qué no contiene, ni
§2.7, autoridad sobre el cambio de intención.

---

## CT-7 — Mecánica del ORQUESTADOR

**Qué conserva.** REVOLUTIONS §4.6 declara qué no decide el ORQUESTADOR, pero no especifica el
comportamiento mecánico que debe implementarse: validaciones, resolución de instancia, detención
ordenada por el humano y conducta ante fallas.

**Autoridad.** `reglas-orquestador-ai : REGLAS-ORQUESTADOR.md`.

**Obligaciones del documento autoritativo.** Distinguir arranque externo de pases internos;
validar mecánicamente `protocol`, `work_id`, presencia y tipos de campos, combinaciones
`human_need`/`final`, sucesión exacta de `turn_id` y valores admitidos de `next_instance` con su
consistencia respecto de `next_actor`; extraer el último bloque JSON sin interpretar la prosa
previa ni escanear `next_prompt`; entregar `next_prompt` literalmente sin resumir, reescribir,
mejorar ni agregar contexto; detenerse y reportar ante un sobre inválido sin repararlo
semánticamente; definir la frontera exacta de `DETENER`, la reanudación literal por `CONTINUAR` y
el transporte de una directiva humana por un canal separado que no modifique el `next_prompt`
emitido; enumerar el estado efímero admisible y prohibir sus equivalentes durables; y fallar
cerrado cuando no pueda satisfacer literalmente `next_instance="current"`, sin convertirlo
silenciosamente en `fresh`.

**Referencia de los demás.** `METODO-MANIFIESTOS.md` referencia `CT-7` cuando explica qué hará el
ORQUESTADOR con el paquete de constitución, sin reproducir sus reglas.

**No redefine.** El contrato `revolutions-hop/v1` de REVOLUTIONS §4.1, al que no se agrega ningún
campo, ni las conductas de detención y terminación de §7 y §4.7.

---

## Asignación resultante

```text
CT-1  cadena del sistema y frontera funcional      METODO-MANIFIESTOS.md
CT-2  paquete de constitución                      METODO-MANIFIESTOS.md
CT-3  política periódica de relevo derivable       METODO-MANIFIESTOS.md
CT-4  concurrencia y semántica de PROJECT.md       METODO-MANIFIESTOS.md
CT-5  fuentes auxiliares y no ampliación           METODO-MANIFIESTOS.md
CT-6  identidad y estructura de la biblioteca      manifiestos-trabajo-ai : README.md
CT-7  mecánica del ORQUESTADOR                     reglas-orquestador-ai : REGLAS-ORQUESTADOR.md
```

Cada contrato tiene exactamente una autoridad. Ningún documento aparece como autoridad de un
contrato cuyo texto normativo deba escribirse en otro.

La concentración en `METODO-MANIFIESTOS.md` no es un desbalance a corregir: es consecuencia de que
ese documento es el que produce la constitución, y las reglas sobre cómo se produce le pertenecen.
Repartirlas por simetría crearía autoridades que no corresponden a quien decide.

---

## Contratos examinados y descartados

Un contrato que no conserva información irreducible ni protege una propiedad material no existe.
Se examinaron y se descartaron:

- **Contrato del sobre `revolutions-hop/v1`.** Ya es autoridad de REVOLUTIONS §4.1. Reproducirlo
  en `REGLAS-ORQUESTADOR.md` crearía una segunda fuente sobre la misma forma, y el manifiesto
  excluye agregarle campos desde ese repositorio.
- **Fronteras de escritura de los roles.** Fijadas por REVOLUTIONS §5.1 y por los archivos de rol.
  Ninguno de los tres documentos las redefine ni las amplía.
- **Protocolo de derivación e invariantes `P1`–`P8`.** Autoridad de REVOLUTIONS §3.
- **Taxonomía de necesidades humanas.** REVOLUTIONS §7 distingue `material` de `no_material` y
  declara expresamente que no se construye una taxonomía.
- **Forma de `EVENTO.md` y de las auditorías.** Autoridad de REVOLUTIONS §2.4 y del invariante
  `P8`.
- **Selección de modelo o runtime.** El manifiesto lo excluye expresamente del contrato. Una
  exclusión no es un contrato: no hay regla que asignar.
- **Convención de mensajes de commit.** REVOLUTIONS §3.4 declara que no existe y que ninguna
  operación del protocolo los lee.
