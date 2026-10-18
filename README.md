# ArchiNet

## Sistema de gestión de expedientes

ArchiNet es una aplicación de escritorio en Python y Tkinter. Guarda los registros en archivos JSON locales y organiza el recorrido de cada expediente desde la recepción hasta su derivación y seguimiento.

## Funciones

- Registro de remitente, identidad, documento, asunto y archivos adjuntos.
- Códigos automáticos consecutivos de expediente y de tipo documental: Carta (`BOG001`), Solicitud (`BEN001`), Formulario (`ARD001`) y prefijo de tres letras para «Otro».
- Validación de DNI, carné de extranjería y pasaporte.
- Fecha y hora automáticas al registrar.
- Cotejo de modalidad, folios, anexos, firma, legibilidad, integridad, responsable, observaciones y excepciones autorizadas.
- Guardado y recuperación de recepciones observadas.
- Ficha PDF y confirmación de foliación, con control de folios verificados.
- Cargo PDF de recepción, con opciones para abrir e imprimirlo.
- Clasificación por unidad orgánica, trámite, categoría y prioridad.
- Relación PDF de despacho por unidad.
- Derivaciones físicas o digitales, cargos internos y registro de entrega o devolución.
- Búsqueda, seguimiento, historial de movimientos, alertas y resumen de actividad.
- Configuración editable de la entidad, unidades y sugerencias de destino.
- Navegación persistente y desplazamiento vertical en todas las pantallas.

Las derivaciones digitales se guardan como movimientos locales. ArchiNet no realiza transferencias electrónicas.

## Archivos adjuntos y PDF

Se admiten DOC, DOCX, ODT, RTF, PDF, PNG, JPG, JPEG, TIF, TIFF, BMP, GIF y WEBP. Los archivos se copian dentro de `datos/adjuntos/`, separados por expediente. Las fichas, cargos y relaciones se guardan en subcarpetas de `datos/`.

## Instalación y ejecución

Se necesita Python 3.10 o posterior con Tkinter disponible. ArchiNet no requiere paquetes externos para funcionar.

```powershell
python -c "import tkinter; print('Tkinter disponible')"
python main.py
```

## Datos locales

- `datos/expedientes.json`: expedientes y su historial.
- `datos/borradores.json`: recepciones observadas pendientes.
- `datos/configuracion.json`: entidad, unidades y destinos sugeridos.
- `datos/adjuntos/`: archivos recibidos.
- `datos/cargos/`, `datos/foliacion/`, `datos/cargos_derivacion/` y `datos/relaciones_despacho/`: documentos PDF generados.

Estos datos permanecen en el equipo y pueden contener información personal.

## Pruebas

Las pruebas de desarrollo usan `pytest`:

```powershell
python -m pytest pruebas/
```

## Estructura

```text
ArchiNet/
├── componentes/
├── datos/
├── interfaz/
│   ├── pantalla_busqueda.py
│   ├── pantalla_clasificacion.py
│   ├── pantalla_configuracion.py
│   ├── pantalla_derivaciones.py
│   ├── pantalla_foliacion.py
│   ├── pantalla_historial.py
│   ├── pantalla_inicio.py
│   ├── pantalla_listado.py
│   ├── pantalla_registro.py
│   └── navegacion.py
├── modelos/
├── pruebas/
├── servicios/
├── main.py
└── README.md
```
