from aiogram import Router
from aiogram.types import Message

from lexicon.subloader import JSONFileManager

router = Router()

file_manager = JSONFileManager()
messages = file_manager.get_json("messages.json")

@router.message()
async def cmd_echo(message: Message):
    await message.answer(f"{messages['unclear']}")