"""Ventanas de confirmación y error."""

from tkinter import messagebox


def exito(texto: str) -> None:
    messagebox.showinfo("ArchiNet", texto)


def error(texto: str) -> None:
    messagebox.showerror("Revisa los datos", texto)
