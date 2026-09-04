"""Comprobaciones estructurales y sus mutantes.

Cada comprobación se ejercita dos veces: contra el sujeto real, donde debe pasar, y contra un
mutante sintético que viola exactamente esa obligación, donde debe fallar.

Una comprobación que no falla sobre su mutante no discrimina nada y no entra en la evidencia.
Esa es la exigencia E6 del contrato congelado.
"""

import builtins
import inspect
import re

import orquestador as mod


class Sujeto:
    """Lo que una comprobación necesita observar. El mutante es una copia con un cambio."""

    def __init__(self, clase=None, acciones=None, estado_admitido=None, fuente=None):
        self.clase = clase or mod.Orquestador
        self.acciones = acciones if acciones is not None else mod.ACCIONES
        self.estado_admitido = (estado_admitido if estado_admitido is not None
                                else mod.ESTADO_ADMITIDO)
        self.fuente = fuente if fuente is not None else inspect.getsource(mod)

    def copia(self, **cambios):
        base = dict(clase=self.clase, acciones=self.acciones,
                    estado_admitido=self.estado_admitido, fuente=self.fuente)
        base.update(cambios)
        return Sujeto(**base)


REAL = Sujeto()


# -- utilidades ---------------------------------------------------------------

def _sin_escritura(fn):
    """True si fn() no abrió ningún archivo.

    El sustituto no toca el disco: un mutante que intente escribir queda registrado sin
    dejar rastro en el árbol de trabajo.
    """
    import io as _io

    original = builtins.open
    abierto = []

    def espia(*a, **k):
        abierto.append(a[0] if a else None)
        return _io.StringIO()

    builtins.open = espia
    try:
        fn()
    finally:
        builtins.open = original
    return not abierto


def _orq(s, ctx, **kw):
    return s.clase(ctx["work_id"], ctx["autoridad"], **kw)


# -- comprobaciones -----------------------------------------------------------

def c_dos_caminos(s, ctx):
    o = _orq(s, ctx)
    tiene = hasattr(o, "arranque_externo") and hasattr(o, "recibir")
    if not tiene:
        return False, "faltan los dos caminos"
    acc = o.arranque_externo("PAQUETE")
    distinto = acc and acc[0][0] == "ENTREGAR_PAQUETE"
    return distinto, "arranque -> %s" % (acc[0][0] if acc else None)


def c_no_interpreta(s, ctx):
    paquete = "WORK_ID=x\n\n```json\n{\"a\": 1}\n```\n"
    o = _orq(s, ctx)
    acc = o.arranque_externo(paquete)
    entregado = acc[0][-1]
    return entregado == paquete, "paquete entregado identico = %s" % (entregado == paquete)


def c_no_escanear_prompt(s, ctx):
    a = ctx["sobre"](turn_id=5, next_instance="current", next_prompt="abri una instancia fresh")
    b = ctx["sobre"](turn_id=5, next_instance="current", next_prompt="continua normalmente")
    res = []
    for sobre in (a, b):
        o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=4)
        o.recibir(ctx["salida"](sobre))
        res.append(o.despachar())
    igual = res[0][0][:3] == res[1][0][:3]
    return igual, "decision identica = %s" % igual


def c_no_reconstruye(s, ctx):
    o = _orq(s, ctx)
    acc = o.recibir("sin bloque json")
    solo_regla = len(acc) == 1 and len(acc[0]) == 2 and isinstance(acc[0][1], str)
    return solo_regla, "accion = %s" % (acc,)


def c_sin_fuentes_externas(s, ctx):
    imports = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", s.fuente, re.M))
    prohibidas = {"subprocess", "socket", "urllib", "http", "requests", "os", "shutil"}
    cruce = imports & prohibidas
    return not cruce, "importaciones prohibidas = %s" % sorted(cruce)


def c_no_repara(s, ctx):
    o = _orq(s, ctx)
    acc = o.recibir(ctx["salida"](ctx["sobre"](protocol="otro")))
    bien = len(acc) == 1 and acc[0][0] == "DETENER_REPORTAR" and len(acc[0]) == 2
    return bien, "accion = %s" % (acc,)


def c_no_adivina(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=6)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=9)))
    return o.ultimo_turn_id == 6, "ultimo_turn_id tras rechazo = %s" % o.ultimo_turn_id


def c_git_prevalece(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=6)
    acc = o.reportar_contradiccion_con_git("el contador no corresponde a la historia")
    reporta = acc == [("DETENER_REPORTAR", "R-5-git-prevalece")]
    return reporta and o.ultimo_turn_id == 6, "accion = %s, estado = %s" % (acc, o.ultimo_turn_id)


