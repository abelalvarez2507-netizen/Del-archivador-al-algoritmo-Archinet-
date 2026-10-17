from modelos.expediente import Expediente
from datetime import datetime
from servicios import generador_codigos, operaciones_listas, repositorio_json, validaciones


class ServicioExpedientes:
    def __init__(self) -> None:
        self.expedientes = repositorio_json.cargar()

    def registrar(self, datos: dict[str, str]) -> Expediente:
        datos_limpios = {k: v.strip() for k, v in datos.items()}
        ahora = datetime.now()
        datos_limpios["fecha_recepcion"] = ahora.strftime("%d/%m/%Y")
        datos_limpios["hora_recepcion"] = ahora.strftime("%H:%M:%S")
        datos_limpios["codigo_paciente"] = generador_codigos.codigo_paciente_para(
            self.expedientes,
            datos_limpios.get("tipo_documento_identidad", ""),
            datos_limpios.get("numero_documento", ""),
        )
        validaciones.validar(datos_limpios)
        datos_limpios["codigo"], datos_limpios["codigo_documento"] = generador_codigos.generar_codigos(
            self.expedientes,
            datos_limpios["tipo_documento_presentado"],
            datos_limpios.get("tipo_documento_otro", ""),
        )
        expediente = Expediente(**datos_limpios)
        expedientes_actualizados = [*self.expedientes, expediente.a_dict()]
        repositorio_json.guardar(expedientes_actualizados)
        self.expedientes = expedientes_actualizados
        return expediente

    def codigos_siguientes(self, tipo_documento: str, otro: str = "") -> tuple[str, str]:
        return generador_codigos.generar_codigos(self.expedientes, tipo_documento, otro)

    def buscar(self, codigo: str) -> dict[str, str] | None:
        return operaciones_listas.buscar_por_codigo(self.expedientes, codigo)

    def listar_ordenados(self) -> list[dict[str, str]]:
        return operaciones_listas.ordenar_por_codigo(self.expedientes)

    def codigo_paciente(self, tipo_identidad: str, numero: str) -> str:
        return generador_codigos.codigo_paciente_para(self.expedientes, tipo_identidad, numero)

    def buscar_por_paciente(self, codigo: str) -> list[dict[str, str]]:
        return operaciones_listas.buscar_por_codigo_paciente(self.expedientes, codigo)
