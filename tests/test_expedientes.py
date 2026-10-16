import unittest

from expedientes import RepositorioExpedientes


class PruebasRepositorioExpedientes(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioExpedientes()
        self.registro = {
            "codigo": "EXP-001",
            "ciudadano": "María García",
            "tipo_doc_identidad": "DNI",
            "numero_doc_identidad": "12345678",
            "tipo_documento": "Solicitud",
            "asunto": "Solicitud de constancia",
            "fecha_recepcion": "16/10/2026",
        }

    def test_registro_correcto(self):
        mensaje = self.repo.registrar(**self.registro)
        self.assertIn("registrado correctamente", mensaje)
        self.assertEqual(self.repo.cantidad(), 1)
        self.assertEqual(self.repo.codigos[0], "EXP-001")
        self.assertEqual(self.repo.ciudadanos[0], "María García")

    def test_rechaza_campo_vacio(self):
        registro = dict(self.registro)
        registro["asunto"] = "   "
        with self.assertRaisesRegex(ValueError, "Completa todos los campos"):
            self.repo.registrar(**registro)
        self.assertEqual(self.repo.cantidad(), 0)

    def test_rechaza_codigo_duplicado_sin_distinguir_mayusculas(self):
        self.repo.registrar(**self.registro)
        registro = dict(self.registro)
        registro["codigo"] = "exp-001"
        with self.assertRaisesRegex(ValueError, "Ya existe un expediente"):
            self.repo.registrar(**registro)
        self.assertEqual(self.repo.cantidad(), 1)


if __name__ == "__main__":
    unittest.main()
