import tempfile
import unittest
from pathlib import Path

from src.archinet.repositories.json_expediente_repository import RepositorioJSONExpedientes
from src.archinet.services.expediente_service import ExpedienteService


class PruebasServicio(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.repo = RepositorioJSONExpedientes(Path(self.temporal.name) / "expedientes.json")
        self.servicio = ExpedienteService(self.repo)

    def tearDown(self):
        self.temporal.cleanup()

    def test_registra_un_expediente_valido(self):
        resultado = self.servicio.registrar({
            "codigo": "exp-010",
            "ciudadano": "Ana Torres",
            "tipo_doc_identidad": "DNI",
            "numero_doc_identidad": "98765432",
            "tipo_documento": "Oficio",
            "asunto": "Actualización de datos",
            "fecha_recepcion": "01/10/2026",
        })
        self.assertEqual(resultado.codigo, "EXP-010")
        self.assertEqual(self.servicio.cantidad(), 1)

    def test_no_registra_si_la_fecha_es_invalida(self):
        with self.assertRaises(ValueError):
            self.servicio.registrar({
                "codigo": "EXP-011",
                "ciudadano": "Ana Torres",
                "tipo_doc_identidad": "DNI",
                "numero_doc_identidad": "98765432",
                "tipo_documento": "Oficio",
                "asunto": "Actualización de datos",
                "fecha_recepcion": "31/02/2026",
            })
        self.assertEqual(self.servicio.cantidad(), 0)


if __name__ == "__main__":
    unittest.main()
