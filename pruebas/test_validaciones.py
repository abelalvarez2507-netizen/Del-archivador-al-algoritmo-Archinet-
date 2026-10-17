from datetime import date, timedelta

import pytest

from servicios.validaciones import validar


def datos_validos():
    return {
        "nombre_completo": "María Pérez",
        "tipo_documento_identidad": "DNI",
        "numero_documento": "12345678",
        "tipo_documento_presentado": "Solicitud",
        "tipo_documento_otro": "",
        "asunto": "Consulta",
        "fecha_recepcion": date.today().strftime("%d/%m/%Y"),
        "hora_recepcion": "10:30:00",
    }


def test_acepta_datos_validos():
    validar(datos_validos())


@pytest.mark.parametrize(("tipo", "numero"), [
    ("DNI", "1234567"),
    ("DNI", "1234567A"),
    ("Carné de extranjería", "12345678"),
    ("Pasaporte", "ABC12"),
    ("Pasaporte", "ABC1234567"),
])
def test_rechaza_numeros_de_identidad_invalidos(tipo, numero):
    datos = datos_validos()
    datos["tipo_documento_identidad"] = tipo
    datos["numero_documento"] = numero
    with pytest.raises(ValueError):
        validar(datos)


def test_rechaza_fecha_que_no_es_hoy():
    datos = datos_validos()
    datos["fecha_recepcion"] = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    with pytest.raises(ValueError, match="fecha actual"):
        validar(datos)


def test_rechaza_fecha_futura():
    datos = datos_validos()
    datos["fecha_recepcion"] = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    with pytest.raises(ValueError, match="fecha actual"):
        validar(datos)


def test_rechaza_formato_fecha_distinto():
    datos = datos_validos()
    datos["fecha_recepcion"] = date.today().strftime("%Y-%m-%d")
    with pytest.raises(ValueError, match="DD/MM/AAAA"):
        validar(datos)


def test_exige_detalle_para_otro():
    datos = datos_validos()
    datos["tipo_documento_presentado"] = "Otro"
    with pytest.raises(ValueError, match="Especifica"):
        validar(datos)
