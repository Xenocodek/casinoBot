from typing import List

def format_number(num):
    formatted_num = "{:.1f}".format(num)
    if formatted_num.endswith('.0'):
        return str(int(num))
    return formatted_num 
    
async def get_str_combo(dice_value: int) -> List[str]:

    values = ["BAR", "GRAPES", "LEMON", "SEVEN"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result

async def get_result(dice_value, value):
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
    return value * multipliers.get(dice_value, 0)