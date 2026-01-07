import pygame
from src.config import *

class TitleManager:
    def __init__(self):
        self.active = True
        self.state = "TITLE"  # TITLE | CONTROLS
        self.timer = 0
        self.show_text = True

        # RECURSOS
        font_path = os.path.join(ASSETS_DIR, "fonts", "default_font.ttf")
        try:
            self.font_big = pygame.font.Font(font_path, 12)  # Títulos
            self.font_small = pygame.font.Font(font_path, 6)  # Texto normal
        except:
            self.font_big = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 16)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:

            # PANTALLA DE TÍTULO
            if self.state == "TITLE":
                if event.key == pygame.K_RETURN or event.key == pygame.K_z:
                    self.state = "CONTROLS"  # Pasar a controles

            # PANTALLA DE CONTROLES
            elif self.state == "CONTROLS":
                if event.key == pygame.K_RETURN or event.key == pygame.K_z:
                    self.active = False  # ¡EMPEZAR JUEGO!

    def update(self):
        self.timer += 1
        if self.timer > 30:
            self.timer = 0
            self.show_text = not self.show_text

    def draw(self, surface):
        surface.fill((20, 20, 40))

        if self.state == "TITLE":
            # 1. Título del Juego
            title_surf = self.font_big.render("POKEMON DEMO", False, (255, 215, 0))  # Dorado
            # Centrar
            title_rect = title_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 3))
            surface.blit(title_surf, title_rect)

            # 2. Texto Parpadeante
            if self.show_text:
                start_surf = self.font_small.render("PRESIONA ENTER", False, (255, 255, 255))
                start_rect = start_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT * 2 // 3))
                surface.blit(start_surf, start_rect)

            # Créditos pie de página
            credits = self.font_small.render("2026 - Wilson Blanco", False, (100, 100, 150))
            surface.blit(credits, (10, VIRTUAL_HEIGHT - 15))

        elif self.state == "CONTROLS":
            # Encabezado
            header = self.font_big.render("CONTROLES", False, (255, 255, 255))
            surface.blit(header, (20, 10))

            # Lista de teclas
            controls = [
                ("FLECHAS", "Moverse / Menu"),
                ("Z", "Interactuar / Aceptar"),
                ("X", "Cancelar / Volver"),
                ("ENTER", "Abrir Menu / Start"),
                ("L-SHIFT", "Correr"),
            ]

            y = 40
            for key, action in controls:
                # Dibujar Tecla (Amarillo)
                key_surf = self.font_small.render(key, False, (255, 215, 0))
                surface.blit(key_surf, (30, y))

                # Dibujar Acción (Blanco)
                act_surf = self.font_small.render(f": {action}", False, (200, 200, 200))
                surface.blit(act_surf, (80, y))

                y += 15  # Espaciado

            # Botón Continuar
            if self.show_text:
                cont_surf = self.font_small.render("PRESIONA Z PARA INICIAR", False, (100, 255, 100))
                surface.blit(cont_surf, (30, y))