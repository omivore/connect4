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

root = computer.generate_squares([[0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0]])

def build_node(new_state):
    # Receives the state of this node.
    state_hash = hash(new_state)

    # Check that this node hasn't already been created.
    pass
    
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
    else: # That is, if the game is undetermined right now.
        col1, result1 = build_node(step_state(new_state, 0))
        col2, result2 = build_node(step_state(new_state, 1))
        col3, result3 = build_node(step_state(new_state, 2))
        col4, result4 = build_node(step_state(new_state, 3))
        col5, result5 = build_node(step_state(new_state, 4))
        col6, result6 = build_node(step_state(new_state, 5))
        col7, result7 = build_node(step_state(new_state, 6))
        result = compute_result(whose_turn(new_state), [result1, result2, result3, result4, result5, result6, result7])

    # Enter this node into the database.
    pass
    
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
   pass 

def whose_turn(state):
    # Returns whose turn it is now at the state.
    checkers = 0
    for x, y in itertools.product(range(7), range(6)):
        if state[x][y].state != computer.State.empty: checkers += 1
    if checkers % 2 == 0: return 1
    else: return 2

if __name__ == "__main__":
    print(root)
    print("Testing step_state...")
    new_state = step_state(root, 2)
    print(new_state)
    print(new_state[2][0].state)
    print("Testing whose_turn...")
    print(whose_turn(new_state))
