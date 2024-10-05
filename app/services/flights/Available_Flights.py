import pandas as pd


class Flights:

    def __init__(self):
        """
        Inicializa el objeto Vuelos.
        Args:
        Ninguno
        Returns:
        Ninguno
        """
        self.cache = {}
        self.df = pd.read_csv('dataset1.csv')

    def get_available_flights_by_destination(self, destination):
        """
        Recupera los vuelos disponibles para un destino
        Args:
            destino (str): El nombre de la ciudad de destino.
        Returns:
            dict: Un diccionario que contiene los vuelos disponibles para el origen y destino dados. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        available_flights = self.df[self.df["destination"].isin(destination)].to_dict(orient='records')
        return available_flights



    def get_available_flights_by_origin(self, iata):
        """
        Recupera los vuelos disponibles para un origen
        Args:
            origen (str): El nombre de la ciudad de origen.
        Returns:
            dict: Un diccionario que contiene los vuelos disponibles para el origen y destino dados. Si ocurre un error, el diccionario contendrá una clave 'error' con un mensaje de error.
        """
        available_flights = self.df[self.df["origin"].isin(iata)].to_dict(orient='records')
        return available_flights