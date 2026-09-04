# BOOTSTRAP — CONSTRUCTOR

Hechos de constitución de este trabajo. No registra estado actual y no se reescribe para
simular vigencia posterior de ninguna fuente.

## Constitución

WORK_ID=revolutions-orchestra-ai
CARRIL=I
ROL=CONSTRUCTOR

## Bootstrap del AUDITOR constituyente

AUDITOR_BOOTSTRAP_REPO=https://github.com/francogg89-ai/audit-chatgpt-i
AUDITOR_BOOTSTRAP_PATH=BOOTSTRAP.md
AUDITOR_BOOTSTRAP_SHA=4830e31767649f181526c24d592e6eddfaf2305f

Arista irreducible: las historias Git de work-claude-i y audit-chatgpt-i son independientes y
ninguna puede inferir de cuál constitución proviene la otra. Esta identidad se preserva aquí
por esa razón y no como estado.

## Método gobernante

METHOD_REPO=https://github.com/francogg89-ai/revolutions-orchestra-ai
METHOD_SHA=e05b24cc501ce839ffabee6d9666d069e056255c

PATHS_CONSTITUTIVOS:
- metodo/REVOLUTIONS.md
- metodo/ROL-AUDITOR.md
- metodo/ROL-CONSTRUCTOR.md

ARCHIVOS_CARGADOS_POR_ESTE_ACTOR_AL_CONSTITUIR:
- metodo/REVOLUTIONS.md
- metodo/ROL-CONSTRUCTOR.md

METHOD_WRITE=PROHIBIDO

## Manifiesto de constitución

MANIFEST_REPO=https://github.com/francogg89-ai/manifiestos-trabajo-ai
MANIFEST_PATH=manifiestos/revolutions-orchestra-ai/MANIFIESTO_TRABAJO.md
MANIFEST_SHA=bb985e6580fbb8208f141a2af7646815bd1f7cdc

PROJECT=NO_APLICA

## Repositorios del loop

WORK_REPO=https://github.com/francogg89-ai/work-claude-i
AUDIT_REPO=https://github.com/francogg89-ai/audit-chatgpt-i

CONDICION_CONSTITUTIVA_WORK_REPO=VACIO

Al constituir este CONSTRUCTOR no existía WORK_SHA ni bootstrap propio previo. La intervención
que crea este archivo es el commit raíz de work-claude-i.

CONDICION_CONSTITUTIVA_AUDIT_REPO_OBSERVADA=un unico commit, 4830e31767649f181526c24d592e6eddfaf2305f, cuyo arbol contiene exclusivamente BOOTSTRAP.md

## Repositorios fuente y objeto

### manifiestos-trabajo-ai

REPO=https://github.com/francogg89-ai/manifiestos-trabajo-ai
FUNCION=biblioteca durable; contiene el manifiesto aprobado de este trabajo y es tambien objeto del trabajo
CORTE_CONSTITUTIVO=bb985e6580fbb8208f141a2af7646815bd1f7cdc

### reglas-orquestador-ai

REPO=https://github.com/francogg89-ai/reglas-orquestador-ai
FUNCION=objetivo del trabajo; construir las reglas mecanicas del orquestador
ESTADO_EN_CONSTITUCION=VACIO

### metodo-manifiestos-ai

REPO=https://github.com/francogg89-ai/metodo-manifiestos-ai
FUNCION=objetivo del trabajo; construir el metodo para constituir manifiestos
ESTADO_EN_CONSTITUCION=VACIO

### revolutions-orchestra-ai

REPO=https://github.com/francogg89-ai/revolutions-orchestra-ai
FUNCION=metodo autoritativo y fuente de solo lectura
CORTE_CONSTITUTIVO=e05b24cc501ce839ffabee6d9666d069e056255c

## Raíz y paths locales

ROOT_LOCAL=C:\Franco_Metodos_AI

