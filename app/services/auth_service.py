from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.connect import connect_db
from app.models.modelo import Usuario


class AuthService:
    @staticmethod
    def register(username, email, nombre, apellido, password, rol_id):
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

    @staticmethod
    def login(username, password):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, username, email, nombre, apellido, password, rol_id FROM usuarios WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()
                if user and check_password_hash(user[5], password):
                    access_token = create_access_token(identity={
                        'id': user[0],
                        'username': user[1],
                        'email': user[2],
                        'nombre': user[3],
                        'apellido': user[4],
                        'rol_id': user[6]
                    })
                    return {
                        'id': user[0],
                        'username': user[1],
                        'access_token': access_token
                    }
                return "Credenciales inválidas."
        except Exception as e:
            return f"Error al iniciar sesión: {e}"
        finally:
            conn.close()