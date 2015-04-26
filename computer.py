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
        claimeven = 1
        baseinverse = 2
        vertical = 3
        aftereven = 4
        lowinverse = 5
        highinverse = 6
        baseclaim = 7
        before = 8
        specialbefore = 9

class Square():
        def __init__(self, x=None, y=None, state=State.empty, availability=True):
                self.x = x
                self.y = y
                self.state = state
                self.available = availability

        def __str__(self):
                return "<(" + str(self.x) + ", " + str(self.y) + "): " + self.state.name + ">"

        def __repr__(self):
                return str(self)

        def __eq__(self, other):
                # If *exact* same; state and availability included.
                if isinstance(other, Square):
                        if self.x == other.x and self.y == other.y and self.state == other.state and self.available == other.available:
                                return True
                        else: return False
                else: return NotImplemented

        def __hash__(self):
                return id(self)

        def coords(self):
                return (self.x, self.y)

class Problem():
        def __init__(self, threat, solution_indices=[]):
                self.threat = threat
                self.solutions = solution_indices

class Solution():
        def __init__(self, rule, squares, solved):
                self.rule = rule
                self.squares = squares
                self.solved = solved

        def __eq__(self, other):
                if isinstance(other, Solution):
                        if self.rule == other.rule and self.squares == other.squares and self.solved == other.solved:
                                return True
                        else: return False
                else: return NotImplemented

        def __hash__(self):
                return id(self)

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

        def ensure_same_color(previous_square_state, current_square_state, direction=None):
                if direction:
                        if direction.value not in range(5): return False
                if previous_square:
                        if current_square.state == previous_square.state: return True
                elif current_square.state != State.empty: return True
                else: return False

        four_streaks = find_streaks(grid, 4, ensure_same_color)
        
        if len(four_streaks) > 0:
                return grid[four_streaks[0][0][0]][four_streaks[0][0][1]].state.value
        else: return State.empty.value

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
        grid = [[Square() for s in range(6)] for s in range(7)]
        for x, y in itertools.product(range(7), range(6)):
                grid[x][y].x = x
                grid[x][y].y = y
        for grid_coords, board_coords in zip(itertools.product(range(7), range(6)), itertools.product(range(7), range(5, -1, -1))):
                grid[grid_coords[0]][grid_coords[1]].state = State(board[board_coords[0]][board_coords[1]])
        return grid

def generate_problems(board, me):
        def ensure_isnt_me(previous_square, current_square, direction=None):
                if direction:
                        if direction.value not in range(5): return False
                if current_square.state != me: return True
                else: return False

        return find_streaks(board, 4, ensure_isnt_me)

def is_useful_solution(board, solved, me):
        for solution in solved:
                problems = generate_problems(board, me)
                for problem in problems:
                        for square in solution:
                                if square in problem: continue
                                else: break
                        else: return True
        return False

def playables(board):
        playable = []
        for row in board:
                for y in range(5):
                        if row[y].state.value == State.empty.value:
                                playable.append(row[y].coords())
                                break
        return playable

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

        def test_rule(rule, board):
                grid = generate_squares(board)
                solutions = list(rule.generate_solutions(grid, State.black))
                useful = 0
                for solution in solutions:
                        if is_useful_solution(grid, solution.solved, State.black):
                                for square in solution.solved:
                                        print(square, end=" ")
                                print()
                                useful += 1
                print(useful, "solutions total through", solutions[0].rule.name + ".")

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
                for square in problem:
                        print(square, end=" ")
                print()
        print(len(problems), " problems total.")
        print("End block.\n")

        print("Function playables testing block. Should be bottom seven squares' coordinates.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 1, 1],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        print(playables(generate_squares(board)))
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
        test_rule(rules.claimeven, board)
        print("End block.\n")

        print("Testing module rules/baseinverse.")
        import rules.baseinverse
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 1, 1],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.baseinverse, board)
        print("End block.\n")

        print("Testing module rules/vertical.")
        import rules.vertical
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 2, 2, 2, 1, 1],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 1, 1, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.vertical, board)
        print("End block.\n")        

        print("Testing module rules/aftereven.")
        import rules.aftereven
        board = [[0, 0, 0, 0, 2, 2],
                 [0, 0, 1, 2, 1, 1],
                 [0, 0, 2, 1, 1, 1],
                 [0, 0, 2, 1, 2, 1],
                 [0, 0, 2, 1, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.aftereven, board)
        print("End block.\n")

        print("Testing module rules/lowinverse.")
        import rules.lowinverse
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 2],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.lowinverse, board)
        print("End block.\n") 

        print("Testing module rules/highinverse.")
        import rules.highinverse
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.highinverse, board)
        print("End block.\n") 

        print("Testing module rules/baseclaim.")
        import rules.baseclaim
        board = [[0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 1, 2, 1, 2, 1],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 2]]
        test_rule(rules.baseclaim, board)
        print("End block.\n") 
