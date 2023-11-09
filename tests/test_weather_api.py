import logging
import pytest
import requests
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError, RequestException
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