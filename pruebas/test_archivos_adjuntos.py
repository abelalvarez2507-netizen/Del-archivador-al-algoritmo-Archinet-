import pytest

from servicios import archivos_adjuntos


def test_copia_archivo_adjuntado(tmp_path, monkeypatch):
    origen = tmp_path / "solicitud.pdf"
    origen.write_bytes(b"contenido PDF")
    monkeypatch.setattr(archivos_adjuntos, "DIRECTORIO_DATOS", tmp_path / "datos")

    rutas = archivos_adjuntos.copiar_adjuntos([str(origen)], "EXP001")

    assert rutas == ["datos/adjuntos/EXP001/solicitud.pdf"]
    assert (tmp_path / rutas[0]).read_bytes() == b"contenido PDF"


def test_rechaza_extension_no_compatible(tmp_path, monkeypatch):
    origen = tmp_path / "programa.exe"
    origen.write_bytes(b"contenido")
    monkeypatch.setattr(archivos_adjuntos, "DIRECTORIO_DATOS", tmp_path / "datos")

    with pytest.raises(ValueError, match="no está permitido"):
        archivos_adjuntos.copiar_adjuntos([str(origen)], "EXP001")
