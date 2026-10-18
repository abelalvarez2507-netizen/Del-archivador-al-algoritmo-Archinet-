import tkinter as tk
from tkinter import ttk

from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaInicio(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        self.tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        self.tarjeta.pack(fill="both", expand=True)
        ttk.Label(self.tarjeta, text="Resumen", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.tarjeta, text="Estado actual del flujo de expedientes.", style="Hint.TLabel").pack(anchor="w", pady=(4, 16))
        self.indicadores = ttk.Frame(self.tarjeta, style="Card.TFrame")
        self.indicadores.pack(fill="x")
        self.valores = {}
        for indice, (clave, titulo) in enumerate((("recibidos", "Recibidos"), ("observados", "Observados"),
                                                   ("pendientes_clasificar", "Por clasificar"), ("urgentes", "Urgentes"),
                                                   ("listos", "Listos para derivación"), ("derivados", "Derivados"))):
            bloque = ttk.Frame(self.indicadores, style="Card.TFrame", padding=(12, 14))
            bloque.grid(row=indice // 3, column=indice % 3, sticky="nsew", padx=5, pady=5)
            ttk.Label(bloque, text=titulo, style="Hint.TLabel").pack(anchor="w")
            self.valores[clave] = tk.StringVar(value="0")
            ttk.Label(bloque, textvariable=self.valores[clave], style="Title.TLabel").pack(anchor="w", pady=(6, 0))
        for columna in range(3):
            self.indicadores.columnconfigure(columna, weight=1)
        ttk.Label(self.tarjeta, text="Alertas y pendientes", style="Title.TLabel").pack(anchor="w", pady=(20, 8))
        self.alertas = tk.Listbox(self.tarjeta, height=12, relief="solid", borderwidth=1)
        self.alertas.pack(fill="both", expand=True)
        ttk.Button(self.tarjeta, text="Actualizar", command=self.actualizar).pack(anchor="e", pady=(12, 0))
        self.actualizar()

    def actualizar(self) -> None:
        resumen = self.servicio.resumen()
        for clave, variable in self.valores.items():
            variable.set(str(resumen.get(clave, 0)))
        self.alertas.delete(0, "end")
        alertas = resumen.get("alertas", [])
        if not alertas:
            self.alertas.insert("end", "No hay alertas pendientes.")
        for alerta in alertas:
            self.alertas.insert("end", alerta)
