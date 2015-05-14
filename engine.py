# engine.py

import gui
import computer
import copy
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo

class engine():
    def __init__(self):
        self.turn = 1
        self.players = 2

        self.root = Tk()
        self.root.geometry("750x500")
        self.root.title("Connect 4")

        container = Frame(self.root, width=gui.WINDOW_WIDTH, height=gui.WINDOW_HEIGHT)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.game = gui.game_frame(lambda event: self.square_click_handler(event), container)
        self.welcome = gui.welcome_frame(lambda: self.players_handler(2), lambda: self.players_handler(1), container)

        self.game.grid(row=0, column=0, sticky=NSEW)
        self.welcome.grid(row=0, column=0, sticky=NSEW)

    def run(self):
        self.set_frame("welcome")
        self.root.mainloop()
        
    def set_frame(self, frame):
        if frame == "welcome":
            self.welcome.lift()
        elif frame == "game":
            self.game.lift()
        else:
            raise TypeError("frame argument is invalid. Should be \"welcome\", or \"game\".")
            
    def players_handler(self, num_of_players):
        self.game.set_player2_icon(num_of_players)
        self.game.set_icon_highlight(1, True)
        self.game.set_icon_highlight(2, False)
        self.game.set_state([[0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0]])
        self.turn = 1
        self.players = num_of_players
        self.set_frame("game")
        
    def square_click_handler(self, event):
        column = int((event.x - 10) / 60)
        
        # Check if a move right now is allowed.
        if not self.turn_allowed(): return
        if not self.move_allowed(column): return
        
        self.set_square(column, self.turn)
        result = computer.check_for_win(self.game.state)
        
        if result != None:
            self.end_game(result)
            return
        self.change_turn()
        
        # Now deal with the computer player's move if this is a one-player game.
        #if self.players == 1: self.game.after(100, self.computer_play)
        
    def set_square(self, column, player):
        # Assumes column is not full
        for row in range(6)[::-1]:
            if self.game.state[column][row] == 0:
                self.game.draw_checker(column, row, player)
                return
    
    def computer_play(self):
        pass
        
    def turn_allowed(self):
        # If there are two players, then the turn is allowed, definitely.
        if self.players == 2: return True
        else:
            # Otherwise, the turn is allowed only if it is the player's turn.
            if self.turn == 1: return True
        return False
    
    def change_turn(self):
        self.turn = 1 if self.turn == 2 else 2
        
        self.game.set_icon_highlight(1, False)
        self.game.set_icon_highlight(2, False)
        self.game.set_icon_highlight(self.turn, True)
        
    def move_allowed(self, desired_column):
        if self.game.state[desired_column][0] != 0:
            return False
        else: return True
        
    def end_game(self, winner):
        showinfo("Game Ended", ("Player " + str(winner) + " has won!") if winner != 0 else "Game is a draw")
        self.set_frame("welcome")

if __name__ == "__main__":
    new_game = engine()
    new_game.run()