def c_handle_efimero(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=0)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=1, next_instance="fresh")))
    return _sin_escritura(o.despachar), "no se escribio ningun archivo"


def c_fail_closed_no_crea(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=4)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=5, next_instance="current")))
    o.despachar()
    return o.instancias == {}, "instancias tras fail-closed = %s" % o.instancias


def c_fail_closed_no_entrega(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=4)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=5, next_instance="current")))
    acc = o.despachar()
    return all(a[0] != "ENTREGAR" for a in acc), "acciones = %s" % (acc,)


def c_unit_no_decide(s, ctx):
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=10)
    antes = dict(o.instancias)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=11, next_instance="current", unit="u2 -> u3")))
    o.despachar()
    return o.instancias == antes, "instancias sin cambio = %s" % (o.instancias == antes)


def c_vocabulario_cerrado(s, ctx):
    prohibidas = {"APROBAR_AUDITORIA", "EXIGIR_CORRECCION", "CERRAR_UNIDAD",
                  "DECIDIR_RELEVO", "DECIDIR_NECESIDAD", "OTORGAR_PERMISO"}
    cruce = set(s.acciones) & prohibidas
    return not cruce, "acciones de decision = %s" % sorted(cruce)


def c_sin_modelo(s, ctx):
    prohibidas = {"ELEGIR_MODELO", "SELECCIONAR_RUNTIME"}
    cruce = set(s.acciones) & prohibidas
    return not cruce, "acciones de modelo = %s" % sorted(cruce)


def c_sin_cadencia(s, ctx):
    nombres = [n for n, _ in inspect.getmembers(s.clase)]
    nombres += [n for n in dir(mod) if not n.startswith("__")]
    patron = re.compile(r"cadencia|relevo|rev_list|contar|counter", re.I)
    sosp = [n for n in nombres if patron.search(n)]
    imports = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", s.fuente, re.M))
    return (not sosp and "subprocess" not in imports,
            "miembros sospechosos = %s" % sorted(sosp))


def c_prompt_intacto(s, ctx):
    prompt = "línea uno\nlínea dos con acentos: auditoría\nlínea tres"
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=2)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=3, next_instance="current",
                                         next_prompt=prompt)))
    acc = o.despachar()
    entregado = acc[-1][-1]
    return entregado == prompt, "prompt identico = %s" % (entregado == prompt)


def c_no_extiende(s, ctx):
    prohibidas = {"next_model", "next_runtime"}
    presentes = [p for p in prohibidas if p in s.fuente]
    return not presentes, "campos agregados = %s" % presentes


def c_detener_no_necesidad(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    acc = o.detener()
    return all(a[0] != "MOSTRAR_NECESIDAD" for a in acc), "acciones = %s" % (acc,)


def c_detener_sin_io(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    return _sin_escritura(o.detener), "DETENER no escribio ningun archivo"


def c_flag_efimero(s, ctx):
    o = _orq(s, ctx)
    o.detener()
    return ("stop_requested" in o.estado_efimero() and o.stop_requested is True,
            "stop_requested = %s" % o.stop_requested)


def c_frontera(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    acc = o.detener()
    preservado = o.sobre_pendiente is not None
    return (acc == [("PAUSA_SIN_ENTREGAR",)] and preservado,
            "acciones = %s, sobre preservado = %s" % (acc, preservado))


def c_continuar_mismo_objeto(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current",
                                         next_prompt="pase original")))
    guardado = o.sobre_pendiente
    o.detener()
    acc = o.continuar()
    return acc[-1][-1] == guardado["next_prompt"], "prompt entregado = %r" % acc[-1][-1]


def c_directiva_no_releva(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    antes = dict(o.instancias)
    o.detener()
    o.continuar("RELEVAR AUDITOR")
    return o.instancias == antes, "instancias sin cambio = %s" % (o.instancias == antes)


def c_directiva_no_modifica(s, ctx):
    prompt = "pase original con acentos: auditoría"
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current",
                                         next_prompt=prompt)))
    o.detener()
    acc = o.continuar("RELEVAR AUDITOR")
    entrega = [a for a in acc if a[0] == "ENTREGAR"][0]
    return entrega[-1] == prompt, "prompt entregado = %r" % entrega[-1]


