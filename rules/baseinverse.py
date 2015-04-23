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
        solution = computer.Solution(computer.Rule.baseinverse, solved, [solved])
        if computer.is_useful_solution(board, solution.solved, me): yield solution
