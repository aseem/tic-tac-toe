import Board from "./Board.jsx";
import { useState } from "react";

const API_URL = "http://localhost:8000";

function Status({ winner, isDraw, currentPlayer }) {
  if (winner) {
    return <p>Winner: {winner}</p>;
  }
  if (isDraw) {
    return <p>The game ended in a tie!</p>;
  }
  return <p>Current Player: {currentPlayer}</p>;
}

export default function App() {
  const [game, setGame] = useState(null);

  async function handleNewGameClick() {
    const response = await fetch(`${API_URL}/games`, { method: "POST" });
    const data = await response.json();
    setGame(data);
  }

  async function handleSquareClick(index) {
    if (game === null) return;
    const response = await fetch(`${API_URL}/games/${game.id}/moves`, { 
      method: "POST",
      headers: {"Content-Type": "application/json" },
      body:JSON.stringify({ position: index})
    });
    const data = await response.json();
    setGame(data);
  }

  if (game === null) {
    return (
      <main>
        <h1>Tic-Tac-Toe</h1>
        <button onClick={handleNewGameClick}>New Game</button>
      </main>
    );
  }

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Status
        winner={game.winner}
        isDraw={game.is_draw}
        currentPlayer={game.current_player}
      />
      <Board board={game.board} onSquareClick={handleSquareClick} />
      <button onClick={handleNewGameClick}>New Game</button>
    </main>
  );
}
