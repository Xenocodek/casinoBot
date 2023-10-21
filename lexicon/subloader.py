import os
import json

class JSONFileManager:
    def __init__(self, base_path="lexicon"):
        self.base_path = base_path

    def get_json(self, file_path):
        full_path = os.path.join(self.base_path, file_path)
        try:
            with open(full_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}")
            return None