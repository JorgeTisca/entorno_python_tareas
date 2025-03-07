import io
import locale
from datetime import date, datetime

from django.http.response import FileResponse
from INTRANET.settings.firebird import conexion
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


# Datos para la tabla
def generar_retencion(periodo):
    datos = conexion.consulta(
        f"SELECT  * FROM pension_nomina_retencion_report('{periodo}')"
    )
    # Generar lista para tabla
    retenciones = [list(retencion.values())[0:7] for retencion in datos]
    # Dar formato
    for retencion in retenciones:
        retencion[7] = diferencia_tiempo(
            fecha_periodo=retencion[7], fecha_retencion=retencion[4]
        )
        if retencion[7] < 2:
            retencion[7] = ""
        retencion[6] = formato_pesos(retencion[6])
        retencion[4] = formato_fecha(retencion[4])

    # Añadir encabezado
    encabezado_tabla = [
        "INTERNO",
        "RFC",
        "NOMBRE",
        "QNA INI",
        "F. INICIO",
        "# QNAS.R",
        "T. IMPORTE",
        ">2A",
    ]
    retenciones.insert(0, encabezado_tabla)

    return retenciones


# Crear encabezado
def formato_pesos(numero):
    return f"${numero:,.2f}"


def formato_fecha(fecha):
    if isinstance(fecha, date):
        return fecha.strftime("%d/%m/%Y")  # Devuelve la fecha formateada
    return fecha


def diferencia_tiempo(fecha_periodo, fecha_retencion):
    años = fecha_periodo.year - fecha_retencion.year
    resultado = []
    if años > 0:
        resultado.append(años)
    return años


# Crear PDF
def reporte_acumulado_retenciones(nombre_archivo, periodo: str):
    buffer = io.BytesIO()

    # Configuración del documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=80,
        leftMargin=20,
        rightMargin=20,
        bottomMargin=30,
    )
    # Generar datos de la tabla
    datos_retencion = generar_retencion(periodo)

    # Crear la tabla
    tabla = Table(
        datos_retencion, colWidths=[45, 77, "*", 36, 50, 34, 66, 20], repeatRows=1
    )
    estilo = TableStyle(
        [
            # (columna_inicio, fila_inicio) , (columna_fin, fila_fin)
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (2, 0), (2, -1), "LEFT"),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("ALIGN", (6, 0), (6, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("FONTSIZE", (5, 0), (5, 0), 6.5),  # Tamaño fuente col 5 --encabezado
            ("FONTSIZE", (2, 1), (2, -1), 7.6),  # Tamaño fuente col 3--Nombre
            ("FONTSIZE", (1, 1), (1, -1), 8),  # Tamaño fuente col 2
            ("FONTSIZE", (6, 1), (6, -1), 8),  # Tamaño fuente col 6
            ("FONTSIZE", (7, 1), (7, -1), 8),  # Tamaño fuente col 7
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]
    )
    tabla.setStyle(estilo)

    # Lista de elementos que se incluirán en el PDF
    elementos = []
    elementos.append(tabla)

    def encabezado(canvas, doc):
        canvas.saveState()

        # LOGO
        canvas.drawImage(
            "static/global_assets/images/ISSSSPEA2.png",
            20,
            730,
            width=95,
            height=40,
        )
        # TITULO
        canvas.setFont("Helvetica-Bold", 12)
        titulo = f"Reporte Quincenal Acumulado de las Retenciones Periodo {periodo}"
        ancho_pagina = letter[0]  # Ancho de la página
        text_width = canvas.stringWidth(titulo, "Helvetica-Bold", 12)
        canvas.drawString((ancho_pagina - text_width) / 2, 740, titulo)
        # LINEA
        canvas.line(20, 720, 590, 720)  # Línea de separación

        # FECHA
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        canvas.setFont("Helvetica", 10)
        canvas.drawString(530, 760, f"{fecha_actual}")

        # PIE DE PAGINA
        pagina_numero = doc.page
        canvas.setFont("Helvetica", 10)
        canvas.drawString(300, 20, f"{pagina_numero}")
        canvas.restoreState()

    # Crear el PDF con los encabezados y pie de página personalizados
    doc.build(elementos, onFirstPage=encabezado, onLaterPages=encabezado)

    buffer.seek(0)
    pdf: bytes = buffer.getvalue()
    return FileResponse(buffer, as_attachment=False, filename=nombre_archivo)
