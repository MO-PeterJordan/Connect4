import unittest
from SlotClass import Slot
from PlayerClass import Player


class TestSlot(unittest.TestCase):

    def setUp(self):
        self.slot1 = Slot()
        self.slot2 = Slot()
        self.player = Player("Geraldine", "Red")
        self.slot2.assign_owner(self.player)

    def test_get_owner_no_owner(self):
        self.assertEqual(self.slot1.get_owner(), None)

    def test_get_owner_Geraldine(self):
        self.assertEqual(self.slot2.get_owner(), self.player)

    # def tearDown(self):
    #     self.slot1.dispose()
    #     self.slot2.dispose()
    #     self.player.dispose()
