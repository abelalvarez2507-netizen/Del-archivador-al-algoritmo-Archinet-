import re
import unicodedata


PREFIJOS_DOCUMENTO = {
    "Carta": "BOG",
    "Solicitud": "BEN",
    "Formulario": "ARD",
}


def siguiente_codigo(codigos: list[str], prefijo: str) -> str:
    patron = re.compile(rf"^{re.escape(prefijo)}(\d+)$", re.IGNORECASE)
    ultimo = max((int(m.group(1)) for c in codigos if (m := patron.fullmatch(c))), default=0)
    return f"{prefijo}{ultimo + 1:03d}"


def prefijo_otro(tipo: str) -> str:
    normalizado = unicodedata.normalize("NFKD", tipo)
    letras = "".join(c for c in normalizado if c.isalpha() and not unicodedata.combining(c))
    prefijo = letras[:3].upper()
    if len(prefijo) != 3:
        raise ValueError("Escribe un tipo de documento con al menos tres letras.")
    return prefijo


def generar_codigos(expedientes: list[dict[str, str]], tipo_documento: str, otro: str = "") -> tuple[str, str]:
    codigo_expediente = siguiente_codigo([e.get("codigo", "") for e in expedientes], "EXP")
    prefijo = PREFIJOS_DOCUMENTO.get(tipo_documento)
    if tipo_documento == "Otro":
        prefijo = prefijo_otro(otro)
    if prefijo is None:
        raise ValueError("Selecciona un tipo de documento presentado válido.")
    codigos_documento = [e.get("codigo_documento", "") for e in expedientes]
    return codigo_expediente, siguiente_codigo(codigos_documento, prefijo)


def codigo_paciente_para(expedientes: list[dict[str, str]], tipo_identidad: str, numero: str) -> str:
    if not tipo_identidad or not numero:
        return ""
    identidad = numero.strip().casefold()
    for expediente in expedientes:
        if (expediente.get("tipo_documento_identidad") == tipo_identidad
                and expediente.get("numero_documento", "").strip().casefold() == identidad
                and expediente.get("codigo_paciente")):
            return expediente["codigo_paciente"]
    codigos = [e.get("codigo_paciente", "") for e in expedientes]
    return siguiente_codigo(codigos, "PAC")
