from .npc import Npc


class Roark(Npc):
    def __init__(self, x, y):
        super().__init__(x, y, "NPC_163_Gym_Leader_Roark.png", "roark_intro")
        self.nombre = "Roark"
        self.medalla = "Medalla Roca"
        self.derrotado = False

    def interact(self, text_manager):
        if not self.derrotado:
            texto_jugador = text_manager.get_dialogue("player_before_battle")
            texto_roark = text_manager.get_dialogue("roark_intro")
            dialogo_completo = texto_jugador + texto_roark

            return dialogo_completo

        else:
            return text_manager.get_dialogue("roark_defeat")

    def defeat(self):
        self.derrotado = True