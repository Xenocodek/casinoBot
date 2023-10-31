from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from utils.currency import CurrencyConverter

converter = CurrencyConverter()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")

async def prepare_user_profile(user_data, first_name):
    if user_data:
        user_id, username, amount, wins = user_data
    
        base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
        usd, eur = await converter.get_multi_exchange()

        parts = [
            f"{messages_data['greetings']}{hbold(first_name)}\n\n",
            f"{hbold(messages_data['currency'])}\n",
            f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n",
            f"{hbold(messages_data['user_profile'])}\n",
            f"{messages_data['user_id']}{hbold(user_id)}\n",
            f"{messages_data['user_username']}@{hbold(username)}\n",
            f"{messages_data['wins']}{hbold(wins)}\n\n",
            f"{hbold(messages_data['user_balance'])}\n",
            f"{messages_data['user_chips']}{hbold(amount)}\n"
        ]
        
        return ''.join(parts)
    return None