# ArchiNet - versión 0.1

Aplicación inicial en Python para el registro de expedientes.

## Qué incluye esta etapa

- Ventana de escritorio construida con Tkinter.
- Formulario con los campos básicos del expediente.
- Validación de campos obligatorios.
- Rechazo de códigos duplicados sin distinguir mayúsculas y minúsculas.
- Organización inicial mediante listas paralelas.
- Pruebas automáticas para el registro, los campos vacíos y los códigos repetidos.

## Qué todavía no incluye

Los registros se conservan solo en memoria mientras la aplicación está abierta. Si se cierra el programa, se pierden. La persistencia en JSON, la búsqueda por código, el ordenamiento y la validación de fechas se añadirán de forma gradual en próximos avances. No se debe presentar esta etapa como el prototipo completo.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, normalmente incluido en la instalación estándar de Python para Windows.
- No requiere paquetes externos.

## Ejecutar en Windows

1. Descomprime la carpeta.
2. Abre una terminal dentro de la carpeta `ArchiNet_v0.1`.
3. Ejecuta:

   ```powershell
   python main.py
   ```

## Ejecutar las pruebas

Desde la misma carpeta, ejecuta:

```powershell
python -m unittest discover -s tests -v
```

## Uso inicial de Git

Cuando se cree el repositorio del equipo en GitHub, abre una terminal en esta carpeta y sigue las instrucciones de configuración de Git de tu equipo. Los commits deben registrar avances reales; no se debe crear un historial ficticio.

Una vez configurados el nombre y el correo en Git, los primeros comandos serán:

```powershell
git init
git add .
git commit -m "Crear estructura inicial de ArchiNet y registro básico"
```

Después se conectará el repositorio local con la URL real del repositorio creado por el equipo.
