# specialbefore.py

import computer
import itertools

def generate_solutions(board, me):
    def ensure_for_before(previous_square, current_square, direction=None):
        if direction:
            if direction.value not in range(5): return False
        if current_square.state.value == computer.State.empty.value and current_square.y == 5: return False
        if current_square.state != me.other(): return True
        else: return False
    before_groups = computer.find_streaks(board, 4, ensure_for_before)
    playables = [board[x][y] for x, y in computer.playables(board)]
    for group in before_groups.copy():
        for square in group:
            if square.state.value == computer.State.empty.value and square in playables:
                break
        else: before_groups.discard(group) # Remove group if cycled through all squares and no empty playables.
    
    for group in before_groups:
        before_columns = [square.x for square in group]
        other_squares = [square for square in playables if square.x not in before_columns]
        playables_in_group = [square for square in group if square in playables]
        for other in other_squares:
            solved = []
            # Successor solutions
            solution = []
            for square in [square for square in group if square.state.value == computer.State.empty.value]:
                solution.append(board[square.x][square.y + 1])
            solved.append(tuple(solution))

            # Two playables solution
            for playable in playables:
                if playable == other: continue # Can't have two of the same square
                solved.append((other, playable))

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
                        
            solution = computer.Solution(computer.Rule.specialbefore, group + (other,), solved)
            solution.claimevens = claimevens
            yield solution
