"""Contrato común para los repositorios de expedientes."""

from abc import ABC, abstractmethod
from typing import Sequence

from src.archinet.models.expediente import Expediente


class RepositorioBase(ABC):
    """Define las operaciones que debe ofrecer cualquier repositorio.

    La clase concreta de JSON hereda de esta clase y completa sus métodos.
    Se utiliza herencia para mantener separada la forma de guardar los datos
    de las reglas de negocio y de la interfaz.
    """

    @abstractmethod
    def registrar(self, expediente: Expediente) -> None:
        """Agrega un expediente y conserva los cambios."""

    @abstractmethod
    def listar(self) -> Sequence[Expediente]:
        """Devuelve los expedientes guardados."""

    @abstractmethod
    def guardar(self) -> None:
        """Persiste los expedientes en el medio definido por el repositorio."""

    @abstractmethod
    def cantidad(self) -> int:
        """Devuelve la cantidad de expedientes existentes."""
