from datetime import datetime, timedelta

import pytest

from servicios import configuracion, repositorio_json
from servicios.servicio_expedientes import ServicioExpedientes


def cotejo_valido():
    return {
        "modalidad": "Física", "folios_declarados": 2, "folios_verificados": 2,
        "presenta_anexos": False, "cantidad_anexos": 0, "anexos": [], "firma": "Sí",
        "legible": True, "completo": True, "responsable": "Abel Ruiz", "observaciones": "",
        "excepcion_autorizada": False, "motivo_excepcion": "",
    }


def datos_expediente(tipo="Carta"):
    return {
        "nombre_completo": "Ana Díaz", "tipo_documento_identidad": "DNI", "numero_documento": "12345678",
        "tipo_documento_presentado": tipo, "tipo_documento_otro": "", "asunto": "Archivo",
        "fecha_recepcion": "", "hora_recepcion": "", "archivos_adjuntos": [], "cotejo": cotejo_valido(),
    }


def servicio_temporal(tmp_path, monkeypatch):
    monkeypatch.setattr(repositorio_json, "ARCHIVO_DATOS", tmp_path / "expedientes.json")
    servicio = ServicioExpedientes()
    servicio.directorio_datos = tmp_path / "datos"
    servicio.archivo_borradores = tmp_path / "borradores.json"
    return servicio


def test_registra_codigos_fecha_hora_y_recarga(tmp_path, monkeypatch):
    servicio = servicio_temporal(tmp_path, monkeypatch)
    ahora = datetime.now()
    primero = servicio.registrar(datos_expediente("Carta"))
    segundo = servicio.registrar(datos_expediente("Solicitud"))

    assert primero.codigo == "EXP001"
    assert segundo.codigo == "EXP002"
    assert primero.codigo_documento == "BOG001"
    assert segundo.codigo_documento == "BEN001"
    registrado = datetime.strptime(f"{primero.fecha_recepcion} {primero.hora_recepcion}", "%d/%m/%Y %H:%M:%S")
    assert ahora - timedelta(seconds=5) <= registrado <= datetime.now()
    recargado = ServicioExpedientes()
    assert recargado.buscar("EXP001")["codigo_documento"] == "BOG001"


def test_guarda_borrador_observado_y_lo_elimina_al_registrar(tmp_path, monkeypatch):
    servicio = servicio_temporal(tmp_path, monkeypatch)
    datos = datos_expediente()
    datos["cotejo"]["observaciones"] = "Falta una firma."
    codigo_borrador = servicio.guardar_borrador(datos)
    assert servicio.listar_borradores()[0]["estado_cotejo"] == "Observado"
    datos["cotejo"] = cotejo_valido()
    datos["borrador_id"] = codigo_borrador
    servicio.registrar(datos)
    assert servicio.listar_borradores() == []


def test_flujo_foliacion_cargo_clasificacion_y_derivacion(tmp_path, monkeypatch):
    servicio = servicio_temporal(tmp_path, monkeypatch)
    monkeypatch.setattr(configuracion, "cargar", lambda: {"nombre_entidad": "", "unidades": ["Mesa de partes"], "sugerencias": {}})
    registro = servicio.registrar(datos_expediente())
    ficha = servicio.generar_foliacion(registro.codigo, "Abel Ruiz")
    assert ficha.is_file()
    servicio.confirmar_foliacion(registro.codigo, 2, "Abel Ruiz")
    cargo = servicio.generar_cargo(registro.codigo)
    assert cargo.is_file() and cargo.read_bytes().startswith(b"%PDF")
    servicio.guardar_clasificacion(registro.codigo, {
        "unidad": "Mesa de partes", "tramite": "Registro", "categoria": "Entrada",
        "prioridad": "Normal", "motivo_prioridad": "", "responsable": "Abel Ruiz",
    })
    servicio.marcar_listo_derivacion(registro.codigo, "Abel Ruiz")
    servicio.derivar(registro.codigo, {"modalidad": "Digital", "responsable": "Abel Ruiz", "receptor": "Unidad", "guia": "G-1"})
    movimiento = servicio.buscar(registro.codigo)["derivaciones"][0]
    assert movimiento["estado"] == "Enviado"
    assert "no se realizó una transferencia electrónica" in movimiento["nota_transferencia"]
    recibo = servicio.generar_cargo_derivacion(registro.codigo)
    assert recibo.is_file()
    servicio.confirmar_entrega(registro.codigo, "Unidad")
    assert servicio.buscar(registro.codigo)["estado"] == "Entregado"


def test_no_prepara_despacho_si_falta_foliacion_o_cargo(tmp_path, monkeypatch):
    servicio = servicio_temporal(tmp_path, monkeypatch)
    monkeypatch.setattr(configuracion, "cargar", lambda: {"nombre_entidad": "", "unidades": ["Unidad"], "sugerencias": {}})
    registro = servicio.registrar(datos_expediente())
    servicio.guardar_clasificacion(registro.codigo, {
        "unidad": "Unidad", "tramite": "Registro", "categoria": "Entrada",
        "prioridad": "Normal", "motivo_prioridad": "", "responsable": "Abel Ruiz",
    })
    with pytest.raises(ValueError, match="foliación"):
        servicio.marcar_listo_derivacion(registro.codigo, "Abel Ruiz")
