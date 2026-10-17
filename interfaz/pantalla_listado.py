import tkinter as tk
from tkinter import ttk

from servicios.servicio_expedientes import ServicioExpedientes


class PantallaListado(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent, padding=28)
        self.servicio = servicio
        tarjeta = ttk.Frame(self, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        encabezado = ttk.Frame(tarjeta, style="Card.TFrame")
        encabezado.pack(fill="x", pady=(0, 16))
        ttk.Label(encabezado, text="Expedientes", style="Title.TLabel").pack(side="left")
        ttk.Button(encabezado, text="Actualizar", command=self.actualizar).pack(side="right")
        columnas = ("codigo", "codigo_documento", "nombre", "tipo", "asunto", "fecha")
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=14)
        for columna, titulo, ancho in zip(columnas, ("Expediente", "Documento", "Nombre completo", "Tipo", "Asunto", "Recepción"), (100, 100, 190, 130, 190, 100)):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.actualizar()

    def actualizar(self) -> None:
        self.tabla.delete(*self.tabla.get_children())
        for e in self.servicio.listar_ordenados():
            tipo = e.get("tipo_documento_otro") or e["tipo_documento_presentado"]
            self.tabla.insert("", "end", values=(e["codigo"], e.get("codigo_documento", ""), e["nombre_completo"], tipo, e["asunto"], e["fecha_recepcion"]))
