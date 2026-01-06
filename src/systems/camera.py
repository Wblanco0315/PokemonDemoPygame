import pygame
from src.config import *


class Camera:
    def __init__(self, map_width, map_height):
        # Necesitamos saber cuánto mide el mapa para no salirnos
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # 1. Calcular la posición ideal (centrada en el jugador)
        x = -target.rect.x + int(VIRTUAL_WIDTH / 2)
        y = -target.rect.y + int(VIRTUAL_HEIGHT / 2)

        # 2. LIMITAR LA CÁMARA (Clamping)
        # Límite Izquierdo (No pasar de 0)
        x = min(0, x)
        # Límite Arriba (No pasar de 0)
        y = min(0, y)

        # Límite Derecho (No mostrar lo negro más allá del ancho del mapa)
        # La cámara no puede ir más allá de -(AnchoMapa - AnchoPantalla)
        x = max(-(self.map_width - VIRTUAL_WIDTH), x)

        # Límite Abajo (No mostrar lo negro más allá del alto del mapa)
        y = max(-(self.map_height - VIRTUAL_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)