import json
from src.config import *


class TextManager:
    def __init__(self, filename):
        path = os.path.join("assets", "language", filename)

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: No se encontro el archivo de diálogos en {path}")
            self.data = {}

    def get_dialogue(self, dialogue_id):
        return self.data.get(dialogue_id, ["...", f"Error: Falta ID '{dialogue_id}'"])