import pygame
from src.config import *


class DialogueManager:
    def __init__(self):
        self.active = False
        self.dialogue_lines = []
        self.current_line_index = 0

        self.box_height = 45
        self.box_rect = pygame.Rect(0, VIRTUAL_HEIGHT - self.box_height, VIRTUAL_WIDTH, self.box_height)

        try:
            self.font = pygame.font.Font(FONTS_DIR, 8)
        except FileNotFoundError:
            print("ERROR: Fuente no encontrada")
            self.font = pygame.font.Font(None, 12)

        self.bg_color = (40, 40, 50)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)

        # MARGEN INTERNO DEL TEXTO
        self.padding = 8

    def start_dialogue(self, lines):
        self.active = True
        self.dialogue_lines = lines
        self.current_line_index = 0

    def advance(self):
        self.current_line_index += 1
        if self.current_line_index >= len(self.dialogue_lines):
            self.active = False
            return False
        return True

    def draw(self, surface):
        if not self.active:
            return

        # DIBUJAR LA CAJA
        pygame.draw.rect(surface, self.bg_color, self.box_rect)
        pygame.draw.rect(surface, self.border_color, self.box_rect, 2)

        # PROCESAR EL TEXTO
        text_content = self.dialogue_lines[self.current_line_index]

        # FUNCIÓN RÁPIDA PARA DIVIDIR EL TEXTO EN LÍNEAS QUE QUEPAN
        lines_to_draw = self.wrap_text(text_content, self.box_rect.width - (self.padding * 2))

        # DIBUJAR LÍNEAS
        y_offset = self.box_rect.y + self.padding

        for line in lines_to_draw:
            text_surface = self.font.render(line, False, self.text_color)
            surface.blit(text_surface, (self.box_rect.x + self.padding, y_offset))
            y_offset += self.font.get_height() + 2

    #  UNA FUNCIÓN PARA DIVIDIR EL TEXTO EN LINEAS
    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            width, _ = self.font.size(test_line)

            if width < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)
        return lines