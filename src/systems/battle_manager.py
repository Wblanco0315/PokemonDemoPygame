import pygame
from src.config import *


class BattleManager:
    def __init__(self):
        self.active = False
        self.turn = "PLAYER"  # Turno actual: PLAYER | ENEMY | WAIT
        self.timer = 0

        # --- UI CONFIG ---
        self.font = pygame.font.Font(None, 20)
        self.bg_color = (20, 20, 20)  # Fondo oscuro casi negro

        # Rectángulos visuales (Placeholders para los sprites)
        # Enemigo
        self.enemy_pos = (VIRTUAL_WIDTH - 80, 20)
        self.enemy_rect = pygame.Rect(self.enemy_pos[0], self.enemy_pos[1], 40, 40)

        # Jugador
        self.player_pos = (40, VIRTUAL_HEIGHT - 60)
        self.player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 40, 40)

        # Panel de Comandos
        self.panel_rect = pygame.Rect(0, VIRTUAL_HEIGHT - 48, VIRTUAL_WIDTH, 48)

    def start_battle(self, enemy_npc):
        """Inicia la batalla contra un NPC"""
        self.active = True
        self.enemy = enemy_npc
        self.turn = "PLAYER"
        print(f"--- BATALLA INICIADA CONTRA {enemy_npc.nombre} ---")

    def update(self):
        # Aquí irá la lógica de turnos, animaciones, daño, etc.
        # Por ahora, solo detectamos si queremos salir con ESC
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.active = False
            print("--- BATALLA TERMINADA (Huida) ---")

    def draw(self, surface):
        # 1. Fondo de batalla
        surface.fill(self.bg_color)

        # 2. Base del Enemigo (Círculo simple por ahora)
        pygame.draw.ellipse(surface, (100, 100, 100), (self.enemy_pos[0] - 10, self.enemy_pos[1] + 30, 60, 20))
        # Sprite Enemigo (Placeholder Rojo)
        pygame.draw.rect(surface, (255, 50, 50), self.enemy_rect)

        # 3. Base del Jugador
        pygame.draw.ellipse(surface, (100, 100, 100), (self.player_pos[0] - 10, self.player_pos[1] + 30, 60, 20))
        # Sprite Jugador (Placeholder Azul)
        pygame.draw.rect(surface, (50, 50, 255), self.player_rect)

        # 4. Panel de Texto/Comandos
        pygame.draw.rect(surface, (255, 255, 255), self.panel_rect)  # Fondo blanco
        pygame.draw.rect(surface, (0, 0, 0), self.panel_rect, 2)  # Borde negro

        # Texto de estado
        text = f"Turno: {self.turn} | [ESPACIO] Atacar | [ESC] Huir"
        text_surf = self.font.render(text, True, (0, 0, 0))
        surface.blit(text_surf, (10, VIRTUAL_HEIGHT - 35))