from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()


def extract_data(*keys):
    """Extrae y retorna los datos especificados del request JSON."""
    return {key: request.json.get(key) for key in keys}


@auth_blueprint.route('/register', methods=['POST'])
def register():
    required_fields = ['username', 'email', 'nombre', 'apellido', 'password', 'rol_id']
    optional_fields = ['imagen']
    data = extract_data(*required_fields, *optional_fields)
    result = auth_service.register(**data)
    return jsonify({"message": result}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    required_fields = ['username', 'password']
    data = extract_data(*required_fields)
    result = auth_service.login(data['username'], data['password'])
    if isinstance(result, dict):
        return jsonify(result), 200
    return jsonify({"message": result}), 401


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200