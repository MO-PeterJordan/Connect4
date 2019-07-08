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

    def add_counter(self, player):
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

    def check_win(self):
        """
        Checks if the column contains a win.
        If win found, returns winning player.
        If no winner returns false.
        :return:
        """
        winner = False
        current_winner = None
        row_length = 0
        for slot in self._slots:
            if slot.get_owner() == "None":
                #empty slot found. No more counters in this line.
                break
            else:
                if slot.get_owner() == current_winner:
                #slot owned by same player as slot immediately below
                    row_length += 1
                else:
                #slot owned by different player to slot immediately below
                    current_winner = slot.get_owner()
                    row_length = 1
            #Check for winner
            if row_length == self._win_length:
                winner = current_winner
                break

        return winner


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


class Slot:

    _owner: Player

    def __init__(self):
        self._owner = "None"

    def assign_owner(self, player):
        self._owner = player

    def get_owner(self):
        return self._owner


class Board_State:

    _row: str
    _base: str
    _game_ended: bool
    _spaces_filled: int
    _max_spaces_filled: int

    def __init__(self, board_width, board_height, win_length):
        self._board_width = board_width
        self._board_height = board_height
        self._win_length = win_length
        self._spaces_filled = 0
        self._max_spaces_filled = board_width * board_height
        self._game_ended = False
        #Create columns
        self._cols = []
        self._create_columns()

    def get_game_ended(self):
        return self._game_ended

    def get_no_counters(self):
        return self._spaces_filled

    def _create_columns(self):
        for i in range(0, self._board_width):
            _col = Column(i+1, self._board_height, self._win_length)
            self._cols.append(_col)

    def insert_counter(self, column_no, player):  #type --> bool
        success = False
        if(1 <= column_no <= self._board_width):
            #Player selected valid column
            chosen_column = self._cols[column_no-1]  # Column labels 1-indexed whereas array is 0-indexed
            success = chosen_column.add_counter(player)
            if chosen_column.check_win() != False:
                print(player.get_name(), "wins!")
                self._game_ended = True
            else:
                self._spaces_filled += 1
                if self._spaces_filled >= self._max_spaces_filled:
                    print("It\'s a draw.")
                    self._game_ended = True
        else:
            print("Invalid selection, please choose another column")
        return success

    def draw_board(self):
        #Create a single row with ascii art
        _draw_rows = []

        for row_no in range(self._board_height):
            _draw_row = "      "
            for col in self._cols:
                # Construct ascii art for current row
                _owner = col.get_slots()[row_no].get_owner()
                _draw_row += "|"
                if _owner == "None":
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


class Game():

    _board_width: int
    _board_height: int
    _win_length: int
    _game_finished: bool
    _player1: Player
    _player2: Player
    _current_player: Player
    _current_board: Board_State

    def __init__(self, board_width, board_height, win_length):
        #Set basic game parameters
        self._board_width = board_width
        self._board_height = board_height
        self._win_length = win_length

        self._current_board = Board_State(self._board_width, self._board_height, self._win_length)
        self._game_finished = False

        #Set up players
        self._player1 = Player(input("Enter first player name: "), "yellow")
        self._player2 = Player(input("Enter second player name: "), "red")
        self._player1.swapTurn()
        self._current_player = None

    def play_game(self):

        while(self._game_finished == False):
            self._current_board.draw_board()

            if self._player1.is_it_my_turn() & self._player2.is_it_my_turn():
                print("error: both player's think it's their turn")
            elif self._player1.is_it_my_turn():
                self._current_player = self._player1
            elif self._player2.is_it_my_turn():
                self._current_player = self._player2
            else:
                print("error: neither player's turn has my turn = true")

            player_prompt = self._current_player.get_name() + "\'s turn. Where would you like to play?"
            print(player_prompt)

            success = False
            while success == False:
                play_column = int(input("\n"))
                success = self._current_board.insert_counter(play_column, self._current_player)

            if self._current_board.get_game_ended() == True:
                self._current_board.draw_board()
                self._game_finished = True

            self._player1.swapTurn()
            self._player2.swapTurn()