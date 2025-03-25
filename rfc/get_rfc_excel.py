import asyncio

import pandas as pd

from firebird.bdFirebird import conexion

rfc_nofound = []
archivo_excel = "./rfc/REPORTE INTEGRAL DE CONSTANCIAS DE INTERESES REALES 2024.xlsx"

df = pd.read_excel(archivo_excel, engine="openpyxl")

columna_rfc = "RfcR"
datos_excel = {
    "folio": "FolioInt",
    "fecha_exp": "FechaExp",
    "rfc": "RfcR",
    "nombre_razon_social": "NomDenRazSocR",
    "domicilio_fiscal": "DomicilioFiscalR",
    "num_contrato": "NumContrato",
    "mes_ini": "MesIni",
    "mes_fin": "MesFin",
    "año": "Ejercicio",
}


def get_interno(rfc):
    datos = conexion.consulta(
        f"select p.interno from personal p where p.rfc containing'{rfc}'"
    )
    # Devolver None si no hay resultados
    if not datos:
        print(f"No se encontró el interno para RFC: {rfc}")
        rfc_nofound.append(rfc)
        return None

    return datos[0]["INTERNO"]


async def insertar_dato(datos_fila):
    interno = get_interno(datos_fila["rfc"][0:10])
    print(f"RFC---{datos_fila["rfc"][0:10]}  Interno--- {interno}")
    print(datos_fila)
    if not interno:
        print("No se encontró un INTERNO válido para el RFC y contrato proporcionados.")

        return
    sql = f"""
    INSERT INTO constancias_rfc (INTERNO , FOLIOINT, FECHAEXP, RFC, NOMBRE_RAZON_SOCIAL,DOMICILIO_FISCAL,NUMCONTRATO,MESINI,MESFIN,EJERCICIO)
    VALUES({interno},'{datos_fila["folio"]}','{datos_fila["fecha_exp"]}','{datos_fila["rfc"]}','{datos_fila["nombre_razon_social"]}','{datos_fila["domicilio_fiscal"]}',{datos_fila["num_contrato"]},{datos_fila["mes_ini"]},{datos_fila["mes_fin"]},{datos_fila["año"]})
    """
    conexion.consulta(sql)


# Seleccionar solo las columnas necesarias y renombrarlas
df_filtrado = df[list(datos_excel.values())].rename(
    columns={v: k for k, v in datos_excel.items()}
)

# Mostrar los primeros registros
# print(df_filtrado.head())

# Si quieres convertirlo a una lista de diccionarios
datos_lista = df_filtrado.to_dict(orient="records")


async def procesar_excel():
    for fila in datos_lista:
        await insertar_dato(fila)
    print(rfc_nofound)


if __name__ == "__main__":
    asyncio.run(procesar_excel())
