import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from keyboards.inlinekb import (menu_keyboard,
                                rating_menu)
from utils.user_data import prepare_rating_total

router = Router()

db = DatabaseManager()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'rating')
async def slot_game(callback: CallbackQuery):
    await callback.answer()

    answer_message = f"{hbold(messages_data['rating'])}"

    await callback.message.edit_text(answer_message, reply_markup=rating_menu)


@router.callback_query(F.data == 'rating_chips')
async def slot_game(callback: CallbackQuery):
    await callback.answer()

    data = await db.get_rating_total()

    answer_message = await prepare_rating_total(data)

    await callback.message.answer(answer_message)
    
    answer_message = f"{messages_data['select_command']}"

    await callback.message.answer(answer_message, reply_markup=menu_keyboard)


@router.callback_query(F.data == 'rating_wins')
async def slot_game(callback: CallbackQuery):
    await callback.answer()