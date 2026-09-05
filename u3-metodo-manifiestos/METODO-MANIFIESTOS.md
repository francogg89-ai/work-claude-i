# MÉTODO PARA CONSTITUIR MANIFIESTOS

Cómo una intención humana todavía incompleta se convierte en un manifiesto durable, una
constitución operativa suficiente y un paquete de arranque.

Cada sección numerada mecánica empieza con un bloque de obligaciones etiquetadas. Ese bloque es la
única superficie normativa del documento. Todo lo que sigue a un marcador `Nota.` explica y no
obliga. La convención completa está en `10`.

## Qué gobierna este documento y qué no

Gobierna cómo se produce un manifiesto, cómo se obtiene la aprobación humana, cómo se publica y
qué forma tiene el paquete de constitución que abre un trabajo.

No gobierna la ejecución. REVOLUTIONS gobierna el trabajo una vez constituido, y este método no
redefine sus autoridades, su protocolo de derivación ni sus fronteras de escritura.

No gobierna el transporte. El comportamiento mecánico del orquestador es autoridad de
`reglas-orquestador-ai : REGLAS-ORQUESTADOR.md`.

No gobierna la estructura de la biblioteca. Los paths, las reglas de creación y modificación y la
identidad de publicación son autoridad de `manifiestos-trabajo-ai : README.md`.

## Principio

> El humano decide qué quiere. El método lo ayuda a cerrarlo, y no decide por él.

---

# 1. Cadena del sistema

```text
R-1-cadena            la cadena es: metodo-manifiestos-ai produce, manifiestos-trabajo-ai
                      congela la intencion y el vinculo con el proyecto, el paquete de
                      constitucion inicia, reglas-orquestador-ai transporta y
                      revolutions-orchestra-ai gobierna la ejecucion
R-1-no-sustituye      ninguno de esos documentos sustituye a otro
R-1-no-amplia         ninguno amplia las autoridades de REVOLUTIONS
R-1-no-ejecuta        este metodo no ejecuta el trabajo tecnico
R-1-no-decide         no decide durante la ejecucion aquello que corresponde al CONSTRUCTOR, al
                      AUDITOR o al HUMANO
```

Nota. Cada pieza conoce su lugar en la cadena porque ninguna puede inferirlo. Este documento es el
único que necesita conocerla entera: parte de una intención informal y debe terminar en algo que
el orquestador pueda consumir sin interpretar.

---

# 2. La entrevista

```text
R-2-cierra            la entrevista cierra, cuando sean aplicables: objetivo, motivo, resultado
                      observable esperado, alcance, exclusiones, restricciones, riesgos,
                      criterios de exito, decisiones delegadas y decisiones que siguen
                      reservadas al humano
R-2-contexto          cierra tambien, cuando apliquen: sobre que proyecto o sistema se trabaja,
                      que repositorios intervienen, que entornos, que capacidades tiene cada
                      actor, que grado de evidencia y rigor se requiere, que grado de
                      reproducibilidad y que politicas de relevo quiere el humano
R-2-solo-lo-material  pregunta unicamente aquello que materialmente ayuda a cerrar la intencion o
                      a constituir el trabajo
R-2-no-repite         no vuelve a preguntar algo que el humano dejo inequivocamente respondido
R-2-no-formulario     no se convierte en un formulario rigido ni recorre categorias por simetria
R-2-alternativas      puede proponer alternativas con sus consecuencias para ayudar a decidir
R-2-traduce           las categorias de entrevista se traducen a obligaciones concretas cuando
                      importan: que debe verificarse, que evidencia debe preservarse, que riesgos
                      no son aceptables, que resultado debe reproducirse, que acciones estan
                      delegadas y cuales siguen reservadas
```

Nota. Categorías como `exploratorio`, `operativo`, `alta criticidad`, o como `autonomía
restringida`, `amplia` y `muy amplia`, sirven para conversar. No sirven como resultado: lo que
queda escrito son obligaciones concretas, no una etiqueta.

