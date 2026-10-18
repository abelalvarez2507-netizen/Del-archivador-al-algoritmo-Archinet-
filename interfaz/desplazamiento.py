import tkinter as tk
from tkinter import ttk


class MarcoDesplazable(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, style="App.TFrame")
        self.canvas = tk.Canvas(self, background="#f3f6fa", borderwidth=0, highlightthickness=0)
        self.barra = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.barra.set)
        self.barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.interior = ttk.Frame(self.canvas, style="App.TFrame", padding=28)
        self.ventana = self.canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.bind("<Configure>", self._actualizar_region)
        self.canvas.bind("<Configure>", self._ajustar_ancho)

    def _actualizar_region(self, _evento: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _ajustar_ancho(self, evento: tk.Event) -> None:
        self.canvas.itemconfigure(self.ventana, width=evento.width)

    def desplazar_rueda(self, evento: tk.Event) -> None:
        delta = getattr(evento, "delta", 0)
        if delta:
            unidades = int(-delta / 120) if abs(delta) >= 120 else -int(delta)
            if unidades == 0:
                unidades = -1 if delta > 0 else 1
            self.canvas.yview_scroll(unidades, "units")

    def desplazar_unidad(self, unidades: int) -> None:
        self.canvas.yview_scroll(unidades, "units")
