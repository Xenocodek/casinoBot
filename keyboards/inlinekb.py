from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.subloader import JSONFileManager

file_manager = JSONFileManager()
keyboards_data = file_manager.get_json("keyboards.json")

def create_inline_kb(width, *args, **kwargs):
    """ Generate a custom inline keyboard with the specified width and buttons."""
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=keyboards_data[button] if button in keyboards_data else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
            
    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


start_keyboard = create_inline_kb(1, 'start_profile')
menu_keyboard = create_inline_kb(1, 'profile')
back_main_menu_keyboard = create_inline_kb(1, 'back_main_menu')