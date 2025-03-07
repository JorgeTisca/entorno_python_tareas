import io
from datetime import datetime

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.platypus.paragraph import TA_CENTER, TA_RIGHT


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def pdfReconocimiento(NOMBRE: str, CAPACITACION: str, TIPO: str, archivo: str):
    from reportlab.lib.pagesizes import letter

    letter = (letter[1], letter[0])

    def y(posY):
        return letter[1] - posY

    buffer = io.BytesIO()
    pdf = Canvas(buffer, letter)

    # pdf.drawImage("static/global_assets/images/Reconocimiento.jpg", 0, 0, 792, 612)
    pdf.drawImage("Reconocimiento_2025.jpg", 0, 0, 792, 612)

    # pdfmetrics.registerFont(TTFont("GOTHICB", "static/global_assets/fonts/gothicb.ttf"))
    pdfmetrics.registerFont(TTFont("GOTHICB", "gothicb.ttf"))
    # TIPO RECONOCIMIENTO O CONSTANCIA
    style4 = ParagraphStyle(name="Normal")
    style4.fontSize = 56
    style4.fontName = "GOTHICB"
    style4.leading = 18
    style4.textColor = HexColor("#260088")
    style4.alignment = TA_CENTER
    texto4 = Paragraph(f"{TIPO} ", style4)
    texto4.wrapOn(pdf, letter[0], letter[1])
    texto4.drawOn(pdf, -3 * cm, y(8.3 * cm))

    # APARTIR DE AQUI FUERON LAS MODIFICACIONES
    # NOMBRE
    style = ParagraphStyle(name="Normal")
    style.fontName = "Helvetica-Bold"
    style.fontSize = 28
    style.leading = 30
    style.alignment = TA_CENTER
    # style.textColor = HexColor("#de1682")
    style.textColor = HexColor("#de1682")
    # aW = 22 * cm
    aW = 17.5 * cm
    aH = 1 * cm
    nombre = f"{NOMBRE.upper()}"
    texto = Paragraph(nombre, style)
    ancho_texto, alto_texto = texto.wrapOn(pdf, aW, aH)

    # texto.drawOn(pdf, 2.5 * cm, y((13.75 * cm) - texto.height))

    if alto_texto > 30:
        texto.drawOn(pdf, cm * 2.3, y((14.3 * cm) - texto.height))
    else:
        texto.drawOn(pdf, cm * 2.3, y((12.85 * cm) - texto.height))

    # NOMBRE CAPACITACION
    # reconocimiento = f"{CAPACITACION.upper()}{CAPACITACION.upper()}{CAPACITACION.upper()}{CAPACITACION.upper()}{CAPACITACION.upper()} "
    reconocimiento = f"{CAPACITACION.upper()} "
    style2 = ParagraphStyle(name="Normal")
    style2.fontSize = 12
    style2.fontName = "Helvetica-Bold"
    style2.leading = 20
    style2.textColor = HexColor("#28017e")
    style2.alignment = TA_CENTER

    aW = 18 * cm
    aH = 1 * cm
    texto = Paragraph(reconocimiento, style2)
    ancho_texto, alto_texto = texto.wrapOn(pdf, aW, aH)
    texto.drawOn(pdf, cm * 2, y(13 * cm + alto_texto))
    # FECHA
    # FECHA = datetime.strptime(FECHA,"YYYY-mm-dd").strftime("dd/mm/YYYY")
    fecha = "AGUASCALIENTES, AGS 1 DE FEBRERO DE 2023"
    style2.fontSize = 11
    style2.alignment = TA_RIGHT
    texto = Paragraph(fecha, style2)
    ancho_texto, alto_texto = texto.wrapOn(pdf, 11 * cm, 2 * cm)
    texto.drawOn(pdf, 5 * cm, 0.7 * cm)
    # FIRMA
    pdf.drawImage(
        # "static/global_assets/images/firma_MARIO_ALBERTO_ALVAREZ_MICHAUS.png",
        "firma.png",
        (letter[0] / 2) - 240,
        y(575),
        350,
        200,
        mask="auto",
    )

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    # Guardar el archivo PDF en disco
    with open(archivo, "wb") as f:
        f.write(buffer.read())

    return archivo


pdfReconocimiento(
    "ANGÉLICA CECILIA DÍAZ GONZÁLEZ",
    'POR SU VALIOSA PARTICIPACIÓN EN EL CURSO DE "EVACUACIÓN Y SIMULACRO".',
    "RECONOCIMIENTO",
    "Reconocimiento.pdf",
)
