"""Punto de entrada de ArchiNet."""

from pathlib import Path
import tkinter as tk

from interfaz import ArchiNetApp


DIRECTORIO_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_DATOS = DIRECTORIO_PROYECTO / "datos" / "expedientes.csv"


def main() -> None:
    ventana = tk.Tk()
    ArchiNetApp(ventana, ARCHIVO_DATOS)
    ventana.mainloop()


if __name__ == "__main__":
    main()
