from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.connect import connect_db
from app.models.modelo import Usuario
from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService


usuario_blueprint = Blueprint('usuario', __name__)
usuario_service = UsuarioService()


@usuario_blueprint.route('', methods=['POST'])
@jwt_required()
def create_usuario():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    password = data.get('password')
    rol_id = data.get('rol_id')
    result = usuario_service.create_usuario(username, email, nombre, apellido, password, rol_id)
    return jsonify({"message": result}), 201


@usuario_blueprint.route('', methods=['GET'])
@jwt_required()
def get_usuarios():
    result = usuario_service.get_usuarios()
    usuarios = []
    for usuario in result:
        if isinstance(usuario, Usuario):
            usuarios.append(usuario.to_dict())
        else:
            print(f"Advertencia: Se esperaba un objeto Usuario, pero se recibió {type(usuario)}")
    return jsonify(usuarios), 200


@usuario_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_usuario(id):
    result = usuario_service.get_usuario(id)
    if isinstance(result, Usuario):
        return jsonify(result.to_dict()), 200
    else:
        return jsonify({"message": result}), 404


@usuario_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    data = request.json
    nuevo_username = data.get('username')
    nuevo_nombre = data.get('nombre')
    nuevo_apellido = data.get('apellido')
    nuevo_email = data.get('email')
    nuevo_password = data.get('password')
    nuevo_rol_id = data.get('rol_id')
    result = usuario_service.update_usuario(id, nuevo_username,nuevo_email,nuevo_nombre, nuevo_apellido, nuevo_password, nuevo_rol_id)
    return jsonify({"message": result}), 200


@usuario_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(id):
    result = usuario_service.delete_usuario(id)
    return jsonify({"message": result}), 200


