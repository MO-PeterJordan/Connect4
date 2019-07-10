from abc import ABC
from abc import abstractmethod


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
        self._owner = None

    def assign_owner(self, player):
        self._owner = player

    def get_owner(self):
        return self._owner


class LineABC(ABC):
    '''
    A line of slots which can report whether or not a win has been achieved.
    '''

    _length: int

    def __init__(self, length, win_length):
        self._length = length
        self._win_length = win_length
        self._slots = []
        self._create_slots()

    @abstractmethod
    def _create_slots(self):
        pass

    @abstractmethod
    def get_slots(self):
        return self._slots

    def check_for_win(self):
        '''
        Returns true if a player has won in this line and false otherwise.
        :return:
        '''
        game_won = False
        current_winner = None
        counters_in_a_row = 0
        for slot in self._slots:
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

    def check_win(self):
        """
        Checks if the column contains a win. If so returns True, else false.
        :return:
        """
        game_won = False
        current_winner = None
        row_length = 0
        for slot in self._slots:
            if slot.get_owner() == None:
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
                game_won = True
                break

        return game_won


class Row(LineABC):

    def _create_slots(self, slots):
        self._slots = slots

    def get_slots(self):
        return self._slots

    def check_for_win(self):
        super.check_for_win()

class Diagonal(LineABC):

    # def __init__(self, length, win_length, slots):
    #     super.__init__(self, length, win_length)
    #     self._create_slots(slots)

    def _create_slots(self, slots):
        self._slots = slots

    def get_slots(self):
        return self._slots



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
        self._rows = []
        self._diagonals = []


    def get_game_ended(self):
        return self._game_ended

    def get_no_counters(self):
        return self._spaces_filled

    def _create_columns(self):
        for i in range(0, self._board_width):
            _col = Column(i+1, self._board_height, self._win_length)
            self._cols.append(_col)

    def _create_rows(self):
        for y in range(self._board_height):
            slots = []
            for x in range(self._board_width):
                slots.append(self._cols[y].get_slots()[x])
            self._rows[y] = Row(self._board_width, self._win_length, slots)

    def _create_diagonals(self):
        pass

    def insert_counter(self, column_no, player):  #type --> bool
        success = False
        if(1 <= column_no <= self._board_width):
            #Player selected valid column
            chosen_column = self._cols[column_no-1]  # Column labels 1-indexed whereas array is 0-indexed
            if not chosen_column.is_full():
                #Chosen column not already full. Proceed to add counter and check for a win or draw.
                chosen_column.add_counter(player)
                if chosen_column.check_win():
                    print(player.get_name(), "wins!")
                    self._game_ended = True
                else:
                    self._spaces_filled += 1
                    if self._spaces_filled >= self._max_spaces_filled:
                        print("It\'s a draw.")
                        self._game_ended = True
                success = True
            else:
                print("That column is already full, choose another!")
        else:
            print("Invalid selection, please choose another column")
        return success

    def game_won(self):
        pass

    def game_drawn(self):
        if self._spaces_filled >= self._max_spaces_filled:
            print("It\'s a draw.")
            self._game_ended = True
            return True
        else:
            return False

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

            #Chech who goes first
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

            #Run game until win or draw
            success = False
            while success == False:
                play_column = int(input("\n"))
                success = self._current_board.insert_counter(play_column, self._current_player)

            if self._current_board.get_game_ended() == True:
                self._current_board.draw_board()
                self._game_finished = True

            self._player1.swapTurn()
            self._player2.swapTurn()