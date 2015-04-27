# before.py

import computer

def generate_solutions(board, me):
    def ensure_for_before(previous_square, current_square, direction=None):
        if direction:
            if direction.value not in range(5): return False
        if current_square.state.value == computer.State.empty.value and current_square.y == 5: return False
        if current_square.state != me.other(): return True
        else: return False
    before_groups = computer.find_streaks(board, 4, ensure_for_before)

    computer.print_board(board)
    for group in before_groups:
        solution = []
        for square in [square for square in group if square.state.value == computer.State.empty.value]:
            solution.append(board[square.x][square.y + 1])
        print("GROUP:", group)
        print()
        yield computer.Solution(computer.Rule.before, group, [tuple(solution)])
