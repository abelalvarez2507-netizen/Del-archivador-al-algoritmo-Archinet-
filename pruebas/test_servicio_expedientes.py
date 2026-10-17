from datetime import datetime, timedelta

from servicios import repositorio_json
from servicios.servicio_expedientes import ServicioExpedientes


def expediente(tipo_documento, numero_documento, tipo_presentado):
    return {
        "codigo": "",
        "codigo_documento": "",
        "nombre_completo": "Ana Díaz",
        "tipo_documento_identidad": tipo_documento,
        "numero_documento": numero_documento,
        "tipo_documento_presentado": tipo_presentado,
        "tipo_documento_otro": "",
        "asunto": "Archivo",
        "fecha_recepcion": "",
        "hora_recepcion": "",
        "archivos_adjuntos": [],
    }


def test_registra_y_asigna_fecha_hora_actuales(tmp_path, monkeypatch):
    monkeypatch.setattr(repositorio_json, "ARCHIVO_DATOS", tmp_path / "expedientes.json")
    servicio = ServicioExpedientes()
    primero = servicio.registrar(expediente("DNI", "12345678", "Carta"))
    segundo = servicio.registrar(expediente("DNI", "12345678", "Solicitud"))
    ahora = datetime.now()

    assert primero.codigo == "EXP001"
    assert segundo.codigo == "EXP002"
    assert primero.codigo_documento == "BOG001"
    assert segundo.codigo_documento == "BEN001"
    registrado = datetime.strptime(
        f"{primero.fecha_recepcion} {primero.hora_recepcion}", "%d/%m/%Y %H:%M:%S"
    )
    assert ahora - timedelta(seconds=5) <= registrado <= ahora

    recargado = ServicioExpedientes()
    assert recargado.buscar("EXP001")["codigo_documento"] == "BOG001"
