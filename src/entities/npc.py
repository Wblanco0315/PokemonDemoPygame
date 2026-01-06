import pygame
from src.config import *


class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_filename, dialogue_id):
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.dialogue_id = dialogue_id

        try:
            path = os.path.join(SPRITES_DIR, sprite_filename)
            self.image = pygame.image.load(path).convert_alpha()

            # Escalado simple si es muy grande
            if self.image.get_width() > 32:
                self.image = pygame.transform.scale(self.image, (32, 32))
        except Exception:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE + 8))
            self.image.fill((0, 255, 0))  # Placeholder verde

        self.rect = self.image.get_rect()
        target_bottom_y = (y + 1) * TILE_SIZE
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        self.grid_x = x
        self.grid_y = y

    def interact(self, text_manager):
        return text_manager.get_dialogue(self.dialogue_id)