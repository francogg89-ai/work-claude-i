"""Comprobaciones estructurales, su observable y su mutante.

Cada comprobación devuelve `(ok, observable, detalle)`.

Se ejercita dos veces: contra el sujeto real, donde debe pasar, y contra un mutante que viola la
obligación leída, donde debe fallar. El contrato exige además que el observable difiera entre
ambos: si no difiere, el mutante no está violando la propiedad que la comprobación lee, y la
comprobación no discrimina aunque parezca hacerlo.
"""

import builtins
import inspect
import io as _io
import re

import orquestador as mod


class Sujeto:
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
    """(no_escribio, rutas). El sustituto no toca el disco."""
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
    return (not abierto), abierto


def _orq(s, ctx, **kw):
    return s.clase(ctx["work_id"], ctx["autoridad"], **kw)


def _sonda_despachar(orq):
    """Registra el sobre pendiente en el instante en que se entra a despachar."""
    visto = []
    original = orq.despachar

    def envuelto():
        visto.append(dict(orq.sobre_pendiente) if orq.sobre_pendiente else None)
        return original()

    orq.despachar = envuelto
    return visto


def _o(valor):
    return repr(valor)


# -- comprobaciones -----------------------------------------------------------

def c_dos_caminos(s, ctx):
    o = _orq(s, ctx)
    acc = o.arranque_externo("PAQUETE")
    obs = _o(acc[0][0] if acc else None)
    return acc and acc[0][0] == "ENTREGAR_PAQUETE", obs, "arranque -> %s" % obs


def c_no_interpreta(s, ctx):
    paquete = "WORK_ID=x\n\n```json\n{\"a\": 1}\n```\n"
    o = _orq(s, ctx)
    acc = o.arranque_externo(paquete)
    entregado = acc[0][-1]
    return entregado == paquete, _o(entregado), "paquete identico = %s" % (entregado == paquete)


def c_no_escanear_prompt(s, ctx):
    a = ctx["sobre"](turn_id=5, next_instance="current", next_prompt="abri una instancia fresh")
    b = ctx["sobre"](turn_id=5, next_instance="current", next_prompt="continua normalmente")
    res = []
    for sobre in (a, b):
        o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=4)
        o.recibir(ctx["salida"](sobre))
        res.append(o.despachar()[0][:3])
    return res[0] == res[1], _o(res), "decisiones = %s" % _o(res)


def c_no_reconstruye(s, ctx):
    o = _orq(s, ctx)
    acc = o.recibir("sin bloque json")
    ok = len(acc) == 1 and len(acc[0]) == 2 and isinstance(acc[0][1], str)
    return ok, _o(acc), "accion = %s" % _o(acc)


def c_sin_fuentes_externas(s, ctx):
    imports = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", s.fuente, re.M))
    prohibidas = {"subprocess", "socket", "urllib", "http", "requests", "os", "shutil"}
    cruce = sorted(imports & prohibidas)
    return not cruce, _o(cruce), "importaciones prohibidas = %s" % cruce


def c_no_repara(s, ctx):
    o = _orq(s, ctx)
    acc = o.recibir(ctx["salida"](ctx["sobre"](protocol="otro")))
    ok = len(acc) == 1 and acc[0][0] == "DETENER_REPORTAR" and len(acc[0]) == 2
    return ok, _o(acc), "accion = %s" % _o(acc)


def c_no_adivina(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=6)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=9)))
    return o.ultimo_turn_id == 6, _o(o.ultimo_turn_id), "ultimo_turn_id = %s" % o.ultimo_turn_id


def c_git_prevalece(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=6)
    acc = o.reportar_contradiccion_con_git("el contador no corresponde a la historia")
    obs = (acc, o.ultimo_turn_id)
    ok = acc == [("DETENER_REPORTAR", "R-5-git-prevalece")] and o.ultimo_turn_id == 6
    return ok, _o(obs), "accion y estado = %s" % _o(obs)


def c_handle_efimero(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=0)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=1, next_instance="fresh")))
    ok, rutas = _sin_escritura(o.despachar)
    return ok, _o(rutas), "archivos abiertos = %s" % _o(rutas)


