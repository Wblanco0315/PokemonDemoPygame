import json
from src.config import *

class DataManager:
    def __init__(self):
        # CARGAMOS LOS DICCIONARIOS EN MEMORIA AL INICIAR EL JUEGO
        self.pokedex = self.load_json("pokedex.json")
        self.moves = self.load_json("moves.json")

    def load_json(self, filename):
        path = os.path.join(ASSETS_DIR, "data", filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Fallo al cargar {filename}: {e}")
            return {}

    def get_pokemon_data(self, species_id):
        # BUSCA UN POKÉMON (EJ: 'CHARMANDER'). SI NO EXISTE, DEVUELVE NONE.
        return self.pokedex.get(species_id)

    def get_move_data(self, move_id):
        return self.moves.get(move_id)