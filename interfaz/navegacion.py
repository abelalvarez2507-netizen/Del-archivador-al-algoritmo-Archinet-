import tkinter as tk
from tkinter import ttk

from interfaz import estilos
from interfaz.pantalla_busqueda import PantallaBusqueda
from interfaz.pantalla_listado import PantallaListado
from interfaz.pantalla_registro import PantallaRegistro
from servicios.servicio_expedientes import ServicioExpedientes


def iniciar() -> None:
    root = tk.Tk()
    root.title("ArchiNet | Gestión de expedientes")
    root.geometry("1020x700")
    root.minsize(820, 600)
    root.configure(bg=estilos.FONDO)
    configurar_estilos(root)
    servicio = ServicioExpedientes()
    principal = ttk.Frame(root, style="App.TFrame")
    principal.pack(fill="both", expand=True)
    encabezado = ttk.Frame(principal, style="Header.TFrame", padding=(30, 22))
    encabezado.pack(fill="x")
    ttk.Label(encabezado, text="ArchiNet", style="Brand.TLabel").pack(anchor="w")
    ttk.Label(encabezado, text="Gestión y consulta de expedientes", style="HeaderHint.TLabel").pack(anchor="w", pady=(3, 0))
    barra = ttk.Frame(principal, style="Nav.TFrame", padding=(24, 10))
    barra.pack(fill="x")
    zona = ttk.Frame(principal, style="App.TFrame")
    zona.pack(fill="both", expand=True)
    pantallas = {
        "Registro": PantallaRegistro(zona, servicio),
        "Búsqueda": PantallaBusqueda(zona, servicio),
        "Listado": PantallaListado(zona, servicio),
    }
    for pantalla in pantallas.values():
        pantalla.place(relx=0, rely=0, relwidth=1, relheight=1)
    def mostrar(nombre: str) -> None:
        pantallas[nombre].tkraise()
        if nombre == "Listado":
            pantallas[nombre].actualizar()
    for nombre in pantallas:
        ttk.Button(barra, text=nombre, command=lambda n=nombre: mostrar(n)).pack(side="left", padx=(0, 8))
    mostrar("Registro")
    root.mainloop()


def configurar_estilos(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("App.TFrame", background=estilos.FONDO)
    style.configure("Header.TFrame", background=estilos.AZUL)
    style.configure("Brand.TLabel", background=estilos.AZUL, foreground="white", font=("Segoe UI", 21, "bold"))
    style.configure("HeaderHint.TLabel", background=estilos.AZUL, foreground="#dce8f4", font=("Segoe UI", 10))
    style.configure("Nav.TFrame", background="#e8eef5")
    style.configure("Card.TFrame", background=estilos.BLANCO)
    style.configure("Title.TLabel", background=estilos.BLANCO, foreground=estilos.TEXTO, font=("Segoe UI", 17, "bold"))
    style.configure("Hint.TLabel", background=estilos.BLANCO, foreground=estilos.SUAVE, font=("Segoe UI", 10))
    style.configure("Result.TLabel", background=estilos.BLANCO, foreground=estilos.TEXTO, font=("Segoe UI", 11), lineheight=24)
    style.configure("TLabel", font=("Segoe UI", 10), foreground=estilos.TEXTO)
    style.configure("TButton", font=("Segoe UI", 10), padding=(13, 8))
    style.configure("Accent.TButton", background=estilos.AZUL, foreground="white")
    style.map("Accent.TButton", background=[("active", "#23649f")])
    style.configure("TEntry", padding=8)
    style.configure("TCombobox", padding=7)
    style.configure("Treeview", rowheight=32, font=("Segoe UI", 9), background="white", fieldbackground="white")
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e8eef5", padding=8)
