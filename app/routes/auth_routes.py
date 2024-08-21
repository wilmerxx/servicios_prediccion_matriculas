from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    password = data.get('password')
    rol_id = data.get('rol_id')
    result = auth_service.register(username, email, nombre, apellido, password, rol_id)
    return jsonify({"message": result}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = auth_service.login(username, password)
    if isinstance(result, dict):
        return jsonify(result), 200
    else:
        return jsonify({"message": result}), 401


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200


