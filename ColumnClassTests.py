import unittest
from ColumnClass import Column
from PlayerClass import Player
from SlotClass import Slot


class Test_Column(unittest.TestCase):

    def setUp(self):
        self._column_height = 10
        self._win_length = 4
        self.column1 = Column(2, self._column_height, self._win_length)
        self.player1 = Player("Jarvis", "yellow")
        self.player2 = Player("Ultron", "red")

    def test_create_slots(self):
        self.assertEqual(len(self.column1._slots), self.column1._height)
        self.assertIsInstance(self.column1._slots[0], Slot)

    def test_get_slots(self):
        slots = self.column1.get_slots()
        self.assertEqual(len(slots), self.column1._height)
        self.assertIsInstance(slots[0], Slot)

    def test_is_full(self):
        #Fill column slot by slot. Check is_full returns false until final slot is filled:
        self.column1 = Column(2, self._column_height, self._win_length)
        for _ in range(self._column_height-1):
            self.column1.add_counter(self.player1)
            self.assertFalse(self.column1.is_full())
        self.column1.add_counter(self.player1)
        self.assertTrue(self.column1.is_full())

    def test_add_counter(self):
        #Check that counter is added to lowest available slot
        self.column1 = Column(2, self._column_height, self._win_length)
        for i in range(self._column_height):
            self.success = self.column1.add_counter(self.player1)
            self.assertTrue(self.success)

            self.assertEqual(self.column1._slots[i]._owner, self.player1)
            if i < self._column_height-1:
                self.assertEqual(self.column1._slots[i+1]._owner, None)

        #Check that counters not added when column is full
        self.success = self.column1.add_counter(self.player1)
        self.assertFalse(self.success)
        self.assertTrue(len(self.column1._slots), self._column_height) #Check haven't added extra row.

