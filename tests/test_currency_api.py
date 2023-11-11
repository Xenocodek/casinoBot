from datetime import datetime, timedelta
import requests
import logging
from utils.currency_get_api import CurrencyConverter


class TestCurrencyConverter:
    def test_initialize_currency_converter(self):
        # Test case for initializing the CurrencyConverter class
        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        assert converter.api_key == "12345"
        assert converter.symbols == "USD"
        assert converter.exchange_data_cache is None
        assert converter.last_update is None

    def test_fetch_exchange_rate_success(self, mocker):
        # Test case for successful fetching of exchange rate
        mocker.patch("requests.get").return_value.status_code = 200
        mocker.patch("requests.get").return_value.json.return_value = {"rates": {"RUB": 70.0}}
    
        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        response = converter.fetch_exchange_rate("USD")
    
        assert response == {"rates": {"RUB": 70.0}}

    def test_get_exchange_success(self, mocker):
        # Test case for successfully getting exchange rate
        mocker.patch.object(CurrencyConverter, "fetch_exchange_rate").return_value = {"rates": {"RUB": 70.0}}
    
        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        exchange_rate = converter.get_exchange("USD")
    
        assert exchange_rate == 70.0

    def test_get_exchange_rate_not_found(self, mocker):
        # Test case for handling exchange rate not found
        mocker.patch.object(CurrencyConverter, "fetch_exchange_rate").return_value = {"rates": {}}
        mocker.patch("logging.info")

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        exchange_rate = converter.get_exchange("USD")

        assert exchange_rate is None
        logging.info.assert_called_with("RUB rate not found in response.")

    def test_get_multi_exchange_success(self, mocker):
        # Test case for successfully getting multiple exchange rates
        mocker.patch.object(CurrencyConverter, "get_exchange").side_effect = [1.5, 0.8]

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        usd_rate, eur_rate = converter.get_multi_exchange("USD", "EUR")

        assert usd_rate == 1.5
        assert eur_rate == 0.8

    def test_get_multi_exchange_one_currency_failure(self, mocker):
        # Test case for handling failure when getting exchange rate for one currency
        mocker.patch.object(CurrencyConverter, "get_exchange").side_effect = [1.5, None]

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        usd_rate, eur_rate = converter.get_multi_exchange("USD", "EUR")

        assert usd_rate == 1.5
        assert eur_rate is None

    def test_get_multi_exchange_both_currencies_failure(self, mocker):
        # Test case for handling failure when getting exchange rates for both currencies
        mocker.patch.object(CurrencyConverter, "get_exchange").side_effect = [None, None]

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        usd_rate, eur_rate = converter.get_multi_exchange("USD", "EUR")

        assert usd_rate is None
        assert eur_rate is None

    def test_fetch_exchange_rate_http_error(self, mocker):
        # Test case for handling HTTP error during exchange rate fetch
        mocker.patch("requests.get").side_effect = requests.exceptions.HTTPError("HTTP error occurred")
        mocker.patch("logging.info")

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        response = converter.fetch_exchange_rate("USD")

        assert response is None
        logging.info.assert_called_with("HTTP error occurred: HTTP error occurred")

    def test_fetch_exchange_rate_request_exception(self, mocker):
        # Test case for handling general request exception during exchange rate fetch
        mocker.patch("requests.get").side_effect = requests.exceptions.RequestException("An error occurred")
        mocker.patch("logging.info")

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        response = converter.fetch_exchange_rate("USD")

        assert response is None
        logging.info.assert_called_with("An error occurred: An error occurred")

    def test_fetch_exchange_rate_invalid_api_key(self, mocker):
        # Test case for handling invalid API key during exchange rate fetch
        mocker.patch("requests.get").side_effect = requests.exceptions.HTTPError("Invalid API key")
        mocker.patch("logging.info")

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        response = converter.fetch_exchange_rate("USD")

        assert response is None
        logging.info.assert_called_with("HTTP error occurred: Invalid API key")

    def test_get_exchange_cache_hit(self, mocker):
        # Test case for cache hit when getting exchange rate
        mocker.patch.object(CurrencyConverter, "fetch_exchange_rate").return_value = {"rates": {"RUB": 70.0}}

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        converter.exchange_data_cache = {"rates": {"RUB": 70.0}}
        converter.last_update = datetime.now() - timedelta(minutes=5)

        exchange_rate = converter.get_exchange("USD")

        assert exchange_rate == 70.0

    def test_get_exchange_cache_miss(self, mocker):
        # Test case for cache miss when getting exchange rate
        mocker.patch.object(CurrencyConverter, "fetch_exchange_rate").return_value = {"rates": {"RUB": 70.0}}

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        converter.exchange_data_cache = {"rates": {"RUB": 70.0}}
        converter.last_update = datetime.now() - timedelta(minutes=15)

        exchange_rate = converter.get_exchange("USD")

        assert exchange_rate == 70.0

    def test_fetch_exchange_rate_empty_response(self, mocker):
        # Test case for handling empty response during exchange rate fetch
        mocker.patch("requests.get").return_value.status_code = 200
        mocker.patch("requests.get").return_value.json.return_value = {}

        mocker.patch("logging.error")

        converter = CurrencyConverter(exchange_token="12345", symbols="USD")
        response = converter.fetch_exchange_rate("USD")

        assert response == {}