# lowinverse.py

import computer
import itertools

def generate_solutions(board, me):
    # Find all combinations of columns. For each pair's columns, find all possible pairs of two vertically consecutive squares
    # that have an odd upper square and are empty. Find all combinations of these square pairs to each other across columns.
    for col1, col2 in itertools.product(range(7), range(7)):
        if col1 == col2: continue
        for upper1, upper2 in itertools.product(*[[row for row in range(6) if row % 2 == 0 and row != 0
                                                   and board[col][row].state.value == computer.State.empty.value 
                                                   and board[col][row - 1].state.value == computer.State.empty.value] 
                                                  for col in [col1, col2]]):
            # Yield the two upper squares as solutions.
            yield computer.Solution(computer.Rule.lowinverse, 
                                    (board[col1][upper1], board[col1][upper1 - 1], board[col2][upper2], board[col2][upper2 - 1]),
                                    [(board[col1][upper1], board[col2][upper2]), 
                                     (board[col1][upper1], board[col1][upper1 - 1]), (board[col2][upper2], board[col2][upper2 - 1])])
