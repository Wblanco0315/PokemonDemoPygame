import pygame
from src.config import *


class MenuManager:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.selected_index = 0
        self.swap_index = None

        try:
            self.font = pygame.font.Font(FONTS_DIR, 8)
        except FileNotFoundError:
            print("ERROR: Fuente no encontrada")
            self.font = pygame.font.Font(None, 12)

        self.bg_color = (30, 30, 50)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 215, 0)
        self.swapping_color = (255, 100, 100)

    def open_menu(self):
        self.active = True
        self.selected_index = 0
        self.swap_index = None
        print("--- MENÚ ABIERTO ---")

    def close_menu(self):
        self.active = False
        self.swap_index = None

    def handle_input(self, event):
        if not self.active:
            return

        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.player.team)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.player.team)

        elif event.key == pygame.K_z:
            if self.swap_index is None:
                self.swap_index = self.selected_index
            else:
                self.swap_pokemon(self.swap_index, self.selected_index)
                self.swap_index = None

        elif event.key == pygame.K_x or event.key == pygame.K_RETURN:
            if self.swap_index is not None:
                self.swap_index = None
            else:
                self.close_menu()

    def swap_pokemon(self, i1, i2):
        self.player.team[i1], self.player.team[i2] = self.player.team[i2], self.player.team[i1]

    def draw(self, surface):
        if not self.active:
            return

        # 1. Fondo
        surface.fill(self.bg_color)

        # 2. Título (Más pequeño y pegado arriba)
        title = self.font.render("EQUIPO (Z: Mover | X: Salir)", True, self.text_color)
        surface.blit(title, (10, 5))

        # 3. Lista de Pokémon (Espaciado reducido)
        start_y = 25  # Empezamos más arriba
        row_height = 20  # Altura de cada fila (antes 40)

        for i, pokemon in enumerate(self.player.team):
            color = self.text_color
            prefix = " "

            if i == self.swap_index:
                color = self.swapping_color
                prefix = "*"
            elif i == self.selected_index:
                color = self.selected_color
                prefix = ">"

                # Dibujamos Mini Icono (Escalado a 16x16 para que quepa)
            icon_x = 10
            icon_y = start_y + i * row_height

            if pokemon.sprite_front:
                # Usamos sprite_front para el icono
                icon = pygame.transform.scale(pokemon.sprite_front, (16, 16))
                surface.blit(icon, (icon_x, icon_y))

            # Dibujamos Texto al lado del icono
            text_x = 35
            # Ajuste de texto para compensar la posición del icono
            info = f"{prefix} {pokemon.name} N.{pokemon.level}"

            # Barra de vida simple (texto)
            hp_info = f"{pokemon.current_hp}/{pokemon.max_hp}"

            # Renderizamos nombre
            text_surf = self.font.render(info, True, color)
            surface.blit(text_surf, (text_x, icon_y + 2))

            # Renderizamos HP a la derecha (alineado)
            hp_surf = self.font.render(hp_info, True, (200, 200, 200))
            surface.blit(hp_surf, (160, icon_y + 2))