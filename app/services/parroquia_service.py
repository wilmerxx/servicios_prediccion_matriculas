import pymysql
from app.models.modelo import Parroquia
from app.models.connect import connect_db


class ParroquiaService:
    def create_parroquia(self, codigo_parroquia, nombre_parroquia):
        conn = connect_db()

        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO parroquias (codigo_parroquia, nombre_parroquia) VALUES (%s, %s)"
                cursor.execute(sql, (codigo_parroquia, nombre_parroquia))
                conn.commit()
                return "Parroquia creada exitosamente."
        except Exception as e:
            return f"Error al crear la parroquia: {e}"
        finally:
            conn.close()

    def get_parroquias(self):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM parroquias")
                result = cursor.fetchall()
                parroquias = []
                for parroquia in result:
                    parroquias.append(Parroquia(parroquia[0], parroquia[1]))
                return parroquias
        except Exception as e:
            return f"Error al obtener las parroquias: {e}"
        finally:
            conn.close()

    def get_parroquia(self, codigo_parroquia):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM parroquias WHERE codigo_parroquia = %s"
                cursor.execute(sql, (codigo_parroquia,))
                result = cursor.fetchone()
                if result:
                    return Parroquia(result[0], result[1])
                return "Parroquia no encontrada."
        except Exception as e:
            return f"Error al obtener la parroquia: {e}"
        finally:
            conn.close()

    def update_parroquia(self, codigo_parroquia, nuevo_nombre):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE parroquias SET nombre_parroquia = %s WHERE codigo_parroquia = %s"
                cursor.execute(sql, (nuevo_nombre, codigo_parroquia))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Parroquia actualizada exitosamente."
                return "Parroquia no encontrada."
        except Exception as e:
            return f"Error al actualizar la parroquia: {e}"
        finally:
            conn.close()

    def delete_parroquia(self, codigo_parroquia):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM parroquias WHERE codigo_parroquia = %s"
                cursor.execute(sql, (codigo_parroquia,))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Parroquia eliminada exitosamente."
                return "Parroquia no encontrada."
        except Exception as e:
            return f"Error al eliminar la parroquia: {e}"
        finally:
            conn.close()
