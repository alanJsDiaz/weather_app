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
        ##Icono
        self.icon_code = data['weather'][0]['icon']
        self.icon_url = f"https://openweathermap.org/img/wn/{self.icon_code}@2x.png"
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'description': self.description,
            'icon': self.icon_url
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
        self.icon_code = data['weather'][0]['icon']
        self.icon_url = f"https://openweathermap.org/img/wn/{self.icon_code}@2x.png"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'humidity': self.humidity,
            'visibility': self.visibility,
            'icon': self.icon_url 
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
        ##Icono
        self.icon_code = data['weather'][0]['icon']
        self.icon_url = f"https://openweathermap.org/img/wn/{self.icon_code}@2x.png"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'lat': self.lat,
            'lon': self.lon,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'pressure': self.pressure,
            'icon': self.icon_url  # Aquí agregas el icono
        })
        return data
