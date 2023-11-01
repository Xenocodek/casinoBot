import os
import json

class JSONFileManager:
    """
    A class for managing JSON files.
    """

    def __init__(self, base_path="lexicon"):
        """
        Initializes the JSONFileManager object.
        """

        self.base_path = base_path

    def get_json(self, file_path):
        """
        Retrieves JSON data from a specified file.
        """

        # Construct the full file path by joining the base path and the file path
        full_path = os.path.join(self.base_path, file_path)

        try:
            # Open the file in read mode with UTF-8 encoding
            with open(full_path, 'r', encoding="utf-8") as file:
                # Load the JSON data from the file
                data = json.load(file)
                # Return the loaded JSON data
                return data
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # If the file is not found or there is an error decoding the JSON data,
            # print the error message and return None
            print(f"Error: {e}")
            return None