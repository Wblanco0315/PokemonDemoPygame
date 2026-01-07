import pygame
import pytmx
from src.config import *

class MapManager:
    def __init__(self, filename):
        tmx_path = os.path.join(MAPS_DIR, filename)

        try:
            self.tmx_data = pytmx.util_pygame.load_pygame(tmx_path)
        except Exception as e:
            print(f"ERROR: No se pudo cargar el mapa en {tmx_path}")
            print(f"Detalle: {e}")
            self.tmx_data = None

        # Dimensiones del mapa
        if self.tmx_data:
            self.width = self.tmx_data.width * self.tmx_data.tilewidth
            self.height = self.tmx_data.height * self.tmx_data.tileheight
        else:
            self.width = VIRTUAL_WIDTH
            self.height = VIRTUAL_HEIGHT

        self.image = self.render_map()

        self.walls = []

        if self.tmx_data:
            for layer in self.tmx_data.layers:
                if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Collisions":
                    for obj in layer:
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.walls.append(rect)

    def render_map(self):
        temp_surface = pygame.Surface((self.width, self.height))

        if self.tmx_data:
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            temp_surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

        return temp_surface

    def draw(self, surface, camera_rect):
        offset_x = -camera_rect.x
        offset_y = -camera_rect.y
        surface.blit(self.image, (offset_x, offset_y))

        # DEBUG: Dibuja cuadros rojos donde hay colisiones
        for wall in self.walls:
            rect_visual = wall.move(offset_x, offset_y)
            pygame.draw.rect(surface, (255, 0, 0), rect_visual, 1)