"""Interfaz de escritorio de ArchiNet desarrollada con Tkinter."""

import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

from expedientes import CAMPOS, ETIQUETAS, buscar_por_codigo, ordenar_por_codigo, validar_expediente
from persistencia import ErrorPersistencia, cargar_expedientes, guardar_expedientes


class ArchiNetApp:
    """Ventana principal; conecta la interfaz con la lógica y el CSV."""

    def __init__(self, ventana: tk.Tk, ruta_datos: str | Path):
        self.ventana = ventana
        self.ruta_datos = Path(ruta_datos)
        self.expedientes: list[dict[str, str]] = []
        self.entradas: dict[str, tk.Widget] = {}

        self.ventana.title("ArchiNet | Gestión de expedientes")
        self.ventana.geometry("1390x760")
        self.ventana.minsize(1100, 620)

        self._construir_interfaz()
        self._cargar_al_iniciar()

    def _construir_interfaz(self) -> None:
        encabezado = ttk.Frame(self.ventana, padding=(18, 14))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="ArchiNet", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            encabezado,
            text="Registro, validación, búsqueda y organización de expedientes",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        contenido = ttk.Frame(self.ventana, padding=(18, 0, 18, 14))
        contenido.pack(fill="both", expand=True)
        contenido.columnconfigure(1, weight=1)
        contenido.rowconfigure(0, weight=1)

        formulario = ttk.LabelFrame(contenido, text="Registrar expediente", padding=12)
        formulario.grid(row=0, column=0, sticky="nsw", padx=(0, 14))

        campos = [
            ("codigo", "Código del expediente"),
            ("nombre", "Nombre completo del ciudadano"),
            ("tipo_doc_identidad", "Tipo de documento de identidad"),
            ("numero_doc_identidad", "Número de documento de identidad"),
            ("tipo_documento", "Tipo de documento presentado"),
            ("asunto", "Asunto"),
            ("fecha_recepcion", "Fecha de recepción (AAAA-MM-DD)"),
        ]

        for fila, (campo, etiqueta) in enumerate(campos):
            ttk.Label(formulario, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", pady=(5, 2))
            if campo == "tipo_doc_identidad":
                entrada = ttk.Combobox(
                    formulario, values=("DNI", "Carné de extranjería", "Pasaporte", "Otro"), width=34
                )
            elif campo == "tipo_documento":
                entrada = ttk.Combobox(
                    formulario, values=("Solicitud", "Carta", "Escrito", "Oficio", "Otro"), width=34
                )
            else:
                entrada = ttk.Entry(formulario, width=37)
            entrada.grid(row=fila * 2 + 1, column=0, sticky="ew", pady=(0, 3))
            self.entradas[campo] = entrada

        botones_formulario = ttk.Frame(formulario)
        botones_formulario.grid(row=len(campos) * 2, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(botones_formulario, text="Registrar", command=self.registrar).pack(side="left", padx=(0, 6))
        ttk.Button(botones_formulario, text="Limpiar", command=self.limpiar_formulario).pack(side="left")

        panel = ttk.LabelFrame(contenido, text="Consulta de expedientes", padding=12)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        busqueda = ttk.Frame(panel)
        busqueda.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(busqueda, text="Código:").pack(side="left", padx=(0, 6))
        self.entrada_busqueda = ttk.Entry(busqueda, width=25)
        self.entrada_busqueda.pack(side="left", padx=(0, 6))
        self.entrada_busqueda.bind("<Return>", lambda _evento: self.buscar())
        ttk.Button(busqueda, text="Buscar", command=self.buscar).pack(side="left", padx=(0, 6))
        ttk.Button(busqueda, text="Mostrar todos", command=self.mostrar_todos).pack(side="left", padx=(0, 6))
        ttk.Button(busqueda, text="Ordenar por código", command=self.ordenar).pack(side="left", padx=(0, 6))
        ttk.Button(busqueda, text="Recargar archivo", command=self.recargar).pack(side="left")

        tabla_frame = ttk.Frame(panel)
        tabla_frame.grid(row=1, column=0, sticky="nsew")
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        columnas = CAMPOS
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=18)
        encabezados = {
            "codigo": ("Código", 95),
            "nombre": ("Ciudadano", 175),
            "tipo_doc_identidad": ("Tipo identidad", 125),
            "numero_doc_identidad": ("N.º identidad", 105),
            "tipo_documento": ("Documento presentado", 145),
            "asunto": ("Asunto", 190),
            "fecha_recepcion": ("Fecha", 105),
        }
        for columna, (titulo, ancho) in encabezados.items():
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, minwidth=75, anchor="w")

        barra_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        barra_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")

        self.estado = tk.StringVar(value="Listo.")
        ttk.Label(self.ventana, textvariable=self.estado, relief="sunken", anchor="w", padding=(10, 5)).pack(fill="x", side="bottom")

    def _cargar_al_iniciar(self) -> None:
        try:
            self.expedientes = cargar_expedientes(self.ruta_datos)
            self._actualizar_tabla(self.expedientes)
            self.estado.set(f"Expedientes cargados: {len(self.expedientes)}")
        except ErrorPersistencia as exc:
            messagebox.showerror("Error al cargar datos", str(exc), parent=self.ventana)
            self.estado.set("No se pudo cargar el archivo. Revisa el mensaje de error.")

    def _datos_formulario(self) -> dict[str, str]:
        return {campo: widget.get() for campo, widget in self.entradas.items()}  # type: ignore[attr-defined]

    def registrar(self) -> None:
        try:
            nuevo = validar_expediente(self._datos_formulario(), self.expedientes)
        except ValueError as exc:
            messagebox.showwarning("Datos por revisar", str(exc), parent=self.ventana)
            return

        self.expedientes.append(nuevo)
        try:
            guardar_expedientes(self.ruta_datos, self.expedientes)
        except ErrorPersistencia as exc:
            self.expedientes.pop()
            messagebox.showerror("No se guardó el expediente", str(exc), parent=self.ventana)
            return

        self.mostrar_todos()
        self.limpiar_formulario()
        self.estado.set(f"Expediente {nuevo['codigo']} registrado y guardado.")
        messagebox.showinfo("Registro correcto", f"El expediente {nuevo['codigo']} se registró correctamente.", parent=self.ventana)

    def buscar(self) -> None:
        codigo = self.entrada_busqueda.get().strip()
        if not codigo:
            messagebox.showwarning("Falta el código", "Escribe el código que deseas buscar.", parent=self.ventana)
            return
        encontrado = buscar_por_codigo(self.expedientes, codigo)
        if encontrado is None:
            self._actualizar_tabla([])
            self.estado.set(f"No se encontró un expediente con el código {codigo.upper()}.")
            messagebox.showinfo("Sin resultados", f"No se encontró el expediente {codigo.upper()}.", parent=self.ventana)
            return
        self._actualizar_tabla([encontrado])
        self.estado.set(f"Expediente encontrado: {encontrado['codigo']}")

    def mostrar_todos(self) -> None:
        self._actualizar_tabla(self.expedientes)
        self.estado.set(f"Expedientes registrados: {len(self.expedientes)}")

    def ordenar(self) -> None:
        ordenados = ordenar_por_codigo(self.expedientes)
        try:
            guardar_expedientes(self.ruta_datos, ordenados)
        except ErrorPersistencia as exc:
            messagebox.showerror("No se pudo guardar el orden", str(exc), parent=self.ventana)
            return
        self.expedientes = ordenados
        self._actualizar_tabla(self.expedientes)
        self.estado.set("Expedientes ordenados por código ascendente y guardados.")

    def recargar(self) -> None:
        try:
            cargados = cargar_expedientes(self.ruta_datos)
        except ErrorPersistencia as exc:
            messagebox.showerror("Error al recargar", str(exc), parent=self.ventana)
            return
        self.expedientes = cargados
        self._actualizar_tabla(self.expedientes)
        self.estado.set(f"Archivo recargado. Expedientes disponibles: {len(self.expedientes)}")

    def limpiar_formulario(self) -> None:
        for widget in self.entradas.values():
            widget.delete(0, tk.END)  # type: ignore[attr-defined]

    def _actualizar_tabla(self, expedientes: list[dict[str, str]]) -> None:
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
        for expediente in expedientes:
            self.tabla.insert("", tk.END, values=[expediente.get(campo, "") for campo in CAMPOS])
