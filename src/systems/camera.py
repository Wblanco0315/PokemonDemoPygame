import pygame
from src.config import *


class Camera:
    def __init__(self, map_width, map_height):
        # OBTENER TAMAÑO DEL MAPA
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # CENTRAR CAMARA EN EL JUGADOR
        x = -target.rect.x + int(VIRTUAL_WIDTH / 2)
        y = -target.rect.y + int(VIRTUAL_HEIGHT / 2)

        # LIMITAR LA CÁMARA
        x = min(0, x)
        y = min(0, y)

        # LIMITE DERECHO (NO MOSTRAR LO NEGRO MÁS ALLÁ DEL ANCHO DEL MAPA)
        x = max(-(self.map_width - VIRTUAL_WIDTH), x)
        # LIMITE ABAJO (NO MOSTRAR LO NEGRO MÁS ALLÁ DEL ALTO DEL MAPA)
        y = max(-(self.map_height - VIRTUAL_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)