import pymysql
from flask import jsonify
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def connect_db():
    """
    Establece una conexión a la base de datos MySQL.

    Returns:
    conn (pymysql.connections.Connection): Objeto de conexión a la base de datos.
    """
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        return conn
    except Exception as e:
        raise Exception(f"Error al conectar a la base de datos: {e}")


def create_tables_if_not_exist():
    """
    Crea las tablas de Provincia, Canton y Parroquia si no existen,
    usando el campo código como PRIMARY KEY.
    """
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # Crear tabla Provincia
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS provincias (
                    codigo_provincia INT PRIMARY KEY,
                    nombre_provincia VARCHAR(100) NOT NULL
                )
            """)
            # Crear tabla Canton
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cantones (
                    codigo_canton INT PRIMARY KEY,
                    nombre_canton VARCHAR(100) NOT NULL
                )
            """)
            # Crear tabla Parroquia
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parroquias (
                    codigo_parroquia INT PRIMARY KEY,
                    nombre_parroquia VARCHAR(100) NOT NULL
                )
            """)
            conn.commit()

            # Crear tabla roles
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS roles (
                               id INT AUTO_INCREMENT PRIMARY KEY,
                               nombre VARCHAR(50) UNIQUE NOT NULL
                           )
                       """)
            conn.commit()

            # Crear tabla usuarios
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS usuarios (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(50) UNIQUE NOT NULL,
                                email VARCHAR(100) UNIQUE NOT NULL,
                                nombre VARCHAR(100),
                                apellido VARCHAR(100),
                                password VARCHAR(255) NOT NULL,
                                rol_id INT,
                                FOREIGN KEY (rol_id) REFERENCES roles(id)
                            )
                        """)
            conn.commit()

            # crear la tabla de configuracion
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS configuraciones_usuario (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                usuario_id INT,
                                paleta_colores JSON,
                                nombre_aplicacion VARCHAR(100),
                                tipo_fuente VARCHAR(50),
                                logo_horizontal VARCHAR(255),
                                logo_vertical VARCHAR(255),
                                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                            );
                        """)
            conn.commit()

            # Crear tabla predicciones
            cursor.execute("""
                          CREATE TABLE IF NOT EXISTS predicciones (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              PERIODO VARCHAR(50),
                              ZONA VARCHAR(50),
                              CODPROVINCIA INT,
                              CODPARROQUIA INT,
                              CODCANTON INT,
                              AMIE VARCHAR(50),
                              TIPOEDUCACION VARCHAR(50),
                              NIVELEDUCACION VARCHAR(100),
                              SOSTENIMIENTO VARCHAR(100),
                              AREA VARCHAR(100),
                              REGIMENESCOLAR VARCHAR(100),
                              JURISDICCION VARCHAR(100),
                              MODALIDAD VARCHAR(100),
                              JORNADA VARCHAR(50),
                              TENENCIAINMUEBLEEDIFICIO VARCHAR(50),
                              ACCESOEDIFICIO VARCHAR(50),
                              DOCENTESFEMENINO INT,
                              DOCENTESMASCULINO INT,
                              TOTALDOCENTES INT,
                              ADMINISTRATIVOSFEMENINO INT,
                              ADMINISTRATIVOSMASCULINO INT,
                              TOTALADMINISTRATIVOS INT,
                              ESTUDIANTESFEMENINOTERCERANOBACH INT,
                              ESTUDIANTESMASCULINOTERCERANOBACH INT,
                              ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH INT,
                              ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH INT,
                              ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH INT,
                              ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH INT,
                              ESTUDIANTESFEMENINODESERTORESTERCERANOBACH INT,
                              ESTUDIANTESMASCULINODESERTORESTERCERANOBACH INT,
                              ESTUDIANTESFEMENINONOACTUALIZADOTERCERANOBACH INT,
                              ESTUDIANTESMASCULINONOACTUALIZADOTERCERANOBACH INT,
                              TOTAL_ESTUDIANTESTERCERANOBACH INT,
                              TOTAL_PROMOVIDOSTERCERANOBACH INT,
                              TASA_PROMOCION FLOAT,
                              TOTAL_DESERTORESTERCERANOBACH INT,
                              TASA_DESERCION FLOAT,
                              PROPORCION_DOCENTES_ESTUDIANTE FLOAT,
                              PROPORCION_ADMINISTRATIVOS_ESTUDIANTE FLOAT,
                              TOTAL_NOACTUALIZADOTERCERANOBACH INT,
                              PROPORCION_NOACTUALIZADOS FLOAT,
                              TOTAL_NOPROMOVIDOSTERCERANOBACH INT,
                              PROPORCION_NOPROMOVIDOS FLOAT,
                              ANIO_INICIO INT,
                              ANIO_FIN INT,
                              MES_INICIO VARCHAR(50),
                              MES_FIN VARCHAR(50),
                              PREDICCION_PROMOVIDOS INT
                          )
                      """)
            conn.commit()
    finally:
        conn.close()


