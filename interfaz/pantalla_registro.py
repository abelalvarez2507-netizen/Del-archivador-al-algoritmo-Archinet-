"""Formulario para registrar un expediente."""

import tkinter as tk
from tkinter import ttk

from componentes import mensajes
from interfaz import campos, estilos
from servicios.servicio_expedientes import ServicioExpedientes
from servicios.validaciones import TIPOS_IDENTIDAD, TIPOS_PRESENTADO


class PantallaRegistro(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent, padding=28)
        self.servicio = servicio
        self.variables = {nombre: tk.StringVar() for nombre in (
            "codigo", "nombre_completo", "tipo_documento_identidad", "numero_documento",
            "tipo_documento_presentado", "asunto", "fecha_recepcion",
        )}
        tarjeta = ttk.Frame(self, style="Card.TFrame", padding=26)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Registrar expediente", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Ingresa los datos del documento recibido.", style="Hint.TLabel").pack(anchor="w", pady=(4, 20))
        formulario = ttk.Frame(tarjeta, style="Card.TFrame")
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        filas = [
            ("codigo", "Código"), ("nombre_completo", "Nombre completo"),
            ("tipo_documento_identidad", "Tipo de identidad"), ("numero_documento", "N.º de documento"),
            ("tipo_documento_presentado", "Documento presentado"), ("asunto", "Asunto"),
            ("fecha_recepcion", "Fecha de recepción (AAAA-MM-DD)"),
        ]
        for indice, (clave, etiqueta) in enumerate(filas):
            if clave == "tipo_documento_identidad":
                campos.seleccion(formulario, indice, etiqueta, self.variables[clave], TIPOS_IDENTIDAD)
            elif clave == "tipo_documento_presentado":
                campos.seleccion(formulario, indice, etiqueta, self.variables[clave], TIPOS_PRESENTADO)
            else:
                campos.entrada(formulario, indice, etiqueta, self.variables[clave])
        pie = ttk.Frame(tarjeta, style="Card.TFrame")
        pie.pack(fill="x", pady=(22, 0))
        ttk.Button(pie, text="Limpiar", command=self.limpiar).pack(side="right", padx=(8, 0))
        ttk.Button(pie, text="Registrar expediente", style="Accent.TButton", command=self.registrar).pack(side="right")

    def limpiar(self) -> None:
        for variable in self.variables.values():
            variable.set("")

    def registrar(self) -> None:
        try:
            self.servicio.registrar({k: v.get() for k, v in self.variables.items()})
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        mensajes.exito("El expediente se registró correctamente.")
        self.limpiar()