LOCAL_PATHS:
- WORK_REPO=C:\Franco_Metodos_AI\work-claude-i
- AUDIT_REPO=C:\Franco_Metodos_AI\audit-chatgpt-i
- MANIFEST_REPO=C:\Franco_Metodos_AI\manifiestos-trabajo-ai
- ORCHESTRATOR_RULES_REPO=C:\Franco_Metodos_AI\reglas-orquestador-ai
- MANIFEST_METHOD_REPO=C:\Franco_Metodos_AI\metodo-manifiestos-ai
- REVOLUTIONS_REPO=C:\Franco_Metodos_AI\revolutions-orchestra-ai

C:\Franco_Metodos_AI no es un repositorio Git. _info_local/carril-I-revolutions-orchestra-ai/
es espacio local opcional conforme a REVOLUTIONS §13: no es autoridad, puede desaparecer y
nada indispensable sobrevive solo alli.

## Entornos relevantes

- GitHub remoto para las historias Git autoritativas.
- Windows local bajo C:\Franco_Metodos_AI para el trabajo del CONSTRUCTOR.
- No existe en esta constitucion un entorno productivo externo que deba mutarse.
- No se transportan secretos.

## Capacidades inicialmente delegadas

### CONSTRUCTOR

ACTOR=CONSTRUCTOR
ENTORNO=GitHub remoto + Windows local bajo C:\Franco_Metodos_AI
CAPACIDADES:
- lectura de los repositorios fuente indicados;
- escritura exclusivamente en work-claude-i, conforme a ROL-CONSTRUCTOR;
- uso del filesystem y herramientas locales necesarias dentro de C:\Franco_Metodos_AI;
- ejecucion de verificaciones tecnicamente seguras dentro de ese perimetro;
- no escritura directa en audit-chatgpt-i;
- no escritura directa en metodo-manifiestos-ai, reglas-orquestador-ai, manifiestos-trabajo-ai ni revolutions-orchestra-ai.

### AUDITOR

ACTOR=AUDITOR
ENTORNO=GitHub remoto y fuentes disponibles
CAPACIDADES:
- lectura directa de work-claude-i y de todos los repositorios fuente indicados;
- escritura exclusivamente en audit-chatgpt-i, conforme a ROL-AUDITOR;
- comprobacion independiente mediante GitHub y las fuentes disponibles;
- no modificacion del candidato material;
- no escritura directa en los tres repositorios destino.

La frontera de escritura de cada rol es estructural y no es una capacidad delegable.

## Referencias seguras a credenciales

NINGUNA_REQUERIDA_AL_CONSTITUIR

## Fuentes auxiliares constitutivas

- No se constituye un repositorio de skills.
- metodo-lecciones-ai no es dependencia obligatoria de esta ejecucion.
- La arquitectura resultante debe dejar preparado el punto de extension futuro para
  repositorios auxiliares de lecciones, incidentes, experimentos y skills de solo lectura, sin
  que su existencia amplie autoridad.

## Políticas iniciales de ejecución

- aplicar literalmente revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c;
- reconstruir desde Git y no desde memoria conversacional;
- no crear estado paralelo;
- no almacenar contadores vivos;
- no modificar el bootstrap para simular vigencia posterior de fuentes;
- no crear PROJECT.md por simetria: este trabajo no lo requiere;
- no crear EVENT.md central, lista viva de carriles ni registro redundante de mutaciones;
- los relevos de esta corrida son manuales o los que REVOLUTIONS requiera metodologicamente;
- no aplicar todavia una politica periodica automatica cada N a esta corrida;
- el diseno producido si debe definir y verificar la politica periodica exigida por el manifiesto;
- toda promocion fuera de work-* y audit-* debe respetar las fronteras estructurales de roles.

## Condición especial de bootstrap de este trabajo

metodo-manifiestos-ai y reglas-orquestador-ai son salidas de este mismo trabajo y estaban
vacios al constituir. No se exige SHA previo de ellos y no son autoridades gobernantes de esta
ejecucion. El transporte de esta corrida se apoya directamente en el contrato definido por
revolutions-orchestra-ai@e05b24cc501ce839ffabee6d9666d069e056255c.

## Normalización de contenido

.gitattributes fija `* text=auto eol=lf` desde el commit raiz. La identidad de blob de cada
archivo queda determinada por su contenido normalizado y no por la plataforma local, condicion
necesaria para que la promocion final pueda verificarse por identidad de blob.
