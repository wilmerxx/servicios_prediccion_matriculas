from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from app.routes import provincia_routes, canton_routes, parroquia_routes, auth_routes, configuracion_routes, usuario_routes, prediccion_routes
from app.models.connect import create_tables_if_not_exist
from flask_cors import CORS
import logging
from datetime import timedelta
import os
from werkzeug.utils import secure_filename


def create_app():
    global os
    app = Flask(__name__)
    CORS(app) # Habilitar CORS

    # Configuración JWT
    app.config['JWT_SECRET_KEY'] = 'PREDICCION_ESTUDIANTIL_2024'  # Cambia esto por una clave secreta real y segura
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt = JWTManager(app)

    # Configuración de la carpeta de subida y tipos de archivos permitidos
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    # Configuración para servir archivos estáticos
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # Asegúrate de que la carpeta de uploads exista
    import os
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Ruta para servir archivos estáticos desde la carpeta de uploads
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        filename = secure_filename(filename)
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Inicializar la base de datos
    create_tables_if_not_exist()

    # Registrar Blueprints
    app.register_blueprint(provincia_routes.provincia_blueprint, url_prefix='/provincia')
    app.register_blueprint(canton_routes.canton_blueprint, url_prefix='/canton')
    app.register_blueprint(parroquia_routes.parroquia_blueprint, url_prefix='/parroquia')
    app.register_blueprint(auth_routes.auth_blueprint, url_prefix='/auth')
    app.register_blueprint(configuracion_routes.configuracion_blueprint, url_prefix='/configuracion')
    app.register_blueprint(usuario_routes.usuario_blueprint, url_prefix='/usuario')
    app.register_blueprint(prediccion_routes.predicciones_blueprint, url_prefix='/prediccion')
    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)
    return app
