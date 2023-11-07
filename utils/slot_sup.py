from typing import List
from lexicon.subloader import JSONFileManager

file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")

def format_number(num):
    """
    Format a number to one decimal place and return as a string.
    If num is None, return None or handle it appropriately.
    """

    # Check if num is None
    if num is None:
        # Handle None input; you could return None or raise an error
        return None  # or raise ValueError("Input cannot be None")
    
    # Format the number to one decimal place
    formatted_num = "{:.1f}".format(num)

    # Check if the formatted number ends with '.0'
    if formatted_num.endswith('.0'):
        # If it does, convert it to an integer and return as a string
        return str(int(num))
    
    # If it doesn't, return the formatted number as a string
    return formatted_num
    
    
async def get_str_combo(dice_value: int) -> List[str]:
    """
    Get the string combination for a given dice value.
    """

    # Define the possible values for the string combinations
    values = ["BAR", "GRAPES", "LEMON", "SEVEN"]

    # Subtract 1 from the dice value to adjust for the indexing
    dice_value -= 1

    # Initialize an empty list to store the result
    result = []

    # Loop three times to get the string combination
    for _ in range(3):
        # Append the value from the values list corresponding to the 
        # remainder of the dice value divided by 4 to the result list
        result.append(values[dice_value % 4])

        # Divide the dice value by 4 to get the next digit
        dice_value //= 4

    # Return the result list
    return result


async def get_result(dice_value, value):
    """
    Calculate the result of a dice roll based on the dice value and value.
    """

    # Define the multipliers for each dice value
    multipliers = {
        1: 3,
        22: 5,
        43: 10,
        64: 20,
        2: 0.25,
        3: 0.25,
        4: 0.25,
        17: 0.25,
        33: 0.25,
        49: 0.25,
        6: 0.5,
        21: 0.5,
        23: 0.5,
        24: 0.5,
        38: 0.5,
        54: 0.5,
        11: 1,
        27: 1,
        41: 1,
        42: 1,
        44: 1,
        59: 1,
        16: 1.5,
        32: 1.5,
        48: 1.5,
        61: 1.5,
        62: 1.5,
        63: 1.5,
    }

    # Return the calculated result based on the dice value and initial value
    return value * multipliers.get(dice_value, 0)


def prepare_rule():

    parts = [
        f"{messages_data['rule_message_01']}",
        f"{messages_data['rule_message_02']}",
        f"{messages_data['rule_message_03']}",
        f"{messages_data['rule_message_04']}",
        f"{messages_data['rule_message_05']}",
        f"{messages_data['rule_message_06']}",
        f"{messages_data['rule_message_07']}"
        f"{messages_data['rule_message_08']}"
        f"{messages_data['rule_message_09']}"
        f"{messages_data['rule_message_10']}"
        f"{messages_data['rule_message_11']}"
        f"{messages_data['rule_message_12']}"
    ]
    
    answer_message = ''.join(parts)

    return answer_message