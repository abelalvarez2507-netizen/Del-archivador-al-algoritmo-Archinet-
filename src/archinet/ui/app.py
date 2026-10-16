"""Configuración y arranque de la interfaz de ArchiNet."""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from src.archinet.repositories.json_expediente_repository import RepositorioJSONExpedientes
from src.archinet.services.expediente_service import ExpedienteService
from src.archinet.ui.controllers.registro_controller import RegistroController
from src.archinet.ui.screens.registro_screen import RegistroScreen


RUTA_PROYECTO = Path(__file__).resolve().parents[3]
RUTA_DATOS = RUTA_PROYECTO / "data" / "expedientes.json"


def ejecutar() -> None:
    """Construye las dependencias y abre la ventana principal."""
    root = tk.Tk()
    root.title("ArchiNet | Gestión de expedientes")
    root.geometry("900x650")
    root.minsize(780, 600)

    try:
        repositorio = RepositorioJSONExpedientes(RUTA_DATOS)
    except (OSError, ValueError) as error:
        messagebox.showerror("No se pudieron cargar los datos", str(error), parent=root)
        root.destroy()
        return

    servicio = ExpedienteService(repositorio)
    pantalla = RegistroScreen(root)
    controlador = RegistroController(servicio, pantalla)
    pantalla.establecer_callback_registrar(controlador.registrar)
    pantalla.actualizar_cantidad(servicio.cantidad())
    root.mainloop()
