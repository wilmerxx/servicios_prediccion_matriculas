from app import create_app


def main():
    # Crear la instancia de la aplicacións
    app = create_app()

    # Ejecutar la aplicación en modo de desarrollo
    app.run(debug=True)


if __name__ == "__main__":
    main()
