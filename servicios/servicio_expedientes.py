from modelos.expediente import Expediente
from servicios import generador_codigos, operaciones_listas, repositorio_json, validaciones


class ServicioExpedientes:
    def __init__(self) -> None:
        self.expedientes = repositorio_json.cargar()

    def registrar(self, datos: dict[str, str]) -> Expediente:
        datos_limpios = {k: v.strip() for k, v in datos.items()}
        validaciones.validar(datos_limpios)
        datos_limpios["codigo"], datos_limpios["codigo_documento"] = generador_codigos.generar_codigos(
            self.expedientes,
            datos_limpios["tipo_documento_presentado"],
            datos_limpios.get("tipo_documento_otro", ""),
        )
        expediente = Expediente(**datos_limpios)
        self.expedientes.append(expediente.a_dict())
        repositorio_json.guardar(self.expedientes)
        return expediente

    def codigos_siguientes(self, tipo_documento: str, otro: str = "") -> tuple[str, str]:
        return generador_codigos.generar_codigos(self.expedientes, tipo_documento, otro)

    def buscar(self, codigo: str) -> dict[str, str] | None:
        return operaciones_listas.buscar_por_codigo(self.expedientes, codigo)

    def listar_ordenados(self) -> list[dict[str, str]]:
        return operaciones_listas.ordenar_por_codigo(self.expedientes)
