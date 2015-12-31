# gen_lookup.py

import computer
import sqlite3
import copy,itertools

conn = sqlite3.connect("lookup.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS game_states
             (
             state_hash INTEGER NOT NULL,
             result INTEGER NOT NULL,
             col1 INTEGER,
             col2 INTEGER,
             col3 INTEGER,
             col4 INTEGER,
             col5 INTEGER,
             col6 INTEGER,
             col7 INTEGER,
             PRIMARY KEY(state_hash),
             FOREIGN KEY(col1) REFERENCES game_states(state_hash),
             FOREIGN KEY(col2) REFERENCES game_states(state_hash),
             FOREIGN KEY(col3) REFERENCES game_states(state_hash),
             FOREIGN KEY(col4) REFERENCES game_states(state_hash),
             FOREIGN KEY(col5) REFERENCES game_states(state_hash),
             FOREIGN KEY(col6) REFERENCES game_states(state_hash),
             FOREIGN KEY(col7) REFERENCES game_states(state_hash)
             )''')
conn.commit()

root = computer.generate_squares([[0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0]])

def build_node(new_state):
    # Receives the state of this node.
    state_hash = hash(list_to_tuple(new_state))

    # Check that this node hasn't already been created.
    c.execute("SELECT EXISTS(SELECT 1 FROM game_states WHERE state_hash=? LIMIT 1)", (state_hash,))
    if c.fetchone() != (0,):
        # If this node already exists, then don't bother calculating the result; just pass it on.
        c.execute("SELECT result FROM game_states WHERE state_hash=? LIMIT 1", (state_hash,))
        result = c.fetchone()
        return state_hash, result[0]
    
    winner = computer.check_for_win(new_state)
    if winner != computer.Win.none: # If the game is decided, Set the columns to null.
        col1 = None
        col2 = None
        col3 = None
        col4 = None
        col5 = None
        col6 = None
        col7 = None
        result = winner.value
    else: # That is, if the game is undetermined right now. If the column is full, then that column is None, because there aren't any more possibilities/branches that way.
        col1, result1 = build_node(step_state(new_state, 0)) if step_state(new_state, 0) != None else (None, None)
        col2, result2 = build_node(step_state(new_state, 1)) if step_state(new_state, 1) != None else (None, None)
        col3, result3 = build_node(step_state(new_state, 2)) if step_state(new_state, 2) != None else (None, None)
        col4, result4 = build_node(step_state(new_state, 3)) if step_state(new_state, 3) != None else (None, None)
        col5, result5 = build_node(step_state(new_state, 4)) if step_state(new_state, 4) != None else (None, None)
        col6, result6 = build_node(step_state(new_state, 5)) if step_state(new_state, 5) != None else (None, None)
        col7, result7 = build_node(step_state(new_state, 6)) if step_state(new_state, 6) != None else (None, None)
        result = compute_result(whose_turn(new_state), [result1, result2, result3, result4, result5, result6, result7])

    # Enter this node into the database.
    try:
        c.execute("INSERT INTO game_states VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (state_hash, result, col1, col2, col3, col4, col5, col6, col7))
        conn.commit()
    except sqlite3.InterfaceError as e:
        print(e)
        print("Data:", state_hash, result, col1, col2, col3, col4, col5, col6, col7)
    
    return state_hash, result

def step_state(state, column):
    #new_state = list(state) # Make a copy that's editable.
    new_state = copy.deepcopy(state)
    current_player = whose_turn(state)
    for row in range(6):
        if new_state[column][row].state == computer.State.empty:
            new_state[column][row].state = computer.State(current_player)
            break
    else: # If for ends without breaking, then return the equivalent of 'column full'.
        return None 
    #return tuple(new_state) # Turn back into tuple for immutability's sake.
    return new_state

def compute_result(player, results):
    # If there's at least one player's win in results, player can choose it, b/c it's player's turn. So player wins this node.
    if player in results:
        return player
    # If there isn't, then if there's a tie they can go for that instead.
    if computer.Win.tie.value in results:
        return computer.Win.tie.value # ie -1
    # Since player gets to choose this turn, the only way other can win is if there's no other choice but to go the way of death.
    else:
        return 1 if player == 2 else 2

    # This applies to both sides; it doesn't matter because compute_result decides based on the current player who's going.

def whose_turn(state):
    # Returns whose turn it is now at the state.
    checkers = 0
    for x, y in itertools.product(range(7), range(6)):
        if state[x][y].state != computer.State.empty: checkers += 1
    if checkers % 2 == 0: return 1
    else: return 2

def list_to_tuple(list_board):
    return tuple(tuple(x for x in list_columns) for list_columns in list_board)

##def print_board(board):
##    """
##    Useful function to print a 2D array of squares in a readable format.
##    DEBUGGING USE ONLY
##    """
##    for y in range(5, -1, -1):
##        for x in range(7):
##            print(board[x][y].state.name, " ", end="")
##        print()
##    print()

##print(root)
##print("Testing step_state...")
##new_state = step_state(root, 2)
##print(new_state)
##print(new_state[2][0].state)
##print("Testing whose_turn...")
##print(whose_turn(new_state))
##print("Testing list_to_tuple...")
##print(list_to_tuple(root))
##print("Testing compute_result...")
##assert(compute_result(2, [-1, 1, 1, 2, 1, -1, -1]) == 2)

try:
    build_node(root)
except KeyboardInterrupt:
    c.close()
    conn.close()
