import asyncio
import glob
import os
import xml.etree.ElementTree as ET

from firebird.bdFirebird import conexion

# carpeta = "./rfc_xml/facturas"
carpeta = "./rfc_xml/CONSTANCIAS DE INTERESES REALES 2024"
# Expresión regular para buscar un RFC (Patrón RFC Mexicano)
RFC_REGEX = r"[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}"
rfc_nofound = []
# Buscar todos los archivos XML en la carpeta
archivos_xml = glob.glob(os.path.join(carpeta, "*.xml"))


def extraer_rfc(xml_path):
    # Cargar el XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Espacios de nombres para poder acceder a las etiquetas correctamente del xml
    namespaces = {
        "retenciones": "http://www.sat.gob.mx/esquemas/retencionpago/2",
        "cfdi": "http://www.sat.gob.mx/cfd/4",
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


async def get_interno(rfc_receptor, contrato):
    datos = conexion.consulta(
        # f"select p.interno from personal p left join ppv pv on p.interno=pv.interno left join pmp pm on pm.interno=p.interno where p.rfc containing'{rfc_receptor}' and (pv.no_prestamo={contrato} or (pm.no_prestamo={contrato}))"
        f"select p.interno from personal p where p.rfc containing'{rfc_receptor}'"
    )
    # Devolver None si no hay resultados
    if not datos:
        print(
            f"No se encontró el interno para RFC: {rfc_receptor} y contrato: {contrato}"
        )
        return None

    return datos[0]["INTERNO"]


async def insertar_dato(rfc_receptor, contrato, nom_archivo):
    interno = await get_interno(rfc_receptor, contrato)

    if not interno:
        print("No se encontró un INTERNO válido para el RFC y contrato proporcionados.")
        rfc_nofound.append(nom_archivo)
        return
    sql = f"""
    INSERT INTO WS_DESCARGAS (INTERNO , TIPO, URL_XML, URL_PDF, TITULO, FECHA)
    VALUES( {interno}, 'CONSTANCIA', 'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo}.xml',
    'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo}.pdf',
    'CONSTANCIA DE INTERESES REALES 2024', CURRENT_DATE)
    """
    # sql = f"""
    # INSERT INTO WS_DESCARGAS (INTERNO , TIPO, URL_XML, URL_PDF, TITULO, FECHA)
    # VALUES( {interno}, 'CONSTANCIA', 'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo}.xml',
    # 'DESCARGAS/117735823fadae51db091c7d63e60eb0/{nom_archivo}.pdf',
    # 'CONSTANCIA DE INTERESES REALES 2024', CURRENT_DATE)
    # """
    conexion.consulta(sql)


async def procesar_archivos():
    # Obtener RFCs y procesar cada archivo XML
    for xml in archivos_xml:
        rfc_receptor, contrato = extraer_rfc(xml)
        nom_archivo = os.path.basename(xml).split(".")[0]
        print(f"Archivo: {nom_archivo}")
        print(f"RFC Receptor: {rfc_receptor}, Num Contrato: {contrato}")
        await insertar_dato(rfc_receptor, contrato, nom_archivo)
    print(f"archivos con RFC incorrecto--- {rfc_nofound}")


if __name__ == "__main__":
    asyncio.run(procesar_archivos())
