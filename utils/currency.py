import requests
from settings.config import ExchangeManager

exchange_manager = ExchangeManager()
exchange_token = exchange_manager.token

class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://api.apilayer.com/exchangerates_data/latest"
        self.symbols = "RUB"
        self.api_key = exchange_token

    def get_exchange_response(self, base_currency):
        url = f"{self.api_url}?symbols={self.symbols}&base={base_currency}"
        headers = {"apikey": self.api_key}
        response = requests.get(url, headers=headers)
        return response

    def get_exchange(self, base_currency):
        response = self.get_exchange_response(base_currency)
        if response.status_code == 200:
            result_json = response.json()
            rub_rate = result_json["rates"].get("RUB")
            if rub_rate is not None:
                rounded_rub_rate = round(rub_rate, 2)
                return rounded_rub_rate
            else:
                print("RUB rate not found in response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")