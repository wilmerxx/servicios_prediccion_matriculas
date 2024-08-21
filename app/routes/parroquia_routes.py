from flask import Blueprint, request, jsonify
from app.services.parroquia_service import ParroquiaService
from app.models.modelo import Parroquia
from flask_jwt_extended import jwt_required
parroquia_blueprint = Blueprint('parroquia', __name__)
parroquia_service = ParroquiaService()


@parroquia_blueprint.route('', methods=['POST'])
@jwt_required()
def create_parroquia():
    data = request.json
    codigo_parroquia = data.get('codigo_parroquia')
    nombre_parroquia = data.get('nombre_parroquia')
    result = parroquia_service.create_parroquia(codigo_parroquia, nombre_parroquia)
    return jsonify({"message": result}), 201


@parroquia_blueprint.route('', methods=['GET'])
@jwt_required()
def get_parroquias():
    result = parroquia_service.get_parroquias()
    parroquias = []
    for parroquia in result:
        parroquias.append(parroquia.to_dict())
    return jsonify(parroquias), 200


@parroquia_blueprint.route('/<codigo_parroquia>', methods=['GET'])
@jwt_required()
def get_parroquia(codigo_parroquia):
    result = parroquia_service.get_parroquia(codigo_parroquia)
    if isinstance(result, Parroquia):
        return jsonify(result.to_dict()), 200
    else:
        return jsonify({"message": result}), 404


@parroquia_blueprint.route('/<codigo_parroquia>', methods=['PUT'])
@jwt_required()
def update_parroquia(codigo_parroquia):
    data = request.json
    nuevo_nombre = data.get('nombre_parroquia')
    result = parroquia_service.update_parroquia(codigo_parroquia, nuevo_nombre)
    return jsonify({"message": result}), 200


@parroquia_blueprint.route('/<codigo_parroquia>', methods=['DELETE'])
@jwt_required()
def delete_parroquia(codigo_parroquia):
    result = parroquia_service.delete_parroquia(codigo_parroquia)
    return jsonify({"message": result}), 200
