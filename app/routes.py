from flask import Blueprint, render_template, request
from .services.weather_service import WeatherService

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        user_type = request.form.get('user_type')
        
        # Validación de campos del formulario
        if not city or not user_type:
            error_message = "Por favor, ingresa una ciudad y selecciona un tipo de usuario."
            return render_template('index.html', error=error_message)

        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(city, user_type)

        if isinstance(weather_data, dict) and 'error' in weather_data:
            error_message = weather_data['error']
            return render_template('index.html', error=error_message)

        return render_template('result.html', data=weather_data, user_type=user_type)
    
    # Renderizar la página principal en caso de GET o de error
    return render_template('index.html', error=error_message)
