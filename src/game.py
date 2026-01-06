import pygame
import sys
from src.config import *
from src.entities.roark import Roark
from src.systems import MapManager, Camera, DialogueManager
from src.entities.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicializar Sistemas
        self.map_manager = MapManager("mapa_test.tmx")  # Cargar mapa
        self.camera = Camera(self.map_manager.width, self.map_manager.height)  # Inicializar cámara
        self.dialogue_manager = DialogueManager()  # Inicializar sistema de dialogos

        # Inicializar Entidades
        # Posición inicial (Tiles)
        self.player = Player(10, 10, self.map_manager)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # NPCs y entidades
        self.npcs = pygame.sprite.Group()
        lider_gimnasio = Roark(10, 5)
        self.all_sprites.add(lider_gimnasio)
        self.npcs.add(lider_gimnasio)

        self.map_manager.walls.append(lider_gimnasio.rect)

    def update(self):

        if not self.dialogue_manager.active:
            self.player.update()

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

        self.dialogue_manager.draw(self.virtual_surface)

        # 3. Escalar a pantalla completa
        scaled_surface = pygame.transform.scale(self.virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def check_interaction(self):
        # 1. SI EL DIÁLOGO YA ESTÁ ABIERTO -> Avanzamos texto
        if self.dialogue_manager.active:
            self.dialogue_manager.advance()
            return

        # 2. CALCULAR COORDENADAS (Esto te faltaba) <--- CORREGIDO
        # Calculamos dónde está el jugador en la grilla
        player_grid_x = int(self.player.rect.centerx // TILE_SIZE)
        player_grid_y = int(self.player.rect.centery // TILE_SIZE)  # O usa bottom con ajuste

        # Ajuste fino (opcional, depende de tu sprite):
        # player_grid_y = int((self.player.rect.bottom - 1) // TILE_SIZE)

        target_x = player_grid_x
        target_y = player_grid_y

        # Verificamos hacia dónde mira para definir el tile objetivo
        if self.player.direction == 'left':
            target_x -= 1
        elif self.player.direction == 'right':
            target_x += 1
        elif self.player.direction == 'up':
            target_y -= 1
        elif self.player.direction == 'down':
            target_y += 1

        # 3. BUSCAR NPC
        for npc in self.npcs:
            # Comparamos coordenadas (convertimos a int por seguridad)
            if int(npc.grid_x) == target_x and int(npc.grid_y) == target_y:
                lines = npc.interact()
                if lines:
                    self.dialogue_manager.start_dialogue(lines)
                return

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # AGREGADO: Escuchar la tecla de interacción (Z) <--- CORREGIDO
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.check_interaction()

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()