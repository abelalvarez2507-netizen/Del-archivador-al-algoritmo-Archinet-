import tkinter as tk
from tkinter import ttk

from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaListado(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        encabezado = ttk.Frame(tarjeta, style="Card.TFrame")
        encabezado.pack(fill="x", pady=(0, 16))
        ttk.Label(encabezado, text="Expedientes", style="Title.TLabel").pack(side="left")
        ttk.Button(encabezado, text="Actualizar", command=self.actualizar).pack(side="right")
        columnas = ("codigo", "codigo_documento", "nombre", "tipo", "fecha", "hora", "adjuntos")
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=14)
        for columna, titulo, ancho in zip(columnas, ("Expediente", "Documento", "Nombre", "Tipo", "Fecha", "Hora", "Archivos"), (90, 90, 160, 120, 90, 75, 70)):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.actualizar()

    def actualizar(self) -> None:
        self.tabla.delete(*self.tabla.get_children())
        for e in self.servicio.listar_ordenados():
            tipo = e.get("tipo_documento_otro") or e["tipo_documento_presentado"]
            adjuntos = len(e.get("archivos_adjuntos", []))
            self.tabla.insert("", "end", values=(e["codigo"], e.get("codigo_documento", ""), e["nombre_completo"], tipo, e["fecha_recepcion"], e.get("hora_recepcion", ""), adjuntos))
