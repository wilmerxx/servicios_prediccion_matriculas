from app import create_app


def main():
    # Crear la instancia de la aplicacións
    app = create_app()

    # Ejecutar la aplicación en modo de desarrollo
    app.run(debug=True)

    # Ejecutar la aplicación en modo de desarrollo
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


if __name__ == "__main__":
    main()
