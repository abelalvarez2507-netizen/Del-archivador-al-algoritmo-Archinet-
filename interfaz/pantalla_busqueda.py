import tkinter as tk
from tkinter import ttk

from interfaz import estilos
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaBusqueda(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent, padding=28)
        self.servicio = servicio
        tarjeta = ttk.Frame(self, style="Card.TFrame", padding=26)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Buscar expediente", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Consulta un registro mediante su código.", style="Hint.TLabel").pack(anchor="w", pady=(4, 20))
        barra = ttk.Frame(tarjeta, style="Card.TFrame")
        barra.pack(fill="x")
        self.codigo = tk.StringVar()
        ttk.Entry(barra, textvariable=self.codigo).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(barra, text="Buscar", style="Accent.TButton", command=self.buscar).pack(side="left")
        self.resultado = ttk.Label(tarjeta, text="", style="Result.TLabel", justify="left")
        self.resultado.pack(anchor="w", pady=24)

    def buscar(self) -> None:
        expediente = self.servicio.buscar(self.codigo.get())
        if expediente is None:
            self.resultado.configure(text="No se encontró un expediente con ese código.")
            return
        etiquetas = {
            "codigo": "Código", "nombre_completo": "Nombre completo",
            "tipo_documento_identidad": "Tipo de identidad", "numero_documento": "N.º de documento",
            "tipo_documento_presentado": "Documento presentado", "asunto": "Asunto",
            "fecha_recepcion": "Fecha de recepción",
        }
        self.resultado.configure(text="\n".join(f"{etiquetas[k]}:  {v}" for k, v in expediente.items()))
