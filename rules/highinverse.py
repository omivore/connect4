# highinverse.py

import computer
import itertools

def generate_solutions(board, me):
    # Find all combinations of columns. For each pair's columns, find all possible pairs of three vertically consecutive squares
    # that have an even upper square and are empty. Find all combinations of these square pairs to each other across columns.
    for col1, col2 in itertools.product(range(7), range(7)):
        if col1 == col2: continue
        for upper1, upper2 in itertools.product(*[[row for row in range(6) if row % 2 == 1 and row != 1
                                                   and board[col][row].state.value == computer.State.empty.value 
                                                   and board[col][row - 1].state.value == computer.State.empty.value 
                                                   and board[col][row - 2].state.value == computer.State.empty.value] 
                                                  for col in [col1, col2]]):
            squareset = (board[col1][upper1], board[col1][upper1 - 1], board[col1][upper1 - 2], 
                         board[col2][upper2], board[col2][upper2 - 1], board[col2][upper2 - 1])
            # Yield the two upper squares as solutions.
            yield computer.Solution(computer.Rule.highinverse, squareset,
                                    [(board[col1][upper1], board[col2][upper2])])
            # Yield the two middle squares as solutions.
            yield computer.Solution(computer.Rule.highinverse, squareset,
                                    [(board[col1][upper1 - 1], board[col2][upper2 - 1])])
            # Yield the two pairs of squares at the top of each column.
            yield computer.Solution(computer.Rule.highinverse, squareset,
                                    [(board[col1][5], board[col1][4])])
            yield computer.Solution(computer.Rule.highinverse, squareset,
                                    [(board[col2][5], board[col2][4])])
            # If col1 lowest square is playable, yield lower square of col1 and upper square of col2 as solution.
            if board[col1][upper1 - 2].coords() in computer.playables(board):
                yield computer.Solution(computer.Rule.highinverse, squareset,
                                        [(board[col1][upper1 - 2], board[col2][upper2])])
            # Same with col2, except vice versa.
            if board[col2][upper2 - 2].coords() in computer.playables(board):
                yield computer.Solution(computer.Rule.highinverse, squareset,
                                        [(board[col2][upper2 - 2], board[col1][upper1])])
