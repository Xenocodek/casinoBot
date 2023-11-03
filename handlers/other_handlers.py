from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from lexicon.subloader import JSONFileManager

router = Router()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.message(Command(commands_data['help']))
async def cmd_help(message: Message):
    parts = [
        f"{messages_data['help_message_01']}",
        f"{messages_data['help_message_02']}",
        f"{messages_data['help_message_03']}",
        f"{messages_data['help_message_04']}",
        f"{messages_data['help_message_05']}"
    ]

    answer_message = ''.join(parts)
    await message.answer(answer_message)


@router.message(Command(commands_data['low_bonus']))
async def cmd_help(message: Message):
    parts = [
        f"{messages_data['low_bonus_message_01']}",
        f"{messages_data['low_bonus_message_02']}",
        f"{messages_data['low_bonus_message_03']}",
        f"{messages_data['low_bonus_message_04']}",
        f"{messages_data['low_bonus_message_05']}"
    ]

    answer_message = ''.join(parts)
    await message.answer(answer_message)


@router.message()
async def cmd_echo(message: Message):
    """
    A function that responds to any incoming message by echoing the message back to the user.
    """
    # Responds to any incoming message
    await message.answer(f"{messages_data['unclear']}")