from aiogram import Router, F
from aiogram.types import CallbackQuery

from lexicon.subloader import JSONFileManager
from utils.currency import CurrencyConverter
from utils.user_data import prepare_curency
from keyboards.inlinekb import back_main_menu_keyboard

router = Router()

converter = CurrencyConverter()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'currency')
async def show_currency(callback: CallbackQuery):
    """
    Show the currency callback query handler.
    """

    # Send an acknowledgement message
    await callback.answer(messages_data['accepted_req'])
    
    # Prepare the currency message
    answer_message = await prepare_curency()

    # Edit the message with the currency message and the back main menu keyboard
    await callback.message.edit_text(answer_message, reply_markup=back_main_menu_keyboard)