# EVENTO — U1 contratos transversales

## Qué recibió el CONSTRUCTOR

El corte `work-claude-i@2afab62d970719db6845573ca3437e906266849b` y
`audit-chatgpt-i@91c94d99173c5d0eacab9bfeb4c1e46568f4d76f`.

En ese corte de auditoría, la decisión humana preservada sobre la identidad exacta
`PLAN.md` blob `b4ce319ec3ac432ced27c21ff1d6a25a22e9c9ea`, cuyo alcance habilita la continuación
metodológica hacia la primera unidad y no aprueba por adelantado ninguna entrega material.

La auditoría aplicable a ese `WORK_SHA` declaró resueltos los defectos previos.

## Qué hizo y por qué

Produjo `u1-contratos-transversales/CONTRATOS-TRANSVERSALES.md`: la asignación de autoridad
normativa única de cada contrato transversal, las obligaciones que su documento autoritativo debe
satisfacer, la forma en que los demás documentos lo referencian, y qué no redefine porque ya es
autoridad de REVOLUTIONS.

El documento no contiene el texto normativo de ningún contrato. Escribirlo aquí y copiarlo después
al documento autoritativo crearía dentro de `work-claude-i` una segunda superficie que habría que
mantener sincronizada, que es exactamente la propiedad que `D7` protege. La unidad produce
asignación y obligaciones; el texto normativo se escribe una sola vez, en `U2`, `U3` y `U4`.

Se examinaron candidatos a contrato y se descartaron los que no conservan información irreducible
ni protegen una propiedad material, conforme al criterio de terminación de la unidad. Los
descartes quedaron registrados con su razón, porque un contrato ausente sin explicación es
indistinguible de un contrato olvidado.

## Cambio local respecto de la enumeración de `D7`

`D7` enumera seis contratos. Esta unidad identificó siete: `CT-1` cadena del sistema y frontera
funcional, y `CT-2` paquete de constitución, no figuraban en esa enumeración.

Ambos reciben como autoridad `metodo-manifiestos-ai : METODO-MANIFIESTOS.md`, coherente con la
regla de asignación de `D7`, y ninguno crea una autoridad nueva ni desplaza una existente. Los
seis contratos de `D7` conservan la autoridad que el plan les asignó.

Se trata como cambio local: no modifica intención, alcance macro, arquitectura, secuencia macro,
dependencias, criterios de terminación ni decisiones humanas. `PLAN.md` no se modifica. `D7` fija
la regla de asignación y no declara ser una enumeración cerrada; producir la asignación completa
es precisamente el trabajo que el plan encomienda a esta unidad.

Si el AUDITOR considera que esta ampliación altera el plan y no la unidad, corresponde tratarla
como cambio de plan y no como materia de `U1`.

## Qué verificó

La verificación de esta unidad no es discriminante en el sentido de `PLAN.md` §5.2: no ejercita un
mecanismo contra un entorno ni produce un resultado que pueda pasar o fallar por sí mismo. El plan
reserva el contrato previo para las verificaciones ubicadas por `D5` y para las tres pruebas
obligatorias del manifiesto, ninguna de las cuales pertenece a `U1`. Por eso no se propuso ni se
congeló un contrato previo, y decirlo es parte de la entrega.

Sí se comprobó mecánicamente que cada sección de REVOLUTIONS citada como autoridad existente
existe realmente en la identidad gobernante, para que ninguna afirmación de no-redefinición se
apoye en una referencia inexistente.

```text
comando
  git -C revolutions-orchestra-ai show \
    e05b24cc501ce839ffabee6d9666d069e056255c:metodo/REVOLUTIONS.md \
    | grep -c "^<encabezado>"

encabezados comprobados
  ## 2.1   ## 2.4   ## 2.6   ## 2.7   # 3. Protocolo   ## 3.4
  ## 4.1   ## 4.6   ## 4.7   # 5. Decisiones   ## 5.1   ## 5.2
  # 7. Necesidad   # 9. Realidad   ## 12.2   ## 12.3

resultado
  1 para cada uno de los dieciséis encabezados; código de retorno 0

control negativo
  "## 15.1" -> 0   (no existe, como se esperaba)
  "## 6.1"  -> 1   (existe y no fue citado en este documento)
```

El control negativo existe porque una comprobación que sólo puede dar el resultado buscado no
discrimina nada: si el mecanismo devolviera `1` para cualquier cadena, el resultado positivo no
probaría existencia.

## Limitaciones conocidas

- La comprobación demuestra que los encabezados citados existen. No demuestra que el contenido de
  cada sección sea el que este documento le atribuye; eso corresponde a la lectura independiente
  del AUDITOR sobre la identidad gobernante.
- La suficiencia de las obligaciones de cada contrato sólo puede ejercitarse cuando se escriban
  los documentos autoritativos en `U2`, `U3` y `U4`. Una obligación incompleta se manifestará
  entonces, y corregirla en ese momento es materia de la unidad correspondiente.
- Esta unidad no produce material promovible: nada de lo que contiene llega a los repositorios
  destino.

## Resultado

`u1-contratos-transversales/CONTRATOS-TRANSVERSALES.md`, con siete contratos asignados a una
autoridad única cada uno y siete candidatos descartados con su razón.

## Necesidad humana detectada

Ninguna. El trabajo de esta unidad quedó íntegramente dentro del perímetro delegado en la
constitución.
