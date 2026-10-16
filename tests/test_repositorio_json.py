import json
import tempfile
import unittest
from pathlib import Path

from src.archinet.models.expediente import Expediente
from src.archinet.repositories.json_expediente_repository import RepositorioJSONExpedientes
from src.archinet.repositories.repositorio_base import RepositorioBase
from src.archinet.services.expediente_service import ExpedienteService


class PruebasRepositorioJSON(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.ruta = Path(self.temporal.name) / "expedientes.json"
        self.repo = RepositorioJSONExpedientes(self.ruta)
        self.servicio = ExpedienteService(self.repo)
        self.datos = {
            "codigo": "EXP-001",
            "ciudadano": "María García",
            "tipo_doc_identidad": "DNI",
            "numero_doc_identidad": "12345678",
            "tipo_documento": "Solicitud",
            "asunto": "Solicitud de constancia",
            "fecha_recepcion": "16/10/2026",
        }

    def tearDown(self):
        self.temporal.cleanup()

    def test_repositorio_concreto_hereda_el_contrato_base(self):
        self.assertIsInstance(self.repo, RepositorioBase)

    def test_crea_archivo_json_si_no_existe(self):
        self.assertTrue(self.ruta.exists())
        self.assertEqual(json.loads(self.ruta.read_text(encoding="utf-8")), [])

    def test_registro_se_guarda_y_puede_recuperarse(self):
        self.servicio.registrar(self.datos)
        self.assertEqual(self.repo.cantidad(), 1)
        nuevo_repo = RepositorioJSONExpedientes(self.ruta)
        self.assertEqual(nuevo_repo.cantidad(), 1)
        self.assertEqual(nuevo_repo.listar()[0].ciudadano, "María García")
        self.assertEqual(nuevo_repo.listar()[0].codigo, "EXP-001")

    def test_codigo_duplicado_tambien_se_rechaza_despues_de_reabrir(self):
        self.servicio.registrar(self.datos)
        nuevo_repo = RepositorioJSONExpedientes(self.ruta)
        nuevo_servicio = ExpedienteService(nuevo_repo)
        datos = dict(self.datos, codigo="exp-001")
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            nuevo_servicio.registrar(datos)
        self.assertEqual(nuevo_repo.cantidad(), 1)

    def test_datos_con_acentos_se_guardan_en_utf8(self):
        self.servicio.registrar(self.datos)
        texto = self.ruta.read_text(encoding="utf-8")
        self.assertIn("María García", texto)

    def test_listas_paralelas_mantienen_igual_longitud(self):
        self.servicio.registrar(self.datos)
        self.servicio.registrar(dict(self.datos, codigo="EXP-002", ciudadano="José Ramos"))
        longitudes = {
            len(self.repo.codigos),
            len(self.repo.ciudadanos),
            len(self.repo.tipos_doc_identidad),
            len(self.repo.numeros_doc_identidad),
            len(self.repo.tipos_documento),
            len(self.repo.asuntos),
            len(self.repo.fechas_recepcion),
        }
        self.assertEqual(longitudes, {2})


if __name__ == "__main__":
    unittest.main()
