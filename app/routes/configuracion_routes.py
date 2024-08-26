from flask import Blueprint, request, jsonify, url_for, current_app
from app.services.configuracion_service import ConfiguracionService
from flask_jwt_extended import jwt_required
import logging
# Import the secure_filename function at the top of the file
from werkzeug.utils import secure_filename
import os
configuracion_blueprint = Blueprint('configuracion', __name__)
configuracion_service = ConfiguracionService()


def generate_logo_url(filename):
    """Genera la URL externa para un archivo subido si el nombre de archivo es válido."""
    return url_for('uploaded_file', filename=filename, _external=True) if filename else None


@configuracion_blueprint.route('/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_configuracion(usuario_id):
    result = configuracion_service.get_configuracion(usuario_id)
    if isinstance(result, tuple):
        logo_horizontal_url = generate_logo_url(result[5])
        logo_vertical_url = generate_logo_url(result[6])
        return jsonify({
            "paleta_colores": result[2],
            "nombre_aplicacion": result[3],
            "tipo_fuente": result[4],
            "logo_horizontal": logo_horizontal_url,
            "logo_vertical": logo_vertical_url
        }), 200
    return jsonify({"message": result}), 500


@configuracion_blueprint.route('/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def update_configuracion(usuario_id):
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request form data: {request.form}")
    logging.debug(f"Request files data: {request.files}")

    if not request.form and not request.files:
        return jsonify({"message": "No form data or files received"}), 400

    # Extracción de datos del formulario
    paleta_colores = request.form.get('paleta_colores')
    nombre_aplicacion = request.form.get('nombre_aplicacion')
    tipo_fuente = request.form.get('tipo_fuente')

    # Manejo de los archivos de logos
    upload_folder = current_app.config['UPLOAD_FOLDER']
    logo_horizontal_path = save_logo_if_present('logo_horizontal', upload_folder)
    logo_vertical_path = save_logo_if_present('logo_vertical', upload_folder)

    result = configuracion_service.update_configuracion(
        usuario_id, paleta_colores, nombre_aplicacion, tipo_fuente,
        logo_horizontal_path, logo_vertical_path
    )
    return jsonify({"message": result}), 200



def save_logo_if_present(field_name, upload_folder):
    """Guarda el logo si está presente en los archivos del request."""
    logo_file = request.files.get(field_name)
    if logo_file:
        filename = secure_filename(logo_file.filename)
        file_path = os.path.join(upload_folder, filename)
        logo_file.save(file_path)
        return filename
    return None