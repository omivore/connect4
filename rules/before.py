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

    for group in before_groups:
        solution = []
        for square in [square for square in group if square.state.value == computer.State.empty.value]:
            solution.append(board[square.x][square.y + 1])

        # Find claimeven solutions
        claimeven = computer.rules.claimeven
        claimevens = [] # List of claimevens to attach to object property, so that computer knows they are the claimevens
        for solution in claimeven.generate_solutions(board, me):
            for square in solution.squares:
                if square in group + (other,):
                    continue
            else:
                for solutionset in solution.solved:
                    solved.append(solutionset)
                    claimevens.append(solutionset)
                    
        # Find vertical solutions
        vertical = computer.rules.vertical
        for solution in vertical.generate_solutions(board, me):
            for square in solution.squares:
                if square in group + (other,):
                    continue
            else:
                for solutionset in solution.solved:
                    solved.append(solutionset)
                        
        solution = computer.Solution(computer.Rule.before, group, [tuple(solution)])
        solution.claimevens = claimevens
        yield solution
