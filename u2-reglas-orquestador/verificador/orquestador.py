"""Implementacion determinista del candidato REGLAS-ORQUESTADOR.md.

Implementa unicamente las reglas que el candidato declara. Los hechos que el candidato
refiere a la autoridad de transporte se obtienen de `autoridad.py`, nunca por invencion.

No importa subprocess ni ninguna biblioteca de red: el orquestador no consulta Git y no
deriva ninguna cadencia. Esa ausencia es parte de lo que se verifica.
"""

# Reglas mecanicas declaradas por el candidato. Cada caso del corpus declara cual gobierna.
REGLAS = {
    "R-1.1-primer-turn-id": "el primer sobre del arranque externo lleva turn_id igual a 1",
    "R-2-ultimo-bloque": "se toma el ultimo bloque json de la salida",
    "R-2-no-parsea": "una salida sin bloque json o que no parsea produce sobre invalido",
    "R-2-no-escanear-prompt": "no se inspecciona next_prompt para decidir el transporte",
    "R-V1": "protocol es exactamente revolutions-hop/v1",
    "R-V2": "work_id es el del trabajo transportado",
    "R-V3": "estan presentes todos los campos del contrato",
    "R-V4": "cada campo tiene el tipo que el contrato le asigna",
    "R-V5": "turn_id es el sucesor exacto del ultimo transportado",
    "R-V6": "next_instance tiene un valor admitido",
    "R-V7": "next_instance es null si y solo si next_actor es null",
    "R-V8": "la combinacion es una de las tres formas admitidas por el contrato",
    "R-4-reporte": "el reporte identifica la validacion que fallo y no repara",
    "R-5-no-reinicio": "un relevo no reinicia el contador de turn_id",
    "R-6-resolucion": "current usa la instancia activa, fresh abre una nueva",
    "R-6-fresh-a-current": "una instancia abierta como fresh pasa a ser la current de su rol",
    "R-6.1-fail-closed": "current perdido detiene y nunca degrada a fresh",
    "R-7-orden": "human_need detiene, luego final detiene, luego unit se muestra",
    "R-7-entrega-literal": "next_prompt se entrega sin modificar",
    "R-8-no-cadencia": "el orquestador no cuenta, no deriva cadencia y no consulta Git",
    "R-9.1-detener-constructor": "DETENER durante el CONSTRUCTOR pausa antes de entregar al AUDITOR",
    "R-9.1-detener-auditor": "DETENER durante el AUDITOR permite el pase hacia el CONSTRUCTOR",
    "R-9.1-detencion-natural": "human_need o final del AUDITOR prevalecen sobre la pausa",
    "R-9.1-pendiente": "DETENER con sobre pendiente hacia el AUDITOR detiene sin entregarlo",
    "R-9.2-continuar-literal": "CONTINUAR entrega el pase pendiente exactamente como fue emitido",
    "R-9.3-canal-separado": "la directiva humana viaja aparte y no modifica next_prompt",
    "R-10-estado-efimero": "el estado de runtime es solo el admitido y ninguno paralelo",
    "R-11-secreto-literal": "una referencia segura se transporta literal y no se resuelve",
}

ESTADO_ADMITIDO = {
    "instancias", "ultimo_turn_id", "sobre_pendiente", "stop_requested",
}


def extraer(salida_texto):
    """Devuelve (sobre, None) o (None, regla) sin interpretar la prosa anterior."""
    import json

    marca = "```json"
    inicio = salida_texto.rfind(marca)
    if inicio == -1:
        return None, "R-2-no-parsea"
    cuerpo = salida_texto[inicio + len(marca):]
    fin = cuerpo.find("```")
    if fin == -1:
        return None, "R-2-no-parsea"
    try:
        return json.loads(cuerpo[:fin]), None
    except ValueError:
        return None, "R-2-no-parsea"


def _tipo(valor):
    if valor is None:
        return "null"
    if isinstance(valor, bool):
        return "bool"
    if isinstance(valor, int):
        return "int"
    if isinstance(valor, str):
        return "str"
    if isinstance(valor, dict):
        return "object"
    if isinstance(valor, list):
        return "array"
    return "desconocido"


