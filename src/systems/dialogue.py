import pygame
from src.config import *


class DialogueManager:
    def __init__(self):
        self.active = False  # ¿Hay un diálogo abierto?
        self.dialogue_lines = []  # Lista de frases a decir
        self.current_line_index = 0  # Qué frase estamos mostrando

        # --- CONFIGURACIÓN VISUAL ---
        # Caja de texto en la parte inferior
        self.box_height = 60  # Altura de la caja (en pixeles virtuales)
        self.box_rect = pygame.Rect(0, VIRTUAL_HEIGHT - self.box_height, VIRTUAL_WIDTH, self.box_height)

        # Fuente (Usamos la default de Pygame por ahora, size 16 para GBA)
        self.font = pygame.font.Font(None, 18)

        # Colores
        self.bg_color = (40, 40, 50)  # Azul oscuro tipo Pokémon
        self.border_color = (255, 255, 255)  # Borde blanco
        self.text_color = (255, 255, 255)

    def start_dialogue(self, lines):
        # Este método lo llamará el NPC cuando interactúes
        self.active = True
        self.dialogue_lines = lines
        self.current_line_index = 0

    def advance(self):
        # Avanzar a la siguiente línea o cerrar si no hay más
        self.current_line_index += 1
        if self.current_line_index >= len(self.dialogue_lines):
            self.active = False  # Cierra el diálogo
            return False  # Indica que terminó
        return True  # Indica que sigue hablando

    def draw(self, surface):
        if not self.active:
            return

        # 1. DIBUJAR LA CAJA (Fondo y Borde)
        pygame.draw.rect(surface, self.bg_color, self.box_rect)
        pygame.draw.rect(surface, self.border_color, self.box_rect, 2)  # Borde de 2px

        # 2. RENDERIZAR TEXTO
        # Obtenemos la frase actual
        text_content = self.dialogue_lines[self.current_line_index]

        # Renderizar texto (True para antialias)
        # Nota: En un sistema pro, haríamos text-wrapping (saltos de línea)
        text_surface = self.font.render(text_content, False, self.text_color)

        # Posición del texto con un pequeño margen dentro de la caja
        text_pos = (self.box_rect.x + 10, self.box_rect.y + 10)
        surface.blit(text_surface, text_pos)