Nota. Lo mismo vale para la materialización: preguntar si hace falta un único entorno real, un
entorno reproducible, portabilidad fuerte o reconstrucción total desde fuentes ayuda a decidir.
Después, eso se traduce. Cuando la reproducibilidad es parte del resultado buscado, pertenece al
manifiesto; las rutas, entornos y credenciales pertenecen a la constitución.

---

# 3. Aprobación humana y publicación

```text
R-3-puede             la IA puede entrevistar, detectar ambiguedades, proponer, redactar, senalar
                      contradicciones y sugerir decisiones
R-3-no-publica        no publica un manifiesto como definitivo hasta recibir una aprobacion
                      explicita del humano
R-3-no-silencio       no existe aprobacion por silencio, por ausencia de objecion ni por
                      continuacion informal de la conversacion
R-3-orden             aprobado el manifiesto: se publica en la biblioteca, se obtiene su
                      identidad Git exacta, se publica PROJECT.md si corresponde, se obtienen sus
                      identidades exactas, y recien entonces se produce el paquete de
                      constitucion
```

Nota. El orden importa porque el paquete cita identidades. Producirlo antes de publicar obligaría
a inventar un SHA o a corregirlo después, y las dos cosas rompen la identidad de constitución.

---

# 4. El paquete de constitución

```text
R-4-campos            el paquete lleva WORK_ID, CARRIL, METHOD_REPO, METHOD_SHA, MANIFEST_REPO,
                      MANIFEST_PATH, MANIFEST_SHA, WORK_REPO, AUDIT_REPO, SOURCE_REPOS,
                      ROOT_LOCAL, LOCAL_PATHS, ENTORNOS_RELEVANTES, CAPACIDADES_CONSTRUCTOR,
                      CAPACIDADES_AUDITOR, REFERENCIAS_SEGURAS_A_CREDENCIALES y
                      POLITICAS_DE_EJECUCION_INICIALES
R-4-project           lleva PROJECT_REPO, PROJECT_PATH y PROJECT_SHA cuando el trabajo tiene
                      PROJECT.md, y no los lleva cuando no lo tiene
R-4-aplicables        un campo que no aplica se omite; no se rellena con un valor vacio ni con un
                      marcador que simule una identidad
R-4-identidades       toda identidad Git del paquete es un commit SHA exacto obtenido de Git
                      despues de publicar, nunca inventado ni abreviado
R-4-sin-secretos      el paquete transporta referencias seguras a credenciales y nunca sus
                      valores
R-4-no-bootstrap      el paquete es la entrada con la que el primer AUDITOR construye su
                      BOOTSTRAP.md; no lo sustituye y no redefine que hechos registra
```

Nota. El primer AUDITOR de un trabajo no llega desde un sobre anterior y todavía no existe ningún
bootstrap. REVOLUTIONS fija qué hechos preserva ese bootstrap; lo que este documento fija es la
forma de la entrada que permite construirlo.

Nota. Una referencia segura nombra dónde vive el secreto, no el secreto. `TOKEN_FUDO → variable de
entorno FUDO_TOKEN` es admisible; el valor del token no lo es.

---

# 5. Política periódica de relevo

```text
R-5-pregunta          el metodo pregunta al humano que politica de relevo de actores quiere
R-5-opciones          soporta al menos: nunca automaticamente, solo manual, cada N
                      intervenciones, en ciertos limites de unidad, y combinaciones expresamente
                      definidas
R-5-hechos            una entrega del CONSTRUCTOR es un commit de work-* alcanzable desde el
                      corte; una intervencion del AUDITOR es un commit de audit-* alcanzable
                      desde el corte
R-5-derivacion        la cadencia se deriva contando el conjunto completo de commits alcanzables
                      desde el corte exacto, sin recorrido por primer padre, sin filtro por path
                      y sin leer mensajes de commit
R-5-multiplos         la cadencia opera sobre multiplos absolutos: 10, 20, 30, y un relevo manual
                      no la reinicia
R-5-sin-contadores    no existe CONSTRUCTOR_COUNT, AUDITOR_COUNT, relay_pending ni ningun
                      contador persistido
R-5-uniforme          las intervenciones auditoras con necesidad humana, las que preservan una
                      decision humana y la que cierra el trabajo cuentan como cualquier otra
R-5-constitucion      la politica concreta es politica inicial de ejecucion y llega al bootstrap
                      por la constitucion; no pertenece al manifiesto salvo que el humano la
                      considere parte material de su intencion
R-5-no-orquestador    el ORQUESTADOR no cuenta, no deriva la cadencia y no decide relevos
```

