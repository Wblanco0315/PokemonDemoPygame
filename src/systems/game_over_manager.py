import pygame
from src.config import *


class GameOverManager:
    def __init__(self):
        self.active = False
        self.winner = None  # "PLAYER" o "ENEMY"
        self.restart_requested = False

        # Recursos
        try:
            # Intentamos cargar la fuente del sistema
            self.font_big = pygame.font.Font(FONTS_DIR, 20)
            self.font_small = pygame.font.Font(FONTS_DIR, 8)
        except:
            self.font_big = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 8)

    def show(self, winner):
        self.active = True
        self.winner = winner
        self.restart_requested = False
        print(f"Game Over. Ganador: {winner}")

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                self.restart_requested = True

    def draw(self, surface):
        if not self.active: return

        # Fondo negro sólido
        surface.fill(BLACK)

        if self.winner == "PLAYER":
            text = "¡VICTORIA!"
            color = (255, 215, 0)  # Dorado
            sub_text = "¡Obtuviste la Medalla Carbón!"
        else:
            text = "¡DERROTA!"
            color = (255, 50, 50)  # Rojo
            sub_text = "Se te acabaron los Pokémon..."

        # 1. Título
        title_surf = self.font_big.render(text, False, color)
        title_rect = title_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 3))
        surface.blit(title_surf, title_rect)

        # 2. Subtítulo (Sombra y Texto)
        sub_surf = self.font_small.render(sub_text, False, WHITE)
        sub_rect = sub_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2))
        surface.blit(sub_surf, sub_rect)

        # 3. Reiniciar
        prompt = "Presiona Z para Reiniciar"
        prompt_surf = self.font_small.render(prompt, False, (150, 150, 150))
        prompt_rect = prompt_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT * 4 // 5))
        surface.blit(prompt_surf, prompt_rect)