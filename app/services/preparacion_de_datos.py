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
import os
import sys
import unicodedata
from app.models.connect import connect_db
import category_encoders as ce
import joblib
from app.models.modelo import Prediccion


class PreparacionDeDatos:

    # verificacion del archivo si es acto para el modelo
    @staticmethod
    def verificar_archivo(archivo):
        if archivo.filename.endswith('.csv'):
            return True
        return False

    # lectura del archivo
    @staticmethod
    def leer_archivo(archivo):
        df = pd.read_csv(archivo, delimiter=";", encoding='utf-8')
        return df

    # formatos del titulo
    @staticmethod
    def formaterTitulo(df):
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.upper()
        df.columns = df.columns.str.replace(' ', '')
        df.columns = df.columns.str.replace('-', '')
        df.columns = df.columns.str.replace('_', '')
        df.columns = df.columns.str.replace('/', '_')
        df.columns = df.columns.str.replace('(', '')
        df.columns = df.columns.str.replace(')', '')
        df.columns = df.columns.str.replace('.', '')
        df.columns = df.columns.str.replace(',', '')
        df.columns = df.columns.str.replace('Á', 'A')
        df.columns = df.columns.str.replace('É', 'E')
        df.columns = df.columns.str.replace('Í', 'I')
        df.columns = df.columns.str.replace('Ó', 'O')
        df.columns = df.columns.str.replace('Ú', 'U')
        df.columns = df.columns.str.replace('Ñ', 'N')
        df.columns = df.columns.str.replace('Ü', 'U')
        df.columns = df.columns.str.replace('Ã', 'A')
        df.columns = df.columns.str.replace('Ä', 'A')
        df.columns = df.columns.str.replace('Ö', 'O')
        df.columns = df.columns.str.replace('Ü', 'U')
        df.columns = df.columns.str.replace('Ñ', 'N')
        df.columns = df.columns.str.replace('Ç', 'C')
        return df

    # cambiar los nombres de las columnas
    @staticmethod
    def mapearColumnas(df):
        column_mapping = {
            'ANOLECTIVO': 'PERIODO',
            'NOMBREDELPERIODO': 'PERIODO',
            'ZONAINEC': 'AREA',
            'CODIGOINSTITUCION': 'AMIE',
            'FORMAACCESO': 'ACCESOEDIFICIO',
            'CODIGODEPROVINCIA': 'CODPROVINCIA',
            'CODIGODECANTON': 'CODCANTON',
            'CODIGODEPARROQUIA': 'CODPARROQUIA',
            'MODALLIDAD': 'MODALIDAD',
            'TIPODEEDUCACION': 'TIPOEDUCACION',
            'TENENCIADELINMUEBLE': 'TENENCIAINMUEBLEEDIFICIO',
        }

        # Renombrara las columnas
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df.rename(columns={old_name: new_name}, inplace=True)
        return df

    # seleccionar las columnas
    @staticmethod
    def seleccionColumnas(df):
        columnas = ['PERIODO',
                    'ZONA',
                    'CODPROVINCIA',
                    'CODPARROQUIA',
                    'CODCANTON',
                    'AMIE',
                    'TIPOEDUCACION',
                    'NIVELEDUCACION',
                    'SOSTENIMIENTO',
                    'AREA',
                    'REGIMENESCOLAR',
                    'JURISDICCION',
                    'MODALIDAD',
                    'JORNADA',
                    'TENENCIAINMUEBLEEDIFICIO',
                    'ACCESOEDIFICIO',
                    'DOCENTESFEMENINO',
                    'DOCENTESMASCULINO',
                    'TOTALDOCENTES',
                    'ADMINISTRATIVOSFEMENINO',
                    'ADMINISTRATIVOSMASCULINO',
                    'TOTALADMINISTRATIVOS',
                    'ESTUDIANTESFEMENINOTERCERANOBACH',
                    'ESTUDIANTESMASCULINOTERCERANOBACH',
                    'ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH',
                    'ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH',
                    'ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH',
                    'ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH',
                    'ESTUDIANTESFEMENINODESERTORESTERCERANOBACH',
                    'ESTUDIANTESMASCULINODESERTORESTERCERANOBACH',
                    'ESTUDIANTESFEMENINONOACTUALIZADOTERCERANOBACH',
                    'ESTUDIANTESMASCULINONOACTUALIZADOTERCERANOBACH']

        dataset = df[columnas]

        return dataset

    # llenar los valores nulos de cada dataset
    @staticmethod
    def llenarValoresNulos(df):
        df.fillna(0, inplace=True)
        return df

    @staticmethod
    def cambiartipoDato(dataset):
        for col in dataset.columns:

            if dataset[col].dtype == 'object':
                dataset[col] = dataset[col].astype('category')

            if dataset[col].dtype == 'float64':
                dataset[col] = dataset[col].astype('int64')

        return dataset

    @staticmethod
    def eliminar_tildes(texto):
        """Eliminar tildes de un texto dado."""
        if not isinstance(texto, str):
            return texto
        texto_normalizado = unicodedata.normalize('NFD', texto)
        return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

    @staticmethod
    def normalizar_texto(df):
        # Paso 1: Convertir columnas categóricas a string temporalmente
        cat_columns = df.select_dtypes(['category']).columns
        df[cat_columns] = df[cat_columns].astype(str)

        # Paso 2: Reemplazar valores nulos por una cadena vacía para evitar errores
        df['PERIODO'].fillna('', inplace=True)
        df['TENENCIAINMUEBLEEDIFICIO'].fillna('', inplace=True)
        df['AREA'].fillna('', inplace=True)

        # Paso 3: Definir una función auxiliar para limpiar texto
        def limpiar_texto(columna, reemplazos):
            df[columna] = df[columna].apply(lambda x: x.strip() if isinstance(x, str) else x)
            for antiguo, nuevo in reemplazos.items():
                df[columna] = df[columna].apply(lambda x: x.replace(antiguo, nuevo) if isinstance(x, str) else x)

        # Paso 4: Aplicar las transformaciones necesarias
        limpiar_texto('PERIODO', {'Fin': ''})
        limpiar_texto('TENENCIAINMUEBLEEDIFICIO', {'?': 'ó'})
        limpiar_texto('AREA', {'INEC': ''})

        # convertir en mayusculas
        df[cat_columns] = df[cat_columns].apply(lambda x: x.str.upper())

        # limpieza de tildes
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: PreparacionDeDatos.eliminar_tildes(x))
                # Paso 5: Volver a convertir las columnas categóricas a su tipo original
        df[cat_columns] = df[cat_columns].apply(lambda x: x.str.strip())
        df[cat_columns] = df[cat_columns].astype('category')

        return df

    @staticmethod
    def calcularTotalEstudiantes(df, nombreColun, columna1, columna2):
        df[nombreColun] = df[columna1] + df[columna2]
        return df

    @staticmethod
    def calcular_indicador(numerador, denominador):
        """
        Calcula un indicador basado en una división.
        Este indicador puede representar una tasa, una razón, etc.

        :param numerador: El valor del numerador (p. ej., estudiantes promovidos, total de estudiantes).
        :param denominador: El valor del denominador (p. ej., total de estudiantes, total de docentes).
        :return: El valor del indicador, o 0 si el denominador es cero.
        """
        if denominador == 0:
            return 0
        return numerador / denominador

    @staticmethod
    def calcular_indicadores(df_indicadores):
        # Calcular el total de estudiantes en tercer año de bachillerato
        df_calculado = PreparacionDeDatos.calcularTotalEstudiantes(df_indicadores, 'TOTAL_ESTUDIANTESTERCERANOBACH', 'ESTUDIANTESFEMENINOTERCERANOBACH', 'ESTUDIANTESMASCULINOTERCERANOBACH')

        # Calcular el total de estudiantes promovidos en tercer año de bachillerato
        df_calculado = PreparacionDeDatos.calcularTotalEstudiantes(df_calculado, 'TOTAL_PROMOVIDOSTERCERANOBACH', 'ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH', 'ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH')

        # Calcular la tasa de promoción (porcentaje de estudiantes promovidos sobre el total de estudiantes)
        df_calculado['TASA_PROMOCION'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTAL_PROMOVIDOSTERCERANOBACH'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        # Calcular el total de estudiantes que desertaron en tercer año de bachillerato
        df_calculado = PreparacionDeDatos.calcularTotalEstudiantes(df_calculado, 'TOTAL_DESERTORESTERCERANOBACH', 'ESTUDIANTESFEMENINODESERTORESTERCERANOBACH', 'ESTUDIANTESMASCULINODESERTORESTERCERANOBACH')

        # Calcular la tasa de deserción (porcentaje de estudiantes que desertaron sobre el total de estudiantes)
        df_calculado['TASA_DESERCION'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTAL_DESERTORESTERCERANOBACH'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        # Calcular la proporción de docentes por estudiante (número de docentes por cada estudiante)
        df_calculado['PROPORCION_DOCENTES_ESTUDIANTE'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTALDOCENTES'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        # Calcular la proporción de administrativos por estudiante (número de administrativos por cada estudiante)
        df_calculado['PROPORCION_ADMINISTRATIVOS_ESTUDIANTE'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTALADMINISTRATIVOS'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        # Calcular el total de estudiantes no actualizados en tercer año de bachillerato
        df_calculado = PreparacionDeDatos.calcularTotalEstudiantes(df_calculado, 'TOTAL_NOACTUALIZADOTERCERANOBACH', 'ESTUDIANTESFEMENINONOACTUALIZADOTERCERANOBACH', 'ESTUDIANTESMASCULINONOACTUALIZADOTERCERANOBACH')

        # Calcular la proporción de estudiantes no actualizados (porcentaje de estudiantes no actualizados sobre el total de estudiantes)
        df_calculado['PROPORCION_NOACTUALIZADOS'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTAL_NOACTUALIZADOTERCERANOBACH'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        # Calcular el total de estudiantes no promovidos en tercer año de bachillerato
        df_calculado = PreparacionDeDatos.calcularTotalEstudiantes(df_calculado, 'TOTAL_NOPROMOVIDOSTERCERANOBACH', 'ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH', 'ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH')

        # Calcular la proporción de estudiantes no promovidos (porcentaje de estudiantes no promovidos sobre el total de estudiantes)
        df_calculado['PROPORCION_NOPROMOVIDOS'] = df_calculado.apply(
            lambda row: PreparacionDeDatos.calcular_indicador(row['TOTAL_NOPROMOVIDOSTERCERANOBACH'],
                                           row['TOTAL_ESTUDIANTESTERCERANOBACH']), axis=1)

        return df_calculado

    @staticmethod
    def crearOjetoLeabelEncoder(df_indicadores):
        # Crea un objeto LabelEncoder
        le = LabelEncoder()

        # Ajusta el codificador a los valores únicos en la columna 'PERIODO'
        le.fit(df_indicadores['PERIODO'])

        # Transforma la columna 'PERIODO' usando el codificador
        df_indicadores['PERIODO_CODIFICADO'] = le.transform(df_indicadores['PERIODO'])

        return df_indicadores

    @staticmethod
    def eliminarFilasEnCero(df, columna):
        df = df[df[columna] != 0]
        return df

    # Crear una función para descomponer el período
    @staticmethod
    def descomponer_periodo(periodo):
        inicio, fin = periodo.split('-')
        return int(inicio), int(fin)  # Return a tuple

    # Asegúrate de que asignar_meses devuelve una tupla con dos elementos.
    @staticmethod
    def asignar_meses(regimen):
        periodos_escolares = {
            'SIERRA': {'INICIO': 'SEPTIEMBRE', 'FIN': 'JULIO'},
            'COSTA': {'INICIO': 'MAYO', 'FIN': 'FEBRERO'},
            'PERMANENTE': {'INICIO': 'MAYO', 'FIN': 'FEBRERO'}
        }
        # Convert dictionary values to a tuple before returning
        return tuple(periodos_escolares.get(regimen.upper(), {'INICIO': None, 'FIN': None}).values())

    # Seleccionar las características y la variable objetivo
    @staticmethod
    def seleccionar_caracteristicas_objetivo():
        # Seleccionar las características relevantes
        features = [
            'ZONA',
            'CODPROVINCIA',
            'CODPARROQUIA',
            'CODCANTON',
            'TIPOEDUCACION',
            'NIVELEDUCACION',
            'SOSTENIMIENTO',
            'AREA',
            'REGIMENESCOLAR',
            'JURISDICCION',
            'MODALIDAD',
            'JORNADA',
            'TENENCIAINMUEBLEEDIFICIO',
            'ACCESOEDIFICIO',
            'TOTALDOCENTES',
            'TOTALADMINISTRATIVOS',
            'ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH',
            'ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH',
            'TASA_PROMOCION',
            'TASA_DESERCION',
            'PROPORCION_DOCENTES_ESTUDIANTE',
            'PROPORCION_ADMINISTRATIVOS_ESTUDIANTE',
            'PROPORCION_NOACTUALIZADOS',
            'PROPORCION_NOPROMOVIDOS',
            'ANIO',
            'MES_INICIO',
            'MES_FIN'
        ]

        # Seleccionar la variable objetivo
        target = 'TOTAL_PROMOVIDOSTERCERANOBACH'

        # Crear el codificador TargetEncoder
        encoded_features = [
            'ZONA',
            'CODPROVINCIA',
            'CODPARROQUIA',
            'CODCANTON',
            'TIPOEDUCACION',
            'NIVELEDUCACION',
            'SOSTENIMIENTO',
            'AREA',
            'REGIMENESCOLAR',
            'JURISDICCION',
            'MODALIDAD',
            'JORNADA',
            'TENENCIAINMUEBLEEDIFICIO',
            'ACCESOEDIFICIO',
            'ANIO',
            'MES_INICIO',
            'MES_FIN'
        ]

        return features, target, encoded_features

    # Crear una función para dividir el conjunto de datos en conjuntos de entrenamiento y prueba
    @staticmethod
    def codificar_categoricas_predict(df, features, target, encoded_features):
        """
            Codifica las características categóricas utilizando TargetEncoder y divide los datos en entrenamiento y prueba.

            Parámetros:
            - df: DataFrame con los datos.
            - features: Lista de nombres de las características.
            - encoded_features: Lista de nombres de las características a codificar.

            Retorna:
            - X__encoded: Conjunto de datos de entrenamiento codificado.
            """
        # Dividir los datos en características (X) y la variable objetivo (y)
        X = df[features]
        y = df[target]
        # Crear el codificador TargetEncoder
        encoder = ce.TargetEncoder(cols=encoded_features)

        # Ajustar el codificador a los datos de entrenamiento y transformar tanto los datos de entrenamiento como los de prueba
        x_encoded = encoder.fit_transform(X, y)

        return x_encoded

    @staticmethod
    def cargar_modelo():
        model_path = 'app/models/xgb_model.pkl'

        if os.path.exists(model_path):
            # Load the existing model
            with open(model_path, 'rb') as f:
                modelo = joblib.load(f)
        else:
            raise FileNotFoundError(f"No such file or directory: '{model_path}'")

        return modelo

    @staticmethod
    def predirMatriculas(df_indicadores_predict, loaded_model, X_encoded):
        # Realizar predicciones en el conjunto de datos codificado
        y_pred = loaded_model.predict(X_encoded)

        # Agregar las predicciones al DataFrame original
        df_indicadores_predict['PREDICCION_PROMOVIDOS'] = y_pred

        # convertir a enteros
        df_indicadores_predict['PREDICCION_PROMOVIDOS'] = df_indicadores_predict['PREDICCION_PROMOVIDOS'].astype(int)

        # Mostrar el DataFrame con las predicciones
        df_indicadores_predict['TOTAL_PROMOVIDOS'] = df_indicadores_predict['ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH'] + df_indicadores_predict['ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH']

        return df_indicadores_predict

    def guardar_datos_predichos(self, df_predictivo):
        # Conectar a la base de datos
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                for _, row in df_predictivo.iterrows():
                    cursor.execute("""
                        INSERT INTO predicciones (
                            PERIODO, ZONA, CODPROVINCIA, CODPARROQUIA, CODCANTON, AMIE, TIPOEDUCACION, NIVELEDUCACION,
                            SOSTENIMIENTO, AREA, REGIMENESCOLAR, JURISDICCION, MODALIDAD, JORNADA, TENENCIAINMUEBLEEDIFICIO,
                            ACCESOEDIFICIO, DOCENTESFEMENINO, DOCENTESMASCULINO, TOTALDOCENTES, ADMINISTRATIVOSFEMENINO,
                            ADMINISTRATIVOSMASCULINO, TOTALADMINISTRATIVOS, ESTUDIANTESFEMENINOTERCERANOBACH,
                            ESTUDIANTESMASCULINOTERCERANOBACH, ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH,
                            ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH, ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH,
                            ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH, ESTUDIANTESFEMENINODESERTORESTERCERANOBACH,
                            ESTUDIANTESMASCULINODESERTORESTERCERANOBACH, ESTUDIANTESFEMENINONOACTUALIZADOTERCERANOBACH,
                            ESTUDIANTESMASCULINONOACTUALIZADOTERCERANOBACH, TOTAL_ESTUDIANTESTERCERANOBACH,
                            TOTAL_PROMOVIDOSTERCERANOBACH, TASA_PROMOCION, TOTAL_DESERTORESTERCERANOBACH, TASA_DESERCION,
                            PROPORCION_DOCENTES_ESTUDIANTE, PROPORCION_ADMINISTRATIVOS_ESTUDIANTE, TOTAL_NOACTUALIZADOTERCERANOBACH,
                            PROPORCION_NOACTUALIZADOS, TOTAL_NOPROMOVIDOSTERCERANOBACH, PROPORCION_NOPROMOVIDOS, ANIO_INICIO,
                            ANIO_FIN, MES_INICIO, MES_FIN, PREDICCION_PROMOVIDOS
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row['PERIODO'], row['ZONA'], row['CODPROVINCIA'], row['CODPARROQUIA'], row['CODCANTON'],
                        row['AMIE'],
                        row['TIPOEDUCACION'], row['NIVELEDUCACION'], row['SOSTENIMIENTO'], row['AREA'],
                        row['REGIMENESCOLAR'],
                        row['JURISDICCION'], row['MODALIDAD'], row['JORNADA'], row['TENENCIAINMUEBLEEDIFICIO'],
                        row['ACCESOEDIFICIO'],
                        row['DOCENTESFEMENINO'], row['DOCENTESMASCULINO'], row['TOTALDOCENTES'],
                        row['ADMINISTRATIVOSFEMENINO'],
                        row['ADMINISTRATIVOSMASCULINO'], row['TOTALADMINISTRATIVOS'],
                        row['ESTUDIANTESFEMENINOTERCERANOBACH'],
                        row['ESTUDIANTESMASCULINOTERCERANOBACH'], row['ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH'],
                        row['ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH'],
                        row['ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH'],
                        row['ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH'],
                        row['ESTUDIANTESFEMENINODESERTORESTERCERANOBACH'],
                        row['ESTUDIANTESMASCULINODESERTORESTERCERANOBACH'],
                        row['ESTUDIANTESFEMENINONOACTUALIZADOTERCERANOBACH'],
                        row['ESTUDIANTESMASCULINONOACTUALIZADOTERCERANOBACH'], row['TOTAL_ESTUDIANTESTERCERANOBACH'],
                        row['TOTAL_PROMOVIDOSTERCERANOBACH'], row['TASA_PROMOCION'],
                        row['TOTAL_DESERTORESTERCERANOBACH'],
                        row['TASA_DESERCION'], row['PROPORCION_DOCENTES_ESTUDIANTE'],
                        row['PROPORCION_ADMINISTRATIVOS_ESTUDIANTE'],
                        row['TOTAL_NOACTUALIZADOTERCERANOBACH'], row['PROPORCION_NOACTUALIZADOS'],
                        row['TOTAL_NOPROMOVIDOSTERCERANOBACH'],
                        row['PROPORCION_NOPROMOVIDOS'], row['ANIO_INICIO'], row['ANIO_FIN'], row['MES_INICIO'],
                        row['MES_FIN'],
                        row['PREDICCION_PROMOVIDOS']
                    ))
                conn.commit()
        finally:
            conn.close()

    def obtener_predicciones(self):
        # Conectar a la base de datos
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM vista_prediccion
                """)
                result = cursor.fetchall()
                predicciones = []
                for prediccion in result:
                    prediccion_obj = Prediccion(prediccion[0], prediccion[1], prediccion[2], prediccion[3],
                                                prediccion[4], prediccion[5],
                                                prediccion[6], prediccion[7], prediccion[8], prediccion[9],
                                                prediccion[10], prediccion[11],
                                                prediccion[12], prediccion[13], prediccion[14], prediccion[15],
                                                prediccion[16], prediccion[17],
                                                prediccion[18], prediccion[19], prediccion[20], prediccion[21],
                                                prediccion[22], prediccion[23],
                                                prediccion[24], prediccion[25], prediccion[26], prediccion[27],
                                                prediccion[28], prediccion[29],
                                                prediccion[30], prediccion[31], prediccion[32], prediccion[33],
                                                prediccion[34], prediccion[35],
                                                prediccion[36])
                    predicciones.append(prediccion_obj.to_dict())
                return predicciones
        finally:
            conn.close()

    def existePerido(self, periodo):
        # Conectar a la base de datos
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM predicciones WHERE ANIO_FIN = %s
                """, (periodo,))
                result = cursor.fetchone()
                if result:
                    return True
                return False
        finally:
            conn.close()

    @staticmethod
    def eliminarPredicciones(anio_fin):
        # Conectar a la base de datos
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM predicciones WHERE ANIO_FIN = %s
                """, (anio_fin,))
                conn.commit()
        finally:
            conn.close()
