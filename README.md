# API de Predicción con Flask y XGBoost

Este proyecto proporciona una API basada en Flask para realizar predicciones utilizando un modelo de XGBoost entrenado.

## Estructura del Proyecto


A continuación se muestra un ejemplo de un archivo README.md que puedes incluir en tu proyecto para proporcionar una guía completa sobre la instalación, ejecución y pruebas de la API.

README.md
markdown
Copiar código
# API de Predicción con Flask y XGBoost

Este proyecto proporciona una API basada en Flask para realizar predicciones utilizando un modelo de XGBoost entrenado.

## Estructura del Proyecto
````
my_flask_api/
├── app/
│ ├── init.py
│ ├── models/
│ │ └── xgb_model.pkl
│ ├── routes/
│ │ ├── init.py
│ │ └── predict.py
│ └── services/
│ ├── init.py
│ └── prediction_service.py
├── tests/
│ ├── init.py
│ └── test_predict.py
├── config/
│ ├── init.py
│ └── config.py
├── run.py
└── README.md
````

## Requisitos

- Python 3.x
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/usuario/my_flask_api.git
    cd my_flask_api
    ```

2. Crear un entorno virtual (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instalar las dependencias:

    ```bash
    pip install -r requirements.txt

    ```

## Configuración

La configuración de la aplicación se encuentra en `app/config.py`. Puedes ajustar la configuración según tus necesidades.

## Ejecución de la API

Para ejecutar la API, usa el siguiente comando:

```bash
python run.py
