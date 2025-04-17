import { useState } from 'react';
import './Game.css';

const initialBoard = Array(9).fill(null);

const defaultStats = {
  xWins: 0,
  oWins: 0,
  draws: 0,
  games: 0,
};

function loadStats() {
  const stats = localStorage.getItem("tictactoe-stats");
  return stats ? JSON.parse(stats) : { ...defaultStats };
}

function saveStats(stats) {
  localStorage.setItem("tictactoe-stats", JSON.stringify(stats));
}

export default function Game() {
  const [board, setBoard] = useState(initialBoard);
  const [isXTurn, setIsXTurn] = useState(true);
  const [winner, setWinner] = useState(null);
  const [waiting, setWaiting] = useState(false);
  const [stats, setStats] = useState(loadStats());

  async function getAIMove(board) {
    const response = await fetch("http://localhost:5000/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board: board.map(c => c || " ") })
    });
    const data = await response.json();
    return data.move;
  }

  async function checkWinner(board) {
    const response = await fetch("http://localhost:5000/api/winner", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board: board.map(c => c || " ") })
    });
    const data = await response.json();
    return data.winner;
  }

  async function handleClick(i) {
    if (board[i] || winner || waiting) return;

    const newBoard = [...board];
    newBoard[i] = "X";
    setBoard(newBoard);
    setWaiting(true);

    // Verificăm dacă X a câștigat
    let result = await checkWinner(newBoard);
    if (result) {
      updateStatsAndFinish(result, newBoard);
      return;
    }

    // Mutare AI
    const aiMove = await getAIMove(newBoard);
    if (aiMove !== -1) {
      newBoard[aiMove] = "O";
    }

    result = await checkWinner(newBoard);
    updateStatsAndFinish(result, newBoard);
  }

  function updateStatsAndFinish(result, updatedBoard) {
    setBoard(updatedBoard);
    setWinner(result);
    setWaiting(false);

    if (result) {
      const updatedStats = { ...stats, games: stats.games + 1 };

      if (result === "X") updatedStats.xWins += 1;
      else if (result === "O") updatedStats.oWins += 1;
      else if (result === "Draw") updatedStats.draws += 1;

      setStats(updatedStats);
      saveStats(updatedStats);
    }
  }

  function handleReset() {
    setBoard(initialBoard);
    setIsXTurn(true);
    setWinner(null);
    setWaiting(false);
  }

  function renderSquare(i) {
    return (
      <button className="square" onClick={() => handleClick(i)}>
        {board[i]}
      </button>
    );
  }

  return (
    <div className="game">
      <h1>Tic Tac Toe</h1>
      <div className="status">
        {winner
          ? winner === "Draw"
            ? "Tie!"
            : `Winner: ${winner}`
          : `You are: X`}
      </div>
      <div className="board">
        {[0, 1, 2].map((row) => (
          <div key={row} className="board-row">
            {renderSquare(row * 3)}
            {renderSquare(row * 3 + 1)}
            {renderSquare(row * 3 + 2)}
          </div>
        ))}
      </div>
      <button className="reset" onClick={handleReset}>
        Restart
      </button>

      <div className="stats">
        <h3>Statistics</h3>
        <p>🧍 Wins X: {stats.xWins}</p>
        <p>🤖 Wins O: {stats.oWins}</p>
        <p>⚖️ Tie: {stats.draws}</p>
        <p>🎮 Total Rounds: {stats.games}</p>
      </div>
    </div>
  );
}
