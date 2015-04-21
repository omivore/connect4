# computer.py

from enum import Enum

class Direction(Enum):
        north = 1
        northeast = 2
        east = 3
        southeast = 4

def check_for_win(board):
        """
        Takes the board and sees if there is a winner ie four in a row of a color.
        Returns 0, 1, or 2 for no winner, player 1 winner, or player 2 winner, respectively.
        """
        for col in range(7):
                for row in range(6):
                        streak_color = board[col][row]
                        shift_col, shift_row = col, row
                        if streak_color != 0:
                                for direction in Direction:
                                        # Reset shifted coordinates to starting point.
                                        shift_col, shift_row = col, row
                                        # Run three times because the original col, row already is the first square.
                                        for streak in range(3):
                                                print(streak, col, row, shift_col, shift_row, direction)
                                                if look_ahead(shift_col, shift_row, direction):
                                                        shift_col, shift_row = step(shift_col, shift_row, direction)
                                                        if board[shift_col][shift_row] == streak_color: continue
                                                break
                                        else: return streak_color
                                
def look_ahead(col, row, direction):
        """
        Takes a coordinate and checks to see that there exists another square next to it in given direction.
        """
        new_col, new_row = step(col, row, direction)
        
        if new_col in range(7) and new_row in range(6): return True
        else: return False

def step(col, row, direction):
        """
        Takes a coordinate and returns a coordinate pair having moved in the given direction.
        """
        if direction == Direction.north or direction == Direction.northeast:
                row -= 1
        if direction == Direction.east or direction == Direction.southeast or direction == Direction.northeast:
                col += 1
        if direction == Direction.southeast:
                row += 1

        return col, row

def compute(board):
	"""
	Main function to be run by the engine; will return a column number 0-6.
	Takes a 2-dimensional array of the class square, containing column and 
	row number, between 0-6 and 0-5 respectively. State should
	"""
	# Generate board

class square():
	def __init__(self, col, row, state, availability):
		self.col = col
		self.row = row
		self.state = state
		self.available = availability

if __name__ == "__main__":
        print("Function step testing block. Next four printouts should all be 3 3.")
        print(step(3, 4, Direction.north))
        print(step(2, 3, Direction.east))
        print(step(2, 4, Direction.northeast))
        print(step(2, 2, Direction.southeast))
        print("End block.")

        print("Function look_ahead testing block. Next eight printouts should be False.")
        print(look_ahead(2, 0, Direction.north))
        print(look_ahead(6, 3, Direction.east))
        print(look_ahead(3, 0, Direction.northeast))
        print(look_ahead(6, 0, Direction.northeast))
        print(look_ahead(6, 5, Direction.northeast))
        print(look_ahead(4, 5, Direction.southeast))
        print(look_ahead(6, 0, Direction.southeast))
        print(look_ahead(6, 5, Direction.southeast))
        print("End block.")
