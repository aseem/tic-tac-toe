import Board from "./Board.jsx";
import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function Status({ winner, isDraw, currentPlayer }) {
  if (winner) {
    return <p className="status">Winner: {winner}</p>;
  }
  if (isDraw) {
    return <p className="status">The game ended in a tie!</p>;
  }
  return <p className="status">Current Player: {currentPlayer}</p>;
}

function ErrorMessage({ msg }) {
  if (msg) {
    return <p>Error: {msg}</p>;
  }
  return null;
}

export default function App() {
  const [game, setGame] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [pending, setPending] = useState(false);
  const [startPending, setStartPending] = useState(false);

  async function sendRequest(path, options) {
    try {
      setPending(true);
      const response = await fetch(`${API_URL}${path}`, options);
      const data = await response.json();
      if (response.ok) {
        setGame(data);
        setErrorMsg(null);
      } else if (response.status === 404) {
        setErrorMsg("That game has expired. Start a new one!");
        setGame(null);
      } else {
        setErrorMsg(
          typeof data.detail === "string"
            ? data.detail
            : "Something went wrong",
        );
      }
    } catch {
      setErrorMsg("Something went wrong talking to the server.");
    } finally {
      setPending(false);
    }
  }

  async function handleNewGameClick() {
    setStartPending(true);
    await sendRequest("/games", { method: "POST" });
    setStartPending(false);
  }

  async function handleSquareClick(index) {
    await sendRequest(`/games/${game.id}/moves`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ position: index }),
    });
  }

  if (game === null) {
    return (
      <main className="card">
        <h1>Tic-Tac-Toe</h1>
        <button className="button" onClick={handleNewGameClick}>
          New Game
        </button>
        <ErrorMessage msg={errorMsg} />
      </main>
    );
  }

  return (
    <main className="card">
      <h1>Tic-Tac-Toe</h1>
      <Status
        winner={game.winner}
        isDraw={game.is_draw}
        currentPlayer={game.current_player}
      />
      <Board
        board={game.board}
        onSquareClick={handleSquareClick}
        gameOver={game.winner !== null || game.is_draw}
        requestPending={pending}
      />
      <button className="button" disabled={pending} onClick={handleNewGameClick}>
        {startPending ? "Starting..." : "New Game"}
      </button>
      <ErrorMessage msg={errorMsg} />
    </main>
  );
}
