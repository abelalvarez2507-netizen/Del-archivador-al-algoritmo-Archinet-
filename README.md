# ArchiNet

## Sistema de gestión de expedientes

ArchiNet es una aplicación de escritorio académica desarrollada en Python para registrar, buscar y consultar expedientes. Utiliza Tkinter para la interfaz gráfica y archivos JSON para guardar la información. Es un proyecto independiente.

## 1. Funcionalidades

- Registro de expedientes con código, nombre completo, tipo y número de documento de identidad, documento presentado, asunto y fecha de recepción.
- Código de expediente asignado automáticamente: `EXP001`, `EXP002` y siguientes.
- Códigos de documento por bloque, con numeración independiente: Carta (`BOG001`), Solicitud (`BEN001`) y Formulario (`ARD001`). Para «Otro», se toman las primeras tres letras del tipo especificado y se agrega el siguiente número.
- Código de paciente automático (`PAC001`, `PAC002`...) y reutilizable: los expedientes con el mismo tipo y número de identidad comparten el mismo código.
- Validación de DNI de 8 dígitos, carné de extranjería de 9 dígitos y pasaporte alfanumérico de 6 a 9 caracteres.
- Fecha y hora de recepción asignadas automáticamente al guardar, con formatos `DD/MM/AAAA` y `HH:MM:SS`.
- Validación de campos obligatorios, tipos permitidos y fecha actual.
- Búsqueda de expedientes por código de expediente o de paciente.
- Consulta de expedientes en una lista ordenada por código.
- Almacenamiento local en JSON con codificación UTF-8 para conservar tildes y otros caracteres.
- Interfaz gráfica organizada en las secciones Registro, Búsqueda y Listado.

Los tipos de identidad disponibles son DNI, carné de extranjería y pasaporte. La fecha y la hora se registran automáticamente al guardar; no se pueden editar ni programar fechas pasadas o futuras. Para «Otro», el código se forma con las primeras tres letras del tipo especificado, sin contar tildes, más una numeración de tres o más dígitos.

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
│   ├── generador_codigos.py
│   ├── servicio_expedientes.py
│   └── repositorio_json.py
├── pruebas/
│   ├── test_generador_codigos.py
│   ├── test_validaciones.py
│   └── test_servicio_expedientes.py
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

## 6. Pruebas

Para ejecutar las pruebas automatizadas, instala `pytest` en el entorno de desarrollo y ejecuta:

```powershell
python -m pip install pytest
python -m pytest pruebas/
```
