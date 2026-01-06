import pygame
import sys
from src.config import *
from src.systems.map_manager import MapManager
from src.systems.camera import Camera
from src.entities.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicializar Sistemas
        self.map_manager = MapManager("mapa.tmx")  # Asegúrate del nombre
        self.camera = Camera(self.map_manager.width, self.map_manager.height)

        # Inicializar Entidades
        # Posición inicial (Tiles)
        self.player = Player(10, 10, self.map_manager)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def update(self):
        # Lógica
        self.player.update()
        self.camera.update(self.player)

    def draw(self):
        # Renderizado
        self.virtual_surface.fill(BLACK)

        # 1. Dibujar Mapa (La cámara ya maneja el offset)
        # Nota: Pasamos el rect de la cámara, no la cámara completa
        offset_x = self.camera.camera.x
        offset_y = self.camera.camera.y
        self.virtual_surface.blit(self.map_manager.image, (offset_x, offset_y))

        # 2. Dibujar Sprites (Con offset de cámara)
        for sprite in self.all_sprites:
            # Calculamos dónde dibujar relativo a la cámara
            offset_pos = (sprite.rect.x + offset_x, sprite.rect.y + offset_y)
            self.virtual_surface.blit(sprite.image, offset_pos)

        # 3. Escalar a pantalla completa
        scaled_surface = pygame.transform.scale(self.virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()