from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk

from componentes import mensajes
from interfaz import campos, desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes
from servicios.validaciones import TIPOS_IDENTIDAD, TIPOS_PRESENTADO


class PantallaRegistro(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        self.archivos_seleccionados: list[str] = []
        self.variables = {nombre: tk.StringVar() for nombre in (
            "codigo", "nombre_completo", "tipo_documento_identidad", "numero_documento",
            "tipo_documento_presentado", "tipo_documento_otro", "codigo_documento", "asunto",
            "fecha_recepcion", "hora_recepcion",
        )}
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=26)
        tarjeta.pack(fill="x", expand=True)
        ttk.Label(tarjeta, text="Registrar expediente", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Ingresa los datos del documento recibido.", style="Hint.TLabel").pack(anchor="w", pady=(4, 20))
        formulario = ttk.Frame(tarjeta, style="Card.TFrame")
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        self._fila_codigo(formulario, 0, "Código de expediente", "codigo")
        campos.entrada(formulario, 1, "Nombre completo", self.variables["nombre_completo"])
        campos.seleccion(formulario, 2, "Tipo de identidad", self.variables["tipo_documento_identidad"], TIPOS_IDENTIDAD)
        campos.entrada_identidad(formulario, 3, "N.º de documento", self.variables["numero_documento"], self.variables["tipo_documento_identidad"])
        campos.seleccion(formulario, 4, "Documento presentado", self.variables["tipo_documento_presentado"], TIPOS_PRESENTADO)
        ttk.Label(formulario, text="Archivos adjuntos").grid(row=5, column=0, sticky="nw", padx=(0, 16), pady=7)
        zona_archivos = ttk.Frame(formulario, style="Card.TFrame")
        zona_archivos.grid(row=5, column=1, sticky="ew", pady=7)
        controles = ttk.Frame(zona_archivos, style="Card.TFrame")
        controles.pack(fill="x")
        ttk.Button(controles, text="Seleccionar archivos", command=self.seleccionar_archivos).pack(side="left")
        ttk.Button(controles, text="Quitar seleccionado", command=self.quitar_archivo).pack(side="left", padx=(8, 0))
        self.lista_archivos = tk.Listbox(zona_archivos, height=3, activestyle="none", borderwidth=0, highlightthickness=1)
        self.lista_archivos.pack(fill="x", pady=(7, 0))
        self.etiqueta_otro = ttk.Label(formulario, text="Especifica el documento")
        self.etiqueta_otro.grid(row=6, column=0, sticky="w", padx=(0, 16), pady=7)
        self.entrada_otro = ttk.Entry(formulario, textvariable=self.variables["tipo_documento_otro"], width=38)
        self.entrada_otro.grid(row=6, column=1, sticky="ew", pady=7)
        self._fila_codigo(formulario, 7, "Código de documento", "codigo_documento")
        campos.entrada(formulario, 8, "Asunto", self.variables["asunto"])
        self._fila_codigo(formulario, 9, "Fecha de recepción", "fecha_recepcion")
        self._fila_codigo(formulario, 10, "Hora de recepción", "hora_recepcion")
        self.variables["tipo_documento_presentado"].trace_add("write", self._actualizar_codigos)
        self.variables["tipo_documento_otro"].trace_add("write", self._actualizar_codigos)
        self._actualizar_codigos()
        self._actualizar_reloj()
        pie = ttk.Frame(tarjeta, style="Card.TFrame")
        pie.pack(fill="x", pady=(22, 0))
        ttk.Button(pie, text="Limpiar", command=self.limpiar).pack(side="right", padx=(8, 0))
        ttk.Button(pie, text="Registrar expediente", style="Accent.TButton", command=self.registrar).pack(side="right")

    def _fila_codigo(self, contenedor: ttk.Frame, fila: int, etiqueta: str, clave: str) -> None:
        ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(contenedor, textvariable=self.variables[clave], state="readonly", width=38).grid(row=fila, column=1, sticky="ew", pady=7)

    def seleccionar_archivos(self) -> None:
        tipos = [
            ("Documentos compatibles", "*.doc *.docx *.odt *.rtf *.pdf *.png *.jpg *.jpeg *.tif *.tiff *.bmp *.gif *.webp"),
            ("Todos los archivos", "*.*"),
        ]
        for ruta in filedialog.askopenfilenames(title="Adjuntar documentos", filetypes=tipos):
            if ruta not in self.archivos_seleccionados:
                self.archivos_seleccionados.append(ruta)
                self.lista_archivos.insert(tk.END, Path(ruta).name)

    def quitar_archivo(self) -> None:
        seleccion = self.lista_archivos.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_archivos.delete(indice)
            self.archivos_seleccionados.pop(indice)

    def limpiar(self) -> None:
        for clave in ("nombre_completo", "tipo_documento_identidad", "numero_documento",
                      "tipo_documento_presentado", "tipo_documento_otro", "asunto"):
            self.variables[clave].set("")
        self.archivos_seleccionados.clear()
        self.lista_archivos.delete(0, tk.END)
        self._actualizar_codigos()

    def _actualizar_reloj(self) -> None:
        ahora = datetime.now()
        self.variables["fecha_recepcion"].set(ahora.strftime("%d/%m/%Y"))
        self.variables["hora_recepcion"].set(ahora.strftime("%H:%M:%S"))
        self.after(1000, self._actualizar_reloj)

    def _actualizar_codigos(self, *_args) -> None:
        tipo = self.variables["tipo_documento_presentado"].get()
        otro = self.variables["tipo_documento_otro"].get()
        if tipo == "Otro":
            self.etiqueta_otro.grid()
            self.entrada_otro.grid()
        else:
            self.etiqueta_otro.grid_remove()
            self.entrada_otro.grid_remove()
        try:
            expediente, documento = self.servicio.codigos_siguientes(tipo, otro)
        except ValueError:
            expediente, documento = self.servicio.codigos_siguientes("Carta")[0], ""
        self.variables["codigo"].set(expediente)
        self.variables["codigo_documento"].set(documento)

    def registrar(self) -> None:
        try:
            datos = {clave: variable.get() for clave, variable in self.variables.items()}
            datos["archivos_adjuntos"] = list(self.archivos_seleccionados)
            expediente = self.servicio.registrar(datos)
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        mensajes.exito("El expediente se registró correctamente.")
        self.limpiar()
        self.variables["fecha_recepcion"].set(expediente.fecha_recepcion)
        self.variables["hora_recepcion"].set(expediente.hora_recepcion)
