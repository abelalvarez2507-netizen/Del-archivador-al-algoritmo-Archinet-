# ArchiNet

## Sistema de gestión de expedientes

ArchiNet es una aplicación de escritorio académica desarrollada en Python para registrar, buscar y consultar expedientes. Utiliza Tkinter para la interfaz gráfica y archivos JSON para guardar la información. Es un proyecto independiente.

## 1. Funcionalidades

- Registro de expedientes con código, nombre completo, tipo y número de documento de identidad, documento presentado, asunto y fecha de recepción.
- Validación de campos obligatorios, tipos de documento permitidos, fecha válida y códigos duplicados.
- Búsqueda de expedientes por código.
- Consulta de expedientes en una lista ordenada por código.
- Almacenamiento local en JSON con codificación UTF-8 para conservar tildes y otros caracteres.
- Interfaz gráfica organizada en las secciones Registro, Búsqueda y Listado.

La fecha de recepción se ingresa en formato `AAAA-MM-DD`. Los tipos de identidad disponibles son DNI, carné de extranjería y pasaporte. Los tipos de documento presentado son solicitud, carta, formulario y otro.

## 2. Arquitectura

```text
ArchiNet/
├── interfaz/
│   ├── pantalla_registro.py
│   ├── pantalla_busqueda.py
│   ├── pantalla_listado.py
│   ├── campos.py
│   ├── estilos.py
│   └── navegacion.py
├── componentes/
│   └── mensajes.py
├── modelos/
│   └── expediente.py
├── servicios/
│   ├── validaciones.py
│   ├── operaciones_listas.py
│   ├── servicio_expedientes.py
│   └── repositorio_json.py
├── datos/
│   └── expedientes.json
├── main.py
├── requirements.txt
└── README.md
```

La interfaz solicita las operaciones al servicio de expedientes. El servicio valida y coordina los datos con el repositorio JSON; la interfaz no escribe directamente en el archivo.

## 3. Instalación

Se recomienda Python 3.10 o posterior con Tkinter disponible. No se requieren dependencias externas para ejecutar la aplicación.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import tkinter; print('Tkinter disponible')"
```

En Linux, instala el paquete de Tkinter de la distribución si no está incluido con Python.

## 4. Ejecución

Desde la carpeta raíz del proyecto, ejecuta:

```powershell
python main.py
```

La ventana principal permite cambiar entre Registro, Búsqueda y Listado. Los datos se guardan en `datos/expedientes.json` al registrar un expediente.

## 5. Datos locales

El archivo `datos/expedientes.json` puede contener información personal y está excluido de Git mediante `.gitignore`. Mantén una copia de respaldo adecuada de los datos que necesites conservar.

ArchiNet es un prototipo académico. Sus funciones se ampliarán conforme avance el desarrollo.
