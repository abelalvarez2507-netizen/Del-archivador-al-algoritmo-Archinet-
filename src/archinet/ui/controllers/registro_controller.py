"""Controlador de las acciones de la pantalla de registro."""

from collections.abc import Mapping

from src.archinet.services.expediente_service import ExpedienteService
from src.archinet.ui.screens.registro_screen import RegistroScreen


class RegistroController:
    """Conecta los datos del formulario con el servicio de expedientes."""

    def __init__(self, servicio: ExpedienteService, pantalla: RegistroScreen) -> None:
        self.servicio = servicio
        self.pantalla = pantalla

    def registrar(self, datos: Mapping[str, object]) -> None:
        """Solicita el registro y comunica el resultado a la pantalla."""
        try:
            expediente = self.servicio.registrar(datos)
        except (ValueError, OSError) as error:
            self.pantalla.mostrar_error(str(error))
            return

        self.pantalla.limpiar()
        self.pantalla.actualizar_cantidad(self.servicio.cantidad())
        self.pantalla.mostrar_exito(f"El expediente {expediente.codigo} se guardó correctamente.")
