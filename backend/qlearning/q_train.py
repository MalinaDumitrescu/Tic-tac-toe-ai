import random
import pickle
import numpy as np

Q = {}  # Q-table
alpha = 0.3    # learning rate
gamma = 0.9    # discount factor
epsilon = 0.1  # exploration rate
EPISODES = 100_000

def get_empty_positions(state):
    return [i for i, v in enumerate(state) if v == " "]

def get_new_state(state, action, player):
    return state[:action] + player + state[action+1:]

def check_winner(state):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if state[a] == state[b] == state[c] and state[a] != " ":
            return state[a]
    if " " not in state:
        return "Draw"
    return None

def choose_action(state, player):
    if random.random() < epsilon:
        return random.choice(get_empty_positions(state))

    q_vals = [Q.get((state, a), 0) for a in get_empty_positions(state)]
    actions = get_empty_positions(state)
    return actions[np.argmax(q_vals)]

def update_q(state, action, reward, next_state):
    old_value = Q.get((state, action), 0)
    future_rewards = [Q.get((next_state, a), 0) for a in get_empty_positions(next_state)]
    best_future = max(future_rewards) if future_rewards else 0
    new_value = old_value + alpha * (reward + gamma * best_future - old_value)
    Q[(state, action)] = new_value

def train():
    for _ in range(EPISODES):
        state = " " * 9
        player = "X"
        game_history = []

        while True:
            action = choose_action(state, player)
            next_state = get_new_state(state, action, player)
            game_history.append((state, action, player))
            winner = check_winner(next_state)
            if winner:
                break
            state = next_state
            player = "O" if player == "X" else "X"

        # Assign rewards
        for state, action, player in reversed(game_history):
            if winner == "Draw":
                reward = 0.5
            elif winner == player:
                reward = 1
            else:
                reward = -1
            next_state = get_new_state(state, action, player)
            update_q(state, action, reward, next_state)

    with open("qlearning/q_table.pkl", "wb") as f:
        pickle.dump(Q, f)
    print("Model antrenat și salvat în qlearning/q_table.pkl ✅")

if __name__ == "__main__":
    train()
