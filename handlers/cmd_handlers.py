from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager


router = Router()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name
    answer_message = f"{messages_data['greetings']}{hbold(user_name)}"
    await message.answer(answer_message)