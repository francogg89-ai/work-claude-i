"""Extraccion mecanica de la autoridad de transporte.

El candidato REGLAS-ORQUESTADOR.md no enumera los campos, los tipos ni las tres formas
admitidas del sobre: los refiere a revolutions-orchestra-ai como autoridad. Este modulo
obtiene esos hechos de esa fuente exacta, para que el verificador no invente ninguna regla
que el candidato no declara ni obtiene por referencia autoritativa explicita.

Solo lectura. Sin red. Sin modelo de lenguaje.
"""

import json
import re
import subprocess

TRANSPORT_AUTHORITY_SHA = "e05b24cc501ce839ffabee6d9666d069e056255c"
TRANSPORT_AUTHORITY_PATH = "metodo/REVOLUTIONS.md"
TRANSPORT_CONTRACT = "revolutions-hop/v1"

FORMA_RE = re.compile(
    r"human_need\s*(==|!=)\s*null\s+y\s+final\s*==\s*(true|false)\s*"
    r"→\s*[^;]+;\s*next_actor,\s*next_instance\s+y\s+next_prompt\s+(presentes|null)"
)


def _leer_autoridad(repo):
    return subprocess.run(
        ["git", "-C", repo, "show",
         "%s:%s" % (TRANSPORT_AUTHORITY_SHA, TRANSPORT_AUTHORITY_PATH)],
        check=True, stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")


def _bloques_json(texto):
    bloques = []
    for cuerpo in re.findall(r"```json\n(.*?)```", texto, re.S):
        bloques.append(json.loads(cuerpo))
    return bloques


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


class Autoridad:
    """Campos, tipos admitidos y formas admitidas, derivados de la fuente congelada."""

    def __init__(self, repo_metodo):
        self.TRANSPORT_CONTRACT = TRANSPORT_CONTRACT
        texto = _leer_autoridad(repo_metodo)
        objetos = _bloques_json(texto)

        completos = [o for o in objetos if len(o) > 5]
        if not completos:
            raise RuntimeError("la autoridad no expone ningun sobre completo de ejemplo")
        claves = {frozenset(o.keys()) for o in completos}
        if len(claves) != 1:
            raise RuntimeError("los sobres completos de la autoridad no comparten campos")

        self.campos = sorted(next(iter(claves)))

        tipos = {c: set() for c in self.campos}
        for objeto in objetos:
            for clave, valor in objeto.items():
                if clave in tipos:
                    tipos[clave].add(_tipo(valor))
        self.tipos = {c: frozenset(v) for c, v in tipos.items()}

        formas = []
        for signo, final, trio in FORMA_RE.findall(texto):
            formas.append((signo == "!=", final == "true", trio == "null"))
        if len(formas) != 3 or len(set(formas)) != 3:
            raise RuntimeError("la autoridad no expone tres formas admitidas distintas")
        self.formas = tuple(formas)

    def forma_admitida(self, sobre):
        """True si la combinacion recibida es una de las formas que el contrato admite."""
        hay_necesidad = sobre.get("human_need") is not None
        final = sobre.get("final") is True
        trio_null = all(
            sobre.get(c) is None for c in ("next_actor", "next_instance", "next_prompt")
        )
        for f_necesidad, f_final, f_trio_null in self.formas:
            if f_necesidad == hay_necesidad and f_final == final:
                return trio_null == f_trio_null
        return False
