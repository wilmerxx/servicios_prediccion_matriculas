import pymysql
from app.models.modelo import Canton
from app.models.connect import connect_db


class CantonService:
    def create_canton(self, codigo_canton, nombre_canton):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO cantones (codigo_canton, nombre_canton) VALUES (%s, %s)"
                cursor.execute(sql, (codigo_canton, nombre_canton))
                conn.commit()
                return "Canton creado exitosamente."
        except Exception as e:
            return f"Error al crear el canton: {e}"
        finally:
            conn.close()

    def get_cantones(self):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cantones")
                result = cursor.fetchall()
                cantones = []
                for canton in result:
                    cantones.append(Canton(canton[0], canton[1]))
                return cantones
        except Exception as e:
            return f"Error al obtener los cantones: {e}"
        finally:
            conn.close()

    def get_canton(self, codigo_canton):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM cantones WHERE codigo_canton = %s"
                cursor.execute(sql, (codigo_canton,))
                result = cursor.fetchone()
                if result:
                    return Canton(result[0], result[1])
                return "Canton no encontrado."
        except Exception as e:
            return f"Error al obtener el canton: {e}"
        finally:
            conn.close()

    def update_canton(self, codigo_canton, nuevo_nombre):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE cantones SET nombre_canton = %s WHERE codigo_canton = %s"
                cursor.execute(sql, (nuevo_nombre, codigo_canton))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Canton actualizado exitosamente."
                return "Canton no encontrado."
        except Exception as e:
            return f"Error al actualizar el canton: {e}"
        finally:
            conn.close()

    def delete_canton(self, codigo_canton):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM cantones WHERE codigo_canton = %s"
                cursor.execute(sql, (codigo_canton,))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Canton eliminado exitosamente."
                return "Canton no encontrado."
        except Exception as e:
            return f"Error al eliminar el canton: {e}"
        finally:
            conn.close()
