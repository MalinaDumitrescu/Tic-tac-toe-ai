from flask import Flask, request, jsonify
from flask_cors import CORS
from qlearning.q_player import get_ai_move_q
from game_logic import check_winner  # păstrăm pentru verificare câștigător

app = Flask(__name__)
CORS(app)

@app.route("/api/move", methods=["POST"])
def get_move():
    data = request.get_json()
    board = data.get("board")

    if not board or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400

    move = get_ai_move_q(board)
    return jsonify({"move": move})

@app.route("/api/winner", methods=["POST"])
def get_winner():
    data = request.get_json()
    board = data.get("board")
    winner = check_winner(board)
    return jsonify({"winner": winner})

if __name__ == "__main__":
    app.run(debug=True)
