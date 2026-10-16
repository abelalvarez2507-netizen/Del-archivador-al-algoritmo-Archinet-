"""Validación de fechas usadas en el registro de expedientes."""

from datetime import datetime
import re


FORMATO_FECHA = "%d/%m/%Y"


def validar_fecha_recepcion(fecha: str) -> str:
    """Valida una fecha real con formato DD/MM/AAAA y devuelve el valor limpio."""
    fecha_limpia = str(fecha).strip()
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha_limpia):
        raise ValueError("La fecha debe tener el formato DD/MM/AAAA.")
    try:
        datetime.strptime(fecha_limpia, FORMATO_FECHA)
    except ValueError as error:
        raise ValueError("La fecha ingresada no existe en el calendario.") from error
    return fecha_limpia
