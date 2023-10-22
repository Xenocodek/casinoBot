from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from database import requests as db


router = Router()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    answer_message = f"{messages_data['greetings']}{hbold(user.first_name)}"
    await db.new_user(user.id, user.username.lower(), user.first_name)
    await message.answer(answer_message)