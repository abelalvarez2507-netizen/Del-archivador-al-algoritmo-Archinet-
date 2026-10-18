import tkinter as tk
from tkinter import ttk

from componentes import mensajes
from interfaz import desplazamiento
from servicios import configuracion


class PantallaConfiguracion(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.marco = desplazamiento.MarcoDesplazable(self)
        self.marco.pack(fill="both", expand=True)
        tarjeta = ttk.Frame(self.marco.interior, style="Card.TFrame", padding=24)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(tarjeta, text="Configuración", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text="Define la entidad, sus unidades orgánicas y sugerencias de destino.", style="Hint.TLabel").pack(anchor="w", pady=(4, 18))
        ttk.Label(tarjeta, text="Nombre de la entidad").pack(anchor="w", pady=(4, 5))
        self.entidad = tk.StringVar()
        ttk.Entry(tarjeta, textvariable=self.entidad).pack(fill="x")
        ttk.Label(tarjeta, text="Unidades orgánicas (una por línea)").pack(anchor="w", pady=(16, 5))
        self.unidades = tk.Text(tarjeta, height=8, wrap="word")
        self.unidades.pack(fill="x")
        ttk.Label(tarjeta, text="Sugerencias de destino (tipo de documento=unidad)").pack(anchor="w", pady=(16, 5))
        self.sugerencias = tk.Text(tarjeta, height=6, wrap="word")
        self.sugerencias.pack(fill="x")
        ttk.Button(tarjeta, text="Guardar configuración", style="Accent.TButton", command=self.guardar).pack(anchor="e", pady=(16, 0))
        self.cargar()

    def cargar(self) -> None:
        datos = configuracion.cargar()
        self.entidad.set(datos.get("nombre_entidad", ""))
        self.unidades.delete("1.0", "end")
        self.unidades.insert("1.0", "\n".join(datos.get("unidades", [])))
        self.sugerencias.delete("1.0", "end")
        self.sugerencias.insert("1.0", "\n".join(f"{tipo}={unidad}" for tipo, unidad in datos.get("sugerencias", {}).items()))

    def guardar(self) -> None:
        unidades = list(dict.fromkeys(linea.strip() for linea in self.unidades.get("1.0", "end").splitlines() if linea.strip()))
        sugerencias = {}
        try:
            for linea in self.sugerencias.get("1.0", "end").splitlines():
                linea = linea.strip()
                if not linea:
                    continue
                if "=" not in linea:
                    raise ValueError("Cada sugerencia debe tener el formato tipo=unidad.")
                tipo, unidad = (parte.strip() for parte in linea.split("=", 1))
                if not tipo or unidad not in unidades:
                    raise ValueError(f"La sugerencia '{linea}' debe apuntar a una unidad configurada.")
                sugerencias[tipo] = unidad
            configuracion.guardar({"nombre_entidad": self.entidad.get().strip(), "unidades": unidades, "sugerencias": sugerencias})
        except (ValueError, OSError) as error:
            mensajes.error(str(error))
            return
        mensajes.exito("La configuración quedó guardada.")
