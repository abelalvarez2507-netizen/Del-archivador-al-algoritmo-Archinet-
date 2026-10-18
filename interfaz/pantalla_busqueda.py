import tkinter as tk
from tkinter import ttk
from pathlib import Path

from interfaz import desplazamiento
from servicios.servicio_expedientes import ServicioExpedientes


class PantallaBusqueda(ttk.Frame):
    def __init__(self, parent: tk.Widget, servicio: ServicioExpedientes) -> None:
        super().__init__(parent)
        self.servicio = servicio
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=26)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Buscar expediente", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Consulta un registro mediante su código de expediente.", style="Hint.TLabel").pack(anchor="w", pady=(4, 20))
        barra = ttk.Frame(tarjeta, style="Card.TFrame")
        barra.pack(fill="x")
        self.codigo = tk.StringVar()
        ttk.Entry(barra, textvariable=self.codigo).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(barra, text="Buscar", style="Accent.TButton", command=self.buscar).pack(side="left")
        self.resultado = ttk.Label(tarjeta, text="", style="Result.TLabel", justify="left")
        self.resultado.pack(anchor="w", pady=24)

    def buscar(self) -> None:
        clave = self.codigo.get().strip()
        expediente = self.servicio.buscar(clave)
        expedientes = [expediente] if expediente is not None else []
        if not expedientes:
            self.resultado.configure(text="No se encontró un expediente con ese código.")
            return
        etiquetas = {
            "codigo": "Código de expediente", "codigo_documento": "Código de documento", "nombre_completo": "Nombre completo",
            "tipo_documento_identidad": "Tipo de identidad", "numero_documento": "N.º de documento",
            "tipo_documento_presentado": "Tipo de documento presentado", "tipo_documento_otro": "Detalle del documento", "asunto": "Asunto",
            "fecha_recepcion": "Fecha de recepción", "hora_recepcion": "Hora de recepción", "archivos_adjuntos": "Archivos adjuntos",
            "estado": "Estado actual",
        }
        bloques = []
        for registro in expedientes:
            valores = []
            for clave, valor in registro.items():
                if valor and clave in etiquetas:
                    texto = ", ".join(Path(archivo).name for archivo in valor) if clave == "archivos_adjuntos" else valor
                    valores.append(f"{etiquetas[clave]}:  {texto}")
            cotejo = registro.get("cotejo", {})
            foliacion = registro.get("foliacion", {})
            cargo = registro.get("cargo", {})
            clasificacion = registro.get("clasificacion", {})
            valores.extend((
                f"Cotejo: {cotejo.get('estado', 'Pendiente')} | modalidad {cotejo.get('modalidad', '')} | folios {cotejo.get('folios_verificados', 0)} | anexos {cotejo.get('cantidad_anexos', 0)}",
                f"Responsable de recepción: {cotejo.get('responsable', '')}",
                f"Observaciones: {cotejo.get('observaciones') or 'Ninguna'}",
                f"Foliación: {foliacion.get('estado', 'Pendiente')} | rango {foliacion.get('rango', '')} | responsable {foliacion.get('responsable', '')}",
                f"Cargo de recepción: {'Emitido' if cargo.get('emitido') else 'Pendiente'}",
                f"Clasificación: {clasificacion.get('estado', 'Pendiente')} | unidad {clasificacion.get('unidad', '')} | trámite {clasificacion.get('tramite', '')} | categoría {clasificacion.get('categoria', '')} | prioridad {clasificacion.get('prioridad', '')}",
            ))
            for movimiento in registro.get("derivaciones", []):
                valores.append(f"Derivación {movimiento.get('fecha', '')} {movimiento.get('hora', '')}: {movimiento.get('unidad', '')} | {movimiento.get('estado', '')} | recibe {movimiento.get('receptor', '')}")
                if movimiento.get("nota_transferencia"):
                    valores.append(movimiento["nota_transferencia"])
            for evento in registro.get("historial", []):
                valores.append(f"Historial {evento.get('fecha', '')} {evento.get('hora', '')}: {evento.get('accion', '')} — {evento.get('responsable', '')} — {evento.get('detalle', '')}")
            bloques.append("\n".join(valores))
        self.resultado.configure(text="\n\n".join(bloques))
