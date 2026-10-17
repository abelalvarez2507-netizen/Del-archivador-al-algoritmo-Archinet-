from datetime import date

TIPOS_IDENTIDAD = ("DNI", "Carné de extranjería", "Pasaporte")
TIPOS_PRESENTADO = ("Solicitud", "Carta", "Formulario", "Otro")


def validar(datos: dict[str, str], codigos_existentes: list[str]) -> None:
    campos = (
        "codigo", "nombre_completo", "tipo_documento_identidad",
        "numero_documento", "tipo_documento_presentado", "asunto", "fecha_recepcion",
    )
    if any(not datos.get(campo, "").strip() for campo in campos):
        raise ValueError("Completa todos los campos del expediente.")
    if datos["tipo_documento_identidad"] not in TIPOS_IDENTIDAD:
        raise ValueError("Selecciona un tipo de documento de identidad válido.")
    if datos["tipo_documento_presentado"] not in TIPOS_PRESENTADO:
        raise ValueError("Selecciona un tipo de documento presentado válido.")
    if datos["codigo"].strip() in codigos_existentes:
        raise ValueError("Ya existe un expediente con ese código.")
    try:
        date.fromisoformat(datos["fecha_recepcion"].strip())
    except ValueError as exc:
        raise ValueError("La fecha debe ser válida y usar el formato AAAA-MM-DD.") from exc
