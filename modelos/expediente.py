from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Expediente:
    codigo: str
    codigo_documento: str
    nombre_completo: str
    tipo_documento_identidad: str
    numero_documento: str
    tipo_documento_presentado: str
    tipo_documento_otro: str
    asunto: str
    fecha_recepcion: str
    hora_recepcion: str
    archivos_adjuntos: list[str]
    cotejo: dict[str, Any]
    foliacion: dict[str, Any]
    cargo: dict[str, Any]
    clasificacion: dict[str, Any]
    derivaciones: list[dict[str, Any]]
    estado: str
    historial: list[dict[str, Any]]

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)
