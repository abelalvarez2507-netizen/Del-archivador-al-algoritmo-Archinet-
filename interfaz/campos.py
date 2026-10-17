import tkinter as tk
from tkinter import ttk


def entrada(contenedor: tk.Widget, fila: int, etiqueta: str, variable: tk.StringVar) -> None:
    ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
    ttk.Entry(contenedor, textvariable=variable, width=38).grid(row=fila, column=1, sticky="ew", pady=7)


def seleccion(contenedor: tk.Widget, fila: int, etiqueta: str, variable: tk.StringVar, opciones: tuple[str, ...]) -> None:
    ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
    ttk.Combobox(contenedor, textvariable=variable, values=opciones, state="readonly", width=35).grid(row=fila, column=1, sticky="ew", pady=7)
