from servicios.operaciones_listas import buscar_por_codigo, ordenar_por_codigo


def test_busqueda_y_ordenamiento():
    registros = [{"codigo": "B-2"}, {"codigo": "A-1"}]
    assert buscar_por_codigo(registros, "a-1") == registros[1]
    assert [e["codigo"] for e in ordenar_por_codigo(registros)] == ["A-1", "B-2"]
