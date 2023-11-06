import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums.dice_emoji import DiceEmoji

from lexicon.subloader import JSONFileManager
from database.db import DatabaseManager
from utils.slot_sup import (format_number,
                            get_str_combo, 
                            get_result)
from keyboards.inlinekb import (menu_keyboard, 
                                get_bet_keyboard)

router = Router()

db = DatabaseManager()

user_data_bet = {}

file_manager = JSONFileManager()
commands_data = file_manager.get_json("commands.json")
messages_data = file_manager.get_json("messages.json")

@router.callback_query(F.data == 'game')
async def game_slot(callback: CallbackQuery, ):
    """
    Handles the callback query for the 'game' data.
    """
    # Respond to the callback query
    await callback.answer()

    # Get the user ID from the callback query
    user_id = callback.from_user.id

    # Check if the user ID exists
    balance = await db.get_user_balance(user_id) if user_id else None

    # Get the user's bet value from the user_data_bet dictionary
    user_value = user_data_bet.get(user_id, 10)

    # Format and send the message to the user
    message = (
        f"{hbold(messages_data['current_balance'])}"
        f"{hbold(format_number(balance))}"
        f"{messages_data['chips']}\n\n"
        f"{hbold(messages_data['change_bet'])}"
    )
    await callback.message.edit_text(
        message,
        reply_markup=get_bet_keyboard(str(user_value))
    )


@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: CallbackQuery):
    """
    Handles callback queries related to the "num_" data.
    """

    # Get the user ID from the callback query
    user_id = callback.from_user.id

    # Get the user's bet value from the user_data_bet dictionary
    user_value = user_data_bet.get(user_id, 10)

    # Extract the action from the callback data
    action = callback.data.split("_")[1]

    # Define an inner function to update the user's bet value
    async def update_bet(new_value):
        # Update the user's bet value in the user_data_bet dictionary
        user_data_bet[user_id] = new_value
        # Update the reply markup of the callback message
        await callback.message.edit_reply_markup(reply_markup=get_bet_keyboard(str(new_value)))

    # Check the action and update the user's bet value accordingly
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
        # If the action is not valid, send a message to the user
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
    """
    A function that handles the callback query for the 'bet' data.
    """
    # Get the user's bet value from the user_data_bet dictionary
    user_value = user_data_bet.get(callback.from_user.id, 10)

    # Send the user's bet value back to them
    await callback.answer(f"{messages_data['bet_value']}{user_value}")


@router.callback_query(F.data == 'twist')
async def twist_slot(callback: CallbackQuery):
    """
    Asynchronous function that handles the callback query for the 'twist' data.
    """
    # Answer the callback query
    await callback.answer()
    
    # Get the user ID from the callback query
    user_id = callback.from_user.id

    # Get the user's balance from the database
    balance = await db.get_user_balance(user_id) if user_id else None

    # Get the user's bet value or default to 10
    user_value = user_data_bet.get(user_id, 10)

    # Check if the user has enough balance to place the bet
    if balance >= user_value:
        # Delete the message that triggered the callback query
        await callback.message.delete()

        # Send a dice emoji and wait for 2 seconds
        data_slot = await callback.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
        score_change = data_slot.dice.value

        await asyncio.sleep(2.0)

        # Get the combinations and format the result
        combinations = await get_str_combo(score_change)
        formatted_combination = ' '.join(combinations)

        # Get the result of the slot game
        slot_result = await get_result(score_change,  user_value)

        if slot_result == 0:
            # Change the user's balance and Log the transaction
            await asyncio.gather(
            db.change_balance(-user_value, 0, user_id),
            db.change_transactions(messages_data['transaction_lose'], formatted_combination, -user_value, user_id)
            )

            # User lost the bet
            balance = balance - user_value

            # User lost the bet
            await callback.message.answer(f"{messages_data['lose']}-{hbold(user_value)}{messages_data['chips']}")

        else:
            # Change the user's balance and Log the transaction
            await asyncio.gather(
            db.change_balance(slot_result, 1, user_id),
            db.change_transactions(messages_data['transaction_win'], formatted_combination, slot_result, user_id)
            )

            # User won the bet
            balance = balance + slot_result

            # User won the bet
            await callback.message.answer(f"{hbold(messages_data['win'])}{hbold(format_number(slot_result))}{messages_data['chips']}")


        # Send a message with the current balance and prompt the user to change the bet
        await callback.message.answer(
            f"{hbold(messages_data['current_balance'])}{hbold(format_number(balance))}{messages_data['chips']}\n\n{hbold(messages_data['change_bet'])}",
            reply_markup=get_bet_keyboard(str(user_value)))
        
    else:
        # User does not have enough balance to place the bet
        await callback.message.edit_text(f"{hbold(messages_data['no_money'])}", reply_markup=menu_keyboard)