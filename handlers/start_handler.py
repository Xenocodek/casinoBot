from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.currency import CurrencyConverter
from keyboards.inlinekb import (start_keyboard,
                                menu_keyboard)

router = Router()

converter = CurrencyConverter()

db = DatabaseManager()

user_data_bet = {}

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handles the start command received in a message.
    """
    
    # Extract user information from the message
    user = message.from_user
    user_id, username, first_name, last_name = user.id, user.username.lower(), user.first_name, user.last_name

    # Compose the response message
    answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
    answer_message = answer_message + f"{messages_data['select_command']}"

    # Send the composed message back to the user with a start keyboard
    await message.answer(answer_message, reply_markup=start_keyboard)

    # Add the new user to the database (assuming 'db' represents the database handler)
    await db.new_user(user_id, username, first_name, last_name)




@router.callback_query(F.data == 'back_main_menu')
async def back_menu(callback: CallbackQuery):
    """
    A callback function that is triggered when the 'back_main_menu' data is received.
    """

    # Acknowledges the callback query
    await callback.answer()

    # Edits the original message triggered by the callback with a new message
    await callback.message.edit_text(f"{messages_data['main_menu']}", reply_markup=menu_keyboard)