from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from utils.currency_get_api import CurrencyConverter
from utils.weather_get_api import GetWeather
from utils.slot_sup import format_number
from .slot_sup import format_number

converter = CurrencyConverter()
weather = GetWeather()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")

def prepare_user_profile(user_data, first_name):
    """
    Generates the user profile information based on the provided user data and first name.
    """

    # Check if user_data is not empty
    if user_data:
        # Unpack user_data into variables
        # user_id, username, amount, wins = (user_data['user_id'], user_data['username'], user_data['total'], user_data['wins'])
        user_id = user_data[0]
        username = user_data[1]
        amount = user_data[2]
        wins = user_data[3]

        # Create a list of strings to be joined later
        parts = [
            f"{messages_data['greetings']}{hbold(first_name)}\n\n",
            f"{hbold(messages_data['user_profile'])}\n",
            f"{messages_data['user_id']}{hbold(user_id)}\n",
            f"{messages_data['user_username']}@{hbold(username)}\n" if username != 'unknown' else f"{messages_data['user_username']}{hbold(username)}\n",
            f"{messages_data['wins']}{hbold(wins)}\n\n",
            f"{hbold(messages_data['user_balance'])}\n",
            f"{messages_data['user_chips']}{hbold(format_number(amount))}\n"
        ]

        # Join all the parts into a single string and return it
        return ''.join(parts)
    # If user_data is empty, return None
    return None


def prepare_curency():
    """
    Prepares the currency by getting the base currency exchange rates and creating a list of strings to be joined later.
    """
    # Get base currency exchange rates
    base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
    usd, eur = converter.get_multi_exchange(base_currency_usd, base_currency_eur)

    # Create a list of strings to be joined later
    parts = [
        f"{hbold(messages_data['currency'])}\n\n",
        f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n",
    ]

    # Join all the parts into a single string and return it
    return ''.join(parts)


def prepare_weather():
    """
    Prepares the weather data and returns a formatted string with the weather information.
    """
    # Get the weather data
    weather_data = weather.get_data_weather()

    if not weather_data:
        return "Weather data is not available at the moment."

    weather_name = weather_data.get("name", "N/A")
    weather_description = weather_data.get("weather", [{}])[0].get("description", "N/A").capitalize()
    weather_temp = weather_data.get("main", {}).get("temp", "N/A")
    weather_wind_speed = weather_data.get("wind", {}).get("speed", "N/A")

    # Create a list of formatted strings with the weather information
    parts = [
        f"{hbold(messages_data['city_name'])}{weather_name}",
        f"{hbold(messages_data['city_weather'])}{weather_description}",
        f"{hbold(messages_data['city_temp'])}{weather_temp}°C",
        f"{hbold(messages_data['speed_wind'])}{weather_wind_speed} м/с"
    ]

            # Join the formatted strings with newlines and return the result
    return '\n'.join(parts)


def prepare_rating(data, rating_type):
    """
    Generates a formatted message text based on the given data and rating type.
    """
    data_type = data

    # Define the medals to be displayed
    medals = ["🥇", "🥈", "🥉"] + [""] * (10 - 3)

    if rating_type == 'chips':
        # Generate the formatted message text for the chips rating
        rating_title = messages_data['rating_total']
        message_text = f"{hbold(rating_title)}\n\n" + "\n".join([
            f"{index + 1}. {medals[index]}{'@' if entry[0] != 'unknown' else ''}{entry[0]} - имеет {format_number(entry[1])} фишек"
            if entry[0] else ""
            for index, entry in enumerate(data_type[:10])
        ])
    elif rating_type == 'wins':
        # Generate the formatted message text for the wins rating
        rating_title = messages_data['rating_wins']
        message_text = f"{hbold(rating_title)}\n\n" + "\n".join([
            f"{index + 1}. {medals[index]}{'@' if entry[0] != 'unknown' else ''}{entry[0]} - имеет {entry[1]} побед"
            if entry[0] else ""
            for index, entry in enumerate(data_type[:10])
        ])
    else:
        message_text = "Unsupported rating type"

    # Return the formatted message text
    return message_text