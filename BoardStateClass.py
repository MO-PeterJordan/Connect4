import numpy as np
from ColumnClass import Column
from SlotClass import Slot
#from CheckForWin import check_line_for_win


class Board_State:

    _row: str
    _base: str
    _game_ended: bool
    _spaces_filled: int
    _max_spaces_filled: int
    _game_board: Slot

    def __init__(self, board_width, board_height, win_length):
        self._board_width = board_width
        self._board_height = board_height
        self._win_length = win_length
        self._spaces_filled = 0
        self._max_spaces_filled = board_width * board_height

        self._cols = []
        self._create_columns()

    def _create_columns(self):
        for i in range(0, self._board_width):
            _col = Column(i+1, self._board_height, self._win_length)
            self._cols.append(_col)

    def create_board_array(self):
        '''
        Returns an array of slots representing the game board. Information taken from the columns.
        :return:
        '''
        game_board = np.array(Slot)
        temp_list_board = []
        for col in self._cols:
            col = np.array(col.get_slots())
            temp_list_board.append(col)
        game_board = np.transpose(np.array(temp_list_board))
        return game_board

    def insert_counter(self, column_no, player):  #type --> bool
        success = False
        if(1 <= column_no <= self._board_width):
            #Player selected valid column
            chosen_column = self._cols[column_no-1]  # Column labels 1-indexed whereas array is 0-indexed
            if not chosen_column.is_full():
                #Chosen column has space.
                chosen_column.add_counter(player)
                self._spaces_filled += 1
                success = True
            else:
                print("That column is already full, choose another!")
        else:
            print("Invalid selection, please choose another column")
        return success

    def game_drawn(self):
        if self._spaces_filled >= self._max_spaces_filled:
            print("It\'s a draw.")
            self._game_ended = True
            return True
        else:
            return False

    def game_won(self):
        won = False
        #Collect all possible lines in which a win could occur
        lines = self._get_rows() + self._get_columns() + self._get_diagonals()
        #Check for a win with a horizontal row:
        for line in lines:
            if self._check_line_for_win(line):
                won = True
                break
        return won

    def _get_columns(self):
        cols = []
        for col in self._cols:
            cols.append(col.get_slots())
        return cols

    def _get_rows(self):
        rows = []
        for y in range(self._board_height):
            row = []
            for col in self._cols:
                row.append(col.get_slots()[y])
            rows.append(row)
        return rows

    def _get_diagonals(self):
        diagonals = []
        game_board = self.create_board_array()

        #Falling diagonals:
        #Diagonals starting from top of board
        for x in range(self._board_width):
            diagonals.append(np.diagonal(game_board, x))
        #Diagonals starting from left of board
        for y in range(-self._board_height+1, 0):
            diagonals.append(np.diagonal(game_board, y))

        #Rising diagonals - flip the board and repeat process for falling diagonals:
        game_board = np.fliplr(game_board)
        #Diagonals starting from top of flipped board
        for x in range(self._board_width):
            diagonals.append(np.diagonal(game_board, x))
        #Diagonals starting from left of flipped board
        for y in range(-self._board_height+1, 0):
            diagonals.append(np.diagonal(game_board, y))

        return diagonals

    def _check_line_for_win(self, line):
        '''
            Takes a line, which is a list of slots.
            Returns true if a player has won in this line and false otherwise.
            :return:
        '''
        game_won = False
        current_winner = None
        counters_in_a_row = 0
        for slot in line:
            if slot.get_owner() is None:
                counters_in_a_row = 0
            elif slot.get_owner() == current_winner:
                #slot owned by same player as slot immediately below
                counters_in_a_row += 1
                #Check for winner
                if counters_in_a_row == self._win_length:
                    game_won = True
                    break
            else:
                #slot owned by different player to slot immediately below
                current_winner = slot.get_owner()
                counters_in_a_row = 1

        return game_won

    def draw_board(self):
        #Create a single row with ascii art
        _draw_rows = []

        for row_no in range(self._board_height):
            _draw_row = "      "
            for col in self._cols:
                # Construct ascii art for current row
                _owner = col.get_slots()[row_no].get_owner()
                _draw_row += "|"
                if _owner == None:
                    _draw_row += "   "
                elif _owner.get_colour() == "yellow":
                    _draw_row += " y "
                elif _owner.get_colour() == "red":
                    _draw_row += " r "
                else:
                    print("Slot has invalid owner or owner colour.")
            _draw_row += "|"
            _draw_rows.append(_draw_row)

        #Print the board
        _draw_rows.reverse()
        for row in _draw_rows:
            print(row)

        #Print base:
        _indices = "        1   2   3   4   5   6   7"
        _base = "      "
        for x in range(self._board_width):
            _base += "----"
        _base += "-"
        print(_base)
        print(_indices)


#class GameWon