# claimeven.py

import computer

def generate_solutions(board, me):
    for square in [square for row in board for square in row 
                   if square.state.value == computer.State.empty.value and square.y % 2 == 1]: # % 2 == 1 since off-by-one; want even
        if computer.look_ahead(square.x, square.y, computer.Direction.south):
            lower_x, lower_y = computer.step(square.x, square.y, computer.Direction.south)
            lower_square = board[lower_x][lower_y]
            if lower_square.state.value == computer.State.empty.value:
                # Then both are empty
                yield computer.Solution(computer.Rule.claimeven, (square, lower_square), [(square,)])
