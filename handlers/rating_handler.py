import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from keyboards.inlinekb import (menu_keyboard,
                                rating_menu)
from utils.user_data import prepare_rating

router = Router()

db = DatabaseManager()

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")


@router.callback_query(F.data == 'rating')
async def slot_game(callback: CallbackQuery):
    """
    A callback function for handling rating data.
    """
    # Send a callback answer to acknowledge the query
    await callback.answer()

    # Create a message with the rating data
    answer_message = f"{hbold(messages_data['rating'])}"

    # Edit the message text with the rating data and show the rating menu
    await callback.message.edit_text(answer_message, reply_markup=rating_menu)


@router.callback_query(F.data.startswith("rating_"))
async def callbacks_num(callback: CallbackQuery):
    """
    Callback function for handling rating-related callback queries.
    """
    # Answer the callback query
    await callback.answer()

    # Extract the action from the callback data
    action = callback.data.split("_")[1]

    # If the action is "chips"
    if action == "chips":
        # Retrieve the total rating data
        data = await db.get_rating_total()

    # If the action is "wins"
    elif action == "wins":
        # Retrieve the rating data for wins
        data = await db.get_rating_wins()

    # Prepare the rating message
    answer_message = prepare_rating(data, action)
    
    # Delete the original message
    await callback.message.delete()
    # Send the rating message as a reply
    await callback.message.answer(answer_message)

    # Prepare the select command message
    answer_message = f"{messages_data['select_command']}"
    # Send the select command message with a menu keyboard
    await callback.message.answer(answer_message, reply_markup=menu_keyboard)




# @router.callback_query(F.data == 'rating_chips')
# async def slot_game(callback: CallbackQuery):
#     """
#     Callback function for handling rating chips.
#     """
#     # Send an answer to the callback query
#     await callback.answer()

#     # Retrieve the rating total from the database
#     data = await db.get_rating_total()

#     # Prepare the rating total message
#     answer_message = prepare_rating_total(data)

#     # Delete the original message
#     await callback.message.delete()

#     # Send the rating total message as a response
#     await callback.message.answer(answer_message)
    
#     # Prepare a message for selecting a command
#     answer_message = f"{messages_data['select_command']}"

#     # Send the command selection message with a menu keyboard
#     await callback.message.answer(answer_message, reply_markup=menu_keyboard)


# @router.callback_query(F.data == 'rating_wins')
# async def slot_game(callback: CallbackQuery):
#     """
#     A function that handles the callback query for the 'rating_wins' data. 
#     """
#     # Answer the callback query to let Telegram know that the button press was received
#     await callback.answer()

#     # Get the rating wins data from the database
#     data = await db.get_rating_wins()

#     # Prepare the answer message using the rating wins data
#     answer_message = prepare_rating_wins(data)

#     # Delete the original message that triggered the callback query
#     await callback.message.delete()

#     # Send the answer message to the user
#     await callback.message.answer(answer_message)
    
#     # Send a follow-up message with a prompt for the user
#     answer_message = f"{messages_data['select_command']}"

#     # Send the follow-up message with a custom keyboard
#     await callback.message.answer(answer_message, reply_markup=menu_keyboard)