Nota. Contar el conjunto alcanzable y no un recorrido es lo que hace exacta la derivación. Un
recorrido por primer padre omite los commits alcanzables por los padres secundarios de un merge,
que también son entregas, y ningún invariante garantiza que ambas cuentas coincidan.

Nota. El contador conceptual pertenece al trabajo, no a la instancia que ocupa el rol. Por eso los
múltiplos son absolutos: un relevo manual no mueve la grilla.

---

# 6. `PROJECT.md` y trabajos concurrentes

```text
R-6-contrato          PROJECT.md es un contrato estable de vinculacion entre un trabajo y el
                      proyecto sobre el que opera
R-6-contenido         puede contener PROJECT_ID, identidad del proyecto, repositorios que lo
                      constituyen y la funcion de cada uno, superficies materiales compartidas,
                      entornos relevantes, limites de integracion, recursos protegidos, la
                      superficie que el trabajo puede afectar y la que no, que tipos de trabajo
                      pueden coexistir, reglas estables de concurrencia e integracion, el
                      criterio ante solapamiento o drift, y la autoridad para resolver conflictos
                      que no sean tecnicamente resolubles
R-6-prohibido         no registra trabajo activo, trabajo terminado, ultimo SHA, ultimo
                      despliegue, ultimo actor, locks, semaforos, contadores ni lista viva de
                      workers o carriles
R-6-aislado           un trabajo aislado no necesita PROJECT.md, y el metodo no lo crea por
                      simetria
R-6-superficie        una superficie se declara como repositorio mas conjunto de paths
R-6-descubrimiento    antes de una mutacion material sobre una superficie compartida se toma el
                      corte constitutivo de ese repositorio congelado en el bootstrap, se lee su
                      referencia actual, se obtienen los paths modificados entre ambos y se
                      intersectan con la superficie propia declarada
R-6-no-presuncion     interseccion vacia significa compatibilidad demostrable y habilita
                      proceder; interseccion no vacia significa compatibilidad no demostrable y
                      no se procede por presuncion
R-6-rutea             ante interseccion no vacia el CONSTRUCTOR preserva y entrega, y el AUDITOR
                      determina si el conflicto se resuelve tecnicamente o si existe NECESIDAD
                      DEL HUMANO
R-6-sin-registro      el descubrimiento no usa EVENT.md central, lista viva de carriles ni
                      registro redundante de mutaciones
R-6-sha-constitutivo  consultar la vigencia de un repositorio compartido no reescribe el
                      PROJECT_SHA congelado en el bootstrap
```

Nota. Los repositorios compartidos son su propia fuente. Lo que otro trabajo modificó ya está
demostrado por el repositorio, y no hace falta saber qué otros trabajos existen ni consultar un
registro que replique lo que Git ya prueba.

Nota. La regla que esto persigue es una sola: dos trabajos avanzan en paralelo cuando sus
perímetros materiales son demostrablemente compatibles. Si el solapamiento no está resuelto, el
trabajo no supone que puede proceder.

---

# 7. Fuentes auxiliares

```text
R-7-source-repos      las fuentes auxiliares de lecciones, incidentes, experimentos o skills
                      viajan dentro de SOURCE_REPOS, con repositorio, identidad exacta y funcion
                      declarada
R-7-solo-lectura      son de solo lectura para los actores
R-7-no-autoriza       una skill puede explicar como realizar una accion y nunca autoriza por si
                      misma a realizarla
R-7-capacidades       las capacidades se derivan de la constitucion mas las decisiones humanas
                      posteriores; la existencia de una fuente auxiliar no las amplia
R-7-sin-campos        admitir fuentes auxiliares no agrega ningun campo al contrato de transporte
R-7-utilidad          el metodo determina si una fuente auxiliar es materialmente util para una
                      ejecucion y como localizarla de forma exacta, sin cargar indiscriminadamente
                      su contenido
```

