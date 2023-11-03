from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from utils.currency import CurrencyConverter
from utils.slot_sup import format_number

converter = CurrencyConverter()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")

async def prepare_user_profile(user_data, first_name):
    """
    Generates the user profile information based on the provided user data and first name.
    """

    # Check if user_data is not empty
    if user_data:
        # Unpack user_data into variables
        user_id, username, amount, wins = user_data

        # If username is None, set it to 'None'
        if username is None:
            username = messages_data['username_null']

        # Get base currency exchange rates
        # base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
        # usd, eur = await converter.get_multi_exchange(base_currency_usd, base_currency_eur)

        # Create a list of strings to be joined later
        parts = [
            f"{messages_data['greetings']}{hbold(first_name)}\n\n",
            f"{hbold(messages_data['user_profile'])}\n",
            f"{messages_data['user_id']}{hbold(user_id)}\n",
            f"{messages_data['user_username']}@{hbold(username)}\n",
            f"{messages_data['wins']}{hbold(wins)}\n\n",
            f"{hbold(messages_data['user_balance'])}\n",
            f"{messages_data['user_chips']}{hbold(format_number(amount))}\n"
        ]

        # Join all the parts into a single string and return it
        return ''.join(parts)
    # If user_data is empty, return None
    return None


async def prepare_curency():

    # Get base currency exchange rates
    base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
    usd, eur = await converter.get_multi_exchange(base_currency_usd, base_currency_eur)

    # Create a list of strings to be joined later
    parts = [
        f"{hbold(messages_data['currency'])}\n\n",
        f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n",
    ]

    # Join all the parts into a single string and return it
    return ''.join(parts)
