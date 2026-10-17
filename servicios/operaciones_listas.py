"""Búsqueda y ordenamiento de expedientes."""


def buscar_por_codigo(expedientes: list[dict[str, str]], codigo: str) -> dict[str, str] | None:
    clave = codigo.strip().casefold()
    return next((e for e in expedientes if e["codigo"].casefold() == clave), None)


def ordenar_por_codigo(expedientes: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(expedientes, key=lambda e: e["codigo"].casefold())