def c_directiva_fuera_del_json(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    guardado = dict(o.sobre_pendiente)
    o.detener()
    acc = o.continuar("RELEVAR AUDITOR")
    en_sobre = any("RELEVAR" in str(v) for v in guardado.values())
    aparte = any(a[0] == "ENTREGAR_DIRECTIVA" for a in acc)
    return (not en_sobre) and aparte, "en sobre = %s, canal aparte = %s" % (en_sobre, aparte)


def c_directiva_no_saltea(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    o.detener()
    acc = o.continuar("RELEVAR AUDITOR")
    entregado = any(a[0] == "ENTREGAR" and a[1] == "AUDITOR" for a in acc)
    return entregado, "la entrega pendiente se entrego = %s" % entregado


def c_estado_admitido(s, ctx):
    o = _orq(s, ctx)
    claves = set(o.estado_efimero().keys())
    return claves == set(s.estado_admitido), "estado = %s" % sorted(claves)


def c_estado_sin_paralelo(s, ctx):
    o = _orq(s, ctx)
    claves = set(o.estado_efimero().keys()) | set(vars(o).keys())
    cruce = claves & set(mod.ESTADO_PROHIBIDO)
    return not cruce, "estado paralelo = %s" % sorted(cruce)


def c_reinicio_fail_closed(s, ctx):
    """Reinicio: instancia perdida, el salto no se degrada."""
    o = _orq(s, ctx, instancias={}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current")))
    acc = o.despachar()
    detiene = any(a[0] == "DETENER_REPORTAR" for a in acc)
    return detiene, "acciones = %s" % (acc,)


def c_reinicio_no_degrada(s, ctx):
    o = _orq(s, ctx, instancias={}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current")))
    o.despachar()
    return o.instancias == {}, "instancias = %s" % o.instancias


def c_sin_secretos(s, ctx):
    o = _orq(s, ctx)
    patron = re.compile(r"token|secret|password|credential|api_key", re.I)
    sosp = [k for k in vars(o) if patron.search(k)]
    sosp += [n for n, _ in inspect.getmembers(s.clase) if patron.search(n)]
    return not sosp, "miembros con secretos = %s" % sorted(set(sosp))


def c_referencia_no_resuelta(s, ctx):
    prompt = "usar TOKEN_FUDO → variable de entorno FUDO_TOKEN, sin resolverla"
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current",
                                         next_prompt=prompt)))
    acc = o.despachar()
    return acc[-1][-1] == prompt, "prompt entregado identico = %s" % (acc[-1][-1] == prompt)


def c_sin_logs(s, ctx):
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current",
                                         next_prompt="TOKEN_FUDO → FUDO_TOKEN")))
    return _sin_escritura(o.despachar), "no se escribio ningun log"


# -- mutantes -----------------------------------------------------------------

def _clase_mutante(**metodos):
    return type("Mutante", (mod.Orquestador,), metodos)


def m_dos_caminos():
    def arranque_externo(self, paquete):
        return self.recibir(paquete)
    return REAL.copia(clase=_clase_mutante(arranque_externo=arranque_externo))


def m_interpreta():
    def arranque_externo(self, paquete):
        self.instancias["AUDITOR"] = "AUDITOR#externo"
        return [("ENTREGAR_PAQUETE", "AUDITOR", "AUDITOR#externo", paquete.strip().upper())]
    return REAL.copia(clase=_clase_mutante(arranque_externo=arranque_externo))


def m_escanea_prompt():
    base = mod.Orquestador

    def despachar(self):
        if self.sobre_pendiente and "fresh" in (self.sobre_pendiente.get("next_prompt") or ""):
            self.sobre_pendiente = dict(self.sobre_pendiente, next_instance="fresh")
        return base.despachar(self)
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_reconstruye():
    def recibir(self, salida_texto):
        sobre, regla = self.extraer(salida_texto)
        if regla is not None:
            return [("DETENER_REPORTAR", regla, {"protocol": "revolutions-hop/v1"})]
        return mod.Orquestador.recibir(self, salida_texto)
    return REAL.copia(clase=_clase_mutante(recibir=recibir))


def m_importa_git():
    return REAL.copia(fuente="import subprocess\n" + REAL.fuente)


def m_repara():
    def recibir(self, salida_texto):
        acc = mod.Orquestador.recibir(self, salida_texto)
        if acc[0][0] == "DETENER_REPORTAR":
            return [acc[0] + ("sugerencia: corregir protocol",)]
        return acc
    return REAL.copia(clase=_clase_mutante(recibir=recibir))


def m_adivina():
    def recibir(self, salida_texto):
        sobre, regla = self.extraer(salida_texto)
        if regla is None and sobre["turn_id"] != self.ultimo_turn_id + 1:
            self.ultimo_turn_id = sobre["turn_id"]
        return mod.Orquestador.recibir(self, salida_texto)
    return REAL.copia(clase=_clase_mutante(recibir=recibir))


