import requests
import logging
from datetime import datetime, timedelta

from settings.config import WeatherManager

weather_manager = WeatherManager()
token = weather_manager.token

class GetWeather:
    def __init__(self, weather_token=token, city_id="524311", unit='metric', lang='ru'):
        """
        Initializes an instance of the class with the given weather token, city ID, unit, and language.
        """
        self.token = weather_token
        self.city_id = city_id
        self.unit = unit
        self.lang = lang
        self.weather_data_cache = None
        self.last_update = None

    def get_data_weather(self):
        """
        Retrieves the weather data from the OpenWeatherMap API.
        """
        # Check if the weather data is already cached and if it was updated less than 10 minutes ago
        if self.weather_data_cache and datetime.now() - self.last_update < timedelta(minutes=10):
            return self.weather_data_cache
        
        # Construct the URL for the API request
        url = f"https://api.openweathermap.org/data/2.5/weather?id={self.city_id}&units={self.unit}&lang={self.lang}&appid={self.token}"
        
        try:
            # Send a GET request to the API
            response = requests.get(url)
            response.raise_for_status()

            # Cache the weather data and update the last update time
            self.weather_data_cache = response.json()
            self.last_update = datetime.now()
            return self.weather_data_cache
        
        except requests.exceptions.HTTPError as err:
            # Log an error if an HTTP error occurs
            logging.info(f"HTTP error occurred: {err}")

        except requests.exceptions.RequestException as err:
            # Log an error if any other error occurs
            logging.info(f"An error occurred: {err}")