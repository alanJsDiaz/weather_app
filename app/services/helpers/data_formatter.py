class WeatherData:
    """
    Clase base para formatear datos de clima.
    """
    def __init__(self, data):
        self.city = data['name']
        self.temperature = data['main']['temp']

    def to_dict(self):
        """
        Convierte los datos del clima a un diccionario.
        Returns:
            dict: Los datos del clima.
        """
        return {
            'city': self.city,
            'temperature': self.temperature
        }


class TuristaWeatherData(WeatherData):
    """
    Clase que formatea los datos del clima para turistas.
    """
    def __init__(self, data):
        super().__init__(data)
        self.description = data['weather'][0]['description']

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'description': self.description
        })
        return data


class SobrecargoWeatherData(WeatherData):
    """
    Clase que formatea los datos del clima para sobrecargos.
    """
    def __init__(self, data):
        super().__init__(data)
        self.humidity = data['main']['humidity']
        self.visibility = data.get('visibility', 'N/A')

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'humidity': self.humidity,
            'visibility': self.visibility
        })
        return data


class PilotoWeatherData(WeatherData):
    """
    Clase que formatea los datos del clima para pilotos.
    """
    def __init__(self, data):
        super().__init__(data)
        self.lat = data['coord']['lat']
        self.lon = data['coord']['lon']
        self.wind_speed = data['wind']['speed']
        self.wind_deg = data['wind']['deg']
        self.pressure = data['main']['pressure']

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'lat': self.lat,
            'lon': self.lon,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'pressure': self.pressure
        })
        return data
