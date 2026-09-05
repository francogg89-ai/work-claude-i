"""Registro de comprobaciones y unico despachador que las ejerce.

Toda invocacion de una comprobacion —la que califica al candidato real y la de cualquier control—
pasa por `ejercer`. `ejercer` no le cree a la etiqueta: observa con `observador.Travesia` en que
bloque de codigo entro la invocacion, y esa entrada es la identidad que queda en la evidencia.

Por eso un control no puede declarar `S01` y ejercitar otra comprobacion, y no puede existir una
comprobacion que solo los controles alcancen: ambas cosas quedan visibles en el registro.
"""

import comprobaciones as K
import constituyente as C
import observador
import superficie

ARCHIVOS_DE_COMPROBACION = ("comprobaciones.py",)

CALIFICACION = "calificacion"
CONTROL = "control"


class Comprobacion(object):
    def __init__(self, sid, obligacion, tipo, clave, fn, fragmentos=(), mutacion=None):
        self.sid = sid
        self.obligacion = obligacion
        self.tipo = tipo
        self.clave = clave
        self.fn = fn
        self.fragmentos = tuple(fragmentos)
        self.mutacion = mutacion

    def superficie_declarada(self):
        return "%s:%s" % (self.tipo, self.clave)


# -- fragmentos que cada comprobacion de documento busca ----------------------

CADENA = ("metodo-manifiestos-ai produce", "manifiestos-trabajo-ai congela la intencion",
          "el paquete de constitucion inicia", "reglas-orquestador-ai transporta",
          "revolutions-orchestra-ai gobierna")
NO_SUSTITUYE = ("ninguno de esos documentos sustituye a otro",)
NO_AMPLIA = ("ninguno amplia las autoridades de REVOLUTIONS",)
REFERENCIAS = ("CT-6", "manifiestos-trabajo-ai : README.md",
               "CT-7", "reglas-orquestador-ai : REGLAS-ORQUESTADOR.md")
NO_REEMPLAZA = ("no reemplaza a REVOLUTIONS", "ni redefine sus autoridades")


def contexto(aperturas, remoto, vigencia, respuestas):
    return {"cadena": CADENA, "no_sustituye": NO_SUSTITUYE, "no_amplia": NO_AMPLIA,
            "referencias": REFERENCIAS, "no_reemplaza": NO_REEMPLAZA,
            "aperturas": aperturas, "remoto": remoto, "vigencia": vigencia,
            "respuestas": respuestas}


# -- el sujeto de conducta ----------------------------------------------------

def sujeto_conducta(vigencia):
    """Las conductas del mecanismo, cada una bajo su clave. Un mutante reemplaza una sola."""
    return {
        "acciones": C.acciones(),
        "referencias": C.referencias_externas,
        "politica_relevo": C.politica_relevo,
        "descubrir": C.descubrir,
        "constituir": C.constituir,
        "capacidades": C.capacidades,
        "campos_transporte": C.campos_de_transporte_agregados,
        "admitir": C.admitir_fuente,
        "vigencia": vigencia,
    }


def conducta_mutada(sujeto, clave, valor):
    return dict(sujeto, **{clave: valor})


# -- mutantes de conducta -----------------------------------------------------

def _acciones_mas(extra):
    def mutar(sujeto):
        return conducta_mutada(sujeto, "acciones", set(sujeto["acciones"]) | {extra})
    return mutar


def _acciones_menos(quitar):
    def mutar(sujeto):
        return conducta_mutada(sujeto, "acciones", set(sujeto["acciones"]) - {quitar})
    return mutar


def _referencias_con_sha(sujeto):
    def referencias():
        return ({"contrato": "CT-6", "repositorio": "manifiestos-trabajo-ai",
                 "path": "README.md", "sha": "1" * 40},)
    return conducta_mutada(sujeto, "referencias", referencias)


def _politica_con_default(sujeto):
    def politica(eleccion, persiste_contador=False):
        return {"politica": eleccion or "cada_n", "vive_en": "constitucion"}, None
    return conducta_mutada(sujeto, "politica_relevo", politica)


def _vigencia_local(sujeto):
    return conducta_mutada(sujeto, "vigencia",
                           {"argv": ["git", "-C", ".", "rev-parse", "refs/heads/main"]})


REGISTRO_COLADO = {}


def _descubrir_con_registro(sujeto):
    """Mantiene efectivamente un registro central. No lo nombra: lo mantiene."""
    def descubrir(paths, superficie_propia):
        REGISTRO_COLADO[len(REGISTRO_COLADO)] = tuple(paths)
        return C.descubrir(paths, superficie_propia)
    return conducta_mutada(sujeto, "descubrir", descubrir)


def _descubrir_que_muta(sujeto):
    def descubrir(paths, superficie_propia):
        paths.append("colado/por/el/mecanismo.md")
        return C.descubrir(paths, superficie_propia)
    return conducta_mutada(sujeto, "descubrir", descubrir)


def _capacidades_ampliadas(sujeto):
    def capacidades(constitucion, decisiones, fuentes):
        return sorted(set(constitucion) | set(decisiones) | set(fuentes))
    return conducta_mutada(sujeto, "capacidades", capacidades)


def _transporte_con_campo(sujeto):
    def campos():
        return ("next_model",)
    return conducta_mutada(sujeto, "campos_transporte", campos)


