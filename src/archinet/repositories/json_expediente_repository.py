"""Repositorio JSON con listas paralelas y persistencia en disco."""

import json
from pathlib import Path
from typing import Sequence

from src.archinet.models.expediente import Expediente
from src.archinet.repositories.repositorio_base import RepositorioBase


class RepositorioJSONExpedientes(RepositorioBase):
    """Guarda los expedientes en JSON y organiza cada campo en una lista paralela.

    Hereda el contrato definido por RepositorioBase. Todas las listas mantienen
    el mismo índice para representar los datos de un expediente.
    """

    def __init__(self, ruta_archivo: str | Path) -> None:
        self.ruta_archivo = Path(ruta_archivo)
        self.codigos: list[str] = []
        self.ciudadanos: list[str] = []
        self.tipos_doc_identidad: list[str] = []
        self.numeros_doc_identidad: list[str] = []
        self.tipos_documento: list[str] = []
        self.asuntos: list[str] = []
        self.fechas_recepcion: list[str] = []
        self._cargar()

    def _cargar(self) -> None:
        """Carga el archivo al iniciar; crea un archivo vacío si no existe."""
        if not self.ruta_archivo.exists():
            self.guardar()
            return

        try:
            with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"El archivo {self.ruta_archivo.name} contiene JSON inválido. "
                "Conserva una copia y revisa su contenido antes de continuar."
            ) from error
        except OSError as error:
            raise ValueError(f"No se pudo leer el archivo de datos: {error}") from error

        if not isinstance(registros, list):
            raise ValueError("El archivo de datos debe contener una lista de expedientes.")

        codigos_vistos: set[str] = set()
        for registro in registros:
            if not isinstance(registro, dict):
                raise ValueError("El archivo de datos contiene un registro con formato incorrecto.")
            expediente = Expediente.desde_diccionario(registro)
            clave = expediente.codigo.strip().casefold()
            if clave in codigos_vistos:
                raise ValueError(f"El archivo de datos contiene el código duplicado {expediente.codigo}.")
            codigos_vistos.add(clave)
            self._agregar_a_listas(expediente)

    def _agregar_a_listas(self, expediente: Expediente) -> None:
        """Agrega todos los campos en la misma posición de sus listas."""
        self.codigos.append(expediente.codigo)
        self.ciudadanos.append(expediente.ciudadano)
        self.tipos_doc_identidad.append(expediente.tipo_doc_identidad)
        self.numeros_doc_identidad.append(expediente.numero_doc_identidad)
        self.tipos_documento.append(expediente.tipo_documento)
        self.asuntos.append(expediente.asunto)
        self.fechas_recepcion.append(expediente.fecha_recepcion)

    def _quitar_ultimo_de_listas(self) -> None:
        """Revierte una inserción si ocurre un error al guardar."""
        for lista in (
            self.codigos,
            self.ciudadanos,
            self.tipos_doc_identidad,
            self.numeros_doc_identidad,
            self.tipos_documento,
            self.asuntos,
            self.fechas_recepcion,
        ):
            if lista:
                lista.pop()

    def registrar(self, expediente: Expediente) -> None:
        """Registra un expediente y persiste el resultado de forma inmediata."""
        if any(codigo.casefold() == expediente.codigo.casefold() for codigo in self.codigos):
            raise ValueError("Ya existe un expediente con ese código.")
        self._agregar_a_listas(expediente)
        try:
            self.guardar()
        except (OSError, TypeError, ValueError):
            self._quitar_ultimo_de_listas()
            raise

    def listar(self) -> Sequence[Expediente]:
        """Reconstruye los expedientes respetando los índices de las listas paralelas."""
        return [
            Expediente(
                codigo=self.codigos[i],
                ciudadano=self.ciudadanos[i],
                tipo_doc_identidad=self.tipos_doc_identidad[i],
                numero_doc_identidad=self.numeros_doc_identidad[i],
                tipo_documento=self.tipos_documento[i],
                asunto=self.asuntos[i],
                fecha_recepcion=self.fechas_recepcion[i],
            )
            for i in range(len(self.codigos))
        ]

    def guardar(self) -> None:
        """Escribe los datos en UTF-8 usando reemplazo atómico del archivo."""
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        datos = [expediente.a_diccionario() for expediente in self.listar()]
        archivo_temporal = self.ruta_archivo.with_suffix(self.ruta_archivo.suffix + ".tmp")
        try:
            with archivo_temporal.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
                archivo.write("\n")
            archivo_temporal.replace(self.ruta_archivo)
        except OSError:
            try:
                archivo_temporal.unlink(missing_ok=True)
            except OSError:
                pass
            raise

    def cantidad(self) -> int:
        """Devuelve el total de expedientes cargados."""
        return len(self.codigos)
