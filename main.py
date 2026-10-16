"""Ventana inicial de ArchiNet: formulario de registro en memoria."""

import tkinter as tk
from tkinter import messagebox, ttk

from expedientes import RepositorioExpedientes


class ArchiNetApp:
    def __init__(self, root):
        self.root = root
        self.repositorio = RepositorioExpedientes()
        self.campos = {}

        self.root.title("ArchiNet | Gestión de expedientes")
        self.root.geometry("900x650")
        self.root.minsize(780, 600)

        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 19, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Seccion.TLabel", font=("Segoe UI", 12, "bold"))
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=8)

        contenedor = ttk.Frame(root, padding=24)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="ArchiNet", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Sistema de gestión de expedientes | Primera versión",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", pady=(2, 18))

        aviso = ttk.Label(
            contenedor,
            text=("En esta etapa se puede registrar un expediente y validar campos vacíos "
                  "y códigos repetidos. Los datos permanecen solo durante esta sesión."),
            wraplength=820,
            justify="left"
        )
        aviso.pack(anchor="w", fill="x", pady=(0, 18))

        ttk.Label(contenedor, text="Registro de expediente", style="Seccion.TLabel").pack(anchor="w", pady=(0, 10))
        formulario = ttk.Frame(contenedor)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        especificaciones = [
            ("codigo", "Código del expediente", 0, 0, "entry"),
            ("ciudadano", "Nombre completo del ciudadano", 0, 2, "entry"),
            ("tipo_doc_identidad", "Tipo de documento de identidad", 1, 0, "combo_id"),
            ("numero_doc_identidad", "Número de documento de identidad", 1, 2, "entry"),
            ("tipo_documento", "Tipo de documento presentado", 2, 0, "combo_doc"),
            ("fecha_recepcion", "Fecha de recepción (DD/MM/AAAA)", 2, 2, "entry"),
        ]
        for nombre, etiqueta, fila, columna, tipo in especificaciones:
            ttk.Label(formulario, text=etiqueta).grid(row=fila, column=columna, sticky="w", padx=(0, 12), pady=8)
            if tipo == "combo_id":
                widget = ttk.Combobox(formulario, values=["DNI", "Carné de extranjería", "Pasaporte"], state="readonly")
            elif tipo == "combo_doc":
                widget = ttk.Combobox(formulario, values=["Solicitud", "Oficio", "Carta", "Informe", "Otro"], state="readonly")
            else:
                widget = ttk.Entry(formulario)
            widget.grid(row=fila, column=columna + 1, sticky="ew", pady=8)
            self.campos[nombre] = widget

        ttk.Label(formulario, text="Asunto del trámite").grid(row=3, column=0, sticky="nw", padx=(0, 12), pady=8)
        self.campos["asunto"] = tk.Text(formulario, height=3, wrap="word", font=("Segoe UI", 10))
        self.campos["asunto"].grid(row=3, column=1, columnspan=3, sticky="ew", pady=8)

        acciones = ttk.Frame(contenedor)
        acciones.pack(fill="x", pady=(18, 8))
        ttk.Button(acciones, text="Registrar expediente", style="Accion.TButton", command=self.registrar).pack(side="left")
        ttk.Button(acciones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=10)
        ttk.Button(acciones, text="Salir", command=self.root.destroy).pack(side="right")

        self.estado = ttk.Label(contenedor, text="Expedientes registrados en esta sesión: 0")
        self.estado.pack(anchor="w", pady=(10, 0))

        ttk.Separator(contenedor).pack(fill="x", pady=18)
        ttk.Label(
            contenedor,
            text="Siguiente etapa: mejorar la validación de fechas y guardar los registros en un archivo JSON.",
            wraplength=820,
            justify="left"
        ).pack(anchor="w")

    def registrar(self):
        datos = {
            "codigo": self.campos["codigo"].get(),
            "ciudadano": self.campos["ciudadano"].get(),
            "tipo_doc_identidad": self.campos["tipo_doc_identidad"].get(),
            "numero_doc_identidad": self.campos["numero_doc_identidad"].get(),
            "tipo_documento": self.campos["tipo_documento"].get(),
            "asunto": self.campos["asunto"].get("1.0", "end").strip(),
            "fecha_recepcion": self.campos["fecha_recepcion"].get(),
        }
        try:
            mensaje = self.repositorio.registrar(**datos)
        except ValueError as error:
            messagebox.showwarning("No se pudo registrar", str(error), parent=self.root)
            return

        messagebox.showinfo("Registro completado", mensaje, parent=self.root)
        self.limpiar()
        self.estado.config(text=f"Expedientes registrados en esta sesión: {self.repositorio.cantidad()}")

    def limpiar(self):
        for nombre, widget in self.campos.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, "end")
        self.campos["codigo"].focus_set()


def main():
    root = tk.Tk()
    ArchiNetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
