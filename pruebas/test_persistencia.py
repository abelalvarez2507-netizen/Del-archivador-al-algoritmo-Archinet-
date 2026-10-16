"""Pruebas de guardado y recuperación del archivo CSV."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from persistencia import cargar_expedientes, guardar_expedientes


class PruebasPersistencia(unittest.TestCase):
    def test_cargar_archivo_inexistente_devuelve_lista_vacia(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "no_existe.csv"
            self.assertEqual(cargar_expedientes(ruta), [])

    def test_guardar_y_cargar_conserva_datos_y_acentos(self):
        registros = [{
            "codigo": "EXP-001",
            "nombre": "María Pérez",
            "tipo_doc_identidad": "DNI",
            "numero_doc_identidad": "00000000",
            "tipo_documento": "Solicitud",
            "asunto": "Atención al ciudadano",
            "fecha_recepcion": "2026-10-16",
        }]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos" / "expedientes.csv"
            guardar_expedientes(ruta, registros)
            recuperados = cargar_expedientes(ruta)
        self.assertEqual(recuperados, registros)

    def test_guardar_lista_vacia_crea_archivo_con_encabezados(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "expedientes.csv"
            guardar_expedientes(ruta, [])
            self.assertTrue(ruta.exists())
            self.assertEqual(cargar_expedientes(ruta), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
