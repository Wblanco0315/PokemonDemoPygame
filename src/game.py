import pygame
import sys
from src.config import *
from src.entities import Player, Roark, Pokemon
from src.systems import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.setup_game()

    def setup_game(self):
        print("--- INICIANDO/REINICIANDO JUEGO ---")
        # INICIAR SISTEMAS
        self.map_manager = MapManager("mapa_test.tmx")
        self.camera = Camera(self.map_manager.width, self.map_manager.height)
        self.text_manager = TextManager("ES.json")
        self.dialogue_manager = DialogueManager()
        self.battle_manager = BattleManager()
        self.data_manager = DataManager()
        self.menu_manager = MenuManager(None)
        self.title_manager = TitleManager()
        self.game_over_manager = GameOverManager()
        self.next_event = "PLAYER_START_DIALOGUE"

        # GRUPOS DE SPRITES
        self.all_sprites = pygame.sprite.Group()

        # CREAR JUGADOR
        self.player = Player(9, 28, self.map_manager)
        self.all_sprites.add(self.player)

        # ACTUALIZAR MENU MANAGER CON EL JUGADOR REAL
        self.menu_manager.player = self.player
        self.npcs = pygame.sprite.Group()

        # CREAR A ROARK
        lider_gimnasio = Roark(9, 5)
        self.all_sprites.add(lider_gimnasio)
        self.npcs.add(lider_gimnasio)
        self.roark_team = []
        self.roark_defeated = False

        # COLISIONES
        self.map_manager.walls.append(lider_gimnasio.rect)

        # CARGAR POKEMON
        self.load_teams()

    def load_teams(self):
        team_ids = ["bulbasaur", "eevee", "rattata"]
        roark_team_ids = ["geodude", "onix", "diglett"]

        for p_id in team_ids:
            p_data = self.data_manager.get_pokemon_data(p_id)
            if p_data:
                new_poke = Pokemon(p_id, p_data, self.data_manager.moves, level=10)
                self.player.add_pokemon(new_poke)

        for p_id in roark_team_ids:
            p_data = self.data_manager.get_pokemon_data(p_id)
            if p_data:
                new_poke = Pokemon(p_id, p_data, self.data_manager.moves, level=12)
                self.roark_team.append(new_poke)

    def update(self):

        if self.game_over_manager.active:
            if self.game_over_manager.restart_requested:
                self.setup_game()
                self.title_manager.active = False
            return

        if self.title_manager.active:
            self.title_manager.update()
            return

        if self.battle_manager.active:
            self.battle_manager.update()
            return

        if self.menu_manager.active:
            return

        if not self.dialogue_manager.active:
            self.player.update()

        self.camera.update(self.player)

        if not self.dialogue_manager.active and self.next_event == "PLAYER_START_DIALOGUE":
            lines = self.text_manager.get_dialogue("player_start")
            self.dialogue_manager.start_dialogue(lines)
            self.next_event = None

        # Evento: Inicio Batalla
        elif not self.dialogue_manager.active and self.next_event == "START_ROARK_BATTLE":
            self.battle_manager.start_battle(self.player.team, self.roark_team)
            self.next_event = "CHECK_BATTLE_RESULT"

        # Evento: Fin Batalla -> Diálogo Resultado
        elif not self.battle_manager.active and self.next_event == "CHECK_BATTLE_RESULT":
            if self.battle_manager.winner == "PLAYER":
                self.roark_defeated = True
                lines = self.text_manager.get_dialogue(
                    "roark_defeat")  # Asegúrate que tu TextManager use get o get_dialogue
                self.dialogue_manager.start_dialogue(lines)
            else:
                lines = self.text_manager.get_dialogue("roark_win")
                self.dialogue_manager.start_dialogue(lines)

            self.next_event = "WAIT_END_DIALOGUE"

        # Evento: Fin Diálogo -> Pantalla Game Over
        elif not self.dialogue_manager.active and self.next_event == "WAIT_END_DIALOGUE":
            # Mostrar pantalla final
            self.game_over_manager.show(self.battle_manager.winner)
            self.next_event = None

    def draw(self):

        # PANTALLA DE  GAME OVER
        if self.game_over_manager.active:
            self.game_over_manager.draw(self.virtual_surface)

        # PANTALLA DE TÍTULO
        elif self.title_manager.active:
            self.title_manager.draw(self.virtual_surface)

        # BATALLA
        elif self.battle_manager.active:
            self.battle_manager.draw(self.virtual_surface)

        # MENÚ
        elif self.menu_manager.active:
            self.menu_manager.draw(self.virtual_surface)

        # JUEGO NORMAL
        else:
            self.virtual_surface.fill(BLACK)
            offset_x = self.camera.camera.x
            offset_y = self.camera.camera.y

            # DIBUJAR MAPA
            self.virtual_surface.blit(self.map_manager.image, (offset_x, offset_y))

            # DIBUJAR SPRITES
            for sprite in self.all_sprites:
                offset_pos = (sprite.rect.x + offset_x, sprite.rect.y + offset_y)
                self.virtual_surface.blit(sprite.image, offset_pos)

            self.dialogue_manager.draw(self.virtual_surface)

        # ESCALAR A PANTALLA COMPLETA
        scaled_surface = pygame.transform.scale(self.virtual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    # COMPROBAR INTERACCION CON NPCS
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
                if isinstance(npc, Roark):
                    if not self.roark_defeated:
                        lines = self.text_manager.get_dialogue("player_before_battle") + self.text_manager.get_dialogue("roark_intro")
                        self.dialogue_manager.start_dialogue(lines)
                        self.next_event = "START_ROARK_BATTLE"
                    else:
                        lines = self.text_manager.get_dialogue("player_after_roark")
                        self.dialogue_manager.start_dialogue(lines)
                else:
                    lines = npc.interact(self.text_manager)
                    if lines:
                        self.dialogue_manager.start_dialogue(lines)
                return

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.game_over_manager.active:
                    self.game_over_manager.handle_input(event)
                    continue

                if self.title_manager.active:
                    self.title_manager.handle_input(event)
                    continue

                if self.battle_manager.active:
                    self.battle_manager.handle_input(event)
                    continue

                if self.menu_manager.active:
                    if event.type == pygame.KEYDOWN:
                        self.menu_manager.handle_input(event)
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.dialogue_manager.active:
                            self.menu_manager.open_menu()

                    if event.key == pygame.K_z:
                        self.check_interaction()

                    if event.key == pygame.K_b:
                        self.battle_manager.start_battle(self.player.team, self.roark_team)
                        self.next_event = "CHECK_BATTLE_RESULT"

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()