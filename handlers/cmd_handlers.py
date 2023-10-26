import asyncio
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.currency import CurrencyConverter

router = Router()

converter = CurrencyConverter()

db = DatabaseManager()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.message(CommandStart())
async def cmd_start(message: Message):

    base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']

    usd, eur = await asyncio.gather(
        converter.get_exchange(base_currency_usd),
        converter.get_exchange(base_currency_eur)
    )

    user = message.from_user
    user_id, username, first_name, last_name = user.id, user.username.lower(), user.first_name, user.last_name

    answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
    answer_message = answer_message + f"{base_currency_usd}: {hbold(usd)}    {base_currency_eur}: {hbold(eur)}\n\n"
    answer_message = answer_message + f"{messages_data['select_command']}"

    await message.answer(answer_message)
    await db.new_user(user_id, username, first_name, last_name)