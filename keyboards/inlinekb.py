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


def get_bet_keyboard(bet):
    """    
    Generates a bet keyboard with buttons for betting options.
    """
    kb_builder = InlineKeyboardBuilder()

    # Adding buttons for various betting options using the provided texts and callback data
    kb_builder.button(text=f"{keyboards_data['bet_-10']}", callback_data="num_decr")
    kb_builder.button(text=f"{bet} {keyboards_data['chip']}", callback_data="bet")
    kb_builder.button(text=f"{keyboards_data['bet_+10']}", callback_data="num_incr")
    kb_builder.button(text=f"{keyboards_data['bet_min']}", callback_data="num_min")
    kb_builder.button(text=f"{keyboards_data['bet_double']}", callback_data="num_double")
    kb_builder.button(text=f"{keyboards_data['bet_max']}", callback_data="num_max")
    kb_builder.button(text=f"{keyboards_data['twist']}", callback_data="twist")
    kb_builder.button(text=f"{keyboards_data['back']}", callback_data="back_main_menu")

    kb_builder.row()
    kb_builder.adjust(3, 3, 1)

    # Returns the generated keyboard as a markup
    return kb_builder.as_markup()


# Creating inline keyboards
start_keyboard = create_inline_kb(1, 'start_profile', 'game', 'currency', 'help_button')
menu_keyboard = create_inline_kb(1, 'profile', 'game', 'currency', 'help_button')
back_main_menu_keyboard = create_inline_kb(1, 'back_main_menu')