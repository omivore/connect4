# baseclaim.py

import computer
import itertools

def generate_solutions(board, me):
    playables = [board[x][y] for x, y in computer.playables(board)]
    seconds_candidates = {square: board[square.x][square.y + 1] for square in playables 
                           if board[square.x][square.y + 1].state.value == computer.State.empty.value}
    for squareset in [combo for combo in itertools.combinations(playables, 3)]:
        # Make sure that at least one of the squares in squareset is a seconds_candidates.
        for square in squareset:
            if square in [seconds for seconds in seconds_candidates]: 
                second = square
                non_playable = seconds_candidates[second]
                break
        else: continue
        first = squareset[0] if squareset[0] != second else squareset[1]
        for square in squareset:
            if square == first or square == second: continue
            else:
                third = square
                break

        yield computer.Solution(computer.Rule.baseclaim, (first, second, third, non_playable), 
                                [(first, non_playable), (third, non_playable), (second, third), (second, first)])
