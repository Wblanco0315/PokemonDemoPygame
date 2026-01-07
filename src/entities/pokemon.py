import pygame
import os
from src.config import *
from src.entities.move import Move


class Pokemon:
    def __init__(self, species_id, data, all_moves_data, level=5):
        self.species_id = species_id
        self.name = data['name']
        self.level = level
        self.type = data['type']

        # --- ESTADÍSTICAS ---
        self.max_hp = data['base_hp'] + (level * 2)
        self.current_hp = self.max_hp
        self.attack = data['base_attack'] + level
        self.defense = data['base_defense'] + level
        self.is_fainted = False

        # --- CARGAR ATAQUES DESDE JSON ---
        self.moves = []
        # 'data["moves"]' es la lista ["tackle", "vine_whip"] que pusimos en pokedex.json
        for move_id in data.get('moves', []):
            if move_id in all_moves_data:
                # Creamos el objeto Move real y lo guardamos
                new_move = Move(move_id, all_moves_data[move_id])
                self.moves.append(new_move)

        # --- CARGAR SPRITES ---
        self.sprite_front = self.load_sprite(data.get('sprite_front'), is_back=False)
        self.sprite_back = self.load_sprite(data.get('sprite_back'), is_back=True)

    def load_sprite(self, filename, is_back):
        if not filename:
            return None

        path = os.path.join(SPRITES_DIR, "pokemon")

        if is_back:
            path = os.path.join(path, "back")
        else:
            path = os.path.join(path, "front")

        path = os.path.join(path, filename)


        try:
            image = pygame.image.load(path).convert_alpha()
            # Escalamos x3 o x4 porque los sprites de GB son diminutos (64x64 aprox)
            scale_factor = 3
            w = image.get_width() * scale_factor
            h = image.get_height() * scale_factor
            return pygame.transform.scale(image, (w, h))
        except Exception as e:
            print(f"Error cargando sprite {filename}: {e}")
            # Placeholder (Cuadrado de color si falla)
            surf = pygame.Surface((64, 64))
            surf.fill((255, 0, 255))
            return surf

    def take_damage(self, dmg):
        self.current_hp -= dmg
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_fainted = True