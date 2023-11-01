from asyncio import sleep
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums.dice_emoji import DiceEmoji

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.currency import CurrencyConverter
from utils.user_data import prepare_user_profile
from utils.slot_sup import (format_number,
                            get_str_combo, 
                            get_result)
from keyboards.inlinekb import (menu_keyboard, 
                                back_main_menu_keyboard, 
                                get_bet_keyboard)

router = Router()

converter = CurrencyConverter()

db = DatabaseManager()

user_data_bet = {}

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'start_profile')
async def start_user_profile(callback: CallbackQuery):
    await callback.answer(messages_data['accepted_req'])

    answer_message = f"{messages_data['greet_message']}"
    await callback.message.edit_text(answer_message, reply_markup=None)

    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    user_data = await db.get_user_data(user_id) if user_id else None

    answer_message = await prepare_user_profile(user_data, first_name)

    await callback.message.answer(answer_message, reply_markup=back_main_menu_keyboard)


@router.callback_query(F.data == 'profile')
async def user_profile(callback: CallbackQuery):
    await callback.answer(messages_data['accepted_req'])

    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    user_data = await db.get_user_data(user_id) if user_id else None

    answer_message = await prepare_user_profile(user_data, first_name)

    await callback.message.edit_text(answer_message, reply_markup=back_main_menu_keyboard)







@router.callback_query(F.data == 'game')
async def game_slot(callback: CallbackQuery, ):
    await callback.answer()

    user_id = callback.from_user.id
    user_data = (await db.get_user_balance(user_id))[0] if user_id else None
    user_value = user_data_bet.get(user_id, 10)
    await callback.message.edit_text(
        f"{hbold(messages_data['current_balance'])}{hbold(format_number(user_data))}{messages_data['chips']}\n{hbold(messages_data['change_bet'])}",
        reply_markup=get_bet_keyboard(str(user_value))
    )

@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: CallbackQuery):

    user_id = callback.from_user.id
    user_value = user_data_bet.get(user_id, 10)
    action = callback.data.split("_")[1]

    async def update_bet(new_value):
        user_data_bet[user_id] = new_value
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
        await callback.answer(
            f"{messages_data['bet_cnt']}"
            + (
                f"{messages_data['more_500']}"
                if action in ["incr", "max", "double"]
                else f"{messages_data['less_10']}"
            )
        )

@router.callback_query(F.data == 'bet')
async def twist_slot(callback: CallbackQuery):
    user_value = user_data_bet.get(callback.from_user.id, 10)
    await callback.answer(f"{messages_data['bet_value']}{user_value}")


@router.callback_query(F.data == 'twist')
async def twist_slot(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    user_data = (await db.get_user_balance(user_id))[0]
    user_value = user_data_bet.get(user_id, 10)

    if user_data >= user_value:
        await callback.message.delete()

        data_slot = await callback.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
        score_change = data_slot.dice.value
        await sleep(2.0)


        combinations = await get_str_combo(score_change)
        await callback.message.answer(f"Комбинация {combinations}")

        slot_result = await get_result(score_change,  user_value)
        if slot_result == 0:
            await callback.message.answer(f"{messages_data['lose']}")
        else:
            await callback.message.answer(f"{hbold(messages_data['win'])}{hbold(format_number(slot_result))}{messages_data['chips']}")


        user_data = (await db.get_user_balance(user_id))[0] if user_id else None
        await callback.message.answer(
            f"{hbold(messages_data['current_balance'])}{hbold(format_number(user_data))}{messages_data['chips']}\n{hbold(messages_data['change_bet'])}",
            reply_markup=get_bet_keyboard(str(user_value)))
        
    else:
        await callback.message.edit_text(f"{hbold(messages_data['no_money'])}", reply_markup=menu_keyboard)









@router.callback_query(F.data == 'back_main_menu')
async def back_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"{messages_data['main_menu']}", reply_markup=menu_keyboard)