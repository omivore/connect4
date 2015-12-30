# computer.py

from enum import Enum
import itertools
import sqlite3

class Direction(Enum):
        north = 1
        northeast = 2
        east = 3
        southeast = 4

class State(Enum):
        empty = 0
        white = 1
        black = 2
        red = 1
        blue = 2

class Win(Enum):
        tie = -1
        none = 0
        player1 = 1
        player2 = 2

def check_for_win(board):
        """
        Takes the board and sees if there is a winner ie four in a row of a color.
        Returns 0, 1, or 2 for no winner, player 1 winner, or player 2 winner, respectively.
        Otherwise, returns None.
        """
        # This is for unity of the whole module; check_for_win was originally in 'board-mode'. Everything
        #   else in the module was in grid mode, though, and this was the one part that was 'board'. So it
        #   was modified to 'grid-mode' so as to work with look_ahead and step (which had needed to work with
        #   both, and failed to do so. So check_for_win had to change).
        grid = generate_squares(board)

        def ensure_same_color(previous_square, current_square, direction=None):
                if direction:
                        if direction.value not in range(5): return False
                if previous_square:
                        if current_square.state == previous_square.state: return True
                elif current_square.state != State.empty: return True
                else: return False

        # If board is full, return 0.
        for square in [square for row in grid for square in row]:
            if square.state == State.empty: break
        else: return Win.tie
                
        four_streaks = find_streaks(grid, 4, ensure_same_color)
        
        if len(four_streaks) > 0:
                sample = four_streaks.pop()
                return Win(sample[0].state.value)
        else: return Win.none

def find_streaks(board, streak_len, eval_func):
        streak_instances = set()
        for col, row in itertools.product(range(7), range(6)):
                streak_origin = board[col][row]
                shift_col, shift_row = col, row
                if eval_func(None, streak_origin):
                        for direction in Direction:
                                streak = [board[col][row]]
                                shift_col, shift_row = col, row # Reset shifted coordinates to starting point.
                                # Run only streak_len - 1 times because the original col, row already is the first square.
                                for times in range(streak_len - 1):
                                        if look_ahead(shift_col, shift_row, direction):
                                                shift_col, shift_row = step(shift_col, shift_row, direction)
                                                if eval_func(streak_origin, board[shift_col][shift_row], direction): 
                                                        streak.append(board[shift_col][shift_row])
                                                        continue
                                        break
                                else: streak_instances.add(tuple(streak))
        return streak_instances
                                
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
        Takes a 2-dimensional array of the board in the style of the board ie top-down and left-right.
        """
        # Generate board into 
        grid = generate_squares(board)
        # Apply each rule to the board and add solutions to master list.
        # Generate problems.
        # 

def generate_squares(board):
        """
        Takes a graphic coordinate system style board ie the Connect 4 board and turns it into a 
        more logical, (0, 0) at bottom left style grid made up of squares, state included.
        Availability of square is not included.
        """
        grid = [[square() for s in range(6)] for s in range(7)]
        for x, y in itertools.product(range(7), range(6)):
                grid[x][y].x = x
                grid[x][y].y = y
        for grid_coords, board_coords in zip(itertools.product(range(7), range(6)), itertools.product(range(7), range(5, -1, -1))):
                grid[grid_coords[0]][grid_coords[1]].state = State(board[board_coords[0]][board_coords[1]])
        return grid

class square():
	def __init__(self, x=None, y=None, state=State.empty, availability=True):
		self.x = x
		self.y = y
		self.state = state
		self.available = availability

if __name__ == "__main__":
        print("Function step testing block. Next four printouts should all be 3 3.")
        print(step(3, 4, Direction.north))
        print(step(2, 3, Direction.east))
        print(step(2, 4, Direction.northeast))
        print(step(2, 2, Direction.southeast))
        print("End block.\n")

        print("Function look_ahead testing block. Next eight printouts should be False.")
        print(look_ahead(2, 0, Direction.north))
        print(look_ahead(6, 3, Direction.east))
        print(look_ahead(3, 0, Direction.northeast))
        print(look_ahead(6, 0, Direction.northeast))
        print(look_ahead(6, 5, Direction.northeast))
        print(look_ahead(4, 5, Direction.southeast))
        print(look_ahead(6, 0, Direction.southeast))
        print(look_ahead(6, 5, Direction.southeast))
        print("End block.\n")

        print("Function generate_squares testing block. First board will be board-style; second will be grid. Should correspond.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 1, 2],
                 [0, 0, 2, 1, 0, 0],
                 [0, 0, 1, 2, 0, 0],
                 [2, 1, 0, 0, 0, 0],
                 [1, 2, 0, 0, 0, 0]]
        print(board)
        board = generate_squares(board)
        for y in range(5, -1, -1):
                for x in range(7):
                        print(board[x][y].state.name, " ", end="")
                print()
        print()
        print("Continued testing. Next seven printouts should be white.")
        print(board[1][0].state.name)
        print(board[2][1].state.name)
        print(board[3][2].state.name)
        print(board[4][3].state.name)
        print(board[5][4].state.name)
        print(board[6][5].state.name)
