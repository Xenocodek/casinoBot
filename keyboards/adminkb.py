from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.subloader import JSONFileManager

file_manager = JSONFileManager()
keyboards_data = file_manager.get_json("keyboards.json")

def create_inline_kb(width, *args, **kwargs):
    """ Generate a custom inline keyboard with the specified width and buttons."""

    # Create an instance of InlineKeyboardBuilder
    kb_builder = InlineKeyboardBuilder()

    # Initialize an empty list to hold the buttons
    buttons = []

    # If any positional arguments are provided, add them to the buttons list
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=keyboards_data[button] if button in keyboards_data else button,
                callback_data=button))
            
    # If any keyword arguments are provided, add them to the buttons list
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
            
    # Add the buttons to the keyboard builder as a row with the specified width
    kb_builder.row(*buttons, width=width)

    # Return the keyboard as a markup
    return kb_builder.as_markup()

# Creating inline keyboards
start_admin_keyboard = create_inline_kb(1, 'user_list')