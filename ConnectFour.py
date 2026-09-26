import typing
from Colors import *
from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

class ConnectFour:
    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        self.board = board if board is not None else NeoTrellisGame()
        super().__init__()
        self.reset_board()

        for x in range(7):
            self.board.set_callback(x,0, self.handle_button_event)
            self.board.activate_key(x,0, Action.BUTTON_PRESSED)
        self.update_board_colors()

    
        a=GREEN #TODO: Choose a structure to represent what pieces are currently in the game board


    def reset_game(self):
        self.game_state = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
        ] 

        #TODO reset the game state to its original empty state
        pass

    def register_callbacks(self):
        #TODO: Register callbacks that will be run when buttons are pressed and released
        self.board.set_callback(0, 0, self.handle_button_event) # Example of how to register a callback (function) for button 0, 0. Must be done for every button that runs a function
        self.board.activate_key(0, 0, Action.BUTTON_PRESSED) # Even though the callback is set, if the key is not enabled it will not be run. This is how you enable

        pass
  
    def handle_button_event(self, x:int, y: int, action: Action):
        """
        This is an example of how a callback function will look. It takes an x value, y value, and action, which will indicate what button activated the callback and what action the user did to run it.
        See NeoTrellisGame.set_callback() for info about callbacks.
        """
        if action == NeoTrellis.EDGE_RISING:
            self.place_piece(x)

        #TODO: Implement what will happen when the button at position x,y is pressed or released
  

    def find_lowest_empty_row(self, col: int):
        #TODO: Return the lowest empty row in the column.
        #for col in len(self.game_state[row][col]):
                #pass

        return 5

    def place_piece(self, col: int, player :int):
        #TODO: Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece. Don't forget to play a sound!
        row = self.find_lowest_empty_row(col)
        # self.board.set_cell_color(col,row,GREEN)
        self.game_state[row][col] = player


    def update_board_colors(self):
        for row in range(len(self.game_state)):
            for col in range(len(self.game_state[row])):
                player = self.game_state[row][col]
                if player ==1:
                    self.board.set_cell_color(row,col,RED)
                elif player ==2:
                    self.board.set_cell_color(row, col,YELLOW)
                else:
                    self.board.set_cell_color(row,col,OFF)
        self.board.update_display()

                
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        pass

    def switch_player(self):
        #TODO: Change which player is curently placing a piece. Keep track of this in some sort of variable
        pass

    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
        pass

    def is_board_full(self):
        #TODO: Return whether or not the game state has no more legal moves
        pass  

    def get_player_color(self, player) -> tuple[int, int, int]:
        #TODO: Return the color for the given player 
        pass

    def is_column_full(self, col: int):
        #TODO: Return if the given column is currently full
        pass

    def check_win(self):
        #TODO: Check the game state to see if any player has won or if there is a draw
        pass

    def show_winner(self):
        #TODO: Display on the board who won
        pass

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


