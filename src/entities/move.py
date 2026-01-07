class Move:
    def __init__(self, move_id, move_data):
        self.id = move_id
        self.name = move_data.get('name', '???')
        self.type = move_data.get('type', 'normal')
        self.power = move_data.get('power', 0)
        self.current_pp = move_data.get('pp', 0)
        self.max_pp = self.current_pp