from flask import Blueprint, request, jsonify, url_for, current_app
from app.services.configuracion_service import ConfiguracionService
from flask_jwt_extended import jwt_required
import logging

configuracion_blueprint = Blueprint('configuracion', __name__)
configuracion_service = ConfiguracionService()

@configuracion_blueprint.route('/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_configuracion(usuario_id):
    result = configuracion_service.get_configuracion(usuario_id)
    if isinstance(result, tuple):
        logo_horizontal_url = url_for('uploaded_file', filename=result[5], _external=True) if result[5] else None
        logo_vertical_url = url_for('uploaded_file', filename=result[6], _external=True) if result[6] else None
        return jsonify({
            "paleta_colores": result[2],
            "nombre_aplicacion": result[3],
            "tipo_fuente": result[4],
            "logo_horizontal": logo_horizontal_url,
            "logo_vertical": logo_vertical_url
        }), 200
    else:
        return jsonify({"message": result}), 500

@configuracion_blueprint.route('/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def update_configuracion(usuario_id):
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request form data: {request.form}")
    logging.debug(f"Request files data: {request.files}")

    if not request.form and not request.files:
        return jsonify({"message": "No form data or files received"}), 400

    paleta_colores = request.form.get('paleta_colores')
    nombre_aplicacion = request.form.get('nombre_aplicacion')
    tipo_fuente = request.form.get('tipo_fuente')
    logo_horizontal = request.files.get('logo_horizontal')
    logo_vertical = request.files.get('logo_vertical')

    upload_folder = current_app.config['UPLOAD_FOLDER']
    logo_horizontal_path = configuracion_service.save_logo(logo_horizontal, upload_folder) if logo_horizontal else None
    logo_vertical_path = configuracion_service.save_logo(logo_vertical, upload_folder) if logo_vertical else None

    result = configuracion_service.update_configuracion(
        usuario_id, paleta_colores, nombre_aplicacion, tipo_fuente,
        logo_horizontal_path, logo_vertical_path
    )
    return jsonify({"message": result}), 200