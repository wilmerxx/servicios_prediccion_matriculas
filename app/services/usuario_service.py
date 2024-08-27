from app.models.connect import connect_db
from app.models.modelo import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import logging
import os
from werkzeug.utils import secure_filename


class UsuarioService:
    def create_usuario(self, username, email, nombre, apellido, password, rol_id, imagen=None):
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
                if imagen:
                    sql = "INSERT INTO usuarios (username, email, nombre, apellido, password, rol_id, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id, imagen))
                else:
                    sql = "INSERT INTO usuarios (username, email, nombre, apellido, password, rol_id) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id))
                conn.commit()
                return "Usuario registrado exitosamente."
        except Exception as e:
            return f"Error al registrar usuario: {e}"
        finally:
            conn.close()

    def update_usuario(self, id, username, email, nombre, apellido, password, rol_id, imagen=None):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                # Verificar si el usuario existe
                sql = "SELECT COUNT(*) FROM usuarios WHERE id = %s"
                cursor.execute(sql, (id,))
                if cursor.fetchone()[0] == 0:
                    return "Usuario no encontrado. Por favor, verifique el ID."

                # Actualizar el usuario
                hashed_password = generate_password_hash(password) if password else None
                if imagen:
                    sql = """
                    UPDATE usuarios
                    SET username = %s, email = %s, nombre = %s, apellido = %s,
                        password = COALESCE(%s, password), rol_id = %s, imagen = %s
                    WHERE id = %s
                    """
                    cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id, imagen, id))
                else:
                    sql = """
                    UPDATE usuarios
                    SET username = %s, email = %s, nombre = %s, apellido = %s,
                        password = COALESCE(%s, password), rol_id = %s
                    WHERE id = %s
                    """
                    cursor.execute(sql, (username, email, nombre, apellido, hashed_password, rol_id, id))
                conn.commit()
                logging.debug(
                    f"Usuario actualizado: {id}, {username}, {email}, {nombre}, {apellido}, {rol_id}, {imagen}")
                return "Usuario actualizado exitosamente."
        except Exception as e:
            logging.error(f"Error al actualizar usuario: {e}")
            return f"Error al actualizar usuario: {e}"
        finally:
            conn.close()

    def save_image_locally(file, upload_folder):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            return file_path
        return None

    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
                        Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario[5], usuario[6], usuario[7]))
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
                    return Usuario(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                return "Usuario no encontrado."
        except Exception as e:
            return f"Error al obtener el usuario: {e}"
        finally:
            conn.close()