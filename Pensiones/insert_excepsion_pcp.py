import os
import sys

# Ruta para encontrar mi_firebird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from firebird_db import conexion

# Cargar la primera pestaña del archivo Excel
df = pd.read_excel("RIESGOS DE TRABAJO PARCIALES.xlsx", sheet_name=0)

# Recorrer las filas del DataFrame
for row in df.itertuples():
    interno = row[2]

    # Ignorar si la celda está vacía (NaN)
    if pd.isna(interno):
        print(f"❌ Fila vacía ignorada: {row}")
        continue

    # Intentar convertir a entero. Si es un texto como 'INTERNO', se ignora.
    try:
        interno_val = int(interno)
    except (ValueError, TypeError):
        print(f"⚠️ Encabezado o texto ignorado: '{interno}'")
        continue

    sql = f"""
    INSERT INTO EXCEPCION_PENSIONADOS_PCP(interno)
    VALUES ({interno_val})
    """

    try:
        conexion.consulta(sql)
        print(f"✅ Insertado: {interno_val}")
    except Exception as e:
        print(f"❌ Error al insertar interno {interno_val}:")
        print(e)
