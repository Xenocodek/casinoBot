import requests
import logging
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
        self.exchange_data_cache = None
        self.last_update = None

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
        # Check if exchange data is already cached and not older than 10 minutes
        if self.exchange_data_cache and datetime.now() - self.last_update < timedelta(minutes=10):
            exchange_data = self.exchange_data_cache
        else:
            # Fetch the exchange rate and cache it
            exchange_data = self.fetch_exchange_rate(base_currency)
            self.exchange_data_cache = exchange_data
            self.last_update = datetime.now()
        
        # Get the exchange rate for RUB
        rub_rate = exchange_data["rates"].get("RUB")

        # If RUB rate is found, round it and return
        if rub_rate is not None:
            return round(rub_rate, 2)
        else:
            # Log if RUB rate is not found and return None
            logging.info("RUB rate not found in response.")
            return None

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