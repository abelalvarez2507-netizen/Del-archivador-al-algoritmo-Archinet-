from servicios.servicio_expedientes import ServicioExpedientes
from servicios import repositorio_json


def test_registrar_y_buscar(tmp_path, monkeypatch):
    ruta = tmp_path / "datos.json"
    monkeypatch.setattr(repositorio_json, "ARCHIVO_DATOS", ruta)
    servicio = ServicioExpedientes()
    datos = {"codigo": "A-1", "nombre_completo": "Ana Díaz", "tipo_documento_identidad": "DNI", "numero_documento": "123", "tipo_documento_presentado": "Carta", "asunto": "Archivo", "fecha_recepcion": "2026-10-17"}
    servicio.registrar(datos)
    assert servicio.buscar("a-1")["nombre_completo"] == "Ana Díaz"
