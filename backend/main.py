# backend/main.py
from game_logic import check_winner, get_ai_move

def print_board(board):
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i+3]))
        if i < 6:
            print("---------")

def main():
    board = [" "] * 9
    print("Tic Tac Toe - Tu ești X, AI-ul este O")
    print_board(board)

    while True:
        # Mutarea jucătorului
        while True:
            try:
                player_move = int(input("Alege o poziție (0-8): "))
                if board[player_move] == " ":
                    board[player_move] = "X"
                    break
                else:
                    print("Poziție ocupată.")
            except (ValueError, IndexError):
                print("Introduceți o poziție validă (0-8).")

        print_board(board)
        winner = check_winner(board)
        if winner:
            print(f"Rezultat: {winner}")
            break

        # Mutarea AI-ului
        ai_move = get_ai_move(board)
        board[ai_move] = "O"
        print(f"\nAI-ul a ales poziția {ai_move}:")
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"Rezultat: {winner}")
            break

if __name__ == "__main__":
    main()
