from modelos.expediente import Expediente
from datetime import datetime
from typing import Any
from servicios import archivos_adjuntos, generador_codigos, operaciones_listas, repositorio_json, validaciones


class ServicioExpedientes:
    def __init__(self) -> None:
        self.expedientes = repositorio_json.cargar()

    def registrar(self, datos: dict[str, Any]) -> Expediente:
        datos_limpios = {k: v.strip() if isinstance(v, str) else v for k, v in datos.items()}
        ahora = datetime.now()
        datos_limpios["fecha_recepcion"] = ahora.strftime("%d/%m/%Y")
        datos_limpios["hora_recepcion"] = ahora.strftime("%H:%M:%S")
        validaciones.validar(datos_limpios)
        datos_limpios["codigo"], datos_limpios["codigo_documento"] = generador_codigos.generar_codigos(
            self.expedientes,
            datos_limpios["tipo_documento_presentado"],
            datos_limpios.get("tipo_documento_otro", ""),
        )
        datos_limpios["archivos_adjuntos"] = archivos_adjuntos.copiar_adjuntos(
            datos_limpios.get("archivos_adjuntos", []), datos_limpios["codigo"]
        )
        expediente = Expediente(**datos_limpios)
        expedientes_actualizados = [*self.expedientes, expediente.a_dict()]
        repositorio_json.guardar(expedientes_actualizados)
        self.expedientes = expedientes_actualizados
        return expediente

    def codigos_siguientes(self, tipo_documento: str, otro: str = "") -> tuple[str, str]:
        return generador_codigos.generar_codigos(self.expedientes, tipo_documento, otro)

    def buscar(self, codigo: str) -> dict[str, Any] | None:
        return operaciones_listas.buscar_por_codigo(self.expedientes, codigo)

    def listar_ordenados(self) -> list[dict[str, Any]]:
        return operaciones_listas.ordenar_por_codigo(self.expedientes)
