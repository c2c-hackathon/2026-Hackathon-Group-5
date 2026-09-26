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

    
        a=GREEN #TODO: Choose a structure to represent what pieces are currently in the game board


    def reset_game(self):

        self.game_state = []
        for i in range(NUM_ROWS):
            row = []
            for i in range(NUM_COLS):
                row.append(0)
            self.game_state.append(row)
        
        for col in range(8):
            self.board.set_cell_color(col, 1, OFF)
    
        
        self.board.update_display()
                
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
        row = NUM_ROWS-1
        while row>=0:
            if self.game_state[row][col] != 0:
                row -= 1
            else:
                return row
        

        return -1

    def place_piece(self, col: int):
        #TODO: Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece. Don't forget to play a sound!
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
            NeoTrellis.play_sound("err.mp3")


    def update_board_colors(self):
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
    
                
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        pass

    def switch_player(self):
        #TODO: Change which player is curently placing a piece. Keep track of this in some sort of variable
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1
        self.show_current_player()

    
    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
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
        #TODO: Return whether or not the game state has no more legal moves
        for col in range(NUM_COLS):
            if not is_column_full(col):
                return False
        return True

    def get_player_color(self, player) -> tuple[int, int, int]:
        #TODO: Return the color for the given player 
        if self.current_player == 1:
            return self.player_one_color
        return self.player_two_color


    def is_column_full(self, col: int):
        #TODO: Return if the given column is currently full
        column_full = self.game_state[0][col] != 0
        if column_full:
            self.board.play_sound("aww.mp3")

        return column_full

        return (self.game_state[0][col] != 0)

    def get_cell(self, col: int, row: int, vector: tuple[int,int]):
        # row is y, col is x
        # row increases down and decreases up
        # col increases right and decreases left
        # tuple = (delta_col: int, delta_row: int)
        # self.game_state[row][col]
        try:
            return self.game_state[row + vector[1]][col + vector[0]] == self.current_player
        except Exception:
            return False

    def get_direction(self, col: int, row: int, vector: tuple[int, int], length: int = 3):
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
        
        #print("True: " + str(i + 1))
        return False


    def check_win(self, col: int, row:int):
        #TODO: Check the game state to see if any player has won or if there is a draw
        for vector in VECTOR_LIST:
            win = self.get_direction(col, row, vector, 3)
            if win:
                self.show_winner()
                return
        # Check win from top
        # print("To the right: " + str(self.get_cell(col, row, 1, 0)))
        # print("To the left: " + str(self.get_cell(col, row, -1, 0)))
        # print("Up: " + str(self.get_cell(col, row, 0, -1)))
        # print("Down: " + str(self.get_cell(col, row, 0, 1)))
        

    def show_winner(self):
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
        for row in range(8):
            for col in range(8):
                self.board.set_cell_color(col, row, color)

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


