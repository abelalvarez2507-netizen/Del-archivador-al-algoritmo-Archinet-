import os
import tkinter as tk
import webbrowser
from tkinter import ttk

from componentes import mensajes
from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaFoliacion(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Foliación y cargos", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Prepara la ficha, confirma los folios y genera el cargo de recepción en PDF.", style="Hint.TLabel").pack(anchor="w", pady=(4, 18))
        form = ttk.Frame(tarjeta, style="Card.TFrame")
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)
        self.codigo = tk.StringVar()
        self.total = tk.StringVar()
        self.responsable = tk.StringVar()
        ttk.Label(form, text="Código de expediente").grid(row=0, column=0, sticky="w", pady=7, padx=(0, 16))
        ttk.Entry(form, textvariable=self.codigo).grid(row=0, column=1, sticky="ew", pady=7)
        ttk.Button(form, text="Consultar", command=self.consultar).grid(row=0, column=2, padx=(8, 0))
        self.detalle = ttk.Label(tarjeta, text="", style="Result.TLabel", justify="left")
        self.detalle.pack(anchor="w", fill="x", pady=12)
        ttk.Label(form, text="Folios foliados").grid(row=1, column=0, sticky="w", pady=7, padx=(0, 16))
        ttk.Entry(form, textvariable=self.total).grid(row=1, column=1, sticky="ew", pady=7)
        ttk.Label(form, text="Responsable de foliación").grid(row=2, column=0, sticky="w", pady=7, padx=(0, 16))
        ttk.Entry(form, textvariable=self.responsable).grid(row=2, column=1, sticky="ew", pady=7)
        ttk.Label(form, text="Explicación de diferencia").grid(row=3, column=0, sticky="nw", pady=7, padx=(0, 16))
        self.explicacion = tk.Text(form, height=3, wrap="word")
        self.explicacion.grid(row=3, column=1, sticky="ew", pady=7)
        acciones = ttk.Frame(tarjeta, style="Card.TFrame")
        acciones.pack(fill="x", pady=(12, 0))
        ttk.Button(acciones, text="Generar ficha de foliación", command=self.generar_ficha).pack(side="left")
        ttk.Button(acciones, text="Confirmar foliación", style="Accent.TButton", command=self.confirmar).pack(side="left", padx=8)
        ttk.Button(acciones, text="Generar cargo PDF", command=self.generar_cargo).pack(side="left")
        ttk.Button(acciones, text="Abrir cargo", command=self.abrir_cargo).pack(side="left", padx=8)
        ttk.Button(acciones, text="Imprimir cargo", command=self.imprimir_cargo).pack(side="left")
        self.ruta_actual = None

    def consultar(self) -> None:
        registro = self.servicio.buscar(self.codigo.get().strip())
        if not registro:
            self.detalle.configure(text="No se encontró el expediente.")
            self.ruta_actual = None
            return
        cotejo = registro.get("cotejo", {})
        folios = cotejo.get("folios_verificados", 0)
        self.total.set(str(folios))
        foliation = registro.get("foliacion", {})
        cargo = registro.get("cargo", {})
        self.detalle.configure(text=(f"Remitente: {registro.get('nombre_completo', '')}\n"
                                     f"Documento: {registro.get('tipo_documento_otro') or registro.get('tipo_documento_presentado', '')}\n"
                                     f"Folios cotejados: {folios} | Anexos: {cotejo.get('cantidad_anexos', 0)}\n"
                                     f"Foliación: {foliation.get('estado', 'Pendiente')} | Cargo: {'Emitido' if cargo.get('emitido') else 'Pendiente'}"))
        self.ruta_actual = self._ruta(cargo.get("ruta", "")) if cargo.get("ruta") else None

    def generar_ficha(self) -> None:
        try:
            ruta = self.servicio.generar_foliacion(self.codigo.get().strip(), self.responsable.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        self.ruta_actual = ruta
        self._abrir(ruta)
        self.consultar()

    def confirmar(self) -> None:
        try:
            folios = int(self.total.get())
            self.servicio.confirmar_foliacion(self.codigo.get().strip(), folios, self.responsable.get(), self.explicacion.get("1.0", "end").strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        mensajes.exito("La foliación quedó confirmada.")
        self.consultar()

    def generar_cargo(self) -> None:
        try:
            ruta = self.servicio.generar_cargo(self.codigo.get().strip())
        except (ValueError, OSError) as error:
            mensajes.error(str(error)); return
        self.ruta_actual = ruta
        self._abrir(ruta)
        self.consultar()

    def abrir_cargo(self) -> None:
        ruta = self._buscar_cargo()
        if ruta:
            self._abrir(ruta)

    def imprimir_cargo(self) -> None:
        ruta = self._buscar_cargo()
        if not ruta:
            return
        try:
            os.startfile(str(ruta), "print")
        except (AttributeError, OSError) as error:
            mensajes.error(f"No se pudo enviar el cargo a imprimir: {error}")

    def _buscar_cargo(self):
        registro = self.servicio.buscar(self.codigo.get().strip())
        ruta = self._ruta(registro.get("cargo", {}).get("ruta", "")) if registro else None
        if not ruta or not ruta.is_file():
            mensajes.error("Este expediente todavía no tiene un cargo PDF generado.")
            return None
        return ruta

    def _ruta(self, ruta: str):
        return self.servicio.directorio_datos.parent / ruta

    @staticmethod
    def _abrir(ruta) -> None:
        webbrowser.open(ruta.resolve().as_uri())
