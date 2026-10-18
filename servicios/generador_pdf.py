import textwrap
from pathlib import Path


def _texto_pdf(texto: str) -> bytes:
    datos = texto.encode("cp1252", errors="replace")
    salida = bytearray(b"(")
    for caracter in datos:
        if caracter in (40, 41, 92):
            salida.append(92)
        if caracter < 32 or caracter > 126:
            salida.extend(f"\\{caracter:03o}".encode("ascii"))
        else:
            salida.append(caracter)
    salida.extend(b")")
    return bytes(salida)


def crear_pdf(ruta: Path, titulo: str, lineas: list[str]) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    renglones = [titulo, "", *[r for linea in lineas for r in textwrap.wrap(str(linea), width=82) or [""]]]
    paginas = [renglones[i:i + 48] for i in range(0, len(renglones), 48)] or [[titulo]]
    objetos: list[bytes] = [b""] * (3 + len(paginas) * 2)
    objetos[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{4 + i * 2} 0 R" for i in range(len(paginas)))
    objetos[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(paginas)} >>".encode("ascii")
    objetos[2] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    for indice, pagina in enumerate(paginas):
        objeto_pagina = 3 + indice * 2
        objeto_contenido = objeto_pagina + 1
        contenido = bytearray(b"BT\n/F1 10 Tf\n48 794 Td\n")
        for linea in pagina:
            contenido.extend(_texto_pdf(linea) + b" Tj\n0 -15 Td\n")
        contenido.extend(b"ET\n")
        objetos[objeto_pagina] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {objeto_contenido + 1} 0 R >>"
        ).encode("ascii")
        objetos[objeto_contenido] = (
            f"<< /Length {len(contenido)} >>\nstream\n".encode("ascii")
            + bytes(contenido) + b"endstream"
        )
    archivo = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for indice, objeto in enumerate(objetos, start=1):
        offsets.append(len(archivo))
        archivo.extend(f"{indice} 0 obj\n".encode("ascii") + objeto + b"\nendobj\n")
    inicio_xref = len(archivo)
    archivo.extend(f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        archivo.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    archivo.extend(
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n".encode("ascii")
    )
    ruta.write_bytes(archivo)
    return ruta
