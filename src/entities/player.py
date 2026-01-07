import pygame
from src.config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_manager):
        super().__init__()
        self.map_manager = map_manager

        sprite_filename = "player_overworld.png"
        sprite_path = os.path.join(SPRITES_DIR, sprite_filename)

        self.animations = {
            'down': [],
            'left': [],
            'right': [],
            'up': []
        }
        self.direction = 'up'
        self.frame_index = 0
        self.animation_speed = 0.21
        self.animation_timer = 0
        self.player_name = "Lucas"
        self.team = []

        try:

            raw_sheet = pygame.image.load(sprite_path).convert_alpha()
            new_width = raw_sheet.get_width() // 2
            new_height = raw_sheet.get_height() // 2
            full_sheet = pygame.transform.scale(raw_sheet, (new_width, new_height))

            directions_list = ['down', 'left', 'right', 'up']

            for row_index, anim_name in enumerate(directions_list):
                for col_index in range(4):
                    x_pos = col_index * 32
                    y_pos = row_index * 32

                    frame = full_sheet.subsurface((x_pos, y_pos, 32, 32))
                    self.animations[anim_name].append(frame)

            # Imagen inicial
            self.image = self.animations['down'][0]

        except Exception as e:
            print(f"Error animación: {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()


        target_bottom_y = (y + 1) * TILE_SIZE
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        self.rect.width = 14
        self.rect.height = 10
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        self.velocity = pygame.math.Vector2(0, 0)
        self.current_speed = PLAYER_SPEED


    def get_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_LSHIFT]:
            self.current_speed = PLAYER_RUN_SPEED
            self.animation_speed = 0.15
        else:
            self.current_speed = PLAYER_SPEED
            self.animation_speed = 0.21

        # Movimiento
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.current_speed
            self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.current_speed
            self.direction = 'right'
        elif keys[pygame.K_UP]:
            self.velocity.y = -self.current_speed
            self.direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.current_speed
            self.direction = 'down'

    def check_collisions(self, direction):
        indice_choque = self.rect.collidelist(self.map_manager.walls)
        if indice_choque != -1:
            wall = self.map_manager.walls[indice_choque]
            if direction == 'horizontal':
                if self.velocity.x > 0:
                    self.rect.right = wall.left
                elif self.velocity.x < 0:
                    self.rect.left = wall.right
            if direction == 'vertical':
                if self.velocity.y > 0:
                    self.rect.bottom = wall.top
                elif self.velocity.y < 0:
                    self.rect.top = wall.bottom

    def animate(self):

        is_moving = self.velocity.x != 0 or self.velocity.y != 0

        if is_moving:
            self.animation_timer += 0.05

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index >= len(self.animations[self.direction]):
                    self.frame_index = 0
        else:

            self.frame_index = 0
            self.animation_timer = 0

        self.image = self.animations[self.direction][int(self.frame_index)]

    def update(self):
        self.get_input()

        # Movimiento X
        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')

        # Movimiento Y
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

        # ANIMACIÓN
        self.animate()

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            self.team.append(pokemon)
            print(f"¡Has obtenido a {pokemon.name}!")
        else:
            print("Tu equipo está lleno.")