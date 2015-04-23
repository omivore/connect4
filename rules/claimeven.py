# claimeven.py

import computer

def generate_solutions(board, me):
    for square in [square for row in board for square in row if square.state.value == computer.State.empty.value  and square.y % 2 == 1]:
        if computer.look_ahead(square.x, square.y, computer.Direction.south):
            lower_square = computer.step(square.x, square.y, computer.Direction.south)
            if board[lower_square[0]][lower_square[1]].state.value == computer.State.empty.value:
                # Then both are empty
                solution = computer.Solution(computer.Rule.claimeven, (square, lower_square), [(square,)])
                if computer.is_useful_solution(board, solution.solved, me): yield solution
