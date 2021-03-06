# computer.py

from enum import Enum
import pkgutil
import itertools
import copy

# import the rules!
def all_rules():
        for importer, modname, ispkg in pkgutil.iter_modules(rules.__path__, rules.__name__ + "."):
                yield modname

import rules
for module in all_rules():
        __import__(module, fromlist="filler")

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
        
class Cooperation(Enum):
        disjoint = 1
        no_ce_below = 2
        column_disequal = 3
        disjoint_and_inversecolumns_disequal = 4
        
        disjoint_and_no_ce_below = 5
        no_ce_below_and_column_disequal = 6

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
                return hash((self.x, self.y, self.state.value))

        def coords(self):
                return (self.x, self.y)

class Problem():
        def __init__(self, threat, solution_indices=[]):
                self.threat = threat
                self.solutions = solution_indices

        def __str__(self):
                return "<" + str(self.threat) + ">" + "\n" + str(self.solutions) + "\n"

        def __repr__(self):
                return str(self)

class Solution():
        def __init__(self, rule, squares, solved, solves=set()):
                self.rule = rule
                self.squares = squares
                self.solved = solved
                self.solves = solves

        def __eq__(self, other):
                if type(other).__name__ == Solution.__name__:
                        # Change any lists into sets so equality works.
                        if self.rule == other.rule and set(self.squares) == set(other.squares) and set(self.solved) == set(other.solved):
                                return True
                        else: return False
                else: return NotImplemented

        def __hash__(self):
                return hash((self.rule.value, self.squares, tuple(self.solved)))

        def __str__(self):
                return self.rule.name + "\n1-[" + str(self.squares) + "]\n2-[" + str(self.solved) + "]\n"

        def __repr__(self):
                return str(self)

def playables(board):
        playable = []
        for row in board:
                for y in range(5):
                        if row[y].state.value == State.empty.value:
                                playable.append(row[y].coords())
                                break
        return playable

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
        else: return State.empty.value
                
        four_streaks = find_streaks(grid, 4, ensure_same_color)
        
        if len(four_streaks) > 0:
                sample = four_streaks.pop()
                return sample[0].state.value
        else: return None

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
        # Convert board into grid.
        grid = generate_squares(board)
        # Generate problems.
        problems = generate_problems(grid, State.black)
        # Apply each rule to the board and see which solutions solve which problems
        solutions = link_problems(grid, problems)
        # Create a node graph of all solutions, where connectedness means incompatibility.
        graph = graph_solutions(solutions)
        print(graph)
        
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

        return {Problem(threat) for threat in find_streaks(board, 4, ensure_isnt_me)}
        
def link_problems(board, problems):
        solution_generator = itertools.chain.from_iterable((__import__(module, fromlist="filler").generate_solutions(board, State.black) for module in all_rules()))
        solutions = set()
        for problem, solution in itertools.product(problems, solution_generator):
                if solution_applies(problem, solution):
                        problem.solutions.append(solution)
                        solution.solves.add(problem)
                        solutions.add(solution)
        return solutions

def solution_applies(problem, solution):
        for solutionset in solution.solved:
                for square in solutionset:
                        if square in problem.threat: continue
                        else: break
                else: return True
        return False

def graph_solutions(solutions):
        graph = {sol:[] for sol in solutions}
        for key in graph:
            for other_sol in graph.keys():
                if other_sol == key: continue # Don't count it if it's the same key.
                
                if solutions_cooperate(key, other_sol):
                    graph[key].append(other_sol)
        return graph        
        