Nota. La distinción entre saber cómo y estar autorizado no es inferible del hecho de que un
repositorio esté declarado en la constitución. Por eso se dice.

---

# 8. Lo que este método no hace

```text
R-8-no-ejecuta        no ejecuta el trabajo tecnico
R-8-no-reemplaza      no reemplaza a REVOLUTIONS ni redefine sus autoridades
R-8-no-decide         no decide durante la ejecucion lo que corresponde al CONSTRUCTOR, al
                      AUDITOR o al HUMANO
R-8-no-estado         no crea estado de ejecucion del trabajo ni lo publica en la biblioteca
R-8-no-circular       no crea dependencias SHA circulares entre documentos metodologicos: las
                      dependencias se declaran por repositorio, path y contrato, y las
                      ejecuciones concretas congelan los SHAs disponibles al constituir
R-8-no-modelo         no selecciona modelo, runtime ni reglas de costo
```

Nota. Casi todas estas prohibiciones nombran cosas que un método de constitución podría hacer con
buena intención y que, hechas, moverían una autoridad de lugar. Decidir durante la ejecución es la
más tentadora: quien constituyó el trabajo cree conocerlo mejor que quien lo ejecuta, y esa
creencia es exactamente la que REVOLUTIONS separa en roles.

---

# 9. Relación con los demás documentos

```text
revolutions-orchestra-ai   gobierna la ejecucion y el contrato de transporte
reglas-orquestador-ai      transporta, y no interpreta el trabajo
manifiestos-trabajo-ai     conserva la intencion humana aprobada y su identidad exacta
```

Cuando este documento necesita una regla ajena la referencia por repositorio, path y contrato, sin
reproducir su texto normativo y sin congelar un SHA de esos documentos. Congelar identidades entre
documentos que se citan mutuamente produciría el ciclo que el manifiesto excluye.

La estructura de paths de la biblioteca, sus reglas de creación y modificación y la identidad de
publicación son autoridad de `manifiestos-trabajo-ai : README.md`. El comportamiento mecánico del
orquestador es autoridad de `reglas-orquestador-ai : REGLAS-ORQUESTADOR.md`.

---

# 10. Superficie normativa de este documento

Esta sección declara dónde vive lo normativo, para que la cobertura de una verificación pueda
medirse contra el documento y no contra una lista paralela.

## Obligaciones

Una obligación es una línea etiquetada dentro del bloque de obligaciones de una sección mecánica:

```text
<identificador><espacios><enunciado>
```

El identificador empieza con `R-`. Una línea que empieza con cuatro o más espacios continúa el
enunciado de la obligación anterior.

El conjunto de obligaciones de este documento es el conjunto de esas líneas. No existe una segunda
lista, ni aquí ni en ninguna implementación. Una obligación no puede quedar fuera del conjunto sin
dejar de estar enunciada.

## Forma de una sección mecánica

```text
1  el encabezado de la seccion
2  el bloque de obligaciones, primer bloque cercado de la seccion
3  opcionalmente, a partir del primer marcador Nota., contenido libre hasta el proximo encabezado
```

Cualquier contenido no vacío entre el encabezado y el bloque de obligaciones, o entre el bloque y
el primer marcador `Nota.`, está fuera de esa forma y es un defecto del documento.

## Notas

El contenido que sigue a un marcador `Nota.` explica, ilustra, cita autoridades y da razones. No
enuncia obligaciones y no tiene fuerza normativa. Una conducta que este documento pretenda exigir
y que sólo aparezca en una nota, no está exigida por este documento.

Esa declaración es lo que hace completo al conjunto de obligaciones: no depende de que alguien
haya inspeccionado bien cada sección, sino de que fuera del bloque etiquetado no hay lugar donde
una obligación pueda existir.

## Secciones no mecánicas

```text
SECCIONES_NO_MECANICAS   9  10
```

Toda otra sección numerada es mecánica y contiene su bloque de obligaciones.

El encabezado del documento y las secciones sin número —`Qué gobierna este documento y qué no` y
`Principio`— delimitan alcance y no pertenecen a la superficie normativa.
