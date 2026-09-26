import typing
from Colors import *
from Vectors import *
import time
from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
NUM_ROWS = 6
NUM_COLS = 8
class ConnectFour:
    
    
    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        # Initializes the game and all main variables
        self.board = board if board is not None else NeoTrellisGame()
        super().__init__()
        self.reset_game()
        self.current_player = 1
        self.player_one_color = RED
        self.player_two_color = YELLOW
        for x in range(NUM_COLS):
            self.board.set_callback(x,0, self.handle_button_event)
            self.board.activate_key(x,0, Action.BUTTON_PRESSED)
        self.update_board_colors()
        self.show_current_player()

    

    def reset_game(self):
        # Resets the game to its default state
        self.game_state = []
        for i in range(NUM_ROWS):
            row = []
            for i in range(NUM_COLS):
                row.append(0)
            self.game_state.append(row)
        
        for col in range(8):
            self.board.set_cell_color(col, 1, OFF)
    
        
        self.board.update_display()
                
        
    def register_callbacks(self):
        self.board.set_callback(0, 0, self.handle_button_event) # Example of how to register a callback (function) for button 0, 0. Must be done for every button that runs a function
        self.board.activate_key(0, 0, Action.BUTTON_PRESSED) # Even though the callback is set, if the key is not enabled it will not be run. This is how you enable

  
    def handle_button_event(self, x:int, y: int, action: Action):
        """
        This is an example of how a callback function will look. It takes an x value, y value, and action, which will indicate what button activated the callback and what action the user did to run it.
        See NeoTrellisGame.set_callback() for info about callbacks.
        """
        if action == NeoTrellis.EDGE_RISING:
            self.place_piece(x)

        

    def find_lowest_empty_row(self, col: int):
        # Will find the lowest emply row, then return that value.
        # If none is found, then it will return -1
        row = NUM_ROWS-1
        while row>=0:
            if self.game_state[row][col] != 0:
                row -= 1
            else:
                return row
        

        return -1

    def place_piece(self, col: int):
        # Function to place a piece and show the dropping animation
        end_row = self.find_lowest_empty_row(col)
        current_row = 2
        if end_row != -1:
            for i in range(end_row):
                self.update_board_colors()
                self.board.set_cell_color(col, current_row,self.get_player_color(self.current_player))
                self.board.update_display()
                current_row += 1
                time.sleep(0.03)

            self.game_state[end_row][col] = self.current_player
            self.update_board_colors()
            self.board.play_sound("clack.mp3")
            self.check_win(col, end_row)
            self.switch_player()
        else:
            self.board.play_sound("err.mp3")


    def update_board_colors(self):
        # Updates the board to show the proper color configuration per player.
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                player = self.game_state[row][col]
                if player ==1:
                    self.board.set_cell_color(col, row+2,self.player_one_color)
                elif player ==2:
                    self.board.set_cell_color(col, row+2,self.player_two_color)
                else:
                    self.board.set_cell_color(col, row+2,WHITE)
        self.board.update_display()

    def switch_player(self):
        # Switches the player after a turn
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1
        self.show_current_player()

    
    def show_current_player(self):
        # Shows the player's color at the top, turning the top pixel of full columns off.
        for col in range(NUM_COLS):
            if self.is_column_full(col):
                self.board.set_cell_color(col, 0,OFF)
                #self.board.activate_key(col,0, Action.BUTTON_PRESSED, False)
            elif self.current_player == 1:
                self.board.set_cell_color(col, 0,self.player_one_color)
            elif self.current_player == 2:
                self.board.set_cell_color(col, 0,self.player_two_color)
        self.board.update_display()

    def is_board_full(self):
        # Returns if the board is completely full
        for col in range(NUM_COLS):
            if not is_column_full(col):
                return False
        return True

    def get_player_color(self, player) -> tuple[int, int, int]:
        # Returns the color of the current player
        if self.current_player == 1:
            return self.player_one_color
        return self.player_two_color


    def is_column_full(self, col: int):
        # Returns whether or not the column is full
        column_full = self.game_state[0][col] != 0
        return column_full

    def get_cell(self, col: int, row: int, vector: tuple[int,int]):
        # Returns if a cell in the vector of the current cordenates is the same color
        # Used for win logic.
        try:
            return self.game_state[row + vector[1]][col + vector[0]] == self.current_player
        except Exception:
            return False

    def get_direction(self, col: int, row: int, vector: tuple[int, int], length: int = 3):
        # Calls get_cell to see if there is a 4 in a row with the given direction, then returns that
        # Used for win logic.
        for i in range(1, length+1):
            cell_is_same = self.get_cell(col, row, (vector[0]*i, vector[1]*i))
            if cell_is_same == False:
                break
            if i == 3:
                return True
        for j in range(4):
            for i in range(1, length+1):
                cell_is_same = self.get_cell(col + vector[0]*j, row + vector[1]*j, (vector[0]*i, vector[1]*i))
                if cell_is_same == False:
                    break
                print(i)
                if i == 4:
                    return True
        
        return False


    def check_win(self, col: int, row:int):
        # Calls get_direction for every possible 4 in a row. 
        # If the return is true, calls the show_winner function to end the game
        for vector in VECTOR_LIST:
            win = self.get_direction(col, row, vector, 3)
            if win:
                self.show_winner()
                return
        

    def show_winner(self):
        # Flashes the screen in the winner's color, then resets the board for another game.
        self.board.play_sound("cheer.mp3")
        for i in range(3):
            self.set_full_color(self.get_player_color(self.current_player))
            time.sleep(.5)
            self.board.update_display()
            self.set_full_color((255, 255, 255))
            time.sleep(.5)
            self.board.update_display()
        self.reset_game()
        self.update_board_colors()

    

    def set_full_color(self, color):
        # Sets the board to a single color
        for row in range(8):
            for col in range(8):
                self.board.set_cell_color(col, row, color)

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


