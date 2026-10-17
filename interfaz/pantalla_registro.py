import tkinter as tk
from tkinter import ttk
from datetime import datetime

from componentes import mensajes
from interfaz import campos
from servicios.servicio_expedientes import ServicioExpedientes
from servicios.validaciones import TIPOS_IDENTIDAD, TIPOS_PRESENTADO


class PantallaRegistro(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent, padding=28)
        self.servicio = servicio
        self.variables = {nombre: tk.StringVar() for nombre in (
            "codigo", "codigo_paciente", "nombre_completo", "tipo_documento_identidad", "numero_documento",
            "tipo_documento_presentado", "tipo_documento_otro", "codigo_documento", "asunto",
            "fecha_recepcion", "hora_recepcion",
        )}
        tarjeta = ttk.Frame(self, style="Card.TFrame", padding=26)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Registrar expediente", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Ingresa los datos del documento recibido.", style="Hint.TLabel").pack(anchor="w", pady=(4, 20))
        formulario = ttk.Frame(tarjeta, style="Card.TFrame")
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        self._fila_codigo(formulario, 0, "Código de expediente", "codigo")
        self._fila_codigo(formulario, 1, "Código de paciente", "codigo_paciente")
        campos.entrada(formulario, 2, "Nombre completo", self.variables["nombre_completo"])
        campos.seleccion(formulario, 3, "Tipo de identidad", self.variables["tipo_documento_identidad"], TIPOS_IDENTIDAD)
        campos.entrada_identidad(formulario, 4, "N.º de documento", self.variables["numero_documento"], self.variables["tipo_documento_identidad"])
        campos.seleccion(formulario, 5, "Documento presentado", self.variables["tipo_documento_presentado"], TIPOS_PRESENTADO)
        self.etiqueta_otro = ttk.Label(formulario, text="Especifica el documento")
        self.etiqueta_otro.grid(row=6, column=0, sticky="w", padx=(0, 16), pady=7)
        self.entrada_otro = ttk.Entry(formulario, textvariable=self.variables["tipo_documento_otro"], width=38)
        self.entrada_otro.grid(row=6, column=1, sticky="ew", pady=7)
        self._fila_codigo(formulario, 7, "Código de documento", "codigo_documento")
        campos.entrada(formulario, 8, "Asunto", self.variables["asunto"])
        self._fila_codigo(formulario, 9, "Fecha de recepción", "fecha_recepcion")
        self._fila_codigo(formulario, 10, "Hora de recepción", "hora_recepcion")
        self.variables["tipo_documento_identidad"].trace_add("write", self._tipo_identidad_cambio)
        self.variables["tipo_documento_presentado"].trace_add("write", self._actualizar_codigos)
        self.variables["tipo_documento_otro"].trace_add("write", self._actualizar_codigos)
        self.variables["tipo_documento_identidad"].trace_add("write", self._actualizar_codigo_paciente)
        self.variables["numero_documento"].trace_add("write", self._actualizar_codigo_paciente)
        self._tipo_identidad_cambio()
        self._actualizar_codigos()
        self._actualizar_codigo_paciente()
        self._actualizar_reloj()
        pie = ttk.Frame(tarjeta, style="Card.TFrame")
        pie.pack(fill="x", pady=(22, 0))
        ttk.Button(pie, text="Limpiar", command=self.limpiar).pack(side="right", padx=(8, 0))
        ttk.Button(pie, text="Registrar expediente", style="Accent.TButton", command=self.registrar).pack(side="right")

    def limpiar(self) -> None:
        for clave in ("nombre_completo", "tipo_documento_identidad", "numero_documento",
                      "tipo_documento_presentado", "tipo_documento_otro", "asunto"):
            self.variables[clave].set("")
        self._actualizar_codigos()
        self._actualizar_codigo_paciente()

    def _fila_codigo(self, contenedor: ttk.Frame, fila: int, etiqueta: str, clave: str) -> None:
        ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(contenedor, textvariable=self.variables[clave], state="readonly", width=38).grid(row=fila, column=1, sticky="ew", pady=7)

    def _tipo_identidad_cambio(self, *_args) -> None:
        tipo = self.variables["tipo_documento_identidad"].get()
        numero = self.variables["numero_documento"].get()
        maximo = 8 if tipo == "DNI" else 9
        if len(numero) > maximo:
            self.variables["numero_documento"].set("")
        elif tipo in ("DNI", "Carné de extranjería") and numero and not (numero.isascii() and numero.isdigit()):
            self.variables["numero_documento"].set("")
        elif tipo == "Pasaporte" and numero and not (numero.isascii() and numero.isalnum()):
            self.variables["numero_documento"].set("")

    def _actualizar_codigo_paciente(self, *_args) -> None:
        tipo = self.variables["tipo_documento_identidad"].get()
        numero = self.variables["numero_documento"].get()
        if tipo == "DNI":
            completo = len(numero) == 8 and numero.isascii() and numero.isdigit()
        elif tipo == "Carné de extranjería":
            completo = len(numero) == 9 and numero.isascii() and numero.isdigit()
        else:
            completo = tipo == "Pasaporte" and 6 <= len(numero) <= 9 and numero.isascii() and numero.isalnum()
        codigo = self.servicio.codigo_paciente(tipo, numero) if completo else ""
        self.variables["codigo_paciente"].set(codigo)

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
            datos = {k: v.get() for k, v in self.variables.items()}
            expediente = self.servicio.registrar(datos)
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        mensajes.exito("El expediente se registró correctamente.")
        self.limpiar()
        self.variables["fecha_recepcion"].set(expediente.fecha_recepcion)
        self.variables["hora_recepcion"].set(expediente.hora_recepcion)