def solutions_cooperate(solution1, solution2):
        poss_combos = {Rule.claimeven.value:{Rule.claimeven.value:Cooperation.disjoint,
                                             Rule.baseinverse.value:Cooperation.disjoint,
                                             Rule.vertical.value:Cooperation.disjoint,
                                             Rule.aftereven.value:Cooperation.disjoint,
                                             Rule.lowinverse.value:Cooperation.no_ce_below,
                                             Rule.highinverse.value:Cooperation.no_ce_below,
                                             Rule.baseclaim.value:Cooperation.disjoint,
                                             Rule.before.value:Cooperation.disjoint,
                                             Rule.specialbefore.value:Cooperation.disjoint,},
                       Rule.baseinverse.value:{rule.value:Cooperation.disjoint for rule in Rule},
                       Rule.vertical.value:{rule.value:Cooperation.disjoint for rule in Rule},
                       Rule.aftereven.value:{Rule.claimeven.value:Cooperation.disjoint,
                                             Rule.baseinverse.value:Cooperation.disjoint,
                                             Rule.vertical.value:Cooperation.disjoint,
                                             Rule.aftereven.value:Cooperation.column_disequal,
                                             Rule.lowinverse.value:Cooperation.disjoint_and_no_ce_below,
                                             Rule.highinverse.value:Cooperation.disjoint_and_no_ce_below,
                                             Rule.baseclaim.value:Cooperation.disjoint,
                                             Rule.before.value:Cooperation.column_disequal,
                                             Rule.specialbefore.value:Cooperation.column_disequal},
                       Rule.lowinverse.value:{Rule.claimeven.value:Cooperation.no_ce_below,
                                              Rule.baseinverse.value:Cooperation.disjoint,
                                              Rule.vertical.value:Cooperation.disjoint,
                                              Rule.aftereven.value:Cooperation.disjoint_and_no_ce_below,
                                              Rule.lowinverse.value:Cooperation.disjoint_and_inversecolumns_disequal,
                                              Rule.highinverse.value:Cooperation.disjoint_and_inversecolumns_disequal,
                                              Rule.baseclaim.value:Cooperation.disjoint_and_no_ce_below,
                                              Rule.before.value:Cooperation.no_ce_below_and_column_disequal,
                                              Rule.specialbefore.value:Cooperation.no_ce_below_and_column_disequal},
                       Rule.highinverse.value:{Rule.claimeven.value:Cooperation.no_ce_below,
                                               Rule.baseinverse.value:Cooperation.disjoint,
                                               Rule.vertical.value:Cooperation.disjoint,
                                               Rule.aftereven.value:Cooperation.disjoint_and_no_ce_below,
                                               Rule.lowinverse.value:Cooperation.disjoint_and_inversecolumns_disequal,
                                               Rule.highinverse.value:Cooperation.disjoint_and_inversecolumns_disequal,
                                               Rule.baseclaim.value:Cooperation.disjoint_and_no_ce_below,
                                               Rule.before.value:Cooperation.disjoint_and_no_ce_below,
                                               Rule.specialbefore.value:Cooperation.disjoint_and_no_ce_below,},
                       Rule.baseclaim.value:{Rule.claimeven.value:Cooperation.disjoint,
                                             Rule.baseinverse.value:Cooperation.disjoint,
                                             Rule.vertical.value:Cooperation.disjoint,
                                             Rule.aftereven.value:Cooperation.disjoint,
                                             Rule.lowinverse.value:Cooperation.disjoint_and_no_ce_below,
                                             Rule.highinverse.value:Cooperation.disjoint_and_no_ce_below,
                                             Rule.baseclaim.value:Cooperation.disjoint,
                                             Rule.before.value:Cooperation.disjoint,
                                             Rule.specialbefore.value:Cooperation.disjoint},
                       Rule.before.value:{Rule.claimeven.value:Cooperation.disjoint,
                                          Rule.baseinverse.value:Cooperation.disjoint,
                                          Rule.vertical.value:Cooperation.disjoint,
                                          Rule.aftereven.value:Cooperation.column_disequal,
                                          Rule.lowinverse.value:Cooperation.no_ce_below_and_column_disequal,
                                          Rule.highinverse.value:Cooperation.disjoint_and_no_ce_below,
                                          Rule.baseclaim.value:Cooperation.disjoint,
                                          Rule.before.value:Cooperation.column_disequal,
                                          Rule.specialbefore.value:Cooperation.column_disequal},
                       Rule.specialbefore.value:{Rule.claimeven.value:Cooperation.disjoint,
                                                 Rule.baseinverse.value:Cooperation.disjoint,
                                                 Rule.vertical.value:Cooperation.disjoint,
                                                 Rule.aftereven.value:Cooperation.column_disequal,
                                                 Rule.lowinverse.value:Cooperation.no_ce_below_and_column_disequal,
                                                 Rule.highinverse.value:Cooperation.disjoint_and_no_ce_below,
                                                 Rule.baseclaim.value:Cooperation.disjoint,
                                                 Rule.before.value:Cooperation.column_disequal,
                                                 Rule.specialbefore.value:Cooperation.column_disequal}
        }

        def parse_rules(solution1, solution2, interaction_rule):
                
                squareset1 = solution1.squares
                squareset2 = solution2.squares
                
                if interaction_rule == Cooperation.disjoint:
                        for square in squareset1:
                                if square in squareset2:
                                        return False
                        else: return True
                elif interaction_rule == Cooperation.no_ce_below:
                        inverseset = squareset1 if solution1.rule in (Rule.lowinverse, Rule.highinverse) else squareset2
                        otherset = squareset2 if inverseset == squareset1 else squareset1

                        lowest_inverse = 5
                        for square in inverseset:
                                if square.y < lowest_inverse: lowest_inverse = square.y

                        highest_claimeven = None
                        for square in otherset:
                                if look_ahead(square.x, square.y, Direction.south):
                                        lower_x, lower_y = step(square.x, square.y, Direction.south)
                                        # See if there's another square in the otherset at that position; in effect, does this
                                        #   square exist in otherset?
                                        for poss_square in otherset:
                                                if (poss_square.x == lower_x) and (poss_square.y == lower_y):
                                                        highest_claimeven = square.y

                        if highest_claimeven == None: raise Exception("highest_claimeven doesn't exist...\n" + str(solution1) + str(solution2))

                        if lowest_inverse > highest_claimeven: return False
                        else: return True
                        
                elif interaction_rule == Cooperation.column_disequal:
                        contained = 0
                        for x in [square.x for square in squareset2]:
                                if x in [square.x for square in squareset1]: 
                                        contained += 1
                        return True if contained == 0 or contained == min(len(squareset1), len(squareset2)) else False
                elif interaction_rule == Cooperation.disjoint_and_inversecolumns_disequal:
                        if parse_rules(solution1, solution2, Cooperation.disjoint):
                                set1_col1 = squareset1[0].x
                                for x in [square.x for square in squareset1]:
                                        if x != set1_col1:
                                                set1_col2 = x
                                                break
                                set2_col1 = squareset2[0].x
                                for x in [square.x for square in squareset2]:
                                        if x != set2_col1:
                                                set2_col2 = x
                                                break
                                set1 = {set1_col1, set1_col2}
                                set2 = {set2_col1, set2_col2}
                                if (set1 == set2) or ((set1_col1 not in set2) and (set1_col2 not in set2)):
                                        return True
                        return False
                elif interaction_rule == Cooperation.disjoint_and_no_ce_below:
                        return True if parse_rules(solution1, solution2, Cooperation.disjoint) and \
                                       parse_rules(solution1, solution2, Cooperation.no_ce_below) else False
                elif interaction_rule == Cooperation.no_ce_below_and_column_disequal:
                        return True if parse_rules(solution1, solution2, Cooperation.no_ce_below) and \
                                       parse_rules(solution1, solution2, Cooperation.column_disequal) else False
                else: raise KeyError(interaction_rule)

        print(solution1.rule, solution2.rule)
        return parse_rules(solution1, solution2, poss_combos[solution1.rule.value][solution2.rule.value])

        
