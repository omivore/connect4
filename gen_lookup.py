# gen_lookup.py

import computer
import sqlite3

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

def build_node():
    pass
