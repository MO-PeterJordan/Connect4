from PlayerClass import Player

class Slot:

    _owner: Player

    def __init__(self):
        self._owner = None

    def assign_owner(self, player):
        self._owner = player

    def get_owner(self):
        return self._owner