def print_board(board):
        """
        Useful function to print a 2D array of squares in a readable format.
        DEBUGGING USE ONLY
        """
        for y in range(5, -1, -1):
                for x in range(7):
                        print(board[x][y].state.name, " ", end="")
                print()

def is_useful_solution(board, solution, me):
        """
        Useful function for seeing if a solution makes an impact.
        DEBUGGING USE ONLY
        """
        problems = generate_problems(board, me)
        for problem in problems:
                if solution_applies(problem, solution):
                        return True
        return False

if __name__ == "__main__":

        def test_rule(rule, board):
                grid = generate_squares(board)
                solutions = list(rule.generate_solutions(grid, State.black))
                useful = 0
                for solution in solutions:
                        if is_useful_solution(grid, solution, State.black):
                                for squares in solution.solved:
                                        print(squares, end=" ")
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
                for square in problem.threat:
                        print(square, end=" ")
                print()
        print(len(problems), " problems total.")
        print("End block.\n")

        print("Function check_for_win testing block. Should return 2, 1, then 0.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 2, 2, 1],
                 [0, 0, 0, 0, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        print(check_for_win(board))
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 1, 2, 1],
                 [0, 0, 1, 1, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        print(check_for_win(board))
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 1, 2, 1],
                 [0, 0, 0, 0, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        print(check_for_win(board))
        print("End block.\n")

        print("Function playables testing block. Should be bottom seven squares' coordinates.")
        board = [[0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 1, 1],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        print(playables(generate_squares(board)))
        print("End block.\n")
        
        print("Function solution_applies testing block. Should be true, then false.")
        print(solution_applies(Problem({Square(0, 0, State.white), Square(0, 1, State.empty), Square(0, 2, State.empty), Square(0, 3, State.empty)}), Solution(Rule.vertical, (Square(0, 1, State.empty), Square(0, 2, State.empty)), [(Square(0, 1, State.empty), Square(0, 2, State.empty))])))
        print(solution_applies(Problem({Square(0, 0, State.white), Square(0, 1, State.empty), Square(0, 2, State.empty), Square(0, 3, State.empty)}), Solution(Rule.vertical, (Square(0, 3, State.empty), Square(0, 4, State.empty)), [(Square(0, 3, State.empty), Square(0, 4, State.empty))])))
        print("End block.\n")

        print("Function link_problems testing block.")
        problems = {Problem({Square(0, 0, State.white), Square(0, 1, State.empty), Square(0, 2, State.empty), Square(0, 3, State.empty)})}
        link_problems(generate_squares(board), problems)
        print(problems)
        
        print("Function solutions_cooperate testing block.")
        print(solutions_cooperate(Solution(Rule.vertical, (Square(0, 3, State.empty), Square(0, 4, State.empty)), [(Square(0, 3, State.empty), Square(0, 4, State.empty))]), Solution(Rule.vertical, (Square(0, 3, State.empty), Square(0, 4, State.empty)), [(Square(0, 3, State.empty), Square(0, 4, State.empty))])))
        
        print("Function graph_solutions testing block through compute.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 1],
                 [1, 2, 2, 1, 2, 1],
                 [0, 0, 0, 0, 2, 2],
                 [0, 0, 0, 0, 0, 0],
                 [1, 2, 1, 2, 1, 2]]
        print(compute(board))

        
        """---------------------No longer need these tests; mostly through with testing now.--------------------

        print("Testing module rules/claimeven.")
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
        board = [[0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 1, 2, 1, 2, 1],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 2]]
        test_rule(rules.baseclaim, board)
        print("End block.\n") 

        print("Testing module rules/before.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 1, 2],
                 [0, 0, 2, 1, 2, 1],
                 [0, 0, 2, 1, 2, 1],
                 [0, 0, 0, 0, 0, 2],
                 [0, 1, 2, 1, 2, 1]]
        test_rule(rules.before, board)
        print("End block.\n") 
"""
        print("Testing module rules/specialbefore.")
        board = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 2, 1, 2, 1, 1],
                 [0, 0, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        test_rule(rules.specialbefore, board)
        print("End block.\n") 
