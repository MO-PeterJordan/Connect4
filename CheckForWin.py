from BoardStateClass import Board_State

class Check_For_Win:
    '''
    Initialised with the list of columns constituting the current board.
    Works out if game is won and provides public method to disseminate this information.
    '''
    board: Board_State

    def __init__(self, board):
        self._board = board
        self._board_width = board.get_width()
        self._board_height = board.get_height()

    def _get_columns(self):
        cols = []
        for col in self._board.get_cols():
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

    def _all_spaces_filled(self):
        all_spaces_filled = True
        for col in self._cols:
            for slot in col:
                if slot.get_owner() is None:
                    #Empty space found
                    all_spaces_filled = False
                    break
        return all_spaces_filled

    def game_drawn(self):
        if self._all_spaces_filled:
            print("It\'s a draw.")
            self._game_ended = True
            return True
        else:
            return False

