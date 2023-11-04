from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.filters import Command


from keyboards.adminkb import start_admin_keyboard

from filters.is_admin import IsAdmin

router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

@router.message(Command("admin"))
async def start(message: Message) -> None:
    await message.answer("Вы админ!", reply_markup=start_admin_keyboard)

@router.callback_query(F.data == 'user_list')
async def start_user_profile(callback: CallbackQuery):
    await callback.answer()
    answer_message = "abiba"
    await callback.message.answer(answer_message)