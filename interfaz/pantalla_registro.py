import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime

from componentes import mensajes
from interfaz import campos, desplazamiento
from servicios import validaciones
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaRegistro(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        self.tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        self.tarjeta.pack(fill="both", expand=True)
        self.archivos: list[str] = []
        self.borrador_id = ""
        self.estado_cotejo = "Pendiente"
        self._crear_formulario()
        self._actualizar_reloj()

    def _crear_formulario(self) -> None:
        ttk.Label(self.tarjeta, text="Recepción y registro", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.tarjeta, text="Registra los datos, coteja los documentos y guarda observaciones para continuar después.", style="Hint.TLabel").pack(anchor="w", pady=(4, 18))
        borradores = ttk.Frame(self.tarjeta, style="Card.TFrame")
        borradores.pack(fill="x", pady=(0, 16))
        ttk.Label(borradores, text="Recepciones guardadas").pack(side="left", padx=(0, 10))
        self.borrador_var = tk.StringVar()
        self.borradores_combo = ttk.Combobox(borradores, textvariable=self.borrador_var, state="readonly", width=35)
        self.borradores_combo.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(borradores, text="Cargar", command=self._cargar_borrador).pack(side="left")
        self._actualizar_borradores()

        form = ttk.Frame(self.tarjeta, style="Card.TFrame")
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)
        self.codigo_var = tk.StringVar(value="EXP001")
        self.codigo_documento_var = tk.StringVar(value="")
        self.nombre_var = tk.StringVar()
        self.identidad_tipo_var = tk.StringVar(value="DNI")
        self.identidad_numero_var = tk.StringVar()
        self.documento_tipo_var = tk.StringVar(value="Carta")
        self.documento_otro_var = tk.StringVar()
        self.asunto_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.hora_var = tk.StringVar()
        self.modalidad_var = tk.StringVar(value="Física")
        self.folios_declarados_var = tk.StringVar(value="0")
        self.folios_verificados_var = tk.StringVar(value="0")
        self.presenta_anexos_var = tk.BooleanVar(value=False)
        self.cantidad_anexos_var = tk.StringVar(value="0")
        self.firma_var = tk.StringVar(value="Sí")
        self.legible_var = tk.BooleanVar(value=True)
        self.completo_var = tk.BooleanVar(value=True)
        self.responsable_var = tk.StringVar()
        self.excepcion_var = tk.BooleanVar(value=False)

        fila = 0
        self._campo_solo_lectura(form, fila, "Código de expediente", self.codigo_var); fila += 1
        self._campo_solo_lectura(form, fila, "Código de documento", self.codigo_documento_var); fila += 1
        campos.entrada(form, fila, "Nombre completo", self.nombre_var); fila += 1
        campos.seleccion(form, fila, "Tipo de identidad", self.identidad_tipo_var, validaciones.TIPOS_IDENTIDAD); fila += 1
        campos.entrada_identidad(form, fila, "Número de identidad", self.identidad_numero_var, self.identidad_tipo_var); fila += 1
        campos.seleccion(form, fila, "Documento presentado", self.documento_tipo_var, validaciones.TIPOS_PRESENTADO); fila += 1
        ttk.Label(form, text="Detalle de otro documento").grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        self.otro_entry = ttk.Entry(form, textvariable=self.documento_otro_var)
        self.otro_entry.grid(row=fila, column=1, sticky="ew", pady=7); fila += 1
        campos.entrada(form, fila, "Asunto", self.asunto_var); fila += 1
        self._campo_solo_lectura(form, fila, "Fecha de recepción", self.fecha_var); fila += 1
        self._campo_solo_lectura(form, fila, "Hora de recepción", self.hora_var); fila += 1
        self.documento_tipo_var.trace_add("write", self._actualizar_codigo)
        self.documento_otro_var.trace_add("write", self._actualizar_codigo)
        self._actualizar_codigo()
        self.documento_tipo_var.trace_add("write", self._mostrar_otro)
        self._mostrar_otro()

        ttk.Separator(self.tarjeta).pack(fill="x", pady=18)
        ttk.Label(self.tarjeta, text="Documentos adjuntos", style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.tarjeta, text="Word, PDF e imágenes escaneadas.", style="Hint.TLabel").pack(anchor="w", pady=(4, 8))
        archivos_barra = ttk.Frame(self.tarjeta, style="Card.TFrame")
        archivos_barra.pack(fill="x")
        ttk.Button(archivos_barra, text="Agregar archivos", command=self._agregar_archivos).pack(side="left")
        ttk.Button(archivos_barra, text="Quitar seleccionado", command=self._quitar_archivo).pack(side="left", padx=8)
        self.lista_archivos = tk.Listbox(self.tarjeta, height=4, selectmode="extended", relief="solid", borderwidth=1)
        self.lista_archivos.pack(fill="x", pady=(8, 0))

        ttk.Separator(self.tarjeta).pack(fill="x", pady=18)
        ttk.Label(self.tarjeta, text="Cotejo de recepción", style="Title.TLabel").pack(anchor="w")
        cot = ttk.Frame(self.tarjeta, style="Card.TFrame")
        cot.pack(fill="x", pady=(8, 0))
        cot.columnconfigure(1, weight=1)
        fila = 0
        self._combo(cot, fila, "Modalidad", self.modalidad_var, ("Física", "Digital")); fila += 1
        self._entrada(cot, fila, "Folios declarados", self.folios_declarados_var); fila += 1
        self._entrada(cot, fila, "Folios verificados", self.folios_verificados_var); fila += 1
        ttk.Checkbutton(cot, text="Se recibieron anexos", variable=self.presenta_anexos_var).grid(row=fila, column=1, sticky="w", pady=6); fila += 1
        self._entrada(cot, fila, "Cantidad de anexos", self.cantidad_anexos_var); fila += 1
        ttk.Label(cot, text="Descripción de anexos").grid(row=fila, column=0, sticky="nw", padx=(0, 16), pady=7)
        self.anexos_text = tk.Text(cot, height=4, wrap="word")
        self.anexos_text.grid(row=fila, column=1, sticky="ew", pady=7); fila += 1
        self._combo(cot, fila, "Firma", self.firma_var, ("Sí", "No", "No corresponde")); fila += 1
        ttk.Checkbutton(cot, text="Documento legible", variable=self.legible_var).grid(row=fila, column=1, sticky="w", pady=4); fila += 1
        ttk.Checkbutton(cot, text="Documento completo", variable=self.completo_var).grid(row=fila, column=1, sticky="w", pady=4); fila += 1
        self._entrada(cot, fila, "Responsable del cotejo", self.responsable_var); fila += 1
        ttk.Label(cot, text="Observaciones").grid(row=fila, column=0, sticky="nw", padx=(0, 16), pady=7)
        self.observaciones_text = tk.Text(cot, height=3, wrap="word")
        self.observaciones_text.grid(row=fila, column=1, sticky="ew", pady=7); fila += 1
        ttk.Checkbutton(cot, text="Excepción autorizada", variable=self.excepcion_var).grid(row=fila, column=1, sticky="w", pady=4); fila += 1
        ttk.Label(cot, text="Motivo de excepción").grid(row=fila, column=0, sticky="nw", padx=(0, 16), pady=7)
        self.excepcion_text = tk.Text(cot, height=3, wrap="word")
        self.excepcion_text.grid(row=fila, column=1, sticky="ew", pady=7); fila += 1

        self.estado_var = tk.StringVar(value="Estado del cotejo: pendiente")
        ttk.Label(self.tarjeta, textvariable=self.estado_var, style="Hint.TLabel").pack(anchor="w", pady=(12, 8))
        acciones = ttk.Frame(self.tarjeta, style="Card.TFrame")
        acciones.pack(fill="x", pady=(10, 0))
        ttk.Button(acciones, text="Verificar cotejo", command=self._verificar).pack(side="left")
        ttk.Button(acciones, text="Guardar observación", command=self._guardar_observacion).pack(side="left", padx=8)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar).pack(side="right")
        ttk.Button(acciones, text="Continuar al registro", style="Accent.TButton", command=self._registrar).pack(side="right", padx=8)

    @staticmethod
    def _campo_solo_lectura(padre: ttk.Frame, fila: int, etiqueta: str, variable: tk.StringVar) -> None:
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(padre, textvariable=variable, state="readonly").grid(row=fila, column=1, sticky="ew", pady=7)

    @staticmethod
    def _entrada(padre: ttk.Frame, fila: int, etiqueta: str, variable: tk.StringVar) -> None:
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(padre, textvariable=variable).grid(row=fila, column=1, sticky="ew", pady=7)

    @staticmethod
    def _combo(padre: ttk.Frame, fila: int, etiqueta: str, variable: tk.StringVar, opciones: tuple[str, ...]) -> None:
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Combobox(padre, textvariable=variable, values=opciones, state="readonly").grid(row=fila, column=1, sticky="ew", pady=7)

    def _actualizar_reloj(self) -> None:
        ahora = datetime.now()
        self.fecha_var.set(ahora.strftime("%d/%m/%Y"))
        self.hora_var.set(ahora.strftime("%H:%M:%S"))
        self.after(1000, self._actualizar_reloj)

    def _actualizar_codigo(self, *_args) -> None:
        tipo = self.documento_tipo_var.get()
        otro = self.documento_otro_var.get()
        if tipo == "Otro" and len("".join(c for c in otro if c.isalpha())) < 3:
            self.codigo_documento_var.set("Escribe el tipo de documento")
            return
        try:
            codigo, doc = self.servicio.sugerir_codigo(tipo, otro)
            self.codigo_var.set(codigo)
            self.codigo_documento_var.set(doc)
        except ValueError:
            self.codigo_documento_var.set("")

    def _mostrar_otro(self, *_args) -> None:
        if self.documento_tipo_var.get() == "Otro":
            self.otro_entry.state(["!disabled"])
        else:
            self.otro_entry.state(["disabled"])

    def _agregar_archivos(self) -> None:
        seleccion = filedialog.askopenfilenames(title="Seleccionar documentos", filetypes=[
            ("Documentos e imágenes", "*.doc *.docx *.odt *.rtf *.pdf *.png *.jpg *.jpeg *.tif *.tiff *.bmp *.gif *.webp"),
            ("Todos los archivos", "*.*")])
        for ruta in seleccion:
            if ruta not in self.archivos:
                self.archivos.append(ruta)
                self.lista_archivos.insert("end", ruta)

    def _quitar_archivo(self) -> None:
        for indice in reversed(self.lista_archivos.curselection()):
            self.lista_archivos.delete(indice)
            del self.archivos[indice]

    def _datos_cotejo(self) -> dict:
        anexos = [linea.strip() for linea in self.anexos_text.get("1.0", "end").splitlines() if linea.strip()]
        return {
            "modalidad": self.modalidad_var.get(),
            "folios_declarados": self.folios_declarados_var.get(),
            "folios_verificados": self.folios_verificados_var.get(),
            "presenta_anexos": self.presenta_anexos_var.get(),
            "cantidad_anexos": self.cantidad_anexos_var.get(),
            "anexos": anexos,
            "firma": self.firma_var.get(),
            "legible": self.legible_var.get(),
            "completo": self.completo_var.get(),
            "responsable": self.responsable_var.get().strip(),
            "observaciones": self.observaciones_text.get("1.0", "end").strip(),
            "excepcion_autorizada": self.excepcion_var.get(),
            "motivo_excepcion": self.excepcion_text.get("1.0", "end").strip(),
        }

    def _datos(self) -> dict:
        return {"nombre_completo": self.nombre_var.get().strip(),
                "tipo_documento_identidad": self.identidad_tipo_var.get(),
                "numero_documento": self.identidad_numero_var.get().strip(),
                "tipo_documento_presentado": self.documento_tipo_var.get(),
                "tipo_documento_otro": self.documento_otro_var.get().strip(),
                "asunto": self.asunto_var.get().strip(),
                "fecha_recepcion": self.fecha_var.get(), "hora_recepcion": self.hora_var.get(),
                "archivos_adjuntos": list(self.archivos), "cotejo": self._datos_cotejo(),
                "borrador_id": self.borrador_id}

    def _verificar(self) -> None:
        try:
            validaciones.validar_cotejo(self._datos_cotejo())
        except ValueError as error:
            self.estado_cotejo = "Observado"
            self.estado_var.set("Estado del cotejo: observado. " + str(error))
            return
        self.estado_cotejo = "Conforme"
        self.estado_var.set("Estado del cotejo: conforme. Puedes continuar al registro.")

    def _guardar_observacion(self) -> None:
        datos = self._datos()
        if not datos["cotejo"]["observaciones"]:
            mensajes.error("Escribe la observación antes de guardarla.")
            return
        try:
            self.borrador_id = self.servicio.guardar_borrador(datos, "Observado")
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        self.estado_cotejo = "Observado"
        self.estado_var.set("Observación guardada: " + self.borrador_id)
        self._actualizar_borradores()
        mensajes.exito("La recepción observada quedó guardada para continuar después.")

    def _registrar(self) -> None:
        self._verificar()
        if self.estado_cotejo != "Conforme":
            mensajes.error("Corrige el cotejo o guarda la recepción como observada.")
            return
        try:
            registro = self.servicio.registrar(self._datos())
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        mensajes.exito(f"Expediente registrado con el código {registro.codigo}.")
        self._limpiar()

    def _actualizar_borradores(self) -> None:
        borradores = self.servicio.listar_borradores()
        self._borrador_por_etiqueta = {f"{b.get('borrador_id')} | {b.get('nombre_completo', '')} | {b.get('actualizado', '')}": b for b in borradores}
        valores = list(self._borrador_por_etiqueta)
        self.borradores_combo.configure(values=valores)
        if valores and not self.borrador_var.get():
            self.borrador_var.set(valores[-1])

    def _cargar_borrador(self) -> None:
        borrador = self._borrador_por_etiqueta.get(self.borrador_var.get())
        if not borrador:
            return
        self.borrador_id = borrador.get("borrador_id", "")
        for variable, llave in ((self.nombre_var, "nombre_completo"), (self.identidad_tipo_var, "tipo_documento_identidad"),
                                (self.identidad_numero_var, "numero_documento"), (self.documento_tipo_var, "tipo_documento_presentado"),
                                (self.documento_otro_var, "tipo_documento_otro"), (self.asunto_var, "asunto")):
            variable.set(borrador.get(llave, variable.get()))
        cotejo = borrador.get("cotejo", {})
        for variable, llave in ((self.modalidad_var, "modalidad"), (self.folios_declarados_var, "folios_declarados"),
                                (self.folios_verificados_var, "folios_verificados"), (self.cantidad_anexos_var, "cantidad_anexos"),
                                (self.firma_var, "firma"), (self.responsable_var, "responsable")):
            variable.set(str(cotejo.get(llave, variable.get())))
        self.presenta_anexos_var.set(bool(cotejo.get("presenta_anexos", False)))
        self.legible_var.set(bool(cotejo.get("legible", False)))
        self.completo_var.set(bool(cotejo.get("completo", False)))
        self.excepcion_var.set(bool(cotejo.get("excepcion_autorizada", False)))
        for widget, texto in ((self.anexos_text, "\n".join(cotejo.get("anexos", []))),
                              (self.observaciones_text, cotejo.get("observaciones", "")),
                              (self.excepcion_text, cotejo.get("motivo_excepcion", ""))):
            widget.delete("1.0", "end"); widget.insert("1.0", texto)
        self.archivos = list(borrador.get("archivos_adjuntos", []))
        self.lista_archivos.delete(0, "end")
        for ruta in self.archivos:
            self.lista_archivos.insert("end", ruta)
        self.estado_cotejo = "Observado"
        self.estado_var.set("Recepción observada cargada: " + self.borrador_id)
        self._actualizar_codigo()

    def _limpiar(self) -> None:
        for variable in (self.nombre_var, self.identidad_numero_var, self.documento_otro_var, self.asunto_var, self.responsable_var):
            variable.set("")
        self.identidad_tipo_var.set("DNI")
        self.documento_tipo_var.set("Carta")
        self.modalidad_var.set("Física")
        self.folios_declarados_var.set("0"); self.folios_verificados_var.set("0")
        self.cantidad_anexos_var.set("0"); self.presenta_anexos_var.set(False)
        self.firma_var.set("Sí"); self.legible_var.set(True); self.completo_var.set(True); self.excepcion_var.set(False)
        for widget in (self.anexos_text, self.observaciones_text, self.excepcion_text):
            widget.delete("1.0", "end")
        self.archivos = []; self.lista_archivos.delete(0, "end")
        self.borrador_id = ""; self.estado_cotejo = "Pendiente"
        self.estado_var.set("Estado del cotejo: pendiente")
        self.borrador_var.set("")
        self._actualizar_codigo(); self._actualizar_borradores()
