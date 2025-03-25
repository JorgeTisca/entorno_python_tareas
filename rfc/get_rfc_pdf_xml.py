import glob
import os

# import re
import xml.etree.ElementTree as ET
from datetime import datetime

from firebird.bdFirebird import conexion

# import pdfplumber


CARPETA = "./rfc_xml/facturas"
# Expresión regular para buscar un RFC (Patrón RFC Mexicano)
RFC_REGEX = r"[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}"

fecha_actual = datetime.now().strftime("%d-%m-%Y")


def extraer_rfc(xml_path):
    # Cargar el XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Espacio de nombres de CFDI 3.3 o 4.0
    # ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}
    # Espacios de nombres para poder acceder a las etiquetas correctamente
    namespaces = {
        "retenciones": "http://www.sat.gob.mx/esquemas/retencionpago/2",
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "intereseshipotecarios": "http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios",
    }

    # Buscar RFC del emisor y receptor
    emisor = root.find(".//retenciones:Emisor", namespaces)
    receptor = root.find(".//retenciones:Receptor/retenciones:Nacional", namespaces)
    contrato = root.find(
        ".//intereseshipotecarios:Intereseshipotecarios",
        namespaces,
    )

    rfc_emisor = (
        emisor.get("RfcE", "No encontrado") if emisor is not None else "No encontrado"
    )
    rfc_receptor = (
        receptor.get("RfcR", "No encontrado")
        if receptor is not None
        else "No encontrado"
    )
    num_contrato = (
        contrato.get("NumContrato", "No encontrado")
        if contrato is not None
        else "No encontrado"
    )

    return rfc_emisor, rfc_receptor, num_contrato


# def extraer_rfc_pdf(pdf_file):
#     try:
#         with pdfplumber.open(pdf_file) as pdf:
#             texto = ""
#             for page in pdf.pages:
#                 texto += page.extract_text() + "\n"  # Extraer todo el texto

#         # Buscar RFC con la expresión regular
#         rfc_encontrados = re.findall(RFC_REGEX, texto)
#         rfc_emisor = rfc_encontrados[0] if len(rfc_encontrados) > 0 else "No encontrado"
#         rfc_receptor = (
#             rfc_encontrados[1] if len(rfc_encontrados) > 1 else "No encontrado"
#         )

#         return rfc_emisor, rfc_receptor
#     except Exception as e:
#         print(f"Error procesando PDF {pdf_file}: {e}")
#         return "Error", "Error"


# Buscar todos los archivos XML en la carpeta
archivos_xml = glob.glob(os.path.join(CARPETA, "*.xml"))
# archivos_pdf = glob.glob(os.path.join(CARPETA, "*.pdf"))


#  Ruta del XML
# xml_file = "./rfc_xml/factura.xml"

# Obtener RFCs
for xml in archivos_xml:
    rfc_emisor, rfc_receptor, contrato = extraer_rfc(xml)
    nom_archivo = os.path.basename(xml).split(".")
    datos = conexion.consulta(
        f"select p.interno from personal p left join ppv pv on p.interno=pv.interno left join pmp pm on pm.interno=p.interno where p.rfc='{rfc_receptor}' and (pv.no_prestamo={contrato} or (pm.no_prestamo={contrato}))"
    )
    try:
        inserta = conexion.consulta(
            f"INSERT INTO WS_DESCARGAS (INTERNO , TIPO, URL_XML, URL_PDF, TITULO, FECHA) VALUES( {datos[0]['INTERNO']},'CONSTANCIA', 'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo[0]}.xml', 'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo[0]}.xml', 'CONSTANCIA DE INTERESES REALES 2024', CURRENT_DATE)"
        )
    except Exception as e:
        print("Error en instertar Dato")
        raise e

    print(f"Archivo: {nom_archivo}")
    print(
        f"RFC Emisor: {rfc_emisor}, RFC Receptor: {rfc_receptor}, Num Contrato: {contrato}, Interno: {datos[0]['INTERNO']}\n"
    )

# Procesar PDFs
# for archivo in archivos_pdf:
#     rfc_emisor, rfc_receptor = extraer_rfc_pdf(archivo)
#     print(f"Archivo PDF: {os.path.basename(archivo)}")
#     print(f"RFC Emisor: {rfc_emisor}, RFC Receptor: {rfc_receptor}\n")
