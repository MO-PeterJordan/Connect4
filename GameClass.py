from PlayerClass import Player
from BoardStateClass import Board_State

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
                break
            elif self._player1.is_it_my_turn():
                self._current_player = self._player1
            elif self._player2.is_it_my_turn():
                self._current_player = self._player2
            else:
                print("error: neither player's turn has my turn = true")
                break

            player_prompt = self._current_player.get_name() + "\'s turn. Where would you like to play?"
            print(player_prompt)

            #Run game until win or draw
            success = False
            while success == False:
                play_column = int(input("\n"))
                success = self._current_board.insert_counter(play_column, self._current_player)

            if self._current_board.game_won():
                print(self._current_player.get_name(), "wins!")
                self._current_board.draw_board()
                self._game_finished = True
            elif self._current_board.game_drawn():
                print("It\'s a draw.")
                self._current_board.draw_board()
                self._game_finished = True


            self._player1.swapTurn()
            self._player2.swapTurn()