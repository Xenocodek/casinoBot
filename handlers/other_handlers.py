from aiogram import Router
from aiogram.types import Message

from lexicon.subloader import JSONFileManager

router = Router()

file_manager = JSONFileManager()
messages = file_manager.get_json("messages.json")

@router.message()
async def cmd_echo(message: Message):
    """
    A function that responds to any incoming message by echoing the message back to the user.
    """
    # Responds to any incoming message
    await message.answer(f"{messages['unclear']}")