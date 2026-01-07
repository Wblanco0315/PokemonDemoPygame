import json
from src.config import *


class TextManager:
    def __init__(self, filename="ES.json"):
        path = os.path.join(ASSETS_DIR, "language", filename)

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"DEBUG: Dialogos cargados desde {path}")
        except FileNotFoundError:
            print(f"ERROR CRÍTICO: No se encontró el archivo en {path}")
            self.data = {}
        except json.JSONDecodeError:
            print(f"ERROR: El archivo {filename} tiene un formato JSON invalido.")
            self.data = {}

    def get_dialogue(self, dialogue_id):
        return self.data.get(dialogue_id, [f"MISSING_ID: {dialogue_id}"])