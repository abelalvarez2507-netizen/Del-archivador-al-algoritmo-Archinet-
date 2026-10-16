"""Servicio de aplicación para registrar expedientes."""

from collections.abc import Sequence
from typing import Mapping

from src.archinet.models.expediente import Expediente
from src.archinet.repositories.repositorio_base import RepositorioBase
from src.archinet.validators.expediente_validator import validar_datos_expediente


class ExpedienteService:
    """Coordina la validación del formulario y el repositorio de datos."""

    def __init__(self, repositorio: RepositorioBase) -> None:
        self.repositorio = repositorio

    def registrar(self, datos: Mapping[str, object]) -> Expediente:
        """Valida un registro, lo convierte en modelo y lo guarda."""
        codigos_existentes = [expediente.codigo for expediente in self.repositorio.listar()]
        datos_validados = validar_datos_expediente(datos, codigos_existentes)
        expediente = Expediente(**datos_validados)
        self.repositorio.registrar(expediente)
        return expediente

    def listar(self) -> Sequence[Expediente]:
        """Devuelve los expedientes existentes."""
        return self.repositorio.listar()

    def cantidad(self) -> int:
        """Devuelve el número de expedientes existentes."""
        return self.repositorio.cantidad()
