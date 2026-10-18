import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from modelos.expediente import Expediente
from servicios import archivos_adjuntos, configuracion, generador_codigos, generador_pdf
from servicios import operaciones_listas, repositorio_json, validaciones


class ServicioExpedientes:
    def __init__(self) -> None:
        self.expedientes = [self._normalizar(e) for e in repositorio_json.cargar()]
        self.archivo_borradores = Path(__file__).resolve().parents[1] / "datos" / "borradores.json"
        self.directorio_datos = Path(__file__).resolve().parents[1] / "datos"

    def registrar(self, datos: dict[str, Any]) -> Expediente:
        campos = {k: v.strip() if isinstance(v, str) else v for k, v in datos.items()}
        cotejo = campos.get("cotejo", {})
        validaciones.validar_cotejo(cotejo)
        ahora = datetime.now()
        campos["fecha_recepcion"] = ahora.strftime("%d/%m/%Y")
        campos["hora_recepcion"] = ahora.strftime("%H:%M:%S")
        validaciones.validar(campos)
        codigo, codigo_documento = generador_codigos.generar_codigos(
            self.expedientes, campos["tipo_documento_presentado"], campos.get("tipo_documento_otro", "")
        )
        rutas_adjuntos = [self._resolver_ruta_archivo(ruta) for ruta in campos.get("archivos_adjuntos", [])]
        adjuntos = archivos_adjuntos.copiar_adjuntos(rutas_adjuntos, codigo, self.directorio_datos)
        cotejo["estado"] = "Conforme"
        cotejo["fecha"] = ahora.strftime("%d/%m/%Y")
        cotejo["hora"] = ahora.strftime("%H:%M:%S")
        cotejo["folios_declarados"] = int(cotejo["folios_declarados"])
        cotejo["folios_verificados"] = int(cotejo["folios_verificados"])
        cotejo["cantidad_anexos"] = int(cotejo.get("cantidad_anexos", 0))
        folios = cotejo["folios_verificados"]
        expediente = Expediente(
            codigo=codigo,
            codigo_documento=codigo_documento,
            nombre_completo=campos["nombre_completo"],
            tipo_documento_identidad=campos["tipo_documento_identidad"],
            numero_documento=campos["numero_documento"],
            tipo_documento_presentado=campos["tipo_documento_presentado"],
            tipo_documento_otro=campos.get("tipo_documento_otro", ""),
            asunto=campos["asunto"],
            fecha_recepcion=ahora.strftime("%d/%m/%Y"),
            hora_recepcion=ahora.strftime("%H:%M:%S"),
            archivos_adjuntos=adjuntos,
            cotejo=cotejo,
            foliacion={"total": folios, "rango": "", "estado": "Pendiente", "responsable": "", "fecha": "", "hora": "", "ficha": ""},
            cargo={"emitido": False, "ruta": "", "fecha": "", "hora": ""},
            clasificacion={"unidad": "", "tramite": "", "categoria": "", "prioridad": "Normal", "motivo_prioridad": "", "responsable": "", "fecha": "", "hora": "", "estado": "Pendiente de clasificar"},
            derivaciones=[],
            estado="Pendiente de clasificar",
            historial=[],
        )
        registro = expediente.a_dict()
        self._evento(registro, cotejo["responsable"], "Recepción y cotejo conforme", "", registro["estado"], cotejo.get("observaciones", ""))
        self.expedientes.append(registro)
        self._guardar()
        borrador_id = campos.get("borrador_id")
        if borrador_id:
            borradores = self.listar_borradores()
            self._guardar_borradores([b for b in borradores if b.get("borrador_id") != borrador_id])
        return expediente

    def guardar_borrador(self, datos: dict[str, Any], estado: str = "Observado") -> str:
        borradores = self.listar_borradores()
        codigo = datos.get("borrador_id") or f"BOR-{uuid4().hex[:8].upper()}"
        historial_borrador = list(datos.get("historial_borrador", []))
        historial_borrador.append({"accion": "Cotejo guardado como " + estado,
                                   "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   "detalle": datos.get("cotejo", {}).get("observaciones", "")})
        rutas_adjuntos = [self._resolver_ruta_archivo(ruta) for ruta in datos.get("archivos_adjuntos", [])]
        adjuntos = self._guardar_adjuntos_borrador(rutas_adjuntos, codigo)
        borrador = {**datos, "archivos_adjuntos": adjuntos, "borrador_id": codigo, "estado_cotejo": estado,
                    "historial_borrador": historial_borrador,
                    "actualizado": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        borradores = [b for b in borradores if b.get("borrador_id") != codigo]
        borradores.append(borrador)
        self._guardar_borradores(borradores)
        return codigo

    def listar_borradores(self) -> list[dict[str, Any]]:
        return self._cargar_lista(self.archivo_borradores)

    def _guardar_borradores(self, borradores: list[dict[str, Any]]) -> None:
        self._guardar_lista(self.archivo_borradores, borradores)

    def sugerir_codigo(self, tipo_documento: str, otro: str = "") -> tuple[str, str]:
        return generador_codigos.generar_codigos(self.expedientes, tipo_documento, otro)

    def buscar(self, codigo: str) -> dict[str, Any] | None:
        return operaciones_listas.buscar_por_codigo(self.expedientes, codigo)

    def listar_ordenados(self) -> list[dict[str, Any]]:
        return operaciones_listas.ordenar_por_codigo(self.expedientes)

    def pendientes_clasificacion(self, prioridad: str = "Todas") -> list[dict[str, Any]]:
        registros = [e for e in self.expedientes if e.get("clasificacion", {}).get("estado") != "Listo para derivación"]
        if prioridad != "Todas":
            registros = [e for e in registros if e.get("clasificacion", {}).get("prioridad") == prioridad]
        return sorted(registros, key=lambda e: (e.get("clasificacion", {}).get("prioridad") != "Urgente", e.get("fecha_recepcion", "")))

    def guardar_clasificacion(self, codigo: str, datos: dict[str, str]) -> None:
        registro = self._obtener(codigo)
        config = configuracion.cargar()
        if datos.get("unidad") not in config.get("unidades", []):
            raise ValueError("Selecciona una unidad orgánica configurada.")
        if not all(datos.get(campo, "").strip() for campo in ("tramite", "categoria", "responsable")):
            raise ValueError("Completa el trámite, la categoría y el responsable de clasificación.")
        if datos.get("prioridad") not in ("Normal", "Urgente", "Otra"):
            raise ValueError("Selecciona una prioridad válida.")
        if datos.get("prioridad") in ("Urgente", "Otra") and not datos.get("motivo_prioridad", "").strip():
            raise ValueError("Explica el motivo de la prioridad seleccionada.")
        anterior = registro["estado"]
        clase = registro["clasificacion"]
        clase.update(datos)
        ahora = datetime.now()
        clase.update({"fecha": ahora.strftime("%d/%m/%Y"), "hora": ahora.strftime("%H:%M:%S"), "estado": "Clasificado"})
        registro["estado"] = "Clasificado"
        self._evento(registro, datos["responsable"], "Clasificación guardada", anterior, registro["estado"], datos.get("unidad", ""))
        self._guardar()

    def marcar_listo_derivacion(self, codigo: str, responsable: str) -> None:
        registro = self._obtener(codigo)
        if not responsable.strip():
            raise ValueError("Indica quién prepara el expediente para derivación.")
        if registro["cotejo"].get("estado") != "Conforme":
            raise ValueError("El cotejo debe estar conforme antes del despacho.")
        if registro["foliacion"].get("estado") != "Realizada":
            raise ValueError("Confirma la foliación antes del despacho.")
        ruta_cargo = self.directorio_datos.parent / registro["cargo"].get("ruta", "")
        if not registro["cargo"].get("emitido") or not ruta_cargo.is_file():
            raise ValueError("Genera el cargo de recepción antes del despacho.")
        if registro["clasificacion"].get("estado") != "Clasificado":
            raise ValueError("Guarda la clasificación antes de preparar la derivación.")
        anterior = registro["estado"]
        registro["clasificacion"]["estado"] = "Listo para derivación"
        registro["estado"] = "Listo para derivación"
        self._evento(registro, responsable, "Listo para derivación", anterior, registro["estado"], "Controles previos completos.")
        self._guardar()

    def generar_foliacion(self, codigo: str, responsable: str) -> Path:
        registro = self._obtener(codigo)
        if not responsable.strip():
            raise ValueError("Indica quién prepara la ficha de foliación.")
        folios = int(registro["cotejo"].get("folios_verificados", 0))
        rango = f"1–{folios}" if folios else "Sin folios"
        ahora = datetime.now()
        lineas = [f"Código del expediente: {codigo}", f"Ciudadano/remitente: {registro['nombre_completo']}",
                  f"Total de folios verificados: {folios}", f"Rango asignado: {rango}",
                  f"Anexos: {registro['cotejo'].get('cantidad_anexos', 0)}", f"Responsable: {responsable.strip()}",
                  f"Preparada: {ahora.strftime('%d/%m/%Y %H:%M:%S')}"]
        ruta = self.directorio_datos / "foliacion" / f"{codigo}_ficha.pdf"
        generador_pdf.crear_pdf(ruta, "FICHA DE FOLIACIÓN", lineas)
        registro["foliacion"].update({"total": folios, "rango": rango, "estado": "Preparada", "ficha": ruta.relative_to(self.directorio_datos.parent).as_posix(), "responsable": responsable.strip(), "preparada": ahora.strftime("%d/%m/%Y %H:%M:%S")})
        self._evento(registro, "Sistema", "Ficha de foliación generada", registro["estado"], registro["estado"], rango)
        self._guardar()
        return ruta

    def confirmar_foliacion(self, codigo: str, folios_foliados: int, responsable: str, explicacion: str = "") -> None:
        registro = self._obtener(codigo)
        esperados = int(registro["cotejo"].get("folios_verificados", 0))
        if folios_foliados != esperados:
            raise ValueError(f"Se verificaron {esperados} folios; confirma esa cantidad o registra la diferencia autorizada.")
        if not responsable.strip():
            raise ValueError("Indica quién realizó la foliación.")
        declarados = int(registro["cotejo"].get("folios_declarados", esperados))
        if declarados != esperados and not (explicacion.strip() or registro["cotejo"].get("motivo_excepcion", "").strip()):
            raise ValueError("Explica la diferencia entre los folios declarados y verificados.")
        ficha = self.directorio_datos.parent / registro["foliacion"].get("ficha", "")
        if not ficha.is_file():
            raise ValueError("Genera la ficha de foliación antes de confirmarla.")
        ahora = datetime.now()
        foliation = registro["foliacion"]
        foliation.update({"total": folios_foliados, "rango": f"1–{folios_foliados}" if folios_foliados else "Sin folios",
                          "estado": "Realizada", "responsable": responsable.strip(),
                          "fecha": ahora.strftime("%d/%m/%Y"), "hora": ahora.strftime("%H:%M:%S"), "explicacion": explicacion.strip()})
        self._evento(registro, responsable.strip(), "Foliación confirmada", registro["estado"], registro["estado"], foliation["rango"])
        self._guardar()

    def generar_cargo(self, codigo: str) -> Path:
        registro = self._obtener(codigo)
        if registro["cotejo"].get("estado") != "Conforme":
            raise ValueError("El cotejo debe estar conforme para generar el cargo.")
        if registro["foliacion"].get("estado") != "Realizada":
            raise ValueError("Confirma la foliación antes de generar el cargo.")
        config = configuracion.cargar()
        cotejo = registro["cotejo"]
        lineas = [f"Entidad: {config.get('nombre_entidad') or 'Entidad no configurada'}",
                  f"Ciudadano/remitente: {registro['nombre_completo']}", f"Código único: {codigo}",
                  f"Código de seguimiento: {codigo}",
                  f"Documento: {registro['tipo_documento_otro'] or registro['tipo_documento_presentado']}",
                  f"Asunto: {registro['asunto']}", f"Recepción: {registro['fecha_recepcion']} {registro['hora_recepcion']}",
                  f"Folios: {cotejo.get('folios_verificados', 0)}; anexos: {cotejo.get('cantidad_anexos', 0)}",
                  f"Trabajador receptor: {cotejo.get('responsable', '')}",
                  f"Estado de documentación: {cotejo.get('estado', '')}",
                  f"Observaciones: {cotejo.get('observaciones') or 'Ninguna'}", "", "Sello y firma:", "\n\n"]
        ruta = self.directorio_datos / "cargos" / f"{codigo}.pdf"
        generador_pdf.crear_pdf(ruta, "CARGO DE RECEPCIÓN", lineas)
        if not ruta.is_file() or ruta.stat().st_size == 0:
            raise OSError("No se pudo generar el archivo PDF del cargo.")
        ahora = datetime.now()
        registro["cargo"].update({"emitido": True, "ruta": ruta.relative_to(self.directorio_datos.parent).as_posix(),
                                  "fecha": ahora.strftime("%d/%m/%Y"), "hora": ahora.strftime("%H:%M:%S")})
        self._evento(registro, cotejo.get("responsable", ""), "Cargo de recepción generado", registro["estado"], registro["estado"], str(ruta))
        self._guardar()
        return ruta

    def generar_relacion_despacho(self, unidad: str) -> Path:
        grupo = [e for e in self.expedientes if e.get("clasificacion", {}).get("unidad") == unidad
                 and e.get("clasificacion", {}).get("estado") == "Listo para derivación"]
        if not grupo:
            raise ValueError("No hay expedientes listos para esa unidad.")
        grupo.sort(key=lambda e: (e.get("clasificacion", {}).get("prioridad") != "Urgente", e.get("fecha_recepcion", "")))
        lineas = [f"Unidad de destino: {unidad}", f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ""]
        lineas.extend(f"{e['codigo']} | {e['nombre_completo']} | {e['asunto']} | {e['clasificacion'].get('prioridad', 'Normal')}" for e in grupo)
        ruta = self.directorio_datos / "relaciones_despacho" / f"relacion_{datetime.now():%Y%m%d_%H%M%S_%f}.pdf"
        return generador_pdf.crear_pdf(ruta, "RELACIÓN DE DESPACHO", lineas)

    def derivar(self, codigo: str, datos: dict[str, str]) -> None:
        registro = self._obtener(codigo)
        if registro["clasificacion"].get("estado") != "Listo para derivación":
            raise ValueError("El expediente todavía no está listo para derivación.")
        if registro.get("estado") in ("Derivado", "Entregado"):
            raise ValueError("El último envío todavía no ha sido devuelto.")
        obligatorios = ("modalidad", "responsable", "receptor")
        if any(not datos.get(campo, "").strip() for campo in obligatorios):
            raise ValueError("Completa la modalidad, el responsable y quién recibe.")
        if datos["modalidad"] not in ("Física", "Digital"):
            raise ValueError("Selecciona una modalidad de derivación válida.")
        ahora = datetime.now()
        movimiento = {**datos, "codigo": codigo, "unidad": registro["clasificacion"]["unidad"],
                      "fecha": ahora.strftime("%d/%m/%Y"), "hora": ahora.strftime("%H:%M:%S"), "estado": "Enviado"}
        if datos["modalidad"] == "Digital":
            movimiento["nota_transferencia"] = "Movimiento registrado localmente; no se realizó una transferencia electrónica."
        registro["derivaciones"].append(movimiento)
        anterior = registro["estado"]
        registro["estado"] = "Derivado"
        self._evento(registro, datos["responsable"], "Derivación registrada", anterior, registro["estado"], movimiento.get("nota_transferencia", ""))
        self._guardar()

    def generar_cargo_derivacion(self, codigo: str) -> Path:
        registro = self._obtener(codigo)
        if not registro["derivaciones"]:
            raise ValueError("Registra la derivación antes de generar el cargo interno.")
        movimiento = registro["derivaciones"][-1]
        lineas = [f"Código de expediente: {codigo}", f"Unidad destinataria: {movimiento['unidad']}",
                  f"Modalidad: {movimiento['modalidad']}", f"Responsable: {movimiento['responsable']}",
                  f"Recibe: {movimiento['receptor']}", f"Fecha y hora: {movimiento['fecha']} {movimiento['hora']}",
                  f"Guía/constancia: {movimiento.get('guia', '')}",
                  f"Documentos y anexos: {registro['tipo_documento_presentado']}; {registro['cotejo'].get('cantidad_anexos', 0)} anexos",
                  f"Observaciones: {movimiento.get('observaciones', '')}", movimiento.get("nota_transferencia", "")]
        ruta = self.directorio_datos / "cargos_derivacion" / f"{codigo}_{movimiento['fecha'].replace('/', '')}_{movimiento['hora'].replace(':', '')}.pdf"
        generador_pdf.crear_pdf(ruta, "CARGO INTERNO DE DERIVACIÓN", lineas)
        if not ruta.is_file() or ruta.stat().st_size == 0:
            raise OSError("No se pudo generar el cargo interno de derivación.")
        movimiento["cargo"] = ruta.relative_to(self.directorio_datos.parent).as_posix()
        self._evento(registro, movimiento["responsable"], "Cargo de derivación generado", registro["estado"], registro["estado"], str(ruta))
        self._guardar()
        return ruta

    def confirmar_entrega(self, codigo: str, receptor: str) -> None:
        registro = self._obtener(codigo)
        movimiento = self._ultima_derivacion(registro)
        if movimiento["estado"] != "Enviado":
            raise ValueError("Solo se puede confirmar la entrega de una derivación enviada.")
        if not receptor.strip():
            raise ValueError("Indica quién confirma la recepción.")
        ruta_cargo = self.directorio_datos.parent / movimiento.get("cargo", "")
        if not movimiento.get("cargo") or not ruta_cargo.is_file():
            raise ValueError("Genera el cargo interno antes de confirmar la entrega.")
        movimiento["estado"] = "Entregado"
        movimiento["confirmado_por"] = receptor.strip()
        movimiento["entregado_fecha_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        anterior = registro["estado"]
        registro["estado"] = "Entregado"
        self._evento(registro, receptor, "Entrega confirmada", anterior, registro["estado"], movimiento["unidad"])
        self._guardar()

    def registrar_devolucion(self, codigo: str, responsable: str, observacion: str) -> None:
        registro = self._obtener(codigo)
        movimiento = self._ultima_derivacion(registro)
        if movimiento.get("estado") not in ("Enviado", "Entregado"):
            raise ValueError("Solo se puede registrar una devolución de un expediente enviado o entregado.")
        if not responsable.strip():
            raise ValueError("Indica quién registra la devolución.")
        if not observacion.strip():
            raise ValueError("Describe el motivo de la devolución.")
        movimiento.update({"estado": "Devuelto", "devolucion": observacion.strip(),
                           "devolucion_fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        anterior = registro["estado"]
        registro["estado"] = "Devuelto"
        self._evento(registro, responsable, "Expediente devuelto", anterior, registro["estado"], observacion)
        self._guardar()

    def historial(self, codigo: str = "") -> list[dict[str, Any]]:
        registros = [self._obtener(codigo)] if codigo else self.expedientes
        return [dict(evento, codigo=registro["codigo"]) for registro in registros for evento in registro.get("historial", [])]

    def resumen(self) -> dict[str, Any]:
        estados = [e.get("estado", "") for e in self.expedientes]
        alertas = []
        for e in self.expedientes:
            if e.get("cotejo", {}).get("estado") == "Observado":
                alertas.append(f"{e['codigo']}: cotejo observado")
            if e.get("foliacion", {}).get("estado") != "Realizada":
                alertas.append(f"{e['codigo']}: foliación pendiente")
            if not e.get("cargo", {}).get("emitido"):
                alertas.append(f"{e['codigo']}: cargo pendiente")
            if e.get("clasificacion", {}).get("estado") == "Pendiente de clasificar":
                alertas.append(f"{e['codigo']}: pendiente de clasificar")
        pendientes = self.listar_borradores()
        alertas.extend(f"{b.get('borrador_id')}: cotejo {b.get('estado_cotejo', 'pendiente').lower()}" for b in pendientes)
        return {
            "recibidos": len(self.expedientes),
            "observados": sum(b.get("estado_cotejo") == "Observado" for b in pendientes),
            "pendientes_clasificar": sum(e.get("clasificacion", {}).get("estado") == "Pendiente de clasificar" for e in self.expedientes),
            "urgentes": sum(e.get("clasificacion", {}).get("prioridad") == "Urgente" for e in self.expedientes),
            "listos": estados.count("Listo para derivación"),
            "derivados": sum(e.get("estado") in ("Derivado", "Entregado", "Devuelto") for e in self.expedientes),
            "alertas": alertas,
        }

    @staticmethod
    def _normalizar(registro: dict[str, Any]) -> dict[str, Any]:
        valores_por_defecto = {
            "cotejo": {"estado": "Pendiente", "folios_declarados": 0, "folios_verificados": 0, "cantidad_anexos": 0, "anexos": [], "responsable": ""},
            "foliacion": {"total": 0, "rango": "", "estado": "Pendiente", "responsable": "", "ficha": ""},
            "cargo": {"emitido": False, "ruta": ""},
            "clasificacion": {"unidad": "", "tramite": "", "categoria": "", "prioridad": "Normal", "responsable": "", "estado": "Pendiente de clasificar"},
        }
        for clave, valores in valores_por_defecto.items():
            actual = registro.get(clave)
            registro[clave] = {**valores, **actual} if isinstance(actual, dict) else valores
        if not isinstance(registro.get("derivaciones"), list):
            registro["derivaciones"] = []
        if not isinstance(registro.get("historial"), list):
            registro["historial"] = []
        if not isinstance(registro.get("archivos_adjuntos"), list):
            registro["archivos_adjuntos"] = []
        registro.setdefault("estado", registro["clasificacion"].get("estado", "Pendiente de clasificar"))
        return registro

    def _obtener(self, codigo: str) -> dict[str, Any]:
        registro = self.buscar(codigo)
        if registro is None:
            raise ValueError("No se encontró el expediente indicado.")
        return registro

    @staticmethod
    def _ultima_derivacion(registro: dict[str, Any]) -> dict[str, Any]:
        if not registro.get("derivaciones"):
            raise ValueError("Este expediente todavía no tiene una derivación.")
        return registro["derivaciones"][-1]

    @staticmethod
    def _evento(registro: dict[str, Any], responsable: str, accion: str, anterior: str, nuevo: str, detalle: str = "") -> None:
        ahora = datetime.now()
        registro.setdefault("historial", []).append({
            "responsable": responsable or "No especificado", "accion": accion,
            "fecha": ahora.strftime("%d/%m/%Y"), "hora": ahora.strftime("%H:%M:%S"),
            "estado_anterior": anterior, "estado_nuevo": nuevo, "detalle": detalle,
        })

    def _guardar(self) -> None:
        repositorio_json.guardar(self.expedientes)

    def _resolver_ruta_archivo(self, ruta: str) -> str:
        origen = Path(ruta)
        if not origen.is_absolute():
            origen = self.directorio_datos.parent / origen
        return str(origen)

    def _guardar_adjuntos_borrador(self, rutas: list[str], codigo: str) -> list[str]:
        if not rutas:
            return []
        destino = self.directorio_datos / "adjuntos" / "borradores" / codigo
        destino.mkdir(parents=True, exist_ok=True)
        guardados = []
        for texto in rutas:
            origen = Path(texto)
            if not origen.is_file():
                raise ValueError(f"No se encontró el archivo seleccionado: {origen.name}")
            if origen.suffix.lower() not in archivos_adjuntos.EXTENSIONES_PERMITIDAS:
                raise ValueError(f"El formato de archivo no está permitido: {origen.name}")
            if origen.resolve().parent == destino.resolve():
                guardados.append(origen.relative_to(self.directorio_datos.parent).as_posix())
                continue
            nombre = origen.name
            base, extension = origen.stem, origen.suffix
            numero = 2
            while (destino / nombre).exists():
                nombre = f"{base}_{numero}{extension}"
                numero += 1
            shutil.copy2(origen, destino / nombre)
            guardados.append((Path(self.directorio_datos.name) / "adjuntos" / "borradores" / codigo / nombre).as_posix())
        return guardados

    @staticmethod
    def _cargar_lista(ruta: Path) -> list[dict[str, Any]]:
        if not ruta.exists() or ruta.stat().st_size == 0:
            return []
        with ruta.open("r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        return data if isinstance(data, list) else []

    @staticmethod
    def _guardar_lista(ruta: Path, datos: list[dict[str, Any]]) -> None:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