def c_fail_closed_no_crea(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=4)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=5, next_instance="current")))
    o.despachar()
    return o.instancias == {}, _o(o.instancias), "instancias = %s" % _o(o.instancias)


def c_fail_closed_no_entrega(s, ctx):
    o = _orq(s, ctx, ultimo_turn_id=4)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=5, next_instance="current")))
    acc = o.despachar()
    ok = all(a[0] != "ENTREGAR" for a in acc)
    return ok, _o(acc), "acciones = %s" % _o(acc)


def c_unit_no_decide(s, ctx):
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=10)
    antes = dict(o.instancias)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=11, next_instance="current", unit="u2 -> u3")))
    o.despachar()
    return o.instancias == antes, _o(o.instancias), "instancias = %s" % _o(o.instancias)


def c_vocabulario_cerrado(s, ctx):
    prohibidas = {"APROBAR_AUDITORIA", "EXIGIR_CORRECCION", "CERRAR_UNIDAD",
                  "DECIDIR_RELEVO", "DECIDIR_NECESIDAD", "OTORGAR_PERMISO"}
    cruce = sorted(set(s.acciones) & prohibidas)
    return not cruce, _o(cruce), "acciones de decision = %s" % cruce


def c_sin_modelo(s, ctx):
    cruce = sorted(set(s.acciones) & {"ELEGIR_MODELO", "SELECCIONAR_RUNTIME"})
    return not cruce, _o(cruce), "acciones de modelo = %s" % cruce


def c_sin_cadencia(s, ctx):
    nombres = [n for n, _ in inspect.getmembers(s.clase)]
    patron = re.compile(r"cadencia|relevo|rev_list|contar|counter", re.I)
    sosp = sorted(n for n in nombres if patron.search(n))
    imports = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", s.fuente, re.M))
    obs = (sosp, "subprocess" in imports)
    return (not sosp) and "subprocess" not in imports, _o(obs), "miembros y git = %s" % _o(obs)


def c_prompt_intacto(s, ctx):
    prompt = "línea uno\nlínea dos con acentos: auditoría\nlínea tres"
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=2)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=3, next_instance="current",
                                         next_prompt=prompt)))
    entregado = o.despachar()[-1][-1]
    return entregado == prompt, _o(entregado), "identico = %s" % (entregado == prompt)


def c_no_extiende(s, ctx):
    presentes = sorted(p for p in ("next_model", "next_runtime") if p in s.fuente)
    return not presentes, _o(presentes), "campos agregados = %s" % presentes


def c_detener_no_necesidad(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    acc = o.detener()
    ok = all(a[0] != "MOSTRAR_NECESIDAD" for a in acc)
    return ok, _o(acc), "acciones = %s" % _o(acc)


def c_detener_sin_io(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    ok, rutas = _sin_escritura(o.detener)
    return ok, _o(rutas), "archivos abiertos = %s" % _o(rutas)


def c_flag_efimero(s, ctx):
    o = _orq(s, ctx)
    o.detener()
    obs = ("stop_requested" in o.estado_efimero(), o.stop_requested)
    return obs == (True, True), _o(obs), "flag = %s" % _o(obs)


def c_frontera(s, ctx):
    """Con un sobre CONSTRUCTOR -> AUDITOR pendiente, DETENER pausa y conserva el sobre."""
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    acc = o.detener()
    entregado = any(a[0] == "ENTREGAR" for a in acc)
    conservado = o.sobre_pendiente is not None
    obs = (entregado, conservado)
    return (not entregado) and conservado, _o(obs), "(entregado, conservado) = %s" % _o(obs)


def c_continuar_mismo_objeto(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current",
                                         next_prompt="pase original")))
    guardado = o.sobre_pendiente["next_prompt"]
    o.detener()
    entregado = o.continuar()[-1][-1]
    return entregado == guardado, _o(entregado), "prompt entregado = %s" % _o(entregado)


def c_directiva_no_releva(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    antes = dict(o.instancias)
    o.detener()
    o.continuar("RELEVAR AUDITOR")
    return o.instancias == antes, _o(o.instancias), "instancias = %s" % _o(o.instancias)


def c_directiva_no_modifica(s, ctx):
    prompt = "pase original con acentos: auditoría"
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current",
                                         next_prompt=prompt)))
    o.detener()
    acc = o.continuar("RELEVAR AUDITOR")
    entrega = [a for a in acc if a[0] == "ENTREGAR"][0]
    return entrega[-1] == prompt, _o(entrega[-1]), "prompt entregado = %s" % _o(entrega[-1])


