"""Validaciones del formulario antes de registrar un expediente."""

from collections.abc import Iterable, Mapping

from src.archinet.validators.fecha_validator import validar_fecha_recepcion


CAMPOS_OBLIGATORIOS = (
    "codigo",
    "ciudadano",
    "tipo_doc_identidad",
    "numero_doc_identidad",
    "tipo_documento",
    "asunto",
    "fecha_recepcion",
)

TIPOS_DOCUMENTO_IDENTIDAD = ("DNI", "Carné de extranjería", "Pasaporte")
TIPOS_DOCUMENTO_PRESENTADO = ("Solicitud", "Oficio", "Carta", "Informe", "Otro")


def validar_datos_expediente(
    datos: Mapping[str, object], codigos_existentes: Iterable[str]
) -> dict[str, str]:
    """Valida y normaliza los datos recibidos desde la pantalla de registro."""
    normalizados = {campo: str(datos.get(campo, "") or "").strip() for campo in CAMPOS_OBLIGATORIOS}

    campos_vacios = [campo for campo, valor in normalizados.items() if not valor]
    if campos_vacios:
        etiquetas = {
            "codigo": "código",
            "ciudadano": "nombre del ciudadano",
            "tipo_doc_identidad": "tipo de documento de identidad",
            "numero_doc_identidad": "número de documento de identidad",
            "tipo_documento": "tipo de documento presentado",
            "asunto": "asunto del trámite",
            "fecha_recepcion": "fecha de recepción",
        }
        nombres = ", ".join(etiquetas[campo] for campo in campos_vacios)
        raise ValueError(f"Completa los siguientes campos: {nombres}.")

    normalizados["codigo"] = normalizados["codigo"].upper()

    codigos_normalizados = {str(codigo).strip().casefold() for codigo in codigos_existentes}
    if normalizados["codigo"].casefold() in codigos_normalizados:
        raise ValueError("Ya existe un expediente con ese código.")

    if normalizados["tipo_doc_identidad"] not in TIPOS_DOCUMENTO_IDENTIDAD:
        raise ValueError("Selecciona un tipo de documento de identidad válido.")

    if normalizados["tipo_documento"] not in TIPOS_DOCUMENTO_PRESENTADO:
        raise ValueError("Selecciona un tipo de documento presentado válido.")

    normalizados["fecha_recepcion"] = validar_fecha_recepcion(normalizados["fecha_recepcion"])
    return normalizados
