import glob
import os
import xml.etree.ElementTree as ET

# Usar para la ruta estatica
carpeta = "./rfc/facturas2"


# Sustitur la varibale new_path o carpeta si es que quieres que sea estatico o que tu selecciones la carpeta
archivos_xml = glob.glob(os.path.join(carpeta, "*.xml"))


def extraer_rfc(xml_path):
    # Cargar el XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Espacios de nombres para poder acceder a las etiquetas correctamente del xml
    namespaces = {
        "retenciones": "http://www.sat.gob.mx/esquemas/retencionpago/2",
        "intereseshipotecarios": "http://www.sat.gob.mx/esquemas/retencionpago/1/intereseshipotecarios",
    }
    receptor = root.find(".//retenciones:Receptor/retenciones:Nacional", namespaces)
    contrato = root.find(
        ".//intereseshipotecarios:Intereseshipotecarios",
        namespaces,
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

    return rfc_receptor[:10], num_contrato


# Obtener RFCs y procesar cada archivo XML
for xml in archivos_xml:
    rfc_receptor, contrato = extraer_rfc(xml)
    print(f"RFC Receptor: {rfc_receptor}, Num Contrato: {contrato}")
