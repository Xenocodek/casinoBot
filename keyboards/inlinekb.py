from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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


def get_bet_keyboard(bet):
    kb_builder = InlineKeyboardBuilder()

    kb_builder.button(text="-10", callback_data="num_decr")
    kb_builder.button(text=bet, callback_data="bet")
    kb_builder.button(text="+10", callback_data="num_incr")
    kb_builder.button(text="Мин.", callback_data="num_min")
    kb_builder.button(text="Удвоить", callback_data="num_double")
    kb_builder.button(text="Макс.", callback_data="num_max")
    kb_builder.button(text="Крутить", callback_data="twist")
    kb_builder.button(text="Назад", callback_data="back_main_menu")

    kb_builder.row()
    kb_builder.adjust(3, 3, 1)

    return kb_builder.as_markup()


start_keyboard = create_inline_kb(1, 'start_profile', 'game')
menu_keyboard = create_inline_kb(1, 'profile', 'game')
back_main_menu_keyboard = create_inline_kb(1, 'back_main_menu')