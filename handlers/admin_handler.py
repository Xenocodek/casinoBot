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
    """
    A handler function for the "admin" command. It takes a Message object as a parameter and does not return anything.
    """
    await message.answer("Вы админ!", reply_markup=start_admin_keyboard)

@router.callback_query(F.data == 'user_list')
async def start_user_profile(callback: CallbackQuery):
    # Send a callback answer to the user
    await callback.answer()
    # Create a message to send to the user
    answer_message = "abiba"
    # Send the message to the user
    await callback.message.answer(answer_message)