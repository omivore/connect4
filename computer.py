# computer.py

from enum import Enum
import itertools
import copy

class Direction(Enum):
        north = 1
        northeast = 2
        east = 3
        southeast = 4
        south = 5
        southwest = 6
        west = 7
        northwest = 8

class State(Enum):
        empty = 0
        white = 1
        black = 2
        red = 1
        blue = 2

        def other(self):
                if self == State.white:
                        return State.black
                else: return State.white


class Rule(Enum):
        pass

class square():
        def __init__(self, x=None, y=None, state=State.empty, availability=True):
                self.x = x
                self.y = y
                self.state = state
                self.available = availability

        def __str__(self):
                return str(self.x) + ", " + str(self.y) + ": " + self.state.name

class problem():
        def __init__(self, threat, solution_indices=[]):
                self.threat = threat
                self.solutions = solution_indices

class solution():
        def __init__(self, rule, squareset):
                self.rule = rule
                self.squareset = squareset

def check_for_win(board):
        """
        Takes the board and sees if there is a winner ie four in a row of a color.
        Returns 0, 1, or 2 for no winner, player 1 winner, or player 2 winner, respectively.
        """
        # This is for unity of the whole module; check_for_win was originally in 'board-mode'. Everything
        #   else in the module was in grid mode, though, and this was the one part that was 'board'. So it
        #   was modified to 'grid-mode' so as to work with look_ahead and step (which had needed to work with
        #   both, and failed to do so. So check_for_win had to change).
        grid = generate_grid(squares)

        for col, row in itertools.product(range(7), range(6)):
                streak_color = grid[col][row].state
                shift_col, shift_row = col, row
                if streak_color != State.empty:
                        for direction in [directions for directions in Direction if directions.value in range(5)]:
                                # Reset shifted coordinates to starting point.
                                shift_col, shift_row = col, row
                                # Run three times because the original col, row already is the first square.
                                for streak in range(3):
                                        if look_ahead(shift_col, shift_row, direction):
                                                shift_col, shift_row = step(shift_col, shift_row, direction)
                                                if grid[shift_col][shift_row].state == streak_color: continue
                                        break
                                else: return streak_color.value
        # No winner at all after all the squares.
        return State.empty.value
                                
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
        if "north" in direction.name:
                row += 1
        elif "south" in direction.name:
                row -= 1
        if "east" in direction.name:
                col += 1
        elif "west" in direction.name:
                col -= 1

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
        problems = generate_problems(grid, State.black)
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

def generate_problems(board, me):
        problems = set()
        for col, row in itertools.product(range(7), range(6)):
                shift_col, shift_row = col, row
                if board[col][row].state != me:
                        for direction in [directions for directions in Direction if directions.value in range(5)]:
                                # Reset shifted coordinates to starting point.
                                shift_col, shift_row = col, row
                                # Run three times because the original col, row already is the first square.
                                for streak in range(3):
                                        if look_ahead(shift_col, shift_row, direction):
                                                shift_col, shift_row = step(shift_col, shift_row, direction)
                                                if board[shift_col][shift_row].state != me: continue
                                        break
                                else:
                                        problems.add(((col, row), (shift_col, shift_row)))
        return problems

def is_useful_solution(board, squares, me):
        testboard = copy.deepcopy(board) # So as to not permanently modify the original.
        problems = set(generate_problems(testboard, me))
        for square in squares:
                testboard[square.x][square.y].state = me
        new_problems = set(generate_problems(testboard, me))
        if len(new_problems) < len(problems): return True
        else: return False
        
def print_board(board):
        """
        Useful function to print a 2D array of squares in a readable format.
        DEBUGGING USE ONLY
        """
        for y in range(5, -1, -1):
                for x in range(7):
                        print(board[x][y].state.name, " ", end="")
                print()
if __name__ == "__main__":


        print("Function step testing block. Next four printouts should all be 3 3.")
        print(step(3, 2, Direction.north))
        print(step(2, 3, Direction.east))
        print(step(2, 2, Direction.northeast))
        print(step(2, 4, Direction.southeast))
        print("End block.\n")

        print("Function look_ahead testing block. Next eight printouts should be False.")
        print(look_ahead(3, 5, Direction.north))
        print(look_ahead(6, 3, Direction.east))
        print(look_ahead(4, 5, Direction.northeast))
        print(look_ahead(6, 0, Direction.northeast))
        print(look_ahead(6, 5, Direction.northeast))
        print(look_ahead(4, 0, Direction.southeast))
        print(look_ahead(6, 4, Direction.southeast))
        print(look_ahead(6, 0, Direction.southeast))
        print("End block.\n")

        print("Function generate_squares testing block. First board will be board-style; second will be grid. Should correspond.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 1, 2, 1],
                 [0, 0, 0, 0, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        print(board)
        board = generate_squares(board)
        print_board(board)
        print("End block.\n")

        print("Function generate_problems testing block. Testing based on example contained in Allis' master thesis.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 1, 2, 1],
                 [0, 0, 0, 0, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        problems = generate_problems(generate_squares(board), State.black)
        for problem in problems:
                print(str(problem[0][0]) + "," + str(problem[0][1]), "->", str(problem[1][0]) + "," + str(problem[1][1]))
        print(len(problems), " problems total.")
        print("End block.\n")

        print("Testing module rules/claimeven.")
        import rules.claimeven
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1],
                 [1, 2, 1, 2, 1, 2],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        grid = generate_squares(board)
        solutions = list(rules.claimeven.generate_solutions(grid, State.black)) # list-ed so I can len() it later.
        for solution in solutions:
                print(str(solution.x) + ", " + str(solution.y))
        print(len(solutions), "solutions total through claimeven.")
        print("End block.\n")
