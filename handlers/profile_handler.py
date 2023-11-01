from aiogram import Router, F
from aiogram.types import CallbackQuery

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.currency import CurrencyConverter
from utils.user_data import prepare_user_profile
from keyboards.inlinekb import back_main_menu_keyboard

router = Router()

converter = CurrencyConverter()

db = DatabaseManager()

user_data_bet = {}

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'start_profile')
async def start_user_profile(callback: CallbackQuery):
    """
    Handles the callback query for starting the user profile.
    """

    # Sends an acknowledgment message to the callback
    await callback.answer(messages_data['accepted_req'])

    # Edits the original message triggered by the callback with a new message
    answer_message = f"{messages_data['greet_message']}"
    await callback.message.edit_text(answer_message, reply_markup=None)

    # Extracts user information from the callback
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name

    # Fetches user data from the database based on the user ID
    user_data = await db.get_user_data(user_id) if user_id else None

    # Prepares a user profile message using user data and first name
    answer_message = await prepare_user_profile(user_data, first_name)

    # Sends the prepared user profile message as a response to the callback
    await callback.message.answer(answer_message, reply_markup=back_main_menu_keyboard)


@router.callback_query(F.data == 'profile')
async def user_profile(callback: CallbackQuery):
    """
    Callback function for the 'profile' data callback query.
    """

    # Sends an acknowledgment message to the callback
    await callback.answer(messages_data['accepted_req'])

    # Extracts user information from the callback
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name

    # Fetches user data from the database based on the user ID
    user_data = await db.get_user_data(user_id) if user_id else None

    # Prepares a user profile message using user data and first name
    answer_message = await prepare_user_profile(user_data, first_name)

    # Edits the original message triggered by the callback with the prepared user profile message
    await callback.message.edit_text(answer_message, reply_markup=back_main_menu_keyboard)