def m_resuelve_git():
    def reportar_contradiccion_con_git(self, detalle):
        self.ultimo_turn_id = 0
        return [("RECIBIDO",)]
    return REAL.copia(clase=_clase_mutante(
        reportar_contradiccion_con_git=reportar_contradiccion_con_git))


def m_persiste_handle():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        with open("handle_persistido.tmp", "w") as f:
            f.write(str(self.instancias))
        return acc
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_degrada():
    def despachar(self):
        sobre = self.sobre_pendiente
        if sobre and sobre.get("next_instance") == "current" \
                and sobre["next_actor"] not in self.instancias:
            self.sobre_pendiente = dict(sobre, next_instance="fresh")
        return mod.Orquestador.despachar(self)
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_unit_decide():
    def despachar(self):
        if self.sobre_pendiente and self.sobre_pendiente.get("unit") is not None:
            self.instancias["CONSTRUCTOR"] = "C#reabierto"
        return mod.Orquestador.despachar(self)
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_acciones_decisorias():
    return REAL.copia(acciones=set(mod.ACCIONES) | {"CERRAR_UNIDAD", "DECIDIR_RELEVO"})


def m_acciones_modelo():
    return REAL.copia(acciones=set(mod.ACCIONES) | {"ELEGIR_MODELO"})


def m_deriva_cadencia():
    def derivar_cadencia(self):
        return 0
    return REAL.copia(clase=_clase_mutante(derivar_cadencia=derivar_cadencia))


def m_toca_prompt():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        if acc and acc[-1][0] == "ENTREGAR":
            a = list(acc[-1])
            a[-1] = a[-1].split("\n")[0]
            acc[-1] = tuple(a)
        return acc
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_extiende_contrato():
    return REAL.copia(fuente=REAL.fuente + '\nCAMPO_EXTRA = "next_model"\n')


def m_detener_necesidad():
    def detener(self):
        return [("MOSTRAR_NECESIDAD",)]
    return REAL.copia(clase=_clase_mutante(detener=detener))


def m_detener_escribe():
    def detener(self):
        with open("detencion_durable.tmp", "w") as f:
            f.write("detenido")
        return mod.Orquestador.detener(self)
    return REAL.copia(clase=_clase_mutante(detener=detener))


def m_sin_flag():
    def detener(self):
        return [("PAUSA_SOLICITADA",)]
    return REAL.copia(clase=_clase_mutante(detener=detener))


def m_entrega_en_pausa():
    def detener(self):
        self.stop_requested = True
        return mod.Orquestador.despachar(self)
    return REAL.copia(clase=_clase_mutante(detener=detener))


def m_continuar_reconstruye():
    def continuar(self, directiva=None):
        if self.sobre_pendiente:
            self.sobre_pendiente = dict(self.sobre_pendiente,
                                        next_prompt="pase reconstruido")
        return mod.Orquestador.continuar(self, directiva)
    return REAL.copia(clase=_clase_mutante(continuar=continuar))


def m_aplica_relevo():
    def continuar(self, directiva=None):
        if directiva and "RELEVAR" in directiva:
            self.instancias.pop("AUDITOR", None)
            self.instancias["AUDITOR"] = "AUDITOR#relevado"
        return mod.Orquestador.continuar(self, directiva)
    return REAL.copia(clase=_clase_mutante(continuar=continuar))


def m_concatena_directiva():
    def continuar(self, directiva=None):
        if directiva and self.sobre_pendiente:
            self.sobre_pendiente = dict(
                self.sobre_pendiente,
                next_prompt=self.sobre_pendiente["next_prompt"] + "\n\n" + directiva)
        return mod.Orquestador.continuar(self, directiva)
    return REAL.copia(clase=_clase_mutante(continuar=continuar))


def m_directiva_en_json():
    def continuar(self, directiva=None):
        if directiva and self.sobre_pendiente:
            self.sobre_pendiente = dict(self.sobre_pendiente, unit=directiva)
        return mod.Orquestador.continuar(self, directiva)
    return REAL.copia(clase=_clase_mutante(continuar=continuar))


def m_saltea_entrega():
    def continuar(self, directiva=None):
        if directiva:
            self.sobre_pendiente = None
            return [("ENTREGAR_DIRECTIVA", directiva)]
        return mod.Orquestador.continuar(self, directiva)
    return REAL.copia(clase=_clase_mutante(continuar=continuar))