def c_directiva_fuera_del_json(s, ctx):
    """El sobre observado al despachar, despues de emitir la directiva, no la contiene."""
    directiva = "RELEVAR AUDITOR"
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    recibido = dict(o.sobre_pendiente)
    visto = _sonda_despachar(o)
    o.detener()
    o.continuar(directiva)
    observado = visto[-1] if visto else None
    igual = observado == recibido
    contiene = observado is not None and any(directiva in str(v) for v in observado.values())
    obs = (igual, contiene)
    return igual and not contiene, _o(obs), "(identico, contiene directiva) = %s" % _o(obs)


def c_directiva_no_saltea(s, ctx):
    o = _orq(s, ctx, instancias={"AUDITOR": "A#1"}, ultimo_turn_id=7)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=8, actor="CONSTRUCTOR",
                                         next_actor="AUDITOR", next_instance="current")))
    o.detener()
    acc = o.continuar("RELEVAR AUDITOR")
    entregado = any(a[0] == "ENTREGAR" and a[1] == "AUDITOR" for a in acc)
    return entregado, _o(entregado), "entrega pendiente entregada = %s" % entregado


def c_estado_admitido(s, ctx):
    o = _orq(s, ctx)
    claves = sorted(o.estado_efimero().keys())
    return set(claves) == set(s.estado_admitido), _o(claves), "estado = %s" % claves


def c_estado_sin_paralelo(s, ctx):
    o = _orq(s, ctx)
    claves = set(o.estado_efimero().keys()) | set(vars(o).keys())
    cruce = sorted(claves & set(mod.ESTADO_PROHIBIDO))
    return not cruce, _o(cruce), "estado paralelo = %s" % cruce


def c_reinicio_fail_closed(s, ctx):
    o = _orq(s, ctx, instancias={}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current")))
    acc = o.despachar()
    detiene = any(a[0] == "DETENER_REPORTAR" for a in acc)
    return detiene, _o(acc), "acciones = %s" % _o(acc)


def c_reinicio_no_degrada(s, ctx):
    o = _orq(s, ctx, instancias={}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current")))
    o.despachar()
    return o.instancias == {}, _o(o.instancias), "instancias = %s" % _o(o.instancias)


def c_sin_secretos(s, ctx):
    o = _orq(s, ctx)
    patron = re.compile(r"token|secret|password|credential|api_key", re.I)
    sosp = sorted({k for k in vars(o) if patron.search(k)} |
                  {n for n, _ in inspect.getmembers(s.clase) if patron.search(n)})
    return not sosp, _o(sosp), "miembros con secretos = %s" % sosp


def c_referencia_no_resuelta(s, ctx):
    prompt = "usar TOKEN_FUDO → variable de entorno FUDO_TOKEN, sin resolverla"
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current",
                                         next_prompt=prompt)))
    entregado = o.despachar()[-1][-1]
    return entregado == prompt, _o(entregado), "identico = %s" % (entregado == prompt)


def c_sin_logs(s, ctx):
    o = _orq(s, ctx, instancias={"CONSTRUCTOR": "C#1"}, ultimo_turn_id=12)
    o.recibir(ctx["salida"](ctx["sobre"](turn_id=13, next_instance="current",
                                         next_prompt="TOKEN_FUDO → FUDO_TOKEN")))
    ok, rutas = _sin_escritura(o.despachar)
    return ok, _o(rutas), "archivos abiertos = %s" % _o(rutas)


# -- mutantes -----------------------------------------------------------------

def _mut(**metodos):
    return REAL.copia(clase=type("Mutante", (mod.Orquestador,), metodos))


def m_dos_caminos():
    return _mut(arranque_externo=lambda self, paquete: self.recibir(paquete))


def m_interpreta():
    def arranque_externo(self, paquete):
        self.instancias["AUDITOR"] = "AUDITOR#externo"
        return [("ENTREGAR_PAQUETE", "AUDITOR", "AUDITOR#externo", paquete.strip().upper())]
    return _mut(arranque_externo=arranque_externo)


