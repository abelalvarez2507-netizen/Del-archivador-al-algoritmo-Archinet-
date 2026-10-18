import tkinter as tk
from datetime import datetime
from tkinter import ttk

from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaHistorial(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Historial y reportes", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Consulta los movimientos, responsables, fechas y cambios de estado.", style="Hint.TLabel").pack(anchor="w", pady=(4, 16))
        barra = ttk.Frame(tarjeta, style="Card.TFrame")
        barra.pack(fill="x", pady=(0, 10))
        self.codigo = tk.StringVar()
        ttk.Label(barra, text="Código de expediente").pack(side="left", padx=(0, 8))
        ttk.Entry(barra, textvariable=self.codigo, width=24).pack(side="left")
        ttk.Button(barra, text="Buscar", command=self.actualizar).pack(side="left", padx=8)
        ttk.Button(barra, text="Ver todo", command=self.ver_todo).pack(side="left")
        columnas = ("fecha", "hora", "codigo", "responsable", "accion", "anterior", "nuevo", "detalle")
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=17)
        titulos = ("Fecha", "Hora", "Expediente", "Responsable", "Acción", "Estado anterior", "Estado actual", "Detalle")
        anchos = (90, 75, 105, 140, 190, 125, 125, 220)
        for col, titulo, ancho in zip(columnas, titulos, anchos):
            self.tabla.heading(col, text=titulo); self.tabla.column(col, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.actualizar()

    def actualizar(self) -> None:
        codigo = self.codigo.get().strip()
        try:
            eventos = self.servicio.historial(codigo)
        except ValueError:
            eventos = []
        self.tabla.delete(*self.tabla.get_children())
        def fecha_evento(evento):
            try:
                return datetime.strptime(f"{evento.get('fecha', '')} {evento.get('hora', '')}", "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return datetime.min
        eventos.sort(key=fecha_evento, reverse=True)
        for indice, evento in enumerate(eventos):
            self.tabla.insert("", "end", iid=f"{indice}", values=(evento.get("fecha", ""), evento.get("hora", ""),
                              evento.get("codigo", ""), evento.get("responsable", ""), evento.get("accion", ""),
                              evento.get("estado_anterior", ""), evento.get("estado_nuevo", ""), evento.get("detalle", "")))

    def ver_todo(self) -> None:
        self.codigo.set("")
        self.actualizar()
