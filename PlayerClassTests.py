import unittest
from PlayerClass import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Geraldine", "red")

    def test_check_get_name_is_Geraldine(self):
        self.assertEqual(self.player.get_name(), "Geraldine")

    def test_check_get_colour_is_red(self):
        self.assertEqual(self.player.get_colour(), "red")

    def test_is_it_my_turn_initially_is_false(self):
        self.assertFalse(self.player.is_it_my_turn())

    def test_swap_turn(self):
        my_turn_pre_swap = self.player._myTurn
        self.player.swapTurn()
        if(my_turn_pre_swap == True):
            self.assertFalse(self.player._myTurn)
        elif(my_turn_pre_swap == False):
            self.assertTrue(self.player._myTurn)
        else:
            print("_myTurn property of player is non boolean")
            self.fail()