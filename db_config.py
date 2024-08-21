import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si está en entorno local
ENV = os.getenv('ENV', 'local')
if ENV == 'local':
    load_dotenv()

# Configurar las variables de entorno
DB_HOST = os.getenv('MYSQLHOST', os.getenv('LOCAL_DB_HOST', 'localhost'))
DB_USER = os.getenv('MYSQLUSER', os.getenv('LOCAL_DB_USER', 'wilmer'))
DB_PASSWORD = os.getenv('MYSQLPASSWORD', os.getenv('LOCAL_DB_PASSWORD', '12345'))
DB_NAME = os.getenv('MYSQLDATABASE', os.getenv('LOCAL_DB_NAME', 'db_matriculas'))
DB_PORT = os.getenv('MYSQLPORT', '3306')