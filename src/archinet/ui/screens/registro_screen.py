"""Pantalla de registro para la aplicación ArchiNet."""

import tkinter as tk
from tkinter import messagebox, ttk
from collections.abc import Callable, Mapping


class RegistroScreen:
    """Construye el formulario y muestra los mensajes de la interfaz."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.campos: dict[str, tk.Widget] = {}
        self._callback_registrar: Callable[[Mapping[str, object]], None] | None = None
        self._configurar_estilos()
        self._crear_componentes()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self.root)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 19, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Seccion.TLabel", font=("Segoe UI", 12, "bold"))
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _crear_componentes(self) -> None:
        contenedor = ttk.Frame(self.root, padding=24)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="ArchiNet", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            contenedor,
            text="Sistema de gestión de expedientes | Versión 0.2",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(2, 18))

        ttk.Label(
            contenedor,
            text=("Registra los datos de cada expediente. Los campos se validan y los "
                  "registros se guardan en un archivo local para recuperarlos al volver a abrir el programa."),
            wraplength=820,
            justify="left",
        ).pack(anchor="w", fill="x", pady=(0, 18))

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
            ttk.Label(formulario, text=etiqueta).grid(
                row=fila, column=columna, sticky="w", padx=(0, 12), pady=8
            )
            if tipo == "combo_id":
                widget = ttk.Combobox(
                    formulario,
                    values=["DNI", "Carné de extranjería", "Pasaporte"],
                    state="readonly",
                )
            elif tipo == "combo_doc":
                widget = ttk.Combobox(
                    formulario,
                    values=["Solicitud", "Oficio", "Carta", "Informe", "Otro"],
                    state="readonly",
                )
            else:
                widget = ttk.Entry(formulario)
            widget.grid(row=fila, column=columna + 1, sticky="ew", pady=8)
            self.campos[nombre] = widget

        ttk.Label(formulario, text="Asunto del trámite").grid(
            row=3, column=0, sticky="nw", padx=(0, 12), pady=8
        )
        self.campos["asunto"] = tk.Text(formulario, height=3, wrap="word", font=("Segoe UI", 10))
        self.campos["asunto"].grid(row=3, column=1, columnspan=3, sticky="ew", pady=8)

        acciones = ttk.Frame(contenedor)
        acciones.pack(fill="x", pady=(18, 8))
        ttk.Button(
            acciones, text="Registrar expediente", style="Accion.TButton", command=self._solicitar_registro
        ).pack(side="left")
        ttk.Button(acciones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=10)
        ttk.Button(acciones, text="Salir", command=self.root.destroy).pack(side="right")

        self.estado = ttk.Label(contenedor, text="Expedientes guardados: 0")
        self.estado.pack(anchor="w", pady=(10, 0))

        ttk.Separator(contenedor).pack(fill="x", pady=18)
        ttk.Label(
            contenedor,
            text="En esta versión se incluyen el registro, la validación de fechas y el guardado permanente en JSON. La búsqueda y el ordenamiento se incorporarán en siguientes avances.",
            wraplength=820,
            justify="left",
        ).pack(anchor="w")

    def establecer_callback_registrar(
        self, callback: Callable[[Mapping[str, object]], None]
    ) -> None:
        """Conecta la pantalla con el controlador sin mezclar responsabilidades."""
        self._callback_registrar = callback

    def _solicitar_registro(self) -> None:
        if self._callback_registrar is not None:
            self._callback_registrar(self.obtener_datos())

    def obtener_datos(self) -> dict[str, str]:
        """Obtiene los valores actuales del formulario."""
        datos: dict[str, str] = {}
        for nombre, widget in self.campos.items():
            if isinstance(widget, tk.Text):
                datos[nombre] = widget.get("1.0", "end").strip()
            elif isinstance(widget, ttk.Combobox):
                datos[nombre] = widget.get().strip()
            else:
                datos[nombre] = widget.get().strip()
        return datos

    def limpiar(self) -> None:
        """Limpia todos los campos del formulario."""
        for widget in self.campos.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, "end")
        self.campos["codigo"].focus_set()

    def actualizar_cantidad(self, cantidad: int) -> None:
        """Actualiza el contador visible de registros persistidos."""
        self.estado.config(text=f"Expedientes guardados: {cantidad}")

    def mostrar_exito(self, mensaje: str) -> None:
        messagebox.showinfo("Registro completado", mensaje, parent=self.root)

    def mostrar_error(self, mensaje: str) -> None:
        messagebox.showwarning("No se pudo registrar", mensaje, parent=self.root)
