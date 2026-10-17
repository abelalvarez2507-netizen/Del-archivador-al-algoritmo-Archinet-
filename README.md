# ArchiNet

Aplicación de escritorio sencilla para registrar, buscar y ordenar expedientes. El proyecto es independiente y guarda los registros localmente en `datos/expedientes.json`.

## Requisitos

- Python 3.10 o superior con Tkinter disponible.
- No requiere dependencias externas.

## Preparar y ejecutar

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import tkinter; print('Tkinter disponible')"
python main.py
```

También puede iniciarse con `python main.py` desde la carpeta del proyecto. En Linux, instala el paquete de Tkinter de la distribución si no viene incluido con Python.

## Funciones

- Registrar expedientes con código, nombre, documentos, asunto y fecha.
- Validar campos obligatorios, tipos permitidos, fecha ISO y códigos duplicados.
- Buscar por código y mostrar el listado ordenado por código.
- Guardar JSON en UTF-8, conservando tildes.

La fecha se escribe como `AAAA-MM-DD`. Los tipos de identidad son DNI, carné de extranjería y pasaporte; los documentos presentados pueden ser solicitud, carta, formulario u otro.

## Estructura

`interfaz/` contiene ventanas y estilos; `componentes/`, mensajes reutilizables; `modelos/`, la definición del expediente; `servicios/`, validación, operaciones, coordinación y JSON; `pruebas/`, pruebas de los módulos; `datos/`, almacenamiento local; `docs/`, diagramas y evidencias.

## Pruebas

Con pytest instalado en el entorno de desarrollo, ejecuta `python -m pytest pruebas/`.
