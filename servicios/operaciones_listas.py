from typing import Any


def buscar_por_codigo(expedientes: list[dict[str, Any]], codigo: str) -> dict[str, Any] | None:
    clave = codigo.strip().casefold()
    return next((e for e in expedientes if e["codigo"].casefold() == clave), None)


def ordenar_por_codigo(expedientes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(expedientes, key=lambda e: e["codigo"].casefold())