def _constituir_con_estado(sujeto):
    def constituir(respuestas):
        paquete, rechazo = C.constituir(respuestas)
        if paquete is not None:
            paquete = dict(paquete, unidad_actual="U3", ultima_entrega="abc")
        return paquete, rechazo
    return conducta_mutada(sujeto, "constituir", constituir)


# -- mutantes de documento ----------------------------------------------------

def _doc(viejo, nuevo):
    def mutar(documento, obligacion):
        return superficie.alterado_dentro(documento, obligacion, viejo, nuevo)
    return mutar


D = K.DOCUMENTO
N = K.CONDUCTA


def comprobaciones():
    return [
        Comprobacion("S01", "R-1-cadena", D, "R-1-cadena", K.c_S01, CADENA,
                     _doc("metodo-manifiestos-ai produce", "AJENO produce")),
        Comprobacion("S02", "R-1-no-sustituye", D, "R-1-no-sustituye", K.c_S02, NO_SUSTITUYE,
                     _doc("ninguno de esos documentos sustituye a otro",
                          "algun documento sustituye a otro")),
        Comprobacion("S03", "R-1-no-amplia", D, "R-1-no-amplia", K.c_S03, NO_AMPLIA,
                     _doc("ninguno amplia las autoridades de REVOLUTIONS",
                          "alguno amplia las autoridades de REVOLUTIONS")),
        Comprobacion("S04", "R-1-no-ejecuta", N, "acciones", K.c_S04, (),
                     _acciones_mas("EJECUTAR_TRABAJO")),
        Comprobacion("S05", "R-1-no-decide", N, "acciones", K.c_S05, (),
                     _acciones_mas("DECIDIR_UNIDAD")),
        Comprobacion("S06", "R-1-referencias", D, "R-1-referencias", K.c_S06, REFERENCIAS,
                     _doc("manifiestos-trabajo-ai : README.md", "manifiestos-trabajo-ai")),
        Comprobacion("S07", "R-1-sin-sha", N, "referencias", K.c_S07, (), _referencias_con_sha),
        Comprobacion("S08", "R-2-alternativas", N, "acciones", K.c_S08, (),
                     _acciones_menos("PROPONER")),
        Comprobacion("S09", "R-3-puede", N, "acciones", K.c_S09, (), _acciones_menos("SUGERIR")),
        Comprobacion("S10", "R-5-pregunta", N, "politica_relevo", K.c_S10, (),
                     _politica_con_default),
        Comprobacion("S11", "R-5-no-orquestador", N, "acciones", K.c_S11, (),
                     _acciones_mas("DECIDIR_RELEVO")),
        Comprobacion("S12", "R-6-remoto", N, "vigencia", K.c_S12, (), _vigencia_local),
        Comprobacion("S13", "R-6-sin-registro", N, "descubrir", K.c_S13, (),
                     _descubrir_con_registro),
        Comprobacion("S14", "R-6-sha-constitutivo", N, "descubrir", K.c_S14, (),
                     _descubrir_que_muta),
        Comprobacion("S15", "R-7-capacidades", N, "capacidades", K.c_S15, (),
                     _capacidades_ampliadas),
        Comprobacion("S16", "R-7-sin-campos", N, "campos_transporte", K.c_S16, (),
                     _transporte_con_campo),
        Comprobacion("S17", "R-8-no-ejecuta", N, "acciones", K.c_S17, (),
                     _acciones_mas("DESPLEGAR")),
        Comprobacion("S18", "R-8-no-reemplaza", D, "R-8-no-reemplaza", K.c_S18, NO_REEMPLAZA,
                     _doc("no reemplaza a REVOLUTIONS", "reemplaza a REVOLUTIONS")),
        Comprobacion("S19", "R-8-no-decide", N, "acciones", K.c_S19, (),
                     _acciones_mas("DECLARAR_VEREDICTO")),
        Comprobacion("S20", "R-8-no-estado", N, "constituir", K.c_S20, (),
                     _constituir_con_estado),
        Comprobacion("S21", "R-8-no-circular", N, "referencias", K.c_S21, (),
                     _referencias_con_sha),
        Comprobacion("S22", "R-8-no-modelo", N, "acciones", K.c_S22, (),
                     _acciones_mas("ELEGIR_MODELO")),
    ]


# -- extracto de la superficie que la comprobacion lee ------------------------

def extracto(comp, sujeto):
    """Lo que la comprobacion tiene delante. `E27` exige que el mutante lo altere."""
    if comp.tipo == D:
        return sujeto.superficie(comp.clave)
    valor = sujeto[comp.clave]
    if callable(valor):
        return observador.clave(valor.__code__)
    return repr(sorted(valor)) if isinstance(valor, (set, frozenset)) else repr(valor)


# -- unico despachador --------------------------------------------------------

def ejercer(comp, sujeto, ctx, motivo, sid_declarado=None, etiqueta=""):
    """Ejerce una comprobacion y observa cual se atraveso. La etiqueta no decide nada."""
    with observador.Travesia(ARCHIVOS_DE_COMPROBACION) as t:
        ok, observable = comp.fn(sujeto, ctx)
    return {
        "sid_declarado": sid_declarado or comp.sid,
        "obligacion": comp.obligacion,
        "superficie": comp.superficie_declarada(),
        "motivo": motivo,
        "sujeto": etiqueta or getattr(sujeto, "etiqueta", "conducta"),
        "ok": bool(ok),
        "observable": repr(observable),
        "clase_observable": type(observable).__name__,
        "identidad": t.identidad(),
        "atravesado": list(t.entradas),
    }
