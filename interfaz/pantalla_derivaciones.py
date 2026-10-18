import tkinter as tk
import webbrowser
from tkinter import ttk

from componentes import mensajes
from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaDerivaciones(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Derivaciones y seguimiento", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Registra cada envío, conserva el cargo interno y actualiza la entrega o devolución.", style="Hint.TLabel").pack(anchor="w", pady=(4, 16))
        columnas = ("codigo", "remitente", "unidad", "prioridad", "estado")
        self.tabla = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=7)
        for col, titulo, ancho in zip(columnas, ("Expediente", "Remitente", "Unidad", "Prioridad", "Estado"), (105, 175, 180, 90, 150)):
            self.tabla.heading(col, text=titulo); self.tabla.column(col, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        form = ttk.Frame(tarjeta, style="Card.TFrame")
        form.pack(fill="x", pady=(16, 0)); form.columnconfigure(1, weight=1)
        self.codigo = tk.StringVar(); self.modalidad = tk.StringVar(value="Física")
        self.responsable = tk.StringVar(); self.receptor = tk.StringVar()
        self.guia = tk.StringVar(); self.documentos = tk.StringVar(); self.confirmado_por = tk.StringVar()
        self._entrada(form, 0, "Código de expediente", self.codigo)
        ttk.Label(form, text="Modalidad").grid(row=1, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Combobox(form, textvariable=self.modalidad, values=("Física", "Digital"), state="readonly").grid(row=1, column=1, sticky="ew", pady=7)
        self._entrada(form, 2, "Responsable del envío", self.responsable)
        self._entrada(form, 3, "Persona o unidad que recibe", self.receptor)
        self._entrada(form, 4, "Guía o constancia", self.guia)
        self._entrada(form, 5, "Documentos remitidos", self.documentos)
        ttk.Label(form, text="Observaciones").grid(row=6, column=0, sticky="nw", padx=(0, 16), pady=7)
        self.observaciones = tk.Text(form, height=3, wrap="word")
        self.observaciones.grid(row=6, column=1, sticky="ew", pady=7)
        self.detalle = ttk.Label(tarjeta, text="", style="Hint.TLabel", wraplength=760, justify="left")
        self.detalle.pack(anchor="w", fill="x", pady=(12, 4))
        confirmar = ttk.Frame(tarjeta, style="Card.TFrame")
        confirmar.pack(fill="x", pady=(8, 0)); confirmar.columnconfigure(1, weight=1)
        self._entrada(confirmar, 0, "Confirma recepción por", self.confirmado_por)
        acciones = ttk.Frame(tarjeta, style="Card.TFrame")
        acciones.pack(fill="x", pady=(12, 0))
        ttk.Button(acciones, text="Registrar derivación", command=self.derivar).pack(side="left")
        ttk.Button(acciones, text="Generar cargo interno PDF", command=self.generar_cargo).pack(side="left", padx=8)
        ttk.Button(acciones, text="Confirmar entrega", command=self.entregar).pack(side="left")
        ttk.Button(acciones, text="Registrar devolución", command=self.devolver).pack(side="left", padx=8)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar).pack(side="right")
        self.actualizar()

    @staticmethod
    def _entrada(padre, fila, etiqueta, variable):
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 16), pady=7)
        ttk.Entry(padre, textvariable=variable).grid(row=fila, column=1, sticky="ew", pady=7)

    def actualizar(self) -> None:
        self.tabla.delete(*self.tabla.get_children())
        for registro in self.servicio.expedientes:
            if registro.get("clasificacion", {}).get("estado") != "Listo para derivación" and registro.get("estado") not in ("Derivado", "Entregado", "Devuelto"):
                continue
            clase = registro.get("clasificacion", {})
            self.tabla.insert("", "end", iid=registro["codigo"], values=(registro["codigo"], registro.get("nombre_completo", ""),
                              clase.get("unidad", ""), clase.get("prioridad", "Normal"), registro.get("estado", "")))

    def _seleccionar(self, _evento=None) -> None:
        seleccion = self.tabla.selection()
        if seleccion:
            self.codigo.set(seleccion[0]); self.consultar()

    def consultar(self) -> None:
        registro = self.servicio.buscar(self.codigo.get().strip())
        if not registro:
            self.detalle.configure(text="No se encontró el expediente."); return
        movimientos = registro.get("derivaciones", [])
        if not movimientos:
            self.detalle.configure(text=f"Estado: {registro.get('estado', '')}. Aún no hay movimientos de derivación."); return
        partes = []
        for movimiento in movimientos:
            partes.append(f"{movimiento.get('fecha')} {movimiento.get('hora')} | {movimiento.get('unidad')} | {movimiento.get('estado')} | recibe: {movimiento.get('receptor')}")
            if movimiento.get("nota_transferencia"):
                partes.append(movimiento["nota_transferencia"])
        self.detalle.configure(text="\n".join(partes))

    def derivar(self) -> None:
        datos = {"modalidad": self.modalidad.get(), "responsable": self.responsable.get().strip(),
                 "receptor": self.receptor.get().strip(), "guia": self.guia.get().strip(),
                 "documentos": self.documentos.get().strip(), "observaciones": self.observaciones.get("1.0", "end").strip()}
        try:
            self.servicio.derivar(self.codigo.get().strip(), datos)
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        self.consultar(); self.actualizar()
        mensajes.exito("La derivación quedó registrada.")

    def generar_cargo(self) -> None:
        try:
            ruta = self.servicio.generar_cargo_derivacion(self.codigo.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        webbrowser.open(ruta.resolve().as_uri())
        self.consultar()

    def entregar(self) -> None:
        try:
            self.servicio.confirmar_entrega(self.codigo.get().strip(), self.confirmado_por.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        self.consultar(); self.actualizar()
        mensajes.exito("La entrega quedó confirmada.")

    def devolver(self) -> None:
        try:
            self.servicio.registrar_devolucion(self.codigo.get().strip(), self.responsable.get().strip(), self.observaciones.get("1.0", "end").strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        self.consultar(); self.actualizar()
        mensajes.exito("La devolución quedó registrada.")
