from servicios.validaciones import validar


def datos_validos():
    return {
        "codigo": "EXP-001", "nombre_completo": "María Pérez",
        "tipo_documento_identidad": "DNI", "numero_documento": "12345678",
        "tipo_documento_presentado": "Solicitud", "asunto": "Consulta",
        "fecha_recepcion": "2026-10-17",
    }


def test_datos_validos():
    validar(datos_validos(), [])


def test_codigo_duplicado():
    try:
        validar(datos_validos(), ["EXP-001"])
    except ValueError as error:
        assert "código" in str(error)
    else:
        raise AssertionError("Debió rechazar el código duplicado")
