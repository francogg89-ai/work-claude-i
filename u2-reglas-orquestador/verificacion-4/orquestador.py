"""Implementación determinista de las obligaciones del candidato congelado.

No declara ningún catálogo de reglas: los identificadores que emite deben existir en el
candidato, y el denominador de la cobertura lo aporta `candidato.py`.

No importa subprocess ni ninguna biblioteca de red: el orquestador no consulta Git, no cuenta
entregas y no deriva ninguna cadencia. Esa ausencia es parte de lo que se verifica.
"""

import json
import re

CERCA_JSON = re.compile(r"```json\n(.*?)```", re.S)

ACCIONES = frozenset({
    "ENTREGAR_PAQUETE", "RECIBIDO", "DETENER_REPORTAR", "MOSTRAR_NECESIDAD",
    "MOSTRAR_CIERRE", "MOSTRAR_UNIDAD", "ENTREGAR", "ENTREGAR_DIRECTIVA",
    "PAUSA_SIN_ENTREGAR", "PAUSA_SOLICITADA",
})

ESTADO_ADMITIDO = frozenset({
    "instancias", "ultimo_turn_id", "sobre_pendiente", "stop_requested",
})

ESTADO_PROHIBIDO = frozenset({
    "current_unit", "approved_work_sha", "latest_audit", "relay_pending",
    "work_status", "constructor_count", "auditor_count",
})


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

    # -- estado efímero -------------------------------------------------------

    def estado_efimero(self):
        return {
            "instancias": self.instancias,
            "ultimo_turn_id": self.ultimo_turn_id,
            "sobre_pendiente": self.sobre_pendiente,
            "stop_requested": self.stop_requested,
        }

    # -- forma de la respuesta ------------------------------------------------

    def extraer(self, salida_texto):
        """Comprueba la forma exigida antes de tomar el bloque."""
        bloques = list(CERCA_JSON.finditer(salida_texto))
        if len(bloques) == 0:
            return None, "R-2-parseo"
        if len(bloques) > 1:
            return None, "R-2-unicidad"
        bloque = bloques[0]
        if salida_texto[bloque.end():].strip():
            return None, "R-2-sin-posterior"
        try:
            return json.loads(bloque.group(1)), None
        except ValueError:
            return None, "R-2-parseo"

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
        self.instancias["AUDITOR"] = "AUDITOR#externo"
        return [("ENTREGAR_PAQUETE", "AUDITOR", "AUDITOR#externo", paquete)]

    def recibir(self, salida_texto):
        sobre, regla = self.extraer(salida_texto)
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
            return [("DETENER_REPORTAR", "R-9.2-preserva")]

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
        if sobre["next_instance"] is None:
            return acciones + [("DETENER_REPORTAR", "R-6-null")]
        if sobre["next_instance"] == "current":
            if destino not in self.instancias:
                return acciones + [("DETENER_REPORTAR", "R-6.1-detiene")]
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

    def reportar_contradiccion_con_git(self, detalle):
        """El contador contradice a Git: se reporta y no se resuelve."""
        return [("DETENER_REPORTAR", "R-5-git-prevalece")]
