import pygame
import os
from src.config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_manager):
        super().__init__()
        self.map_manager = map_manager

        # --- CONFIGURACIÓN DE ANIMACIÓN ---
        sprite_filename = "player_overworld.png"
        sprite_path = os.path.join(SPRITES_DIR, sprite_filename)

        # Diccionario para guardar las tiras de imágenes
        self.animations = {
            'down': [],
            'left': [],
            'right': [],
            'up': []
        }
        self.direction = 'up'  # Dirección actual
        self.frame_index = 0  # Qué cuadro de la animación mostrar (0-3)
        self.animation_speed = 0.21  # Velocidad del cambio (más bajo = más rápido)
        self.animation_timer = 0  # Contador interno

        try:
            # 1. Cargar y Escalar (Igual que antes)
            raw_sheet = pygame.image.load(sprite_path).convert_alpha()
            # Escalar al 50% (de 64x64 a 32x32 por cuadro)
            new_width = raw_sheet.get_width() // 2
            new_height = raw_sheet.get_height() // 2
            full_sheet = pygame.transform.scale(raw_sheet, (new_width, new_height))

            directions_list = ['down', 'left', 'right', 'up']

            for row_index, anim_name in enumerate(directions_list):
                for col_index in range(4):  # 4 frames por animación
                    x_pos = col_index * 32
                    y_pos = row_index * 32

                    # Recortamos el cuadro
                    frame = full_sheet.subsurface((x_pos, y_pos, 32, 32))
                    self.animations[anim_name].append(frame)

            # Imagen inicial
            self.image = self.animations['down'][0]

        except Exception as e:
            print(f"Error animación: {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 0, 0))

        # --- FÍSICA Y POSICIÓN ---
        self.rect = self.image.get_rect()

        # Posición inicial
        target_bottom_y = (y + 1) * TILE_SIZE
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        # Hitbox Ajustada
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

        # Solo cambiamos 'self.direction' si se presiona una tecla
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
        # 1. ¿Nos estamos moviendo?
        is_moving = self.velocity.x != 0 or self.velocity.y != 0

        if is_moving:
            # 2. Aumentar el timer
            self.animation_timer += 0.05  # Ajusta este número si va muy lento/rápido

            # 3. Cambiar de frame si el timer supera la velocidad
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index += 1

                # Si llegamos al final (4), volver a empezar
                if self.frame_index >= len(self.animations[self.direction]):
                    self.frame_index = 0
        else:
            # Si está quieto, mostrar el frame 0 (parado) y resetear
            self.frame_index = 0
            self.animation_timer = 0

        # 4. Actualizar la imagen actual según la dirección y el índice
        self.image = self.animations[self.direction][int(self.frame_index)]

    def update(self):
        self.get_input()

        # Movimiento X
        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')

        # Movimiento Y
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

        # ANIMACIÓN (Nuevo paso vital)
        self.animate()