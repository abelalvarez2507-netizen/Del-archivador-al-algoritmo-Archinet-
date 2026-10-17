from datetime import date, datetime
import re

TIPOS_IDENTIDAD = ("DNI", "Carné de extranjería", "Pasaporte")
TIPOS_PRESENTADO = ("Solicitud", "Carta", "Formulario", "Otro")


def validar(datos: dict[str, str]) -> None:
    campos = ("nombre_completo", "tipo_documento_identidad", "numero_documento",
              "tipo_documento_presentado", "asunto", "fecha_recepcion", "hora_recepcion")
    if any(not datos.get(campo, "").strip() for campo in campos):
        raise ValueError("Completa todos los campos del expediente.")
    if datos["tipo_documento_identidad"] not in TIPOS_IDENTIDAD:
        raise ValueError("Selecciona un tipo de documento de identidad válido.")
    if datos["tipo_documento_presentado"] not in TIPOS_PRESENTADO:
        raise ValueError("Selecciona un tipo de documento presentado válido.")
    if datos["tipo_documento_presentado"] == "Otro" and not datos.get("tipo_documento_otro", "").strip():
        raise ValueError("Especifica el tipo de documento presentado.")
    tipo_identidad = datos["tipo_documento_identidad"]
    numero = datos["numero_documento"].strip()
    if tipo_identidad == "DNI" and not re.fullmatch(r"[0-9]{8}", numero):
        raise ValueError("El DNI debe tener exactamente 8 dígitos.")
    if tipo_identidad == "Carné de extranjería" and not re.fullmatch(r"[0-9]{9}", numero):
        raise ValueError("El carné de extranjería debe tener exactamente 9 dígitos.")
    if tipo_identidad == "Pasaporte" and (not re.fullmatch(r"[A-Za-z0-9]{6,9}", numero)):
        raise ValueError("El pasaporte debe tener entre 6 y 9 letras o números.")
    fecha_texto = datos["fecha_recepcion"].strip()
    hora_texto = datos["hora_recepcion"].strip()
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha_texto) or not re.fullmatch(r"\d{2}:\d{2}:\d{2}", hora_texto):
        raise ValueError("La fecha debe usar DD/MM/AAAA y la hora HH:MM:SS.")
    try:
        fecha = datetime.strptime(fecha_texto, "%d/%m/%Y").date()
        datetime.strptime(hora_texto, "%H:%M:%S")
    except ValueError as exc:
        raise ValueError("La fecha debe usar DD/MM/AAAA y la hora HH:MM:SS.") from exc
    if fecha != date.today():
        raise ValueError("La fecha de recepción debe ser la fecha actual.")
