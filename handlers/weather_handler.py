from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from lexicon.subloader import JSONFileManager
from utils.weather_get_api import GetWeather
from utils.user_data import prepare_weather
from keyboards.inlinekb import back_main_menu_keyboard

router = Router()

weather = GetWeather()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'weather_murino')
async def show_currency(callback: CallbackQuery):
    """
    Show the currency callback query handler.
    """

    # Send an acknowledgement message
    await callback.answer(messages_data['accepted_req'])
    await callback.message.edit_text(messages_data['awaiting_req'])

    try:
        answer_message = prepare_weather()

        await callback.message.delete()

        # Send Message with the currency message and the back main menu keyboard
        await callback.message.answer(answer_message)
        await callback.message.answer(messages_data['select_command'], reply_markup=back_main_menu_keyboard)

    except TelegramBadRequest:
        await callback.message.edit_text(messages_data['req_error'], reply_markup=back_main_menu_keyboard)

    except Exception:
        await callback.message.edit_text(messages_data['req_error'], reply_markup=back_main_menu_keyboard)