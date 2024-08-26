from app.models.connect import connect_db
import os
from werkzeug.utils import secure_filename
import logging


class ConfiguracionService:
    def get_configuracion(self, usuario_id):
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM configuraciones_usuario WHERE usuario_id = %s"
                cursor.execute(sql, (usuario_id,))
                result = cursor.fetchone()
                if result:
                    return result
                return "Configuración no encontrada."
        except Exception as e:
            return f"Error al obtener configuración: {e}"
        finally:
            conn.close()

    def save_logo(self, file, upload_folder):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            return file_path
        return None

    def update_configuracion(self, usuario_id, paleta_colores, nombre_aplicacion, tipo_fuente, logo_horizontal, logo_vertical):
        conn = connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM configuraciones_usuario WHERE usuario_id = %s", (usuario_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                sql = """
                        UPDATE configuraciones_usuario
                        SET paleta_colores = %s, nombre_aplicacion = %s, tipo_fuente = %s, logo_horizontal = %s, logo_vertical = %s
                        WHERE usuario_id = %s
                    """
                cursor.execute(sql, (paleta_colores, nombre_aplicacion, tipo_fuente, logo_horizontal, logo_vertical, usuario_id))
                conn.commit()
                return "Configuración actualizada exitosamente."
            else:
                sql = """
                        INSERT INTO configuraciones_usuario (usuario_id, paleta_colores, nombre_aplicacion, tipo_fuente, logo_horizontal, logo_vertical)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                cursor.execute(sql, (usuario_id, paleta_colores, nombre_aplicacion, tipo_fuente, logo_horizontal, logo_vertical))
                conn.commit()
                logging.debug(f"Configuración creada para usuario_id: {usuario_id}")
                return "Configuración creada exitosamente."

        except Exception as e:
            logging.error(f"Error al guardar o actualizar configuración: {e}")
            return f"Error al guardar o actualizar configuración: {e}"
        finally:
            conn.close()

    def allowed_file(self, filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions