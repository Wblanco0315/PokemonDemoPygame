import pygame
import sys
from src.config import *
from src.entities import Player, Roark, Pokemon
from src.systems import MapManager, Camera, DialogueManager, TextManager, BattleManager, DataManager, MenuManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # INICIAR SISTEMAS
        self.map_manager = MapManager("mapa_test.tmx")
        self.camera = Camera(self.map_manager.width, self.map_manager.height)
        self.text_manager = TextManager("ES.json")
        self.dialogue_manager = DialogueManager()
        self.battle_manager = BattleManager()
        self.data_manager = DataManager()

        # GRUPOS DE SPRITES
        self.all_sprites = pygame.sprite.Group()
        # CREAR JUGADOR
        self.player = Player(9, 28, self.map_manager)

        self.all_sprites.add(self.player)
        self.npcs = pygame.sprite.Group()

        # Crear a Roark
        lider_gimnasio = Roark(9, 5)
        self.all_sprites.add(lider_gimnasio)
        self.npcs.add(lider_gimnasio)

        self.menu_manager = MenuManager(self.player)

        # Colisiones
        self.map_manager.walls.append(lider_gimnasio.rect)

        team_ids = ["bulbasaur", "eevee", "rattata"]

        for p_id in team_ids:
            p_data = self.data_manager.get_pokemon_data(p_id)
            if p_data:
                # Creamos el Pokemon
                new_poke = Pokemon(p_id, p_data, self.data_manager.moves, level=5)
                # Lo añadimos a la mochila
                self.player.add_pokemon(new_poke)
                print(f"DEBUG: {new_poke.name} añadido.")

    def update(self):
        if self.battle_manager.active:
            self.battle_manager.update()
            return

        if self.menu_manager.active:
            return

        if not self.dialogue_manager.active:
            self.player.update()

        self.camera.update(self.player)

    def draw(self):
        # --- ESTADO DE BATALLA ---
        if self.battle_manager.active:
            self.battle_manager.draw(self.virtual_surface)

        elif self.menu_manager.active:
            self.menu_manager.draw(self.virtual_surface)
        else:
            self.virtual_surface.fill(BLACK)

            offset_x = self.camera.camera.x
            offset_y = self.camera.camera.y
            self.virtual_surface.blit(self.map_manager.image, (offset_x, offset_y))

            for sprite in self.all_sprites:
                offset_pos = (sprite.rect.x + offset_x, sprite.rect.y + offset_y)
                self.virtual_surface.blit(sprite.image, offset_pos)

            self.dialogue_manager.draw(self.virtual_surface)

        # 3. Escalar a pantalla completa (Común para ambos estados)
        scaled_surface = pygame.transform.scale(self.virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def check_interaction(self):
        if self.dialogue_manager.active:
            self.dialogue_manager.advance()
            return

        player_grid_x = int(self.player.rect.centerx // TILE_SIZE)
        player_grid_y = int(self.player.rect.centery // TILE_SIZE)

        target_x = player_grid_x
        target_y = player_grid_y

        if self.player.direction == 'left':
            target_x -= 1
        elif self.player.direction == 'right':
            target_x += 1
        elif self.player.direction == 'up':
            target_y -= 1
        elif self.player.direction == 'down':
            target_y += 1

        for npc in self.npcs:
            if int(npc.grid_x) == target_x and int(npc.grid_y) == target_y:

                lines = npc.interact(self.text_manager)

                if lines:
                    self.dialogue_manager.start_dialogue(lines)
                return

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.menu_manager.active:
                    if event.type == pygame.KEYDOWN:
                        self.menu_manager.handle_input(event)
                    continue

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:

                        if not self.battle_manager.active and not self.dialogue_manager.active:
                            self.menu_manager.open_menu()

                    if event.key == pygame.K_z:
                        self.check_interaction()

                    if event.key == pygame.K_b:
                        enemy = self.npcs.sprites()[0]
                        self.battle_manager.start_battle(enemy)

            self.update()
            self.draw()
            self.clock.tick(FPS)
            # -----------------------------------

        pygame.quit()
        sys.exit()
