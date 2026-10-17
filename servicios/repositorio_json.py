import json
from pathlib import Path

ARCHIVO_DATOS = Path(__file__).resolve().parents[1] / "datos" / "expedientes.json"


def cargar(ruta: Path = ARCHIVO_DATOS) -> list[dict[str, str]]:
    if not ruta.exists() or ruta.stat().st_size == 0:
        return []
    with ruta.open("r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)
    if not isinstance(contenido, list):
        raise ValueError("El archivo de expedientes debe contener una lista JSON.")
    return contenido


def guardar(expedientes: list[dict[str, str]], ruta: Path = ARCHIVO_DATOS) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(expedientes, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
