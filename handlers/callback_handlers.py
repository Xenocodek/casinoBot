from asyncio import sleep
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums.dice_emoji import DiceEmoji

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.currency import CurrencyConverter
from keyboards.inlinekb import menu_keyboard, back_main_menu_keyboard, get_bet_keyboard

router = Router()

converter = CurrencyConverter()

db = DatabaseManager()

user_data_bet = {}

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'start_profile')
async def start_user_profile(callback: CallbackQuery):
    await callback.answer("Запрос принят!")
    user_id = callback.from_user.id
    user_data = await db.get_user_data(user_id) if user_id else None

    if user_data:
        user_id, username, amount, wins = user_data
    
        answer_message = f"{messages_data['greet_message']}"
        await callback.message.edit_text(answer_message, reply_markup=None)
    
        base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
        usd, eur = await converter.get_multi_exchange()

        first_name = callback.from_user.first_name
        answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
        answer_message = answer_message + f"{hbold(messages_data['currency'])}\n"
        answer_message = answer_message + f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n"
        answer_message = answer_message + f"{hbold(messages_data['user_profile'])}\n"
        answer_message = answer_message + f"{messages_data['user_id']}{hbold(user_id)}\n"
        answer_message = answer_message + f"{messages_data['user_username']}@{hbold(username)}\n"
        answer_message = answer_message + f"{messages_data['wins']}{hbold(wins)}\n\n"
        answer_message = answer_message + f"{hbold(messages_data['user_balance'])}\n"
        answer_message = answer_message + f"{messages_data['user_chips']}{hbold(amount)}\n"
        
        await callback.message.answer(answer_message, reply_markup=back_main_menu_keyboard)


@router.callback_query(F.data == 'profile')
async def user_profile(callback: CallbackQuery):
    await callback.answer("Запрос принят!")
    user_id = callback.from_user.id
    user_data = await db.get_user_data(user_id) if user_id else None

    if user_data:
        user_id, username, amount, wins = user_data
    
        base_currency_usd, base_currency_eur = messages_data['usd'], messages_data['eur']
        usd, eur = await converter.get_multi_exchange()

        first_name = callback.from_user.first_name
        answer_message = f"{messages_data['greetings']}{hbold(first_name)}\n\n"
        answer_message = answer_message + f"{hbold(messages_data['currency'])}\n"
        answer_message = answer_message + f"{base_currency_usd}🇺🇸 : {hbold(usd)}₽    {base_currency_eur}🇪🇺 : {hbold(eur)}₽\n\n"
        answer_message = answer_message + f"{hbold(messages_data['user_profile'])}\n"
        answer_message = answer_message + f"{messages_data['user_id']}{hbold(user_id)}\n"
        answer_message = answer_message + f"{messages_data['user_username']}@{hbold(username)}\n"
        answer_message = answer_message + f"{messages_data['wins']}{hbold(wins)}\n\n"
        answer_message = answer_message + f"{hbold(messages_data['user_balance'])}\n"
        answer_message = answer_message + f"{messages_data['user_chips']}{hbold(amount)}\n"

    await callback.message.edit_text(answer_message, reply_markup=back_main_menu_keyboard)







@router.callback_query(F.data == 'game')
async def game_slot(callback: CallbackQuery, ):
    await callback.answer()
    user_value = user_data_bet.get(callback.from_user.id, 10)
    await callback.message.edit_text(f"Баланс", reply_markup=get_bet_keyboard(str(user_value)))

@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: CallbackQuery):

    user_value = user_data_bet.get(callback.from_user.id, 10)
    action = callback.data.split("_")[1]

    async def update_bet(new_value):
        user_data_bet[callback.from_user.id] = new_value
        await callback.message.edit_reply_markup(reply_markup=get_bet_keyboard(str(new_value)))

    if action == "decr" and user_value - 10 >= 10:
        await update_bet(user_value - 10)
    elif action == "min" and user_value > 10:
        await update_bet(10)
    elif action == "incr" and user_value + 10 <= 500:
        await update_bet(user_value + 10)
    elif action == "max" and user_value < 500:
        await update_bet(500)
    elif action == "double" and user_value * 2 <= 500:
        await update_bet(user_value * 2)
    else:
        await callback.answer("Ставка не может быть " + ("больше 500" if action in ["incr", "max", "double"] else "меньше 10"))

@router.callback_query(F.data == 'bet')
async def twist_slot(callback: CallbackQuery):
    user_value = user_data_bet.get(callback.from_user.id, 10)
    await callback.answer(f"Ставка: {user_value}")


@router.callback_query(F.data == 'twist')
async def twist_slot(callback: CallbackQuery):
    await callback.answer()

    await callback.message.delete()

    data_slot = await callback.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
    score_change = data_slot.dice.value
    await sleep(2.0)

    from typing import List
    def get_combo_parts(dice_value: int) -> List[str]:

        values = ["BAR", "GRAPES", "LEMON", "SEVEN"]

        dice_value -= 1
        result = []
        for _ in range(3):
            result.append(values[dice_value % 4])
            dice_value //= 4
        return result

    score_change = get_combo_parts(1)


    await callback.message.answer(f"{score_change}")

    user_value = user_data_bet.get(callback.from_user.id, 10)
    await callback.message.answer(f"Баланс", reply_markup=get_bet_keyboard(str(user_value)))










@router.callback_query(F.data == 'back_main_menu')
async def back_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"{messages_data['main_menu']}", reply_markup=menu_keyboard)