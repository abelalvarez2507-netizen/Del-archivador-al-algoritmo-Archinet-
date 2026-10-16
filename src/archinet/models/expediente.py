"""Modelo de datos de un expediente."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Expediente:
    """Representa los datos asociados a un expediente recibido."""

    codigo: str
    ciudadano: str
    tipo_doc_identidad: str
    numero_doc_identidad: str
    tipo_documento: str
    asunto: str
    fecha_recepcion: str

    def a_diccionario(self) -> dict[str, str]:
        """Convierte el expediente a un diccionario serializable como JSON."""
        return asdict(self)

    @classmethod
    def desde_diccionario(cls, datos: dict[str, Any]) -> "Expediente":
        """Crea un expediente a partir de un registro leído del archivo JSON."""
        campos = (
            "codigo",
            "ciudadano",
            "tipo_doc_identidad",
            "numero_doc_identidad",
            "tipo_documento",
            "asunto",
            "fecha_recepcion",
        )
        faltantes = [campo for campo in campos if campo not in datos]
        if faltantes:
            raise ValueError(
                "El archivo de datos contiene un expediente incompleto: "
                + ", ".join(faltantes)
            )
        return cls(**{campo: str(datos[campo]) for campo in campos})
