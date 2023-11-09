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

async def prepare_user_profile(user_data, first_name):
    """
    Generates the user profile information based on the provided user data and first name.
    """

    # Check if user_data is not empty
    if user_data:
        # Unpack user_data into variables
        user_id, username, amount, wins = (user_data['user_id'], user_data['username'], user_data['total'], user_data['wins'])

        # If username is None, set it to 'None'
        if username is None:
            username = messages_data['username_null']

        # Create a list of strings to be joined later
        parts = [
            f"{messages_data['greetings']}{hbold(first_name)}\n\n",
            f"{hbold(messages_data['user_profile'])}\n",
            f"{messages_data['user_id']}{hbold(user_id)}\n",
            f"{messages_data['user_username']}{hbold(username)}\n",
            f"{messages_data['wins']}{hbold(wins)}\n\n",
            f"{hbold(messages_data['user_balance'])}\n",
            f"{messages_data['user_chips']}{hbold(format_number(amount))}\n"
        ]

        # Join all the parts into a single string and return it
        return ''.join(parts)
    # If user_data is empty, return None
    return None


async def prepare_curency():
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


async def prepare_weather():
    """
    Prepares the weather data and returns a formatted string with the weather information.
    """
    # Get the weather data
    weather_data = weather.get_data_weather()

    if weather_data:
            # Extract the necessary information from the weather data
            weather_name = weather_data.get("name", "N/A")
            weather_description = weather_data["weather"][0]["description"].capitalize()
            weather_temp = round(weather_data["main"]["temp"])
            weather_wind_speed = weather_data["wind"]["speed"]

            # Create a list of formatted strings with the weather information
            parts = [
                f"{hbold(messages_data['city_name'])}{weather_name}",
                f"{hbold(messages_data['city_weather'])}{weather_description}",
                f"{hbold(messages_data['city_temp'])}{weather_temp}°C",
                f"{hbold(messages_data['speed_wind'])}{weather_wind_speed} м/с"
            ]

            # Join the formatted strings with newlines and return the result
            return '\n'.join(parts)
    
    # If weather data is not available, return a message indicating that
    return "Weather data is not available at the moment."


def prepare_rating_total(data):
    """
    Generates a formatted message text with the top 10 users' ratings and their total number of chips.
    """
    data_total = data

    # Define the medal emojis for the top 3 users and empty strings for the rest
    medals = ["🥇", "🥈", "🥉"] + [""] * (10 - 3)

    # Generate the formatted message text by iterating over the first 10 entries in the data list
    message_text = "\n".join([
        f"{index + 1}. {medals[index]}@{entry['username']} - имеет {format_number(entry['total'])} фишек" 
        if entry['username'] else ""
        for index, entry in enumerate(data_total[:10])
    ])

    # Return the generated message text
    return message_text


def prepare_rating_wins(data):
    """
    Prepares the rating of wins based on the given data.
    """
    data_total = data

    # Define the medals to be displayed
    medals = ["🥇", "🥈", "🥉"] + [""] * (10 - 3)

    # Generate the message text by iterating over the top 10 entries in the data
    message_text = "\n".join([
        f"{index + 1}. {medals[index]}@{entry['username']} - имеет {entry['wins']} побед" 
        if entry['username'] else ""
        for index, entry in enumerate(data_total[:10])
    ])

    # Return the formatted message
    return message_text