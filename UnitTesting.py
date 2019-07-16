import unittest
from ColumnClass import Column
from SlotClass import Slot
from PlayerClass import Player
from BoardStateClass import Board_State
from GameClass import Game



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

    # def tearDown(self):
    #         self.player.dispose()


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


class Test_Board_State(unittest.TestCase):

    def setUp(self):
        self._board_width = 5
        self._board_height = 10
        self._win_number = 4
        self.player1 = Player("Jarvis", "yellow")
        self.player2 = Player("Ultron", "red")

    def test_create_columns(self):
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        self.assertEqual(len(self.board._cols), self._board_width)
        self.assertIsInstance(self.board._cols[0], Column)
        for i in range(self._board_width):
            self.assertEqual(self.board._cols[i]._height, self._board_height)

    def test_insert_counter_input_column_validation(self):
        #Check that you can't add counters to non-existent columns (extant cols labelled 1 -> _board-width):
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        self.assertFalse(self.board.insert_counter(0, self.player1))
        self.assertFalse(self.board.insert_counter(-1, self.player2))
        self.assertNotEqual(self.board.insert_counter(self._board_width+1, self.player2), True)
        self.assertTrue(self.board.insert_counter(self._board_width, self.player1))

    def test_insert_counter_cant_add_to_full_column(self):
        #Check that you can't add a counter to a full column:
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        #print(self.board._cols[0]._slots[0]._owner)
        #Fill up column 1
        for _ in range(self._board_height):
            self.assertTrue(self.board.insert_counter(1, self.player1))
        #Check that column 1 can no longer be added to:
        self.assertFalse(self.board.insert_counter(1, self.player1))

    def test_game_drawn(self):
        #Create a full 3x3 board with no winners. Check that game_drawn returns false before last move and true after:
        self.board = Board_State(3, 3, 4)
        #fill first 2 cols
        for i in [1, 2]:
            self.board.insert_counter(i, self.player1)
            self.board.insert_counter(i, self.player2)
            self.board.insert_counter(i, self.player1)
        #fill final column:
        self.board.insert_counter(3, self.player2)
        self.board.insert_counter(3, self.player1)
        self.assertFalse(self.board.game_drawn())

        self.board.insert_counter(3, self.player2)
        self.board.draw_board()
        self.assertTrue(self.board.game_drawn())


class Test_Check_Game_Ended(unittest.TestCase):

    def setUp(self):
        self._board_width = 5
        self._board_height = 10
        self._win_number = 4
        self.player1 = Player("Jarvis", "yellow")
        self.player2 = Player("Ultron", "red")

    def test_get_diagonals_returns_all_diagonals(self):
        #Create a simple 3x3 board and check that all diagonals are returned:
        self.board = Board_State(3, 3, 4)
        #Board has first column owned by player1 others owned by player2
        for _ in range(3):
            self.board.insert_counter(1, self.player1)
            self.board.insert_counter(2, self.player2)
            self.board.insert_counter(3, self.player2)
        #self.board.draw_board()
        diagonals = self.board._get_diagonals()
        self.assertEqual(len(diagonals), 10)  #Check correct number of diagonals returned

    #Test for winning functions correctly for vertical rows:
    def test_game_won_vertical_happy_path(self):
        #Create winning column for player2 and check that True is returned:
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        self.board.insert_counter(1, self.player1)
        for _ in range(self._win_number):
            self.board.insert_counter(1, self.player2)
            self.board.draw_board()
        self.assertTrue(self.board.game_won())

    def test_game_won_vertical_full_column_no_win(self):
        #create full, non-winning column and check that win is not returned:
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        for _ in range(self._board_height):
            self.board.insert_counter(1, self.player1)
            self.board.insert_counter(1, self.player2)
        self.assertFalse(self.board.game_won())

    def test_game_won_vertical_3_in_a_row_no_win(self):
        #Create a column in which both players have 3 in a row and check that no win occurs:
        self.board = Board_State(self._board_width, self._board_height, 4)
        for _ in range(self._win_number - 1):
            self.board.insert_counter(1, self.player1)
            self.board.insert_counter(1, self.player2)
        self.assertFalse(self.board.game_won())

    #Check wins register correctly for horizontal rows:
    def test_game_won_horizontal_happy_path(self):
        #Create a winning row for player 1 and check that True is returned:
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        self.board.insert_counter(1, self.player1)
        self.board.insert_counter(2, self.player1)
        self.board.insert_counter(3, self.player1)
        self.assertFalse(self.board.game_won()) #need 1 more counter to win
        self.board.insert_counter(4, self.player1)
        self.assertTrue(self.board.game_won())

    def test_game_won_horizontal_full_row_no_win(self):
        self.board = Board_State(self._board_width, self._board_height, self._win_number)
        i = 1
        while i <= self._board_width:
            self.board.insert_counter(i, self.player1)
            i += 1
            self.board.insert_counter(i, self.player2)
            i += 1
        self.board.draw_board()
        self.assertFalse(self.board.game_won())

    def test_game_won_horizontal_3_in_a_row(self):
        #Create a board with both players having 3 counters in a horizontal row and check that no win occurs:
        self.board = Board_State(self._board_width, self._board_height, 4)
        for i in range(1, 4):
            self.board.insert_counter(i, self.player1)
            self.board.insert_counter(i, self.player2)
        self.assertFalse(self.board.game_won())

    #Game wins register correctly for diagonal wins:
    def test_game_won_rising_diagonal_happy_path(self):
        #Create a winning rising diagonal for player1 and check that true is returned:
        self.board = Board_State(4, 4, 4)
        self.board.insert_counter(1, self.player1)
        self.board.insert_counter(2, self.player2)
        self.board.insert_counter(2, self.player1)
        self.board.insert_counter(3, self.player2)
        self.board.insert_counter(3, self.player1)
        self.board.insert_counter(1, self.player2)
        self.board.insert_counter(3, self.player1)
        self.board.insert_counter(4, self.player2)
        self.board.insert_counter(4, self.player1)
        self.board.insert_counter(4, self.player2)
        self.assertFalse(self.board.game_won()) #need one more counter
        self.board.insert_counter(4, self.player1)
        self.board.draw_board()
        self.assertTrue(self.board.game_won())

    def test_game_won_falling_diagonal_happy_path(self):
        #Create a winning falling diagonal for player 2 and check that game is won:
        self.board = Board_State(3, 3, 3)
        self.board.insert_counter(2, self.player1)
        self.board.insert_counter(1, self.player2)
        self.board.insert_counter(1, self.player1)
        self.board.insert_counter(2, self.player2)
        self.board.insert_counter(2, self.player1)
        self.board.insert_counter(3, self.player2)
        self.board.insert_counter(3, self.player1)
        self.assertFalse(self.board.game_won()) #need 1 more play
        self.board.insert_counter(1, self.player2)
        self.board.draw_board()
        self.assertTrue(self.board.game_won())



    def test_draw_board(self):
        pass #Hard to test as output is visual.


if __name__ == '__main__':
    unittest.main()


