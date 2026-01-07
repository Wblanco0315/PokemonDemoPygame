import json
import os
from src.config import *

class DataManager:
    def __init__(self):
        # Cargamos los diccionarios en memoria al iniciar el juego
        self.pokedex = self.load_json("pokedex.json")
        self.moves = self.load_json("moves.json")

    def load_json(self, filename):
        """Función auxiliar para cargar cualquier JSON de forma segura"""
        path = os.path.join(ASSETS_DIR, "data", filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Fallo al cargar {filename}: {e}")
            return {}

    def get_pokemon_data(self, species_id):
        # Busca un pokémon (ej: 'charmander'). Si no existe, devuelve None.
        return self.pokedex.get(species_id)

    def get_move_data(self, move_id):
        return self.moves.get(move_id)