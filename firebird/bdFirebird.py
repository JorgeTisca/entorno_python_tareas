import json

from firebird.base.types import Error
from firebird.driver import connect, driver_config
from firebird.driver.types import DatabaseError

driver_config.server_defaults.host.value = "10.1.18.203"


with open("firebird/secret.json") as f:
    secret = json.loads(f.read())


def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "datos necesarios no encontrados "


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class conexion:
    def consulta(sql):
        conn = None
        cursor = None
        try:
            conn = connect(
                database=get_secret("DB_NAME"),
                user="JPONCE",
                password="456123",
                role="RDB$ADMIN",
                charset="ISO8859_1",
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            # Si la consulta es SELECT, obtener los datos
            if sql.strip().upper().startswith("SELECT"):
                datos = dictfetchall(cursor)
            else:
                conn.commit()  # Confirmar cambios para INSERT, UPDATE, DELETE
                datos = None  # Estas consultas no devuelven datos

            return datos

        except Exception as e:
            error = str(e)
            print("Error en consulta:", error)
            if conn:
                conn.rollback()
            raise DatabaseError({"Base de datos Error": error, "SQL": sql})

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def consultaRowCount(sql):
        print(sql)
        try:
            conn = connect(
                database=get_secret("DB_NAME"),
                user="JPONCE",
                password="456123",
                role="RDB$ADMIN",
                charset="ISO8859_1",
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            datos = dictfetchall(cursor)
            cantDatos = cursor.rowcount
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            error = str(e)
            cursor.close()
            conn.rollback()
            conn.close()
            raise DatabaseError({"Base de datos Error": error, "SQL": sql})
        return datos, cantDatos

    def callproc(callproc):
        """
        PROCEDIMIENTO A LLAMAR CON
        TUPLE( PROCEDIMIENTO:STR "" , PARAMETROS:TUPLE ())
        """
        try:
            conn = connect(
                database=get_secret("DB_NAME"),
                user="JPONCE",
                password="456123",
                role="RDB$ADMIN",
                charset="ISO8859_1",
            )
            cursor = conn.cursor()
            print(callproc)
            cursor.callproc(callproc[0], callproc[1])
            datos = dictfetchall(cursor)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            error = str(e)
            cursor.close()
            conn.rollback()
            conn.close()
            raise DatabaseError(
                {"Base de datos Error": error, "PROCEDIMIENTO Y PARAMETROS": callproc}
            )
        return datos

    def callprocRollback(callproc):
        """
        PROCEDIMIENTO A LLAMAR CON
        TUPLE( PROCEDIMIENTO:STR "" , PARAMETROS:TUPLE ())
        """
        try:
            conn = connect(
                database=get_secret("DB_NAME"),
                user="JPONCE",
                password="456123",
                role="RDB$ADMIN",
                charset="ISO8859_1",
            )
            cursor = conn.cursor()
            print(callproc)
            cursor.callproc(callproc[0], callproc[1])
            datos = dictfetchall(cursor)
            cursor.close()
            conn.rollback()
            conn.close()
        except Exception as e:
            error = str(e)
            cursor.close()
            conn.rollback()
            conn.close()
            raise DatabaseError(
                {"Base de datos Error": error, "PROCEDIMIENTO Y PARAMETROS": callproc}
            )
        return datos

    def rowcount(sql):
        print(sql)
        try:
            conn = connect(
                database=get_secret("DB_NAME"),
                user="JPONCE",
                password="456123",
                role="RDB$ADMIN",
                charset="ISO8859_1",
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            datos = cursor.rowcount
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            error = str(e)
            cursor.close()
            conn.rollback()
            conn.close()
            raise DatabaseError({"Base de datos Error": error, "SQL": sql})
        return datos
