import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from utils.currency import CurrencyConverter
from keyboards.inlinekb import menu_keyboard, back_main_menu_keyboard

router = Router()

converter = CurrencyConverter()

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'start_profile')
async def start_user_profile(callback: CallbackQuery):
    await callback.answer()
    
    answer_message = f"{messages_data['greet_message']}"
    await callback.message.edit_text(answer_message, reply_markup=None)
    
    base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
    usd, eur = await asyncio.gather(
        converter.get_exchange(base_currency_usd),
        converter.get_exchange(base_currency_eur)
    )

    first_name = callback.from_user.first_name
    answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
    answer_message = answer_message + f"{hbold(messages_data['currency'])}\n"
    answer_message = answer_message + f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n"
    answer_message = answer_message + f"{hbold(messages_data['user_profile'])}\n"
    answer_message = answer_message + f"{messages_data['user_id']}\n"
    answer_message = answer_message + f"{messages_data['user_username']}\n"
    answer_message = answer_message + f"{messages_data['wins']}\n\n"
    answer_message = answer_message + f"{hbold(messages_data['user_balance'])}\n"
    answer_message = answer_message + f"{messages_data['user_chips']}\n"
    
    await callback.message.answer(answer_message, reply_markup=back_main_menu_keyboard)


@router.callback_query(F.data == 'profile')
async def user_profile(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"ПРОФИЛЬ", reply_markup=back_main_menu_keyboard)


@router.callback_query(F.data == 'back_main_menu')
async def back_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"{messages_data['main_menu']}", reply_markup=menu_keyboard)