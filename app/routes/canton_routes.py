from flask import Blueprint, request, jsonify
from app.services.canton_service import CantonService
from flask_jwt_extended import jwt_required
from app.models.modelo import Canton
canton_blueprint = Blueprint('canton', __name__)
canton_service = CantonService()


@canton_blueprint.route('', methods=['POST'])
@jwt_required()
def create_canton():
    data = request.json
    codigo_canton = data.get('codigo_canton')
    nombre_canton = data.get('nombre_canton')
    result = canton_service.create_canton(codigo_canton, nombre_canton)
    return jsonify({"message": result}), 201

@canton_blueprint.route('', methods=['GET'])
@jwt_required()
def get_cantones():
    result = canton_service.get_cantones()
    cantones = []
    for canton in result:
        cantones.append(canton.to_dict())
    return jsonify(cantones), 200

@canton_blueprint.route('/<codigo_canton>', methods=['GET'])
@jwt_required()
def get_canton(codigo_canton):
    result = canton_service.get_canton(codigo_canton)
    if isinstance(result, Canton):
        return jsonify(result.to_dict()), 200
    else:
        return jsonify({"message": result}), 404

@canton_blueprint.route('/<codigo_canton>', methods=['PUT'])
@jwt_required()
def update_canton(codigo_canton):
    data = request.json
    nuevo_nombre = data.get('nombre_canton')
    result = canton_service.update_canton(codigo_canton, nuevo_nombre)
    return jsonify({"message": result}), 200

@canton_blueprint.route('/<codigo_canton>', methods=['DELETE'])
@jwt_required()
def delete_canton(codigo_canton):
    result = canton_service.delete_canton(codigo_canton)
    return jsonify({"message": result}), 200
