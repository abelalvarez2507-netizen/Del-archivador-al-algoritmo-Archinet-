import tkinter as tk
from tkinter import ttk
import re


def entrada(contenedor: tk.Widget, fila: int, etiqueta: str, variable: tk.StringVar) -> None:
    ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
    ttk.Entry(contenedor, textvariable=variable, width=38).grid(row=fila, column=1, sticky="ew", pady=7)


def seleccion(contenedor: tk.Widget, fila: int, etiqueta: str, variable: tk.StringVar, opciones: tuple[str, ...]) -> None:
    ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
    ttk.Combobox(contenedor, textvariable=variable, values=opciones, state="readonly", width=35).grid(row=fila, column=1, sticky="ew", pady=7)


def entrada_identidad(contenedor: tk.Widget, fila: int, etiqueta: str, variable: tk.StringVar, tipo: tk.StringVar) -> None:
    ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
    validar = contenedor.register(lambda nuevo: _identidad_permitida(nuevo, tipo.get()))
    ttk.Entry(contenedor, textvariable=variable, width=38, validate="key", validatecommand=(validar, "%P")).grid(row=fila, column=1, sticky="ew", pady=7)


def _identidad_permitida(valor: str, tipo: str) -> bool:
    if tipo == "DNI":
        return len(valor) <= 8 and (not valor or re.fullmatch(r"[0-9]+", valor) is not None)
    if tipo == "Carné de extranjería":
        return len(valor) <= 9 and (not valor or re.fullmatch(r"[0-9]+", valor) is not None)
    if tipo == "Pasaporte":
        return len(valor) <= 9 and (not valor or re.fullmatch(r"[A-Za-z0-9]+", valor) is not None)
    return not valor
