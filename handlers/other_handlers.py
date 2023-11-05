from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from utils.other_handlers_sup import (construct_help_message,
                                    construct_low_bonus_message,
                                    construct_echo_message)

from lexicon.subloader import JSONFileManager

router = Router()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")

@router.message(Command(commands_data['help']))
async def cmd_help(message: Message):
    """
    A function that handles the 'help' command.
    """
    # Construct the help message
    answer_message = construct_help_message()
    
    # Send the help message as a response
    await message.answer(answer_message)

@router.callback_query(F.data == 'help_button')
async def user_profile(callback: CallbackQuery):
    """
    A function that handles the callback query.
    """
    # Respond to the callback query
    await callback.answer()

    # Construct the help message
    answer_message = construct_help_message()

    # Send the help message as a reply to the callback query
    await callback.message.answer(answer_message)


@router.message(Command(commands_data['low_bonus']))
async def cmd_help(message: Message):
    """
    A function that handles the 'low_bonus' command.
    """
    # Construct the low bonus message
    answer_message = construct_low_bonus_message()
    
    # Send the low bonus message as a response
    await message.answer(answer_message)


@router.message()
async def cmd_echo(message: Message):
    """
    A function that responds to any incoming message by echoing the message back to the user.
    """
    # Responds to any incoming message
    await message.answer(construct_echo_message())