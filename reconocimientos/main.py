from firebird.bdFirebird import conexion

periodo = "2124"


datosPersonales = conexion.consulta(
    f"SELECT * FROM pension_nomina_retencion_report('{periodo}')"
)


print(datosPersonales[0].get("FULLNAME"))
