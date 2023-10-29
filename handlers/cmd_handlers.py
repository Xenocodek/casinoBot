import asyncio
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager

from keyboards.inlinekb import start_keyboard

router = Router()

db = DatabaseManager()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.message(CommandStart())
async def cmd_start(message: Message):

    user = message.from_user
    user_id, username, first_name, last_name = user.id, user.username.lower(), user.first_name, user.last_name

    answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
    answer_message = answer_message + f"{messages_data['select_command']}"

    await db.new_user(user_id, username, first_name, last_name)
    await message.answer(answer_message, reply_markup=start_keyboard)