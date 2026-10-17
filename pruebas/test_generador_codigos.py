from servicios.generador_codigos import generar_codigos


def test_codigos_secuenciales_por_tipo():
    expedientes = [
        {"codigo": "EXP001", "codigo_documento": "BOG001"},
        {"codigo": "EXP002", "codigo_documento": "BEN001"},
    ]

    assert generar_codigos(expedientes, "Carta") == ("EXP003", "BOG002")
    assert generar_codigos(expedientes, "Formulario") == ("EXP003", "ARD001")


def test_otro_usa_tres_letras_sin_tilde():
    assert generar_codigos([], "Otro", "Memorándum") == ("EXP001", "MEM001")