def m_escanea_prompt():
    def despachar(self):
        if self.sobre_pendiente and "fresh" in (self.sobre_pendiente.get("next_prompt") or ""):
            self.sobre_pendiente = dict(self.sobre_pendiente, next_instance="fresh")
        return mod.Orquestador.despachar(self)
    return _mut(despachar=despachar)


def m_reconstruye():
    def recibir(self, salida_texto):
        sobre, regla = self.extraer(salida_texto)
        if regla is not None:
            return [("DETENER_REPORTAR", regla, {"protocol": "revolutions-hop/v1"})]
        return mod.Orquestador.recibir(self, salida_texto)
    return _mut(recibir=recibir)


def m_importa_git():
    return REAL.copia(fuente="import subprocess\n" + REAL.fuente)


def m_repara():
    def recibir(self, salida_texto):
        acc = mod.Orquestador.recibir(self, salida_texto)
        if acc[0][0] == "DETENER_REPORTAR":
            return [acc[0] + ("sugerencia: corregir protocol",)]
        return acc
    return _mut(recibir=recibir)


def m_adivina():
    def recibir(self, salida_texto):
        sobre, regla = self.extraer(salida_texto)
        if regla is None and sobre["turn_id"] != self.ultimo_turn_id + 1:
            self.ultimo_turn_id = sobre["turn_id"]
        return mod.Orquestador.recibir(self, salida_texto)
    return _mut(recibir=recibir)


def m_resuelve_git():
    def reportar_contradiccion_con_git(self, detalle):
        self.ultimo_turn_id = 0
        return [("RECIBIDO",)]
    return _mut(reportar_contradiccion_con_git=reportar_contradiccion_con_git)


def m_persiste_handle():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        with open("handle_persistido.tmp", "w") as f:
            f.write("x")
        return acc
    return _mut(despachar=despachar)


def m_degrada():
    def despachar(self):
        s = self.sobre_pendiente
        if s and s.get("next_instance") == "current" and s["next_actor"] not in self.instancias:
            self.sobre_pendiente = dict(s, next_instance="fresh")
        return mod.Orquestador.despachar(self)
    return _mut(despachar=despachar)


def m_unit_decide():
    def despachar(self):
        if self.sobre_pendiente and self.sobre_pendiente.get("unit") is not None:
            self.instancias["CONSTRUCTOR"] = "C#reabierto"
        return mod.Orquestador.despachar(self)
    return _mut(despachar=despachar)


def m_acciones_decisorias():
    return REAL.copia(acciones=set(mod.ACCIONES) | {"CERRAR_UNIDAD", "DECIDIR_RELEVO"})


def m_acciones_modelo():
    return REAL.copia(acciones=set(mod.ACCIONES) | {"ELEGIR_MODELO"})


def m_deriva_cadencia():
    return _mut(derivar_cadencia=lambda self: 0)


def m_toca_prompt():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        if acc and acc[-1][0] == "ENTREGAR":
            a = list(acc[-1])
            a[-1] = a[-1].split("\n")[0]
            acc[-1] = tuple(a)
        return acc
    return _mut(despachar=despachar)


def m_extiende_contrato():
    return REAL.copia(fuente=REAL.fuente + '\nCAMPO_EXTRA = "next_model"\n')


def m_detener_necesidad():
    return _mut(detener=lambda self: [("MOSTRAR_NECESIDAD",)])


def m_detener_escribe():
    def detener(self):
        with open("detencion_durable.tmp", "w") as f:
            f.write("x")
        return mod.Orquestador.detener(self)
    return _mut(detener=detener)


def m_sin_flag():
    return _mut(detener=lambda self: [("PAUSA_SOLICITADA",)])


def m_frontera_entrega():
    """Viola la frontera: con el sobre pendiente hacia el AUDITOR, DETENER lo entrega."""
    def detener(self):
        self.stop_requested = False
        return mod.Orquestador.despachar(self)
    return _mut(detener=detener)


def m_continuar_reconstruye():
    def continuar(self, directiva=None):
        if self.sobre_pendiente:
            self.sobre_pendiente = dict(self.sobre_pendiente,
                                        next_prompt="pase reconstruido")
        return mod.Orquestador.continuar(self, directiva)
    return _mut(continuar=continuar)


