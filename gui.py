# gui.py

from tkinter import *
from tkinter.ttk import *

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 500

class welcome_frame(Frame):
	def __init__(self, two_player_handler, one_player_handler, parent=None):
		Frame.__init__(self, parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
		self.pack_propagate(0)
		
		title = Label(self, text="Connect 4", anchor=CENTER)
		player_selection = Frame(self)
		two_player = Button(player_selection, text="Two Players", command=two_player_handler)
		one_player = Button(player_selection, text="One Player", command=one_player_handler)
		
		s = Style()
		s.configure("TLabel", font="TkDefaultFont 30")
		s.configure("TButton", font="TkDefaultFont 15")
		
		two_player.place(height=35, width=240, rely=.3)
		one_player.place(height=35, width=240, rely=.6)
		title.pack(side=LEFT, expand=True, fill=BOTH)
		player_selection.pack(side=RIGHT, expand=True, fill=BOTH)
		
class game_frame(Frame):
	def __init__(self, square_click_handler, parent=None):
		self.state = [[0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0]]
	
		Frame.__init__(self, parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
		self.pack_propagate(0)
		
		self.gameboard = Canvas(self, width=430, height=360)
		for x in range(8):
			self.gameboard.create_line(60 * x + 5, 5, 60 * x + 5, 355, width=5, capstyle=ROUND)
		
		icon_tray = Frame(self)
		player1_icon = PhotoImage(file="images/player1.gif")
		player2_icon = PhotoImage(file="images/player2.gif")
		computer_icon = PhotoImage(file="images/computer.gif")
		turn_icon = PhotoImage(file="images/turn.gif")
		blank_icon = PhotoImage(file="images/blank.gif")
		self.player1 = Label(icon_tray, image=player1_icon)
		self.player1_indicator = Label(icon_tray, image=blank_icon)
		self.player2 = Label(icon_tray)
		self.player2_indicator = Label(icon_tray, image=blank_icon)
		
		# Make sure a reference is kept to all the images
		self.player1.image = player1_icon
		self.player2.image_twoPlayers = player2_icon
		self.player2.image_onePlayer = computer_icon
		self.player1_indicator.on_image = turn_icon
		self.player2_indicator.on_image = turn_icon
		self.player1_indicator.off_image = blank_icon
		self.player2_indicator.off_image = blank_icon
		
		self.gameboard.pack(pady=20)
		self.player1_indicator.pack(side=LEFT)
		self.player1.pack(side=LEFT, padx=10)
		self.player2_indicator.pack(side=RIGHT)
		self.player2.pack(side=RIGHT, padx=10)
		icon_tray.pack(pady=5)
		
		self.gameboard.bind("<Button-1>", square_click_handler)
	
	def draw_checker(self, x, y, player):
		"""
		Draws a checker at the given coordinates in the color of the player. x and y should be between
		0 and 6, and 0 and 5, respectively. Overwrites anything in that space without erasing. Player
		should be 1 or 2, representing which player is placing a piece, corresponding to red or blue.
		"""
		self.gameboard.create_oval((60 * x) + 10, (60 * y) + 5, (60 * x) + 60, (60 * y) + 55, 
								   outline="#ff2911" if player == 1 else "#2c88ff", 
								   fill="#ff2911" if player == 1 else "#2c88ff")
		self.state[x][y] = player
	
	def draw_Blank(self, x, y):
		"""
		Erases box at the coordinates of x and y on the board. x and y should be between
		0 and 6, and 0 and 5, repectively.
		"""
		self.gameboard.addtag_enclosed("to_delete", (60 * x) + 5, (60 * y), (60 * x) + 65, (60 * y) + 60)
		self.gameboard.delete("to_delete")
		self.state[x][y] = 0
	
	def set_player2_icon(self, num_of_players):
		"""
		Sets the player 2 icon to the human player 2 icon or the computer player icon,
		depending on the number of players passed in through num_of_players, which should
		be 1 or 2.
		"""
		if num_of_players == 1:
			self.player2.config(image=self.player2.image_onePlayer)
		elif num_of_players == 2:
			self.player2.config(image=self.player2.image_twoPlayers)
		else: raise TypeError("Argument \"num_of_players\" is invalid. Should be 1 or 2.")
		
	def set_icon_highlight(self, icon, is_highlighted):
		"""
		Sets the icon (indicated through icon as 1 for player 1 icon or 2 for player 2 icon) 
		on or off depending on whether is_highlighted is true or false, respectively.
		"""
		if icon == 1: active_icon = self.player1_indicator
		elif icon == 2: active_icon = self.player2_indicator
		else: raise TypeError("Argument \"icon\" is invalid. Should be 1 or 2.")
		
		if is_highlighted:
			active_icon.configure(image=active_icon.on_image)
		else:
			active_icon.configure(image=active_icon.off_image)
		
	def set_state(self, new_state):
		"""
		Sets the whole board's state at once.
		"""
		for x in range(7):
			for y in range(6):
				if self.state[x][y] != new_state[x][y]:
					self.draw_Blank(x, y)
					if new_state[x][y] != 0:
						self.draw_checker(x, y, new_state[x][y])
		
if __name__ == '__main__':
	print("Testing welcome_frame...")
	welcome = welcome_frame(lambda: print("Two Players button clicked!"), lambda: print("One Player button clicked!"))
	welcome.pack(fill=BOTH)
	welcome.mainloop()
	
	print("\nTesting game_frame...")
	game = game_frame(lambda event: print("Click at ", int((event.x - 10) / 60), ", ", int((event.y - 5) / 60), "."))
	game.set_player2_icon(2)
	game.set_icon_highlight(2, True)
	game.draw_checker(0, 5, 1)
	game.draw_checker(1, 4, 2)
	game.draw_checker(2, 3, 1)
	game.draw_checker(3, 2, 2)
	game.draw_checker(4, 1, 1)
	game.draw_checker(5, 0, 2)
	game.draw_checker(6, 0, 1)
	game.draw_Blank(0, 5)
	game.draw_Blank(1, 4)
	game.draw_Blank(2, 3)
	game.draw_Blank(3, 2)
	game.draw_Blank(4, 1)
	game.draw_Blank(5, 0)
	game.draw_Blank(6, 0)
	print("Game State: ", game.state)
	game.set_state([[2, 2, 0, 1, 2, 1],
				    [1, 0, 1, 2, 1, 2],
					[2, 1, 2, 1, 2, 1],
					[1, 0, 1, 0, 1, 2],
					[2, 1, 2, 1, 2, 1],
					[1, 0, 1, 2, 1, 2],
					[2, 2, 0, 1, 2, 1]])
	print("New Game State: ", game.state)
	game.set_state([[0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0],
							 [0, 0, 0, 0, 0, 0]])
	game.pack(expand=True, fill=BOTH)
	game.mainloop()