def m_estado_extra():
    def estado_efimero(self):
        d = mod.Orquestador.estado_efimero(self)
        d["work_status"] = "abierto"
        return d
    return REAL.copia(clase=_clase_mutante(estado_efimero=estado_efimero))


def m_estado_paralelo():
    def __init__(self, *a, **k):
        mod.Orquestador.__init__(self, *a, **k)
        self.relay_pending = False
    return REAL.copia(clase=_clase_mutante(__init__=__init__))


def m_reinicio_degrada():
    return m_degrada()


def m_guarda_secreto():
    def __init__(self, *a, **k):
        mod.Orquestador.__init__(self, *a, **k)
        self.api_key = "no deberia existir"
    return REAL.copia(clase=_clase_mutante(__init__=__init__))


def m_expande_referencia():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        if acc and acc[-1][0] == "ENTREGAR":
            a = list(acc[-1])
            a[-1] = a[-1].replace("FUDO_TOKEN", "valor-expandido")
            acc[-1] = tuple(a)
        return acc
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


def m_escribe_log():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        with open("orquestador.log", "a") as f:
            f.write(str(acc))
        return acc
    return REAL.copia(clase=_clase_mutante(despachar=despachar))


# -- registro: obligación -> (comprobación, mutante) --------------------------

COMPROBACIONES = {
    "R-1-dos-caminos":        (c_dos_caminos, m_dos_caminos),
    "R-1.1-no-interpreta":    (c_no_interpreta, m_interpreta),
    "R-2-no-escanear-prompt": (c_no_escanear_prompt, m_escanea_prompt),
    "R-2-no-reconstruye":     (c_no_reconstruye, m_reconstruye),
    "R-3-no-lee-fuentes":     (c_sin_fuentes_externas, m_importa_git),
    "R-4-no-repara":          (c_no_repara, m_repara),
    "R-5-no-adivina":         (c_no_adivina, m_adivina),
    "R-5-git-prevalece":      (c_git_prevalece, m_resuelve_git),
    "R-6-handle-efimero":     (c_handle_efimero, m_persiste_handle),
    "R-6.1-no-degrada":       (c_fail_closed_no_crea, m_degrada),
    "R-6.1-no-inventa":       (c_fail_closed_no_entrega, m_degrada),
    "R-7-unit-no-decide":     (c_unit_no_decide, m_unit_decide),
    "R-7-no-consulta-git":    (c_sin_fuentes_externas, m_importa_git),
    "R-8-no-decide":          (c_vocabulario_cerrado, m_acciones_decisorias),
    "R-8-no-elige-modelo":    (c_sin_modelo, m_acciones_modelo),
    "R-8-no-cadencia":        (c_sin_cadencia, m_deriva_cadencia),
    "R-8-no-toca-prompt":     (c_prompt_intacto, m_toca_prompt),
    "R-8-no-copia-git":       (c_prompt_intacto, m_toca_prompt),
    "R-8-no-extiende":        (c_no_extiende, m_extiende_contrato),
    "R-9-no-necesidad":       (c_detener_no_necesidad, m_detener_necesidad),
    "R-9-no-git":             (c_sin_fuentes_externas, m_importa_git),
    "R-9-no-durable":         (c_detener_sin_io, m_detener_escribe),
    "R-9-flag-efimero":       (c_flag_efimero, m_sin_flag),
    "R-9.1-frontera":         (c_frontera, m_entrega_en_pausa),
    "R-9.2-no-reconstruye":   (c_continuar_mismo_objeto, m_continuar_reconstruye),
    "R-9.3-no-aplica-relevo": (c_directiva_no_releva, m_aplica_relevo),
    "R-9.3-no-modifica":      (c_directiva_no_modifica, m_concatena_directiva),
    "R-9.3-no-en-json":       (c_directiva_fuera_del_json, m_directiva_en_json),
    "R-9.3-no-saltea":        (c_directiva_no_saltea, m_saltea_entrega),
    "R-10-estado-admitido":   (c_estado_admitido, m_estado_extra),
    "R-10-no-paralelo":       (c_estado_sin_paralelo, m_estado_paralelo),
    "R-10.1-fail-closed":     (c_reinicio_fail_closed, m_reinicio_degrada),
    "R-10.1-no-degrada":      (c_reinicio_no_degrada, m_reinicio_degrada),
    "R-11-no-necesita":       (c_sin_secretos, m_guarda_secreto),
    "R-11-no-resuelve":       (c_referencia_no_resuelta, m_expande_referencia),
    "R-11-no-logs":           (c_sin_logs, m_escribe_log),
}
