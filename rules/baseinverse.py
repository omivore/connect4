# baseinverse.py

import computer
import itertools

def generate_solutions(board, me):
    playable = [board[x][y] for x, y in computer.playables(board)]
    for solved in itertools.combinations(playable, 2):
        yield computer.Solution(computer.Rule.baseinverse, solved, [solved])
