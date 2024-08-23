import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
import pydotplus
from sklearn.tree import export_graphviz
from xgboost import XGBRegressor
from os import path
import sys
import unicodedata
from flask_jwt_extended import jwt_required
from app.services.prediccion_service import PrediccionService
import logging

from flask import Blueprint, request, jsonify

predicciones_blueprint = Blueprint("prediccion", __name__)
prediccion_service = PrediccionService()


@predicciones_blueprint.route("/verificarPreparacion", methods=["POST"])
@jwt_required()
def verificacionDePreparacion():
    archivo = request.files["archivo"]
    try:
        x, df = prediccion_service.verificacionDePreparacion(archivo)
        if x is not None:
            if prediccion_service.verificarExistePerido(df):
                logging.debug("El periodo ya existe")
                return jsonify({"message": "El periodo ya existe", "status": "exists"}), 200
            logging.debug("El archivo es apto para predecir")
            return jsonify({"message": "El archivo es apto para predecir", "status": "ready"}), 200
        else:
            logging.debug("El archivo no es apto para predecir")
            return jsonify({"message": "El archivo no es apto para predecir", "status": "invalid"}), 400
    except Exception as e:
        logging.error(f"Error al verificar la preparacion del archivo: {e}")
        return jsonify({"message": "Error el archivo no es cumple con los parametros", "status": "error"}), 400


@predicciones_blueprint.route("/predicirMatricula", methods=["POST"])
@jwt_required()
def predirMatriculas():
    archivo = request.files["archivo"]
    df_prediccion = prediccion_service.predirMatriculas(archivo)
    if prediccion_service.guardarPrediccion(df_prediccion):
        return jsonify(success=True)
    return jsonify(success=False), 400

@predicciones_blueprint.route("/predicciones", methods=["GET"])
def getPredicciones():
    logging.info("Obteniendo predicciones")
    predicciones = prediccion_service.getPredicciones()
    logging.debug(f"Predicciones obtenidas: {predicciones}")
    return jsonify(predicciones)