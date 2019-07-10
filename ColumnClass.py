from SlotClass import Slot


class Column:

    _xIndex: int
    _height: int
    _no_counters: int

    def __init__(self, x_index, height, win_length):
        self._xIndex = x_index
        self._height = height
        self._no_counters = 0
        self._win_length = win_length
        self._slots = []
        self._create_slots()

    def _create_slots(self):
        for i in range( self._height):
            self._slots.append(Slot())

    def get_slots(self):
        return self._slots

    def is_full(self):
        if self._no_counters < self._height:
            return False
        else:
            print("That column is already full, choose another!")
            return True

    def add_counter(self, player):
        '''
        Adds counter to the column if not already full. Returns true if succeeded.
        :param player:
        :return:
        '''
        #Check that this column isn't already full
        success = False
        if self._no_counters >= self._height:
            print("That column is already full, choose another!")
        else:
            #Add counter to lowest available slot:
            self._slots[self._no_counters].assign_owner(player)
            self._no_counters = self._no_counters + 1
            success = True
        return success

