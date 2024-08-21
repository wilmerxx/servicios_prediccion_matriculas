from app.models.connect import connect_db
from app.models.modelo import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


class UsuarioService:
    def create_usuario(self, username, email, nombre, apellido, password, rol_id):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                # Verificar si el rol existe
                sql = "SELECT COUNT(*) FROM roles WHERE id = %s"
                cursor.execute(sql, (rol_id,))
                if cursor.fetchone()[0] == 0:
                    return "Rol no encontrado. Por favor, seleccione un rol válido."

                # Registrar el usuario
                hashed_password = generate_password_hash(password)
                sql = "INSERT INTO usuarios (username, email, nombre, apellido, password, rol_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id))
                conn.commit()
                return "Usuario registrado exitosamente."
        except Exception as e:
            return f"Error al registrar usuario: {e}"
        finally:
            conn.close()

    def get_usuarios(self):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM usuarios"
                cursor.execute(sql)
                result = cursor.fetchall()
                usuarios = []
                for usuario in result:
                    usuarios.append(
                        Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario[5], usuario[6]))
                return usuarios
        except Exception as e:
            return f"Error al obtener los usuarios: {e}"
        finally:
            conn.close()

    def get_usuario(self, id):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                if result:
                    return Usuario(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                return "Usuario no encontrado."
        except Exception as e:
            return f"Error al obtener el usuario: {e}"
        finally:
            conn.close()

    def update_usuario(self, id, username, email, nombre, apellido, password, rol_id):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                hashed_password = generate_password_hash(password)
                sql = "UPDATE usuarios SET username = %s, email = %s, nombre = %s, apellido = %s, password = %s, rol_id = %s WHERE id = %s"
                cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id, id))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Usuario actualizado exitosamente."
                return "Usuario no encontrado."
        except Exception as e:
            return f"Error al actualizar el usuario: {e}"
        finally:
            conn.close()


    def delete_usuario(self, id):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM usuarios WHERE id = %s"
                cursor.execute(sql, (id,))
                conn.commit()
                if cursor.rowcount > 0:
                    return "Usuario eliminado exitosamente."
                return "Usuario no encontrado."
        except Exception as e:
            return f"Error al eliminar el usuario: {e}"
        finally:
            conn.close()
