# baseinverse.py

import computer
import itertools

def generate_solutions(board, me):
    playable = []
    for row in board:
        for y in range(5):
            if row[y].state.value == computer.State.empty.value:
                playable.append(row[y])
                break
    for solved in itertools.combinations(playable, 2):
        yield computer.Solution(computer.Rule.baseinverse, solved, [solved])
