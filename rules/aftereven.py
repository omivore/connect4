# aftereven.py

import computer
import copy
import itertools

def generate_solutions(board, me):
    # Fill in all empty even not-top-row squares with black on a temporary board where square underneath is empty too
    testboard = copy.deepcopy(board)
    for square in [square for row in testboard for square in row 
                   if square.state.value == computer.State.empty.value 
                   and square.y != 5 and square.y % 2 == 1]: # % 2 == 1 since off-by-one; want even
        if computer.look_ahead(square.x, square.y, computer.Direction.south):
            lower_x, lower_y = computer.step(square.x, square.y, computer.Direction.south)
            lower_square = board[lower_x][lower_y]
            if lower_square.state.value == computer.State.empty.value:
                square.state = computer.State.black

    # Find and gather all possible combinations that are horizontal and in the even rows
    def ensure_for_aftereven(previous_square, current_square, direction=None):
        if direction:
            if direction.value != computer.Direction.east.value: return False
        if current_square.y % 2 == 1 and current_square.y != 5 and current_square.state.value == computer.State.black.value:
            return True
        else: return False
    combinations = computer.find_streaks(testboard, 4, ensure_for_aftereven)

    # For each combination, get the columns it's composed of, if the original space on the board is empty
    yielded = set()
    yielded_add = yielded.add
    for combo in combinations:
        columns = set()
        for square in combo:
            if board[square.x][square.y].state.value == computer.State.empty.value:
                columns.add(square.x)
        # Yield solutions for each of the squares above the combination's row
        for column, row in itertools.product(columns, range(combo[0].y + 1, 6)):
            if board[column][row] not in yielded:
                yielded_add(board[column][row])
                yield computer.Solution(computer.Rule.aftereven, combo, [(board[column][row],)])
