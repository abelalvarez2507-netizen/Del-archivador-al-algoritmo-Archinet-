import json
from pathlib import Path
from typing import Any


ARCHIVO_CONFIGURACION = Path(__file__).resolve().parents[1] / "datos" / "configuracion.json"
CONFIGURACION_INICIAL: dict[str, Any] = {
    "nombre_entidad": "",
    "unidades": [],
    "sugerencias": {},
}


def cargar() -> dict[str, Any]:
    if not ARCHIVO_CONFIGURACION.exists():
        return dict(CONFIGURACION_INICIAL)
    with ARCHIVO_CONFIGURACION.open("r", encoding="utf-8") as archivo:
        guardada = json.load(archivo)
    return {**CONFIGURACION_INICIAL, **guardada}


def guardar(config: dict[str, Any]) -> None:
    ARCHIVO_CONFIGURACION.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVO_CONFIGURACION.open("w", encoding="utf-8") as archivo:
        json.dump(config, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
