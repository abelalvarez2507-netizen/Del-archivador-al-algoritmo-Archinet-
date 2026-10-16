# ArchiNet — prototipo de mesa de partes digital

Aplicación de escritorio académica en Python para registrar, validar, buscar, ordenar y almacenar expedientes.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, que normalmente se incluye con las instalaciones estándar de Python para Windows.
- No requiere paquetes externos.

## Ejecutar en Windows con Visual Studio Code

1. Descomprime o abre la carpeta `ArchiNet` en Visual Studio Code.
2. Abre una terminal en esa carpeta.
3. Ejecuta:

   ```powershell
   py main.py
   ```

   Si el comando `py` no está disponible, prueba `python main.py`.

4. Completa los campos del formulario. La fecha se ingresa en formato `AAAA-MM-DD`, por ejemplo `2026-10-16`.
5. El botón **Registrar** valida la información y guarda el registro en `datos/expedientes.csv`.

## Ejecutar las pruebas automatizadas

Desde la carpeta `ArchiNet`, ejecuta:

```powershell
py -m unittest discover -s pruebas -v
```

Las pruebas comprueban la validación de campos, la normalización del código, la detección de duplicados, la fecha, la búsqueda y el ordenamiento. No sustituyen las pruebas manuales de la interfaz.

## Organización del proyecto

- `main.py`: inicia la aplicación y conecta los módulos.
- `interfaz.py`: ventanas, formulario, botones y tabla con Tkinter.
- `expedientes.py`: validación, búsqueda lineal y ordenamiento por selección.
- `persistencia.py`: lectura y escritura de CSV.
- `pruebas/test_expedientes.py`: pruebas automatizadas de la lógica.
- `datos/`: carpeta destinada al archivo de registros.
- `documentacion/`: documentos de apoyo del proyecto.

## Decisiones y limitaciones actuales

- Los registros de prueba deben ser ficticios; no ingreses datos personales reales.
- Los códigos se comparan sin distinguir mayúsculas y minúsculas.
- La ordenación usa el orden lexicográfico del código.
- La fecha debe ser una fecha válida con formato `AAAA-MM-DD`.
- El CSV se guarda localmente. Esta versión no incluye usuarios, permisos, copias de seguridad automáticas ni una base de datos multiusuario.
- Este prototipo académico no reemplaza un sistema institucional completo.

## Git: commits progresivos sugeridos

Ejecuta cada bloque cuando el avance correspondiente esté listo; no es necesario crear todos los commits de una sola vez.

```powershell
git init
git add README.md main.py interfaz.py expedientes.py persistencia.py pruebas
git commit -m "Crea estructura inicial y lógica de expedientes"
```

Después de revisar y ejecutar la interfaz:

```powershell
git add main.py interfaz.py expedientes.py persistencia.py pruebas README.md
git commit -m "Integra interfaz gráfica y persistencia CSV"
```

Crea el repositorio remoto en GitHub y sigue las instrucciones que GitHub muestre para conectar el repositorio local. No se ha creado ni publicado un repositorio remoto desde este paquete.
