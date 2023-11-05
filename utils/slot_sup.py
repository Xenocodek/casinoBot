from typing import List

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
        22: 7,
        43: 10,
        64: 15,
        2: 1,
        3: 1,
        4: 1,
        17: 1,
        33: 1,
        49: 1,
        6: 1.5,
        21: 1.5,
        23: 1.5,
        24: 1.5,
        38: 1.5,
        54: 1.5,
        11: 1.75,
        27: 1.75,
        41: 1.75,
        42: 1.75,
        44: 1.75,
        59: 1.75,
        16: 2.5,
        32: 2.5,
        48: 2.5,
        61: 2.5,
        62: 2.5,
        63: 2.5,
    }

    # Return the calculated result based on the dice value and initial value
    return value * multipliers.get(dice_value, 0)