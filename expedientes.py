"""Funciones y estructuras iniciales para administrar expedientes de ArchiNet.

Esta primera etapa guarda los registros en memoria. El almacenamiento en JSON,
la búsqueda y el ordenamiento se incorporarán en avances posteriores.
"""


class RepositorioExpedientes:
    """Mantiene los datos en listas paralelas, una por cada campo del expediente."""

    def __init__(self):
        self.codigos = []
        self.ciudadanos = []
        self.tipos_doc_identidad = []
        self.numeros_doc_identidad = []
        self.tipos_documento = []
        self.asuntos = []
        self.fechas_recepcion = []

    def cantidad(self):
        """Devuelve la cantidad de expedientes registrados en esta sesión."""
        return len(self.codigos)

    def registrar(self, codigo, ciudadano, tipo_doc_identidad,
                  numero_doc_identidad, tipo_documento, asunto,
                  fecha_recepcion):
        """Registra un expediente con validaciones básicas.

        Raises:
            ValueError: si falta un campo obligatorio o el código ya existe.
        """
        campos = [
            codigo, ciudadano, tipo_doc_identidad, numero_doc_identidad,
            tipo_documento, asunto, fecha_recepcion
        ]
        campos = [str(campo).strip() for campo in campos]

        if any(not campo for campo in campos):
            raise ValueError("Completa todos los campos antes de registrar.")

        (codigo, ciudadano, tipo_doc_identidad, numero_doc_identidad,
         tipo_documento, asunto, fecha_recepcion) = campos

        if any(codigo_existente.casefold() == codigo.casefold()
               for codigo_existente in self.codigos):
            raise ValueError("Ya existe un expediente con ese código.")

        self.codigos.append(codigo)
        self.ciudadanos.append(ciudadano)
        self.tipos_doc_identidad.append(tipo_doc_identidad)
        self.numeros_doc_identidad.append(numero_doc_identidad)
        self.tipos_documento.append(tipo_documento)
        self.asuntos.append(asunto)
        self.fechas_recepcion.append(fecha_recepcion)

        return "Expediente registrado correctamente en esta sesión."
