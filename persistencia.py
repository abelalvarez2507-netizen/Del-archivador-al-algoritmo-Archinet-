"""Lectura y escritura de expedientes en formato CSV."""

import csv
from pathlib import Path
from typing import Iterable

from expedientes import CAMPOS


class ErrorPersistencia(Exception):
    """Error controlado al leer o guardar el archivo de expedientes."""


def cargar_expedientes(ruta: str | Path) -> list[dict[str, str]]:
    """Carga el archivo CSV; si todavía no existe, devuelve una lista vacía."""
    archivo = Path(ruta)
    if not archivo.exists():
        return []

    try:
        with archivo.open("r", newline="", encoding="utf-8-sig") as entrada:
            lector = csv.DictReader(entrada)
            if lector.fieldnames is None:
                return []
            campos_archivo = set(lector.fieldnames)
            if not set(CAMPOS).issubset(campos_archivo):
                raise ErrorPersistencia(
                    "El archivo CSV no tiene las columnas requeridas por ArchiNet. "
                    "Conserva una copia del archivo y revisa su estructura."
                )

            registros = []
            for numero_fila, fila in enumerate(lector, start=2):
                if not fila or all(not str(valor or "").strip() for valor in fila.values()):
                    continue
                registro = {campo: str(fila.get(campo, "") or "").strip() for campo in CAMPOS}
                if not registro["codigo"]:
                    raise ErrorPersistencia(
                        f"El registro de la fila {numero_fila} no tiene código de expediente."
                    )
                registros.append(registro)
            return registros
    except ErrorPersistencia:
        raise
    except (OSError, csv.Error, UnicodeError) as exc:
        raise ErrorPersistencia(f"No se pudo leer el archivo de expedientes: {exc}") from exc


def guardar_expedientes(
    ruta: str | Path, expedientes: Iterable[dict[str, str]]
) -> None:
    """Guarda la colección completa en CSV y crea su carpeta si es necesario."""
    archivo = Path(ruta)
    try:
        archivo.parent.mkdir(parents=True, exist_ok=True)
        with archivo.open("w", newline="", encoding="utf-8-sig") as salida:
            escritor = csv.DictWriter(salida, fieldnames=CAMPOS, extrasaction="ignore")
            escritor.writeheader()
            for expediente in expedientes:
                escritor.writerow({campo: expediente.get(campo, "") for campo in CAMPOS})
    except (OSError, csv.Error, UnicodeError) as exc:
        raise ErrorPersistencia(f"No se pudieron guardar los expedientes: {exc}") from exc
