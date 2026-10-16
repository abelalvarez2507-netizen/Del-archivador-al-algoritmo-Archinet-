"""Pruebas automatizadas de la lógica de ArchiNet."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from expedientes import buscar_por_codigo, ordenar_por_codigo, validar_expediente


def expediente(codigo="EXP-002", **cambios):
    datos = {
        "codigo": codigo,
        "nombre": "Ciudadano de Prueba",
        "tipo_doc_identidad": "DNI",
        "numero_doc_identidad": "00000000",
        "tipo_documento": "Solicitud",
        "asunto": "Consulta de prueba",
        "fecha_recepcion": "2026-10-16",
    }
    datos.update(cambios)
    return datos


class PruebasLogicaArchiNet(unittest.TestCase):
    def test_valida_y_normaliza_codigo(self):
        resultado = validar_expediente(expediente(codigo=" exp-009 "), [])
        self.assertEqual(resultado["codigo"], "EXP-009")
        self.assertEqual(resultado["nombre"], "Ciudadano de Prueba")

    def test_rechaza_campo_obligatorio_vacio(self):
        datos = expediente(asunto="   ")
        with self.assertRaisesRegex(ValueError, "asunto"):
            validar_expediente(datos, [])

    def test_rechaza_codigo_duplicado_sin_distinguir_mayusculas(self):
        existentes = [expediente(codigo="EXP-002")]
        with self.assertRaisesRegex(ValueError, "ya está registrado"):
            validar_expediente(expediente(codigo="exp-002"), existentes)

    def test_rechaza_fecha_invalida(self):
        with self.assertRaisesRegex(ValueError, "fecha debe ser válida"):
            validar_expediente(expediente(fecha_recepcion="2026-02-31"), [])

    def test_busqueda_encuentra_y_no_encuentra(self):
        registros = [expediente(codigo="EXP-002"), expediente(codigo="EXP-001")]
        self.assertEqual(buscar_por_codigo(registros, "exp-001")["codigo"], "EXP-001")
        self.assertIsNone(buscar_por_codigo(registros, "EXP-999"))

    def test_ordenamiento_por_seleccion_conserva_datos_asociados(self):
        registros = [
            expediente(codigo="EXP-003", nombre="Tercero"),
            expediente(codigo="EXP-001", nombre="Primero"),
            expediente(codigo="EXP-002", nombre="Segundo"),
        ]
        resultado = ordenar_por_codigo(registros)
        self.assertEqual([r["codigo"] for r in resultado], ["EXP-001", "EXP-002", "EXP-003"])
        self.assertEqual(resultado[0]["nombre"], "Primero")
        self.assertEqual(registros[0]["codigo"], "EXP-003", "La función no debe modificar la lista original.")

    def test_ordenamiento_lista_vacia(self):
        self.assertEqual(ordenar_por_codigo([]), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
