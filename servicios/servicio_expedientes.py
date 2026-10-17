from modelos.expediente import Expediente
from servicios import operaciones_listas, repositorio_json, validaciones


class ServicioExpedientes:
    def __init__(self) -> None:
        self.expedientes = repositorio_json.cargar()

    def registrar(self, datos: dict[str, str]) -> Expediente:
        datos_limpios = {k: v.strip() for k, v in datos.items()}
        validaciones.validar(datos_limpios, [e["codigo"] for e in self.expedientes])
        expediente = Expediente(**datos_limpios)
        self.expedientes.append(expediente.a_dict())
        repositorio_json.guardar(self.expedientes)
        return expediente

    def buscar(self, codigo: str) -> dict[str, str] | None:
        return operaciones_listas.buscar_por_codigo(self.expedientes, codigo)

    def listar_ordenados(self) -> list[dict[str, str]]:
        return operaciones_listas.ordenar_por_codigo(self.expedientes)
