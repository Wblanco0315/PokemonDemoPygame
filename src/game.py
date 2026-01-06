import pygame
import sys
from src.config import *
from src.entities.roark import Roark
from src.systems import MapManager, Camera, DialogueManager, TextManager
from src.entities.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # INICIAR SISTEMAS
        self.map_manager = MapManager("mapa_test.tmx")
        self.camera = Camera(self.map_manager.width, self.map_manager.height)
        self.text_manager = TextManager("ES.json")
        self.dialogue_manager = DialogueManager()


        # GRUPOS DE SPRITES
        self.all_sprites = pygame.sprite.Group()
        #CREAR JUGADOR
        self.player = Player(9, 28, self.map_manager)


        self.all_sprites.add(self.player)
        self.npcs = pygame.sprite.Group()

        # Crear a Roark
        lider_gimnasio = Roark(9, 5)
        self.all_sprites.add(lider_gimnasio)
        self.npcs.add(lider_gimnasio)

        # Colisiones
        self.map_manager.walls.append(lider_gimnasio.rect)

    def update(self):
        if not self.dialogue_manager.active:
            self.player.update()

        self.camera.update(self.player)

    def draw(self):
        self.virtual_surface.fill(BLACK)

        offset_x = self.camera.camera.x
        offset_y = self.camera.camera.y
        self.virtual_surface.blit(self.map_manager.image, (offset_x, offset_y))

        # 2. DIBUJAR SPRITES (Jugador y NPCs)
        for sprite in self.all_sprites:
            offset_pos = (sprite.rect.x + offset_x, sprite.rect.y + offset_y)
            self.virtual_surface.blit(sprite.image, offset_pos)

        self.dialogue_manager.draw(self.virtual_surface)

        scaled_surface = pygame.transform.scale(self.virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def check_interaction(self):
        if self.dialogue_manager.active:
            self.dialogue_manager.advance()
            return

        player_grid_x = int(self.player.rect.centerx // TILE_SIZE)
        player_grid_y = int(self.player.rect.centery // TILE_SIZE)

        target_x = player_grid_x
        target_y = player_grid_y

        if self.player.direction == 'left':
            target_x -= 1
        elif self.player.direction == 'right':
            target_x += 1
        elif self.player.direction == 'up':
            target_y -= 1
        elif self.player.direction == 'down':
            target_y += 1

        for npc in self.npcs:
            if int(npc.grid_x) == target_x and int(npc.grid_y) == target_y:

                lines = npc.interact(self.text_manager)

                if lines:
                    self.dialogue_manager.start_dialogue(lines)
                return

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.check_interaction()

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()