class Orquestador:
    def __init__(self, work_id, autoridad, instancias=None, ultimo_turn_id=0):
        self.work_id = work_id
        self._autoridad = autoridad
        self.instancias = dict(instancias or {})
        self.ultimo_turn_id = ultimo_turn_id
        self.sobre_pendiente = None
        self.stop_requested = False

    # -- estado efimero -------------------------------------------------------

    def estado_efimero(self):
        return {
            "instancias": self.instancias,
            "ultimo_turn_id": self.ultimo_turn_id,
            "sobre_pendiente": self.sobre_pendiente,
            "stop_requested": self.stop_requested,
        }

    # -- validaciones ---------------------------------------------------------

    def validar(self, sobre):
        if sobre.get("protocol") != self._autoridad.TRANSPORT_CONTRACT:
            return "R-V1"
        if sobre.get("work_id") != self.work_id:
            return "R-V2"
        for campo in self._autoridad.campos:
            if campo not in sobre:
                return "R-V3"
        for campo in self._autoridad.campos:
            if _tipo(sobre[campo]) not in self._autoridad.tipos[campo]:
                return "R-V4"
        if sobre["turn_id"] != self.ultimo_turn_id + 1:
            return "R-1.1-primer-turn-id" if self.ultimo_turn_id == 0 else "R-V5"
        if sobre["next_instance"] not in ("current", "fresh", None):
            return "R-V6"
        if (sobre["next_instance"] is None) != (sobre["next_actor"] is None):
            return "R-V7"
        if not self._autoridad.forma_admitida(sobre):
            return "R-V8"
        return None

    # -- ciclo ----------------------------------------------------------------

    def arranque_externo(self, paquete):
        self.instancias["AUDITOR"] = "AUDITOR#1"
        return [("ENTREGAR_PAQUETE", "AUDITOR", paquete)]

    def recibir(self, salida_texto):
        sobre, regla = extraer(salida_texto)
        if regla is not None:
            return [("DETENER_REPORTAR", regla)]
        regla = self.validar(sobre)
        if regla is not None:
            return [("DETENER_REPORTAR", regla)]
        self.ultimo_turn_id = sobre["turn_id"]
        self.sobre_pendiente = sobre
        return [("RECIBIDO",)]

    def despachar(self):
        sobre = self.sobre_pendiente
        if sobre is None:
            return [("DETENER_REPORTAR", "R-9.2-continuar-literal")]

        if sobre["human_need"] is not None:
            self.sobre_pendiente = None
            return [("MOSTRAR_NECESIDAD",)]
        if sobre["final"] is True:
            self.sobre_pendiente = None
            return [("MOSTRAR_CIERRE",)]

        acciones = []
        if sobre["unit"] is not None:
            acciones.append(("MOSTRAR_UNIDAD", sobre["unit"]))

        if self.stop_requested and sobre["next_actor"] == "AUDITOR":
            return acciones + [("PAUSA_SIN_ENTREGAR",)]

        destino = sobre["next_actor"]
        if sobre["next_instance"] == "current":
            if destino not in self.instancias:
                return acciones + [("DETENER_REPORTAR", "R-6.1-fail-closed")]
            instancia = self.instancias[destino]
        else:
            instancia = "%s#t%d" % (destino, sobre["turn_id"])
            self.instancias[destino] = instancia

        self.sobre_pendiente = None
        acciones.append(("ENTREGAR", destino, instancia, sobre["next_prompt"]))
        return acciones

    def detener(self):
        self.stop_requested = True
        if self.sobre_pendiente is not None and self.sobre_pendiente["next_actor"] == "AUDITOR":
            return [("PAUSA_SIN_ENTREGAR",)]
        return [("PAUSA_SOLICITADA",)]

    def continuar(self, directiva=None):
        self.stop_requested = False
        acciones = self.despachar()
        if directiva is not None:
            acciones.append(("ENTREGAR_DIRECTIVA", directiva))
        return acciones
