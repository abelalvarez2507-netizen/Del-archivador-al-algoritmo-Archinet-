import unittest

from src.archinet.validators.expediente_validator import validar_datos_expediente
from src.archinet.validators.fecha_validator import validar_fecha_recepcion


class PruebasValidadores(unittest.TestCase):
    def setUp(self):
        self.datos = {
            "codigo": " exp-001 ",
            "ciudadano": "María García",
            "tipo_doc_identidad": "DNI",
            "numero_doc_identidad": "12345678",
            "tipo_documento": "Solicitud",
            "asunto": "Solicitud de constancia",
            "fecha_recepcion": "16/10/2026",
        }

    def test_normaliza_codigo_a_mayusculas(self):
        resultado = validar_datos_expediente(self.datos, [])
        self.assertEqual(resultado["codigo"], "EXP-001")

    def test_rechaza_un_campo_vacio(self):
        datos = dict(self.datos, asunto="   ")
        with self.assertRaisesRegex(ValueError, "asunto del trámite"):
            validar_datos_expediente(datos, [])

    def test_rechaza_codigo_duplicado_sin_distinguir_mayusculas(self):
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            validar_datos_expediente(self.datos, ["Exp-001"])

    def test_rechaza_fecha_que_no_existe(self):
        with self.assertRaisesRegex(ValueError, "no existe en el calendario"):
            validar_fecha_recepcion("31/02/2026")

    def test_rechaza_formato_de_fecha_incorrecto(self):
        with self.assertRaisesRegex(ValueError, "formato DD/MM/AAAA"):
            validar_fecha_recepcion("2026-10-16")

    def test_rechaza_tipo_de_documento_no_permitido(self):
        datos = dict(self.datos, tipo_documento="Documento inventado")
        with self.assertRaisesRegex(ValueError, "tipo de documento presentado válido"):
            validar_datos_expediente(datos, [])


if __name__ == "__main__":
    unittest.main()
