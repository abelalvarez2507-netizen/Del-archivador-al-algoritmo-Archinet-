# ArchiNet

## Sistema de gestión de expedientes

ArchiNet es una aplicación de escritorio académica desarrollada en Python para registrar, buscar y consultar expedientes. Utiliza Tkinter para la interfaz gráfica y JSON para guardar la información.

## 1. Funcionalidades

- Registro de expedientes con código automático, datos de identidad, tipo de documento, asunto y recepción.
- Códigos independientes por bloque: Carta (`BOG001`), Solicitud (`BEN001`), Formulario (`ARD001`) y prefijo personalizado para «Otro».
- Validación de DNI de 8 dígitos, carné de extranjería de 9 dígitos y pasaporte alfanumérico de 6 a 9 caracteres.
- Fecha y hora de recepción automáticas, en formatos `DD/MM/AAAA` y `HH:MM:SS`.
- Adjuntar archivos Word, PDF e imágenes de documentos escaneados.
- Búsqueda por código de expediente y listado ordenado.
- Barra vertical a la derecha en cada pantalla, con desplazamiento desde la barra, rueda y touchpad.
- Almacenamiento JSON en UTF-8.

Los archivos adjuntos se copian a `datos/adjuntos/`, dentro de una carpeta para cada expediente. Se admiten DOC, DOCX, ODT, RTF, PDF, PNG, JPG, JPEG, TIF, TIFF, BMP, GIF y WEBP.

## 2. Arquitectura

```text
ArchiNet/
├── interfaz/
│   ├── pantalla_registro.py
│   ├── pantalla_busqueda.py
│   ├── pantalla_listado.py
│   ├── desplazamiento.py
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
│   ├── archivos_adjuntos.py
│   ├── servicio_expedientes.py
│   └── repositorio_json.py
├── pruebas/
├── datos/
│   ├── expedientes.json
│   └── adjuntos/
├── main.py
├── requirements.txt
└── README.md
```

La interfaz solicita las operaciones al servicio de expedientes. El servicio valida los datos, genera códigos y coordina el guardado JSON y la copia de archivos adjuntos.

## 3. Instalación

Se recomienda Python 3.10 o posterior con Tkinter disponible. No se requieren dependencias externas para ejecutar la aplicación.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import tkinter; print('Tkinter disponible')"
```

## 4. Ejecución

Desde la carpeta raíz del proyecto, ejecuta:

```powershell
python main.py
```

La fecha y la hora se asignan automáticamente al registrar. No se pueden editar ni seleccionar fechas pasadas o futuras.

## 5. Datos locales

`datos/expedientes.json` y `datos/adjuntos/` pueden contener información personal; están excluidos de Git mediante `.gitignore`.

## 6. Pruebas

Con `pytest` instalado en el entorno de desarrollo, ejecuta:

```powershell
python -m pytest pruebas/
```
