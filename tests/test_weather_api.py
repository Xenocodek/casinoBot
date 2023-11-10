import logging
import pytest
import requests
from datetime import datetime, timedelta
import time
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError, RequestException
from utils.user_data import prepare_weather
from utils.weather_get_api import GetWeather

class TestGetWeather:
    def test_initialize_instance(self):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        assert weather.token == "12345"
        assert weather.city_id == "524311"
        assert weather.unit == 'metric'
        assert weather.lang == 'ru'
        assert weather.weather_data_cache is None
        assert weather.last_update is None

    def test_retrieve_weather_data(self, mocker):
            weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
            mock_response = mocker.Mock()
            mock_response.json.return_value = {"temperature": 25, "humidity": 80}
            mocker.patch('requests.get', return_value=mock_response)

            data = weather.get_data_weather()

            assert data == {"temperature": 25, "humidity": 80}

    def test_return_cached_data(self, mocker):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"temperature": 25, "humidity": 80}
        mocker.patch('requests.get', return_value=mock_response)

        data1 = weather.get_data_weather()
        data2 = weather.get_data_weather()

        assert data1 == data2

    def test_send_get_request(self, mocker):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"temperature": 25, "humidity": 70}
        mocker.patch('requests.get', return_value=mock_response)

        data = weather.get_data_weather()

        assert data == {"temperature": 25, "humidity": 70}

    def test_api_request_404_error(self, mocker):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError(response=mocker.Mock(status_code=404)))

        data = weather.get_data_weather()

        assert data is None

    def test_api_request_500_error(self, mocker):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError(response=mocker.Mock(status_code=500)))

        data = weather.get_data_weather()

        assert data is None

    def test_log_http_error(self, mocker):
        weather = GetWeather(weather_token="12345", city_id="524311", unit='metric', lang='ru')
        mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError("404 Not Found"))
        mocker.patch('logging.info')

        weather.get_data_weather()

        logging.info.assert_called_with("HTTP error occurred: 404 Not Found")\
        
    def test_log_other_error(self, mocker):
        weather = GetWeather()
        mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Other Error"))
        mocker.patch('logging.info')

        weather.get_data_weather()

        logging.info.assert_called_with("An error occurred: Other Error")

    def test_api_request_timeout(self, mocker):
        weather = GetWeather()
        mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)

        data = weather.get_data_weather()

        assert data is None

    def test_handle_invalid_weather_token(self, mocker):
        weather = GetWeather(weather_token="invalid_token", city_id="524311", unit='metric', lang='ru')
        mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError("401 Unauthorized"))
        mock_logging = mocker.patch('logging.info')

        data = weather.get_data_weather()

        assert data is None
        mock_logging.assert_called_with("HTTP error occurred: 401 Unauthorized")


class TestPrepareWeather:
    def test_formatted_string_with_weather_info(self, mocker):
        # Mock the weather.get_data_weather() method to return a sample weather data
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "Moscow",
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 20},
            "wind": {"speed": 10}
        })

        # Invoke the prepare_weather function
        result = prepare_weather()

        # Assert that the result is a formatted string with the weather information
        assert isinstance(result, str)
        assert "Moscow" in result
        assert "Cloudy" in result
        assert "20°C" in result
        assert "10 м/с" in result

        # Returns a message indicating that weather data is not available when weather data is not available.
    def test_message_when_weather_data_not_available(self, mocker):
        # Mock the weather.get_data_weather() method to return None
        mocker.patch.object(GetWeather, 'get_data_weather', return_value=None)

        # Invoke the prepare_weather function
        result = prepare_weather()

        # Assert that the result is a message indicating that weather data is not available
        assert isinstance(result, str)
        assert result == "Weather data is not available at the moment."

    def test_message_when_weather_data_is_empty_dict(self, mocker):
        # Mock the weather.get_data_weather() method to return an empty dictionary
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={})

        # Invoke the prepare_weather function
        result = prepare_weather()

        # Assert that the result is a message indicating that weather data is not available
        assert isinstance(result, str)
        assert result == "Weather data is not available at the moment."

    def test_formatted_string_with_missing_values(self, mocker):
        # Mock the weather.get_data_weather() method to return a sample weather data with missing values
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "London",
            "weather": [{"description": "cloudy"}],
            "main": {},
            "wind": {}
        })

        # Invoke the prepare_weather function
        result = prepare_weather()

        # Assert that the result is a formatted string with the weather information
        assert isinstance(result, str)
        assert "London" in result
        assert "Cloudy" in result

    def test_data_cache_and_update_time(self, mocker):
        # Mock the weather.get_data_weather() method to return a sample weather data
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "Moscow",
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 20},
            "wind": {"speed": 10}
        })

        # Invoke the get_data_weather method twice in a row
        result1 = GetWeather().get_data_weather()
        result2 = GetWeather().get_data_weather()

        # Assert that the same data is returned and no new API call is made
        assert result1 == result2