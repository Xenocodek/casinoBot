import requests
import logging
import time
from datetime import datetime, timedelta

from settings.config import ExchangeManager

exchange_manager = ExchangeManager()
token = exchange_manager.token

class CurrencyConverter:
    """
    A class for currency conversion using a specified API.
    """

    def __init__(self, exchange_token=token, symbols="RUB"):
        """
        Initializes the CurrencyConverter object.
        """
        self.api_key = exchange_token
        self.symbols = symbols
        self.exchange_data_cache = {}
        self.cache_expiry = 600

    def fetch_exchange_rate(self, base_currency):
        """
        Fetches the exchange rate for a given base currency.
        """
        # Construct the URL with the base currency and symbols
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={self.symbols}&base={base_currency}"
        # Set the headers for the request
        headers = {"apikey": self.api_key}

        try:
            # Make a GET request to the API
            response = requests.get(url, headers=headers)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            # Return the JSON response
            return response.json()
        
        except requests.exceptions.HTTPError as err:
            # Log the HTTP error if one occurs
            logging.info(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as err:
            # Log any other request error that occurs
            logging.info(f"An error occurred: {err}")

    def get_exchange(self, base_currency):
        """
        Get the exchange rate for a given base currency.
        """
        if base_currency in self.exchange_data_cache:
            cached_data, cache_time = self.exchange_data_cache[base_currency]
            current_time = time.time()
            if current_time - cache_time < self.cache_expiry:
                # Return cached exchange rate if not expired
                return round(cached_data.get('rates', {}).get(self.symbols), 2)

        # Fetch exchange rate if not cached or expired
        exchange_data = self.fetch_exchange_rate(base_currency)

        # Cache the fetched data along with current time
        self.exchange_data_cache[base_currency] = (exchange_data, time.time())
        
        # Return the exchange rate
        return round(exchange_data.get('rates', {}).get(self.symbols), 2)


    def get_multi_exchange(self, base_currency_usd, base_currency_eur):
        """
        Retrieves the exchange rates of multiple base currencies to RUB.
        """
        # Retrieve the exchange rate of the base currency to USD
        usd = self.get_exchange(base_currency_usd)
        # Retrieve the exchange rate of the base currency to EUR
        eur = self.get_exchange(base_currency_eur)

        # Return the exchange rates as a tuple
        return usd, eur