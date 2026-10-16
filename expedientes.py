"""Reglas de negocio para el prototipo ArchiNet.

Este módulo no depende de Tkinter; puede probarse de forma independiente.
"""

from datetime import datetime
from typing import Iterable, Mapping

CAMPOS = (
    "codigo",
    "nombre",
    "tipo_doc_identidad",
    "numero_doc_identidad",
    "tipo_documento",
    "asunto",
    "fecha_recepcion",
)

ETIQUETAS = {
    "codigo": "código del expediente",
    "nombre": "nombre completo del ciudadano",
    "tipo_doc_identidad": "tipo de documento de identidad",
    "numero_doc_identidad": "número de documento de identidad",
    "tipo_documento": "tipo de documento presentado",
    "asunto": "asunto",
    "fecha_recepcion": "fecha de recepción",
}


def validar_expediente(
    datos: Mapping[str, object], existentes: Iterable[Mapping[str, str]]
) -> dict[str, str]:
    """Devuelve una copia normalizada del expediente o lanza ValueError.

    Validaciones aplicadas:
    - Ningún campo obligatorio puede estar vacío.
    - El código se normaliza a mayúsculas y debe ser único.
    - La fecha debe usar el formato AAAA-MM-DD y ser una fecha válida.

    No se restringe la longitud ni el formato del documento de identidad porque
    eso depende del tipo de documento y de las reglas que se definan para el caso.
    """
    limpio = {campo: str(datos.get(campo, "") or "").strip() for campo in CAMPOS}

    faltantes = [ETIQUETAS[campo] for campo, valor in limpio.items() if not valor]
    if faltantes:
        raise ValueError("Completa los siguientes campos: " + ", ".join(faltantes) + ".")

    limpio["codigo"] = limpio["codigo"].upper()

    try:
        datetime.strptime(limpio["fecha_recepcion"], "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("La fecha debe ser válida y tener el formato AAAA-MM-DD (por ejemplo, 2026-10-16).") from exc

    codigo_nuevo = limpio["codigo"]
    for expediente in existentes:
        codigo_existente = str(expediente.get("codigo", "")).strip().upper()
        if codigo_existente == codigo_nuevo:
            raise ValueError(f"El código {codigo_nuevo} ya está registrado.")

    return limpio


def buscar_por_codigo(
    expedientes: Iterable[Mapping[str, str]], codigo: str
) -> dict[str, str] | None:
    """Busca linealmente un expediente por su código, sin distinguir mayúsculas."""
    buscado = str(codigo or "").strip().upper()
    if not buscado:
        return None

    for expediente in expedientes:
        if str(expediente.get("codigo", "")).strip().upper() == buscado:
            return dict(expediente)
    return None


def ordenar_por_codigo(
    expedientes: Iterable[Mapping[str, str]],
) -> list[dict[str, str]]:
    """Devuelve una copia ordenada por código usando ordenamiento por selección."""
    ordenados = [dict(expediente) for expediente in expedientes]
    cantidad = len(ordenados)

    for i in range(cantidad - 1):
        indice_menor = i
        for j in range(i + 1, cantidad):
            if ordenados[j]["codigo"].upper() < ordenados[indice_menor]["codigo"].upper():
                indice_menor = j
        if indice_menor != i:
            ordenados[i], ordenados[indice_menor] = ordenados[indice_menor], ordenados[i]

    return ordenados
