import requests

from settings.config import ExchangeManager

exchange_manager = ExchangeManager()
exchange_token = exchange_manager.token

class CurrencyConverter:
    """
    A class for currency conversion using a specified API.
    """

    def __init__(self):
        """
        Initializes the CurrencyConverter object.
        """

        # Set the API endpoint for the latest exchange rates
        self.api_url = "https://api.apilayer.com/fixer/latest"

        # Set the currency symbol for which we want to get the exchange rate
        self.symbols = "RUB"

        # Set the API key for authentication
        self.api_key = exchange_token

    def get_exchange_response(self, base_currency):
        """
        Retrieves exchange rate data from the API for a specified base currency.
        """

        # Construct the URL for the API request.
        # The URL includes the base currency specified by the user.
        url = f"{self.api_url}?symbols={self.symbols}&base={base_currency}"

        # Set the headers for the API request.
        # The headers include the API key required for authentication.
        headers = {"apikey": self.api_key}

        # Send a GET request to the API with the constructed URL and headers.
        response = requests.get(url, headers=headers)

        # Return the response object from the API call.
        return response

    async def get_exchange(self, base_currency):
        """
        Retrieves the exchange rate of the base currency to RUB.
        """

        # Get the response from the API
        response = self.get_exchange_response(base_currency)

        # Check if the response status code is 200 (successful)
        if response.status_code == 200:
            # Convert the response to JSON
            result_json = response.json()

            # Extract the RUB rate from the JSON
            rub_rate = result_json["rates"].get("RUB")

            # If the RUB rate exists, round it to 2 decimal places and return it
            if rub_rate is not None:
                rounded_rub_rate = round(rub_rate, 2)
                return rounded_rub_rate
            else:
                # If the RUB rate is not found, print a message
                print("RUB rate not found in response.")
        else:
            # If the response is not successful, print the status code
            print(f"Failed to fetch data. Status code: {response.status_code}")

    async def get_multi_exchange(self, base_currency_usd, base_currency_eur):
        """
        Retrieves the exchange rates of multiple base currencies to RUB.
        """

        # Retrieve the exchange rate for the base currency in USD
        usd = await self.get_exchange(base_currency_usd)

        # Retrieve the exchange rate for the base currency in EUR
        eur = await self.get_exchange(base_currency_eur)

        # Return the exchange rates of the base currencies to RUB
        return usd, eur