from datetime import date, datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from firebird.bdFirebird import conexion

# Datos para la tabla
periodo = "2124"


def generar_retencion(periodo):
    datos = conexion.consulta(
        f"SELECT * FROM pension_nomina_retencion_report('{periodo}')"
    )
    # Generar lista para tabla
    retenciones = [list(retencion.values())[0:7] for retencion in datos]
    # Dar formato
    for retencion in retenciones:
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
    ]
    retenciones.insert(0, encabezado_tabla)

    return retenciones


# Crear encabezado
def encabezado(canvas, doc):
    canvas.saveState()

    # LOGO
    canvas.drawImage(
        "logo.png",
        20,
        730,
        width=95,
        height=40,
    )
    # TITULO
    canvas.setFont("Helvetica-Bold", 12)
    titulo = f"Reporte Quincenal Acumulado de las Retenciones Periodo {periodo} "
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


# Crear PDF
def crear_pdf(nombre_archivo):
    # Configuración del documento
    doc = SimpleDocTemplate(
        nombre_archivo,
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
        datos_retencion, colWidths=[48, 85, "*", 40, 50, 43, 68], repeatRows=1
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
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]
    )
    tabla.setStyle(estilo)

    # Lista de elementos que se incluirán en el PDF
    elementos = []
    elementos.append(tabla)

    # Crear el PDF con los encabezados y pie de página personalizados
    doc.build(elementos, onFirstPage=encabezado, onLaterPages=encabezado)


def formato_pesos(numero):
    return f"${numero:,.2f}"


def formato_fecha(fecha):
    if isinstance(fecha, date):
        return fecha.strftime("%d/%m/%Y")  # Devuelve la fecha formateada
    return fecha


# Llamar a la función
crear_pdf("reporte_retenciones.pdf")
