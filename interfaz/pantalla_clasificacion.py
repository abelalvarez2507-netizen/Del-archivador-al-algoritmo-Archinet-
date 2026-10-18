import tkinter as tk
from tkinter import ttk
import webbrowser

from componentes import mensajes
from interfaz import desplazamiento
from servicios import configuracion
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaClasificacion(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Clasificación y despacho", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Ordena los expedientes, asigna destino y prepara los que tienen sus controles completos.", style="Hint.TLabel").pack(anchor="w", pady=(4, 16))
        filtros = ttk.Frame(tarjeta, style="Card.TFrame")
        filtros.pack(fill="x", pady=(0, 8))
        self.filtro = tk.StringVar(value="Todas")
        ttk.Label(filtros, text="Prioridad").pack(side="left", padx=(0, 8))
        ttk.Combobox(filtros, textvariable=self.filtro, values=("Todas", "Normal", "Urgente", "Otra"), state="readonly", width=14).pack(side="left")
        ttk.Button(filtros, text="Actualizar", command=self.actualizar).pack(side="right")
        columnas = ("codigo", "remitente", "asunto", "prioridad", "unidad", "estado")
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in zip(columnas, ("Expediente", "Remitente", "Asunto", "Prioridad", "Destino", "Estado"), (105, 150, 190, 100, 150, 165)):
            self.tabla.heading(columna, text=titulo); self.tabla.column(columna, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)
        ttk.Separator(tarjeta).pack(fill="x", pady=18)
        form = ttk.Frame(tarjeta, style="Card.TFrame")
        form.pack(fill="x"); form.columnconfigure(1, weight=1)
        self.codigo = tk.StringVar(); self.unidad = tk.StringVar(); self.tramite = tk.StringVar()
        self.categoria = tk.StringVar(); self.prioridad = tk.StringVar(value="Normal")
        self.motivo_prioridad = tk.StringVar(); self.responsable = tk.StringVar()
        self.unidad_combo = ttk.Combobox(form, textvariable=self.unidad, state="readonly")
        self._combo(form, 0, "Expediente", self.codigo, editable=True)
        self.unidad_combo.grid(row=1, column=1, sticky="ew", pady=7)
        ttk.Label(form, text="Unidad orgánica").grid(row=1, column=0, sticky="w", padx=(0, 16), pady=7)
        self._entrada(form, 2, "Trámite", self.tramite)
        self._entrada(form, 3, "Categoría", self.categoria)
        self._combo(form, 4, "Prioridad", self.prioridad, editable=False, opciones=("Normal", "Urgente", "Otra"))
        self._entrada(form, 5, "Motivo de prioridad", self.motivo_prioridad)
        self._entrada(form, 6, "Responsable", self.responsable)
        ttk.Button(form, text="Sugerir destino", command=self.sugerir_destino).grid(row=7, column=1, sticky="w", pady=6)
        acciones = ttk.Frame(tarjeta, style="Card.TFrame")
        acciones.pack(fill="x", pady=(12, 0))
        ttk.Button(acciones, text="Guardar clasificación", command=self.guardar).pack(side="left")
        ttk.Button(acciones, text="Marcar listo para derivación", style="Accent.TButton", command=self.marcar_listo).pack(side="left", padx=8)
        ttk.Button(acciones, text="Generar relación PDF", command=self.relacion).pack(side="left")
        self.actualizar()

    def _combo(self, padre, fila, etiqueta, variable, editable=False, opciones=()):
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Combobox(padre, textvariable=variable, values=opciones, state="normal" if editable else "readonly").grid(row=fila, column=1, sticky="ew", pady=7)

    @staticmethod
    def _entrada(padre, fila, etiqueta, variable):
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(padre, textvariable=variable).grid(row=fila, column=1, sticky="ew", pady=7)

    def actualizar(self) -> None:
        cfg = configuracion.cargar()
        self.unidad_combo.configure(values=cfg.get("unidades", []))
        self.tabla.delete(*self.tabla.get_children())
        for registro in self.servicio.pendientes_clasificacion(self.filtro.get()):
            clase = registro.get("clasificacion", {})
            self.tabla.insert("", "end", iid=registro["codigo"], values=(registro["codigo"], registro.get("nombre_completo", ""),
                              registro.get("asunto", ""), clase.get("prioridad", "Normal"), clase.get("unidad", ""), clase.get("estado", "")))

    def _seleccionar_fila(self, _evento=None) -> None:
        seleccion = self.tabla.selection()
        if seleccion:
            self.codigo.set(seleccion[0])
            self.cargar()

    def cargar(self) -> None:
        registro = self.servicio.buscar(self.codigo.get().strip())
        if not registro:
            return
        clase = registro.get("clasificacion", {})
        self.unidad.set(clase.get("unidad", "")); self.tramite.set(clase.get("tramite", ""))
        self.categoria.set(clase.get("categoria", "")); self.prioridad.set(clase.get("prioridad", "Normal"))
        self.motivo_prioridad.set(clase.get("motivo_prioridad", "")); self.responsable.set(clase.get("responsable", ""))

    def sugerir_destino(self) -> None:
        registro = self.servicio.buscar(self.codigo.get().strip())
        if not registro:
            mensajes.error("Consulta un expediente antes de sugerir un destino."); return
        sugerencias = configuracion.cargar().get("sugerencias", {})
        tipo = registro.get("tipo_documento_otro") if registro.get("tipo_documento_presentado") == "Otro" else registro.get("tipo_documento_presentado")
        destino = sugerencias.get(tipo) or sugerencias.get(registro.get("tipo_documento_presentado", ""))
        if not destino:
            mensajes.error("No hay una sugerencia configurada para este tipo de documento."); return
        self.unidad.set(destino)

    def guardar(self) -> None:
        datos = {"unidad": self.unidad.get().strip(), "tramite": self.tramite.get().strip(), "categoria": self.categoria.get().strip(),
                 "prioridad": self.prioridad.get(), "motivo_prioridad": self.motivo_prioridad.get().strip(), "responsable": self.responsable.get().strip()}
        try:
            self.servicio.guardar_clasificacion(self.codigo.get().strip(), datos)
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        mensajes.exito("La clasificación quedó guardada.")
        self.actualizar()

    def marcar_listo(self) -> None:
        try:
            self.servicio.marcar_listo_derivacion(self.codigo.get().strip(), self.responsable.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        mensajes.exito("El expediente quedó listo para derivación.")
        self.actualizar()

    def relacion(self) -> None:
        try:
            ruta = self.servicio.generar_relacion_despacho(self.unidad.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        webbrowser.open(ruta.resolve().as_uri())
