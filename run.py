from app import create_app
import os

# Crear instancia de la aplicación Flask
app = create_app()


if __name__ == "__main__":
    # Configurar el host y puerto desde variables de entorno o usar valores predeterminados
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')  
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))  
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True' 

    # Ejecutar la aplicación
    app.run(host=host, port=port, debug=debug_mode)
