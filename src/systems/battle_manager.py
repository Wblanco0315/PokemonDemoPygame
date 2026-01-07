import pygame
import random
from src.config import *


class BattleManager:
    def __init__(self):
        self.active = False
        self.turn = "PLAYER"
        self.state = "MENU"  # MENU | ATTACK_SELECT | ANIMATION | END | SWITCH_POKEMON
        self.timer = 0
        self.turn_step = 0

        # --- RECURSOS ---
        font_path = os.path.join(ASSETS_DIR, "fonts", "default_font.ttf")
        try:
            self.font = pygame.font.Font(font_path, 8)
            self.font_hp = pygame.font.Font(font_path, 8)
        except:
            self.font = pygame.font.Font(None, 12)
            self.font_hp = pygame.font.Font(None, 12)

        bg_path = os.path.join(ASSETS_DIR, "sprites", "backgrounds", "battle_background.png")
        try:
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        except:
            self.bg_image = None

        # Colores
        self.color_bg = (20, 20, 30)
        self.color_ui_bg = (40, 40, 50)
        self.color_hp_high = (100, 255, 100)
        self.color_hp_mid = (255, 200, 50)
        self.color_hp_low = (255, 50, 50)

        # Variables de combate
        self.player_team = []
        self.enemy_team = []
        self.player_pokemon = None
        self.enemy_pokemon = None
        self.current_move = None
        self.message = ""

        # UI Variables
        self.menu_option = 0
        self.move_option = 0
        self.switch_option = 0
        self.force_switch = False

    def start_battle(self, player_team, enemy_team):
        self.active = True
        self.player_team = player_team
        self.enemy_team = enemy_team

        self.player_pokemon = self.get_first_available(player_team)
        self.enemy_pokemon = self.get_first_available(enemy_team)

        if not self.player_pokemon or not self.enemy_pokemon:
            print("Error: Equipos vacíos o todos debilitados")
            self.active = False
            return

        self.turn = "PLAYER"
        self.state = "MENU"
        self.menu_option = 0
        self.message = f"¡{self.enemy_pokemon.name} salvaje aparecio!"

    def get_first_available(self, team):
        for p in team:
            if not p.is_fainted:
                return p
        return None

    def get_available_count(self, team):
        return sum(1 for p in team if not p.is_fainted)

    def calculate_damage(self, attacker, defender, move):
        # 1. Efectividad
        type_chart = {
            "fire": {"grass": 2.0, "water": 0.5, "rock": 0.5},
            "water": {"fire": 2.0, "grass": 0.5, "ground": 2.0, "rock": 2.0},
            "grass": {"water": 2.0, "ground": 2.0, "rock": 2.0, "fire": 0.5},
            "rock": {"fire": 2.0, "ground": 0.5},
            "ground": {"fire": 2.0, "rock": 2.0, "grass": 0.5},
            "normal": {"rock": 0.5}
        }

        multiplier = 1.0
        attacker_chart = type_chart.get(move.type, {})
        multiplier = attacker_chart.get(defender.type, 1.0)

        # 2. Formula
        level_factor = (2 * attacker.level / 5) + 2
        stat_ratio = attacker.attack / defender.defense
        base_damage = (level_factor * move.power * stat_ratio / 50) + 2

        # 3. Variación
        random_factor = random.uniform(0.85, 1.0)
        final_damage = int(base_damage * multiplier * random_factor)
        if final_damage < 1: final_damage = 1

        msg = ""
        if multiplier > 1:
            msg = " ¡Es muy eficaz!"
        elif multiplier < 1:
            msg = " No es muy eficaz..."

        return final_damage, msg

    def handle_input(self, event):
        if self.state == "ANIMATION" or self.state == "END":
            return

        if event.type != pygame.KEYDOWN:
            return

        # --- MENU PRINCIPAL ---
        if self.state == "MENU":
            if event.key == pygame.K_RIGHT:
                self.menu_option = (self.menu_option + 1) % 4
            elif event.key == pygame.K_LEFT:
                self.menu_option = (self.menu_option - 1) % 4
            elif event.key == pygame.K_UP:
                self.menu_option = (self.menu_option - 2) % 4
            elif event.key == pygame.K_DOWN:
                self.menu_option = (self.menu_option + 2) % 4

            elif event.key == pygame.K_z:
                if self.menu_option == 0:  # FIGHT
                    self.state = "ATTACK_SELECT"
                    self.move_option = 0
                elif self.menu_option == 2:  # POKEMON
                    self.state = "SWITCH_POKEMON"
                    self.switch_option = 0
                    self.force_switch = False
                elif self.menu_option == 3:  # RUN
                    self.active = False

        # --- SELECCIÓN ATAQUE ---
        elif self.state == "ATTACK_SELECT":
            num_moves = len(self.player_pokemon.moves)
            if num_moves == 0: return

            if event.key == pygame.K_DOWN:
                self.move_option = (self.move_option + 1) % num_moves
            elif event.key == pygame.K_UP:
                self.move_option = (self.move_option - 1) % num_moves
            elif event.key == pygame.K_x:
                self.state = "MENU"

            elif event.key == pygame.K_z:
                move = self.player_pokemon.moves[self.move_option]
                if move.current_pp > 0:
                    self.current_move = move
                    self.start_turn_sequence()
                else:
                    self.message = "¡No quedan PP!"
                    self.state = "ANIMATION"
                    self.turn_step = 99

        # --- SELECCIÓN DE POKEMON ---
        elif self.state == "SWITCH_POKEMON":
            team_size = len(self.player_team)

            if event.key == pygame.K_DOWN:
                self.switch_option = (self.switch_option + 1) % team_size
            elif event.key == pygame.K_UP:
                self.switch_option = (self.switch_option - 1) % team_size
            elif event.key == pygame.K_x:
                if not self.force_switch:
                    self.state = "MENU"

            elif event.key == pygame.K_z:
                selected_poke = self.player_team[self.switch_option]
                if selected_poke == self.player_pokemon:
                    print("Ya en combate")
                elif selected_poke.is_fainted:
                    print("Está debilitado")
                else:
                    self.player_pokemon = selected_poke
                    self.message = f"¡Adelante {selected_poke.name}!"
                    self.state = "ANIMATION"
                    self.turn_step = 10
                    if not self.force_switch:
                        self.turn_step = 10

    def start_turn_sequence(self):
        self.state = "ANIMATION"
        self.turn_step = 0
        self.timer = 0

    def update(self):
        if self.state == "ANIMATION":
            self.timer += 1
            wait_time = 45

            # --- PASO 0: Texto Jugador ---
            if self.turn_step == 0:
                if self.timer == 1:
                    self.message = f"{self.player_pokemon.name} uso {self.current_move.name}!"
                if self.timer > wait_time:
                    self.timer = 0
                    self.turn_step = 1

            # --- PASO 1: Daño Jugador ---
            elif self.turn_step == 1:
                if self.timer == 1:
                    self.current_move.current_pp -= 1
                    dmg, ef_msg = self.calculate_damage(self.player_pokemon, self.enemy_pokemon, self.current_move)
                    self.enemy_pokemon.take_damage(dmg)
                    self.message = f"Causo {dmg} de daño.{ef_msg}"

                if self.timer > wait_time:
                    self.timer = 0
                    if self.enemy_pokemon.is_fainted:
                        self.turn_step = 5
                    else:
                        self.turn_step = 2

            # --- PASO 2: Turno Enemigo (IA) ---
            elif self.turn_step == 2:
                if self.timer == 1:
                    if self.enemy_pokemon.moves:
                        self.current_move = random.choice(self.enemy_pokemon.moves)
                        self.message = f"¡{self.enemy_pokemon.name} uso {self.current_move.name}!"
                    else:
                        self.message = "¡El enemigo no hace nada!"
                        self.turn_step = 3

                if self.timer > wait_time:
                    self.timer = 0
                    self.turn_step = 3

            # --- PASO 3: Daño Enemigo ---
            elif self.turn_step == 3:
                if self.timer == 1:
                    dmg, ef_msg = self.calculate_damage(self.enemy_pokemon, self.player_pokemon, self.current_move)
                    self.player_pokemon.take_damage(dmg)
                    self.message = f"Recibiste {dmg} de daño.{ef_msg}"

                if self.timer > wait_time:
                    self.timer = 0
                    if self.player_pokemon.is_fainted:
                        self.turn_step = 6
                    else:
                        self.state = "MENU"
                        self.message = "¿Qué debería hacer?"

            # --- PASO 5: ENEMIGO DEBILITADO ---
            elif self.turn_step == 5:
                if self.timer == 1:
                    self.message = f"¡{self.enemy_pokemon.name} se debilito!"

                if self.timer > wait_time:
                    self.timer = 0
                    available_enemies = [p for p in self.enemy_team if not p.is_fainted]
                    if len(available_enemies) > 0:
                        next_poke = random.choice(available_enemies)
                        self.enemy_pokemon = next_poke
                        self.message = f"¡El enemigo envió a {next_poke.name}!"
                        self.turn_step = 9
                    else:
                        self.message = "¡Has derrotado al equipo enemigo!"
                        self.turn_step = 7

            # --- PASO 6: JUGADOR DEBILITADO ---
            elif self.turn_step == 6:
                if self.timer == 1:
                    self.message = f"¡{self.player_pokemon.name} se debilito!"

                if self.timer > wait_time:
                    self.timer = 0
                    if self.get_available_count(self.player_team) > 0:
                        self.state = "SWITCH_POKEMON"
                        self.force_switch = True
                        self.switch_option = 0
                    else:
                        self.message = "¡No te quedan Pokémon! Fin..."
                        self.turn_step = 8

            # --- PASOS FINALES ---
            elif self.turn_step == 7:  # Win
                if self.timer > wait_time * 2: self.active = False

            elif self.turn_step == 8:  # Lose
                if self.timer > wait_time * 2: self.active = False

            elif self.turn_step == 9:  # Nuevo enemigo
                if self.timer > wait_time:
                    self.state = "MENU"
                    self.message = f"¡Adelante, {self.player_pokemon.name}!"

            elif self.turn_step == 10:  # Nuevo jugador
                if self.timer > wait_time:
                    self.timer = 0
                    if self.force_switch:
                        self.state = "MENU"
                        self.message = "¿Qué debería hacer?"
                    else:
                        self.turn_step = 2

            elif self.turn_step == 99:  # Error PP
                if self.timer > 30:
                    self.state = "ATTACK_SELECT"

    def draw(self, surface):
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
        else:
            surface.fill(self.color_bg)

        # SPRITES
        if self.enemy_pokemon and not self.enemy_pokemon.is_fainted:
            spr = self.enemy_pokemon.sprite_front
            if spr: surface.blit(spr, (VIRTUAL_WIDTH - spr.get_width() - 20, 15))

        if self.player_pokemon and not self.player_pokemon.is_fainted:
            spr = self.player_pokemon.sprite_back
            if spr: surface.blit(spr, (30, VIRTUAL_HEIGHT - spr.get_height() - 40))

        # UI
        if not self.enemy_pokemon.is_fainted:
            self.draw_hp_box(surface, self.enemy_pokemon, 10, 10, True)

        self.draw_hp_box(surface, self.player_pokemon, VIRTUAL_WIDTH - 110, VIRTUAL_HEIGHT - 70, False)
        self.draw_ui_panel(surface)

    # --- MÉTODO MODIFICADO PARA MOSTRAR NIVEL Y HP ---
    def draw_hp_box(self, surface, pokemon, x, y, is_enemy):
        if not pokemon: return
        box_width, box_height = 100, 30

        # Fondo y Borde
        pygame.draw.rect(surface, (240, 248, 240), (x, y, box_width, box_height))
        pygame.draw.rect(surface, (80, 80, 90), (x, y, box_width, box_height), 1)

        # 1. NOMBRE (Izquierda)
        name_t = self.font.render(f"{pokemon.name}", False, (0, 0, 0))
        surface.blit(name_t, (x + 5, y + 3))

        # 2. NIVEL (Derecha) - AGREGADO
        lvl_t = self.font.render(f"Nv:{pokemon.level}", False, (0, 0, 0))
        surface.blit(lvl_t, (x + box_width - 30, y + 3))

        # Barra de vida
        bar_x, bar_y, bar_w, bar_h = x + 25, y + 18, 70, 4
        pct = pokemon.current_hp / pokemon.max_hp
        if pct < 0: pct = 0
        fill_w = int(bar_w * pct)
        color = self.color_hp_high if pct > 0.5 else (self.color_hp_mid if pct > 0.2 else self.color_hp_low)

        pygame.draw.rect(surface, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, color, (bar_x, bar_y, fill_w, bar_h))

        # 3. VIDA NUMÉRICA (Solo jugador)
        if not is_enemy:
            hp_str = f"{int(pokemon.current_hp)}/{pokemon.max_hp}"
            surface.blit(self.font_hp.render(hp_str, False, (0, 0, 0)), (x + box_width - 45, y + 23))

    def draw_ui_panel(self, surface):
        panel_h = 48
        panel_y = VIRTUAL_HEIGHT - panel_h
        pygame.draw.rect(surface, self.color_ui_bg, (0, panel_y, VIRTUAL_WIDTH, panel_h))
        pygame.draw.rect(surface, (255, 255, 255), (0, panel_y, VIRTUAL_WIDTH, panel_h), 2)

        if self.state == "MENU":
            options = ["LUCHAR", "MOCHILA", "POKEMON", "HUIR"]
            coords = [(20, panel_y + 10), (130, panel_y + 10), (20, panel_y + 30), (130, panel_y + 30)]
            for i, op in enumerate(options):
                color = (255, 200, 50) if i == self.menu_option else (255, 255, 255)
                surface.blit(self.font.render(f"{'> ' if i == self.menu_option else ''}{op}", False, color), coords[i])

        elif self.state == "ATTACK_SELECT":
            move_x, move_y = 20, panel_y + 10
            for i, move in enumerate(self.player_pokemon.moves):
                col, row = i % 2, i // 2
                color = (255, 200, 50) if i == self.move_option else (255, 255, 255)
                txt = self.font.render(f"{'> ' if i == self.move_option else ''}{move.name}", False, color)
                surface.blit(txt, (move_x + col * 110, move_y + row * 15))
                if i == self.move_option:
                    type_info = f"PP {move.current_pp}/{move.max_pp} {move.type.upper()}"
                    surface.blit(self.font.render(type_info, False, (200, 200, 200)), (140, panel_y + 25))

        elif self.state == "SWITCH_POKEMON":
            list_x, list_y = 20, panel_y + 5
            if self.force_switch:
                header = self.font.render("¡Elige un Pokemon!", False, (255, 50, 50))
                surface.blit(header, (list_x, list_y))
                list_y += 10
            for i, p in enumerate(self.player_team):
                color = (255, 255, 255)
                if p.is_fainted: color = (100, 100, 100)
                if i == self.switch_option: color = (255, 200, 50)
                status = "FNT" if p.is_fainted else f"{int(p.current_hp)} HP"
                txt = f"{'> ' if i == self.switch_option else '  '}{p.name} ({status})"
                col = i // 3
                row = i % 3
                surface.blit(self.font.render(txt, False, color), (list_x + col * 110, list_y + row * 10))

        elif self.state == "ANIMATION":
            msg_surf = self.font.render(self.message, False, (255, 255, 255))
            surface.blit(msg_surf, (20, panel_y + 20))