from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.subloader import JSONFileManager

file_manager = JSONFileManager()

commands_data = file_manager.get_json("commands.json")
keyboards_data = file_manager.get_json("keyboards.json")

async def set_bot_commands(bot: Bot):
    """
    Sets the bot commands for the given bot.
    """
    # Define the list of BotCommand objects
    commands = [
            BotCommand(command=commands_data['start'], description=keyboards_data['start_ui']),
            BotCommand(command=commands_data['help'], description=keyboards_data['help_ui']),
            BotCommand(command=commands_data['low_bonus'], description=keyboards_data['low_bonus_ui'])
        ]

    # Set the bot commands using the Bot.set_my_commands() method
    await bot.set_my_commands(commands)