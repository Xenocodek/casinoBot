from lexicon.subloader import JSONFileManager


file_manager = JSONFileManager()
messages_data = file_manager.get_json("messages.json")

def construct_help_message():
    """
    Constructs and returns a help message by concatenating the values.
    """
    # Define the parts of the help message
    parts = [
        f"{messages_data['help_message_01']}",
        f"{messages_data['help_message_02']}",
        f"{messages_data['help_message_03']}",
        f"{messages_data['help_message_04']}",
        f"{messages_data['help_message_05']}"
    ]
    
    # Join the parts to form the complete help message
    answer_message = ''.join(parts)

    # Return the help message
    return answer_message


def construct_low_bonus_message():
    """
    Constructs and returns a help message by concatenating the values.
    """
    # Define the parts of the low bonus message
    parts = [
        f"{messages_data['low_bonus_message_01']}",
        f"{messages_data['low_bonus_message_02']}",
        f"{messages_data['low_bonus_message_03']}",
        f"{messages_data['low_bonus_message_04']}",
        f"{messages_data['low_bonus_message_05']}"
    ]
    
    # Join the parts to form the complete low bonus message
    answer_message = ''.join(parts)

    # Return the low bonus message
    return answer_message

def construct_echo_message():
    """
    Constructs and returns an echo message.
    """
    # Return the echo message
    return f"{messages_data['unclear']}"