import pygame
import pytmx
import os
from src.config import *


class MapManager:
    def __init__(self, filename):
        # 1. Cargar el archivo .tmx
        tmx_path = os.path.join(MAPS_DIR, filename)

        # 'load_pygame' ayuda a cargar las imágenes correctamente
        try:
            self.tmx_data = pytmx.util_pygame.load_pygame(tmx_path)
        except Exception as e:
            print(f"ERROR: No se pudo cargar el mapa en {tmx_path}")
            print(f"Detalle: {e}")
            # Crear un mapa vacío de emergencia para que no crashee
            self.tmx_data = None

        # Dimensiones del mapa
        if self.tmx_data:
            self.width = self.tmx_data.width * self.tmx_data.tilewidth
            self.height = self.tmx_data.height * self.tmx_data.tileheight
        else:
            self.width = VIRTUAL_WIDTH
            self.height = VIRTUAL_HEIGHT

        # 2. GENERAR IMAGEN VISUAL
        self.image = self.render_map()

        # 3. GENERAR COLISIONES (Esta es la parte que te faltaba)
        self.walls = []  # Creamos la lista vacía

        if self.tmx_data:
            # Recorremos todos los objetos creados en Tiled
            for obj in self.tmx_data.objects:
                # IMPORTANTE: Aquí verificamos el nombre de la capa en Tiled.
                # Asegúrate de que en Tiled tu capa se llame "Colisiones" (o cambia este nombre)
                if obj.parent.name == "Colisiones":
                    # Creamos un rectángulo de PyGame con los datos de Tiled
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.walls.append(rect)

    def render_map(self):
        # Crear un lienzo vacío del tamaño del mapa completo
        temp_surface = pygame.Surface((self.width, self.height))

        if self.tmx_data:
            # Pintamos el suelo y decoración base
            for layer in self.tmx_data.visible_layers:
                # Solo pintamos capas de patrones (tiles), no la capa de objetos (cuadrados rojos)
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            temp_surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

        return temp_surface

    def draw(self, surface, camera_rect):
        # Dibuja el mapa desplazado por la cámara
        offset_x = -camera_rect.x
        offset_y = -camera_rect.y
        surface.blit(self.image, (offset_x, offset_y))

        # (Opcional) Descomenta estas 3 líneas para VER las colisiones en rojo (DEBUG)
        # for wall in self.walls:
        #     rect_visual = wall.move(offset_x, offset_y)
        #     pygame.draw.rect(surface, (255, 0, 0), rect_visual, 1)