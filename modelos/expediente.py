from dataclasses import asdict, dataclass


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

    def a_dict(self) -> dict[str, str]:
        return asdict(self)
