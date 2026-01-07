import pygame
from src.config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_manager):
        super().__init__()
        self.map_manager = map_manager

        # CARGAR SPRITES
        sprite_filename = "player_overworld.png"  # NOMBRE DEL ARCHIVO DEL SPRITESHEET
        sprite_path = os.path.join(SPRITES_DIR, sprite_filename)  # RUTA DE SPRITESHEET

        self.animations = {'down': [], 'left': [], 'right': [], 'up': []}  # DICCIONARIO DE ANIMACIONES
        self.direction = 'up'  # DIRECCION DE SPRITE
        self.frame_index = 0  # INDICE DE FRAME DE ANIMACION
        self.animation_speed = 0.21  # VELOCIDAD DE ANIMACION
        self.animation_timer = 0  # TEMPORIZADOR DE ANIMACION
        self.player_name = "Lucas"  # NOMBRE DEL JUGADOR
        self.team = []  # LISTA DE POKEMON DEL JUGADOR

        try:
            # ESCALAR SPRITESHEET
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

            # POSICION INICIAL
            self.image = self.animations['down'][0]

        except Exception as e:
            print(f"Error animación: {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((255, 0, 0))

        # POSICION EN EL MUNDO
        self.rect = self.image.get_rect()
        target_bottom_y = (y + 1) * TILE_SIZE
        self.rect.midbottom = (x * TILE_SIZE + TILE_SIZE / 2, target_bottom_y)

        # HITBOX
        self.hitbox = self.rect.inflate(-18, -20)
        self.hitbox.width = 14
        self.hitbox.height = 10
        self.hitbox.midbottom = self.rect.midbottom

        # MOVIMIENTO
        self.velocity = pygame.math.Vector2(0, 0)
        self.current_speed = PLAYER_SPEED

    # DETECCION DE ENTRADA
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

    # REVISAR COLISIONES CON PAREDES
    def check_collisions(self, direction):

        indice_choque = self.hitbox.collidelist(self.map_manager.walls)

        if indice_choque != -1:
            wall = self.map_manager.walls[indice_choque]
            if direction == 'horizontal':
                if self.velocity.x > 0:
                    self.hitbox.right = wall.left
                elif self.velocity.x < 0:
                    self.hitbox.left = wall.right
            if direction == 'vertical':
                if self.velocity.y > 0:
                    self.hitbox.bottom = wall.top
                elif self.velocity.y < 0:
                    self.hitbox.top = wall.bottom

    # ANIMACION DE JUGADOR
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

    # ACTUALIZACION DEL JUGADOR
    def update(self):
        self.get_input()

        # MOVER HITBOX EN X
        self.hitbox.x += self.velocity.x
        self.check_collisions('horizontal')

        # MOVER HITBOX EN Y
        self.hitbox.y += self.velocity.y
        self.check_collisions('vertical')

        # SINCRONIZAR: EL SPRITE (RECT) DEBE SEGUIR A LA HITBOX
        self.rect.center = self.hitbox.center

        # ANIMACION
        self.animate()

    # AÑADIR POKEMON AL EQUIPO
    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            self.team.append(pokemon)
            print(f"¡Has obtenido a {pokemon.name}!")
        else:
            print("Tu equipo está lleno.")