def m_aplica_relevo():
    def continuar(self, directiva=None):
        if directiva and "RELEVAR" in directiva:
            self.instancias["AUDITOR"] = "AUDITOR#relevado"
        return mod.Orquestador.continuar(self, directiva)
    return _mut(continuar=continuar)


def m_concatena_directiva():
    def continuar(self, directiva=None):
        if directiva and self.sobre_pendiente:
            self.sobre_pendiente = dict(
                self.sobre_pendiente,
                next_prompt=self.sobre_pendiente["next_prompt"] + "\n\n" + directiva)
        return mod.Orquestador.continuar(self, directiva)
    return _mut(continuar=continuar)


def m_directiva_en_json():
    def continuar(self, directiva=None):
        if directiva and self.sobre_pendiente:
            self.sobre_pendiente = dict(self.sobre_pendiente, unit=directiva)
        return mod.Orquestador.continuar(self, directiva)
    return _mut(continuar=continuar)


def m_saltea_entrega():
    def continuar(self, directiva=None):
        if directiva:
            self.sobre_pendiente = None
            return [("ENTREGAR_DIRECTIVA", directiva)]
        return mod.Orquestador.continuar(self, directiva)
    return _mut(continuar=continuar)


def m_estado_extra():
    def estado_efimero(self):
        d = mod.Orquestador.estado_efimero(self)
        d["work_status"] = "abierto"
        return d
    return _mut(estado_efimero=estado_efimero)


def m_estado_paralelo():
    def __init__(self, *a, **k):
        mod.Orquestador.__init__(self, *a, **k)
        self.relay_pending = False
    return _mut(__init__=__init__)


def m_guarda_secreto():
    def __init__(self, *a, **k):
        mod.Orquestador.__init__(self, *a, **k)
        self.api_key = "no deberia existir"
    return _mut(__init__=__init__)


def m_expande_referencia():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        if acc and acc[-1][0] == "ENTREGAR":
            a = list(acc[-1])
            a[-1] = a[-1].replace("FUDO_TOKEN", "valor-expandido")
            acc[-1] = tuple(a)
        return acc
    return _mut(despachar=despachar)


def m_escribe_log():
    def despachar(self):
        acc = mod.Orquestador.despachar(self)
        with open("orquestador.log", "a") as f:
            f.write("x")
        return acc
    return _mut(despachar=despachar)


# -- registro -----------------------------------------------------------------

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
    "R-9.1-frontera":         (c_frontera, m_frontera_entrega),
    "R-9.2-no-reconstruye":   (c_continuar_mismo_objeto, m_continuar_reconstruye),
    "R-9.3-no-aplica-relevo": (c_directiva_no_releva, m_aplica_relevo),
    "R-9.3-no-modifica":      (c_directiva_no_modifica, m_concatena_directiva),
    "R-9.3-no-en-json":       (c_directiva_fuera_del_json, m_directiva_en_json),
    "R-9.3-no-saltea":        (c_directiva_no_saltea, m_saltea_entrega),
    "R-10-estado-admitido":   (c_estado_admitido, m_estado_extra),
    "R-10-no-paralelo":       (c_estado_sin_paralelo, m_estado_paralelo),
    "R-10.1-fail-closed":     (c_reinicio_fail_closed, m_degrada),
    "R-10.1-no-degrada":      (c_reinicio_no_degrada, m_degrada),
    "R-11-no-necesita":       (c_sin_secretos, m_guarda_secreto),
    "R-11-no-resuelve":       (c_referencia_no_resuelta, m_expande_referencia),
    "R-11-no-logs":           (c_sin_logs, m_escribe_log),
}

# Comprobación sintética de N16: su mutante no altera el observable que ella lee.
def c_sintetica(s, ctx):
    o = _orq(s, ctx)
    obs = _o(sorted(o.estado_efimero().keys()))
    return True, obs, "observable inerte = %s" % obs


def m_sintetico_inerte():
    """Cambia algo que la comprobación no lee: el observable no puede diferir."""
    return _mut(reportar_contradiccion_con_git=lambda self, d: [("RECIBIDO",)])
