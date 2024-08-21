import pymysql
from app.models.modelo import Provincia
from app.models.connect import connect_db


class ProvinciaService:
    def create_provincia(self, codigo_provincia, nombre_provincia):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO provincias (codigo_provincia, nombre_provincia) VALUES (%s, %s)"
                cursor.execute(sql, (codigo_provincia, nombre_provincia))
                conn.commit()
                return "Provincia creada exitosamente."
        except Exception as e:
            return f"Error al crear la provincia: {e}"
        finally:
            conn.close()

    def get_provincias(self):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM provincias")
                result = cursor.fetchall()
                provincias = []
                for provincia in result:
                    provincias.append(Provincia(provincia[0], provincia[1]))
                return provincias
        except Exception as e:
            return f"Error al obtener las provincias: {e}"
        finally:
            conn.close()

    def get_provincia(self, codigo_provincia):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM provincias WHERE codigo_provincia = %s"
                cursor.execute(sql, (codigo_provincia,))
                result = cursor.fetchone()
                if result:
                    return Provincia(result[0], result[1])
                return "Provincia no encontrada."
        except Exception as e:
            return f"Error al obtener la provincia: {e}"
        finally:
            conn.close()

    def update_provincia(self, codigo_provincia, nuevo_nombre):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE provincias SET nombre_provincia = %s WHERE codigo_provincia = %s"
                cursor.execute(sql, (nuevo_nombre, codigo_provincia))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Provincia actualizada exitosamente."
                return "Provincia no encontrada."
        except Exception as e:
            return f"Error al actualizar la provincia: {e}"
        finally:
            conn.close()

    def delete_provincia(self, codigo_provincia):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM provincias WHERE codigo_provincia = %s"
                cursor.execute(sql, (codigo_provincia,))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Provincia eliminada exitosamente."
                return "Provincia no encontrada."
        except Exception as e:
            return f"Error al eliminar la provincia: {e}"
        finally:
            conn.close()
