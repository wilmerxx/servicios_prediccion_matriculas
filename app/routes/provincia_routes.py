from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.provincia_service import ProvinciaService
from app.models.modelo import Provincia

provincia_blueprint = Blueprint('provincia', __name__)
provincia_service = ProvinciaService()


@provincia_blueprint.route('', methods=['POST'])
@jwt_required()
def create_provincia():
    data = request.json
    codigo_provincia = data.get('codigo_provincia')
    nombre_provincia = data.get('nombre_provincia')
    result = provincia_service.create_provincia(codigo_provincia, nombre_provincia)
    return jsonify({"message": result}), 201


@provincia_blueprint.route('', methods=['GET'])
@jwt_required()
def get_provincias():
    result = provincia_service.get_provincias()
    provincias = []
    for provincia in result:
        provincias.append(provincia.to_dict())
    return jsonify(provincias), 200


@provincia_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_provincia(id):
    result = provincia_service.get_provincia(id)
    if isinstance(result, Provincia):
        return jsonify(result.to_dict()), 200
    else:
        return jsonify({"message": result}), 404


@provincia_blueprint.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_provincia(id):
    data = request.json
    nuevo_nombre = data.get('nombre_provincia')
    result = provincia_service.update_provincia(id, nuevo_nombre)
    return jsonify({"message": result}), 200


@provincia_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_provincia(id):
    result = provincia_service.delete_provincia(id)
    return jsonify({"message": result}), 200
