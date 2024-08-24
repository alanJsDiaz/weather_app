from flask import Blueprint, render_template, request
from .services.weather_service import get_weather_data

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        user_type = request.form['user_type']
        weather_data = get_weather_data(city, user_type)

        # Verificar si hay un error en los datos del clima
        if 'error' in weather_data:
            return render_template('index.html', error=weather_data['error'])

        return render_template('result.html', data=weather_data, user_type=user_type)
    
    return render_template('index.html')
