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
from app.services.preparacion_de_datos import PreparacionDeDatos
import logging


class PrediccionService:

    def __init__(self):
        self.preparacion_de_datos = PreparacionDeDatos()

    def verificacionDePreparacion(self, archivo):

        # lectura del archivo
        df = self.preparacion_de_datos.leer_archivo(archivo)

        # formateo de titulos
        df = self.preparacion_de_datos.formaterTitulo(df)

        # mapeo de columnas
        df = self.preparacion_de_datos.mapearColumnas(df)

        # seleccionar columnas
        df = self.preparacion_de_datos.seleccionColumnas(df)

        # llenar los valores nulos de cada dataset
        df = self.preparacion_de_datos.llenarValoresNulos(df)

        # cambiar tipo de dato
        df = self.preparacion_de_datos.cambiartipoDato(df)

        # normalizar texto
        df = self.preparacion_de_datos.normalizar_texto(df)

        # calcular indicadores
        df = self.preparacion_de_datos.calcular_indicadores(df)

        # Crear objeto LabelEncoder
        df = self.preparacion_de_datos.crearOjetoLeabelEncoder(df)

        # eliminar filas de ceros
        df_indicadores = self.preparacion_de_datos.eliminarFilasEnCero(df, 'TOTAL_ESTUDIANTESTERCERANOBACH')

        # Aplicar la función a la columna 'PERIODO' y crear columnas separadas
        # Aplicar la función al DataFrame y extraer los valores como listas
        # Aplicar la función a la columna 'PERIODO' y crear columnas separadas
        df_indicadores.loc[:, 'ANIO_INICIO'] = df_indicadores['PERIODO'].apply(lambda x: self.preparacion_de_datos.descomponer_periodo(x)[0])
        df_indicadores.loc[:, 'ANIO_FIN'] = df_indicadores['PERIODO'].apply(lambda x: self.preparacion_de_datos.descomponer_periodo(x)[1])
        # anio
        df_indicadores.loc[:, 'ANIO'] = df_indicadores['ANIO_FIN']

        # Asignar los valores utilizando .loc para evitar el SettingWithCopyWarning
        df_indicadores.loc[:, 'MES_INICIO'] = df_indicadores['REGIMENESCOLAR'].apply(lambda x: self.preparacion_de_datos.asignar_meses(x)[0])
        df_indicadores.loc[:, 'MES_FIN'] = df_indicadores['REGIMENESCOLAR'].apply(lambda x: self.preparacion_de_datos.asignar_meses(x)[1])

        # eliminar los ceros del total de pormovidos
        df_periodos_actules = df_indicadores[df_indicadores['TOTAL_PROMOVIDOSTERCERANOBACH'] != 0]

        # Eliminar filas con valores nulos o ceros en 'TOTAL_PROMOVIDOSTERCERANOBACH'
        df_periodos_actules_predict = df_periodos_actules[
            (df_periodos_actules['TOTAL_PROMOVIDOSTERCERANOBACH'].notnull()) &
            (df_periodos_actules['TOTAL_PROMOVIDOSTERCERANOBACH'] != 0)]

        features, target, encoded_features = self.preparacion_de_datos.seleccionar_caracteristicas_objetivo()

        # Crear una función para dividir el conjunto de datos en conjuntos de entrenamiento y prueba
        x_encoded = self.preparacion_de_datos.codificar_categoricas_predict(df_periodos_actules_predict, features, target, encoded_features)

        return x_encoded, df_periodos_actules_predict

    def verificarExistePerido(self,df):
        try:
            anio_fin = df['ANIO_FIN'].iloc[0]  # Ensure correct extraction of ANIO_FIN
            if self.preparacion_de_datos.existePerido(anio_fin):
                return True
            return False
        except Exception as e:
            logging.error(f"Error al verificar si existe el periodo: {e}")
            return False

    def predirMatriculas(self, archivo):
        x_encoded, df = self.verificacionDePreparacion(archivo)

        # cargar modelo
        modelo = self.preparacion_de_datos.cargar_modelo()

        # entrenar modelo
        df_predictivo = self.preparacion_de_datos.predirMatriculas(df, modelo, x_encoded)

        return df_predictivo

    def guardarPrediccion(self, df_predictivo):
        # Verificar si el periodo existe
        if self.verificarExistePerido(df_predictivo):
            # Eliminar predicciones existentes para el periodo
            anio_fin = df_predictivo['ANIO_FIN'].iloc[0]
            self.preparacion_de_datos.eliminarPredicciones(anio_fin)

        # Guardar prediccion
        self.preparacion_de_datos.guardar_datos_predichos(df_predictivo)
        return "Prediccion realizada y guardada exitosamente."

    def getPredicciones(self):
        return self.preparacion_de_datos.obtener_predicciones()