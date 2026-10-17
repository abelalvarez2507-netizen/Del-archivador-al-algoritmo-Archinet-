import shutil
from pathlib import Path


EXTENSIONES_PERMITIDAS = {
    ".doc", ".docx", ".odt", ".rtf", ".pdf",
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".webp",
}
DIRECTORIO_DATOS = Path(__file__).resolve().parents[1] / "datos"


def copiar_adjuntos(rutas: list[str], codigo_expediente: str) -> list[str]:
    if not rutas:
        return []
    destino = DIRECTORIO_DATOS / "adjuntos" / codigo_expediente
    destino.mkdir(parents=True, exist_ok=True)
    guardados = []
    for ruta in rutas:
        origen = Path(ruta)
        if origen.suffix.lower() not in EXTENSIONES_PERMITIDAS:
            raise ValueError(f"El formato de archivo no está permitido: {origen.name}")
        if not origen.is_file():
            raise ValueError(f"No se encontró el archivo seleccionado: {origen.name}")
        nombre = origen.name
        base, extension = origen.stem, origen.suffix
        numero = 2
        while (destino / nombre).exists():
            nombre = f"{base}_{numero}{extension}"
            numero += 1
        shutil.copy2(origen, destino / nombre)
        guardados.append((Path("datos") / "adjuntos" / codigo_expediente / nombre).as_posix())
    return guardados
