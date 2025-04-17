# backend/qlearning/q_player.py
import pickle
import os

# Încarcă Q-table la început
Q_PATH = os.path.join(os.path.dirname(__file__), "q_table.pkl")
with open(Q_PATH, "rb") as f:
    Q = pickle.load(f)

def get_ai_move_q(board):
    state = "".join(c if c != None else " " for c in board)
    actions = [i for i, v in enumerate(state) if v == " "]
    if not actions:
        return -1
    q_vals = [Q.get((state, a), 0) for a in actions]
    best_action = actions[q_vals.index(max(q_vals))]
    return best_action
