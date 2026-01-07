import os

VIRTUAL_WIDTH = 240
VIRTUAL_HEIGHT = 160
SCALE = 3
WINDOW_WIDTH = VIRTUAL_WIDTH * SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * SCALE
FPS = 30
TITLE = "Pokemon Tech Demo"

TILE_SIZE = 16
PLAYER_SPEED = 1 # Caminando
PLAYER_RUN_SPEED = 2 # Corriendo

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
MAPS_DIR = os.path.join(ASSETS_DIR, 'maps')
SPRITES_DIR = os.path.join(ASSETS_DIR, 'sprites')
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts", "default_font.ttf")