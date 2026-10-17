import json

from servicios.repositorio_json import cargar, guardar


def test_guardar_y_cargar_con_tildes(tmp_path):
    ruta = tmp_path / "expedientes.json"
    datos = [{"codigo": "1", "nombre_completo": "María Núñez"}]
    guardar(datos, ruta)
    assert cargar(ruta) == datos
    assert "María" in ruta.read_text(encoding="utf-8")


def test_archivo_vacio(tmp_path):
    ruta = tmp_path / "vacio.json"
    ruta.write_text("", encoding="utf-8")
    assert cargar(ruta) == []
