class Player:

    myTurn: bool
    name: str
    number: int

    def __init__(self, name, colour):
        self._name = name
        self._colour = colour
        self._myTurn = False

    def get_name(self):
        return self._name

    def get_colour(self):
        return self._colour

    def is_it_my_turn(self):
        return self._myTurn

    def swapTurn(self):
        if self._myTurn:
            self._myTurn = False
        else:
            self._myTurn = True

