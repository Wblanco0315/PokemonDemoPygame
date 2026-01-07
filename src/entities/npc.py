import pygame
from src.config import *


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_filename, dialogue_id):
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.dialogue_id = dialogue_id

        self.animations = {
            'down': [],
            'left': [],
            'right': [],
            'up': []
        }

        self.direction = 'down'  # DIRECCION DEFAULT

        try:
            sprite_path = os.path.join(SPRITES_DIR, sprite_filename)
            # CARGAR Y ESCALAR
            raw_sheet = pygame.image.load(sprite_path).convert_alpha()
            new_width = raw_sheet.get_width() // 2
            new_height = raw_sheet.get_height() // 2
            full_sheet = pygame.transform.scale(raw_sheet, (new_width, new_height))

            directions_list = ['down', 'left', 'right', 'up']

            for row_index, anim_name in enumerate(directions_list):
                for col_index in range(4):  # 4 frames por animación
                    x_pos = col_index * 32
                    y_pos = row_index * 32

                    # Recortamos el cuadro
                    frame = full_sheet.subsurface((x_pos, y_pos, 32, 32))
                    self.animations[anim_name].append(frame)

            # IMAGEN INICIAL
            self.image = self.animations['down'][0]

        except Exception:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE + 8))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        target_bottom_y = (y + 1) * TILE_SIZE
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        self.grid_x = x
        self.grid_y = y

    def interact(self, text_manager):
        return text_manager.get_dialogue(self.dialogue_id)