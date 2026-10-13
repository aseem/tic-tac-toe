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

function NewGameButton({ pending, onClick }) {
  return (
    <button className="button" disabled={pending !== null} onClick={onClick}>
      {pending === "start" ? "Starting..." : "New Game"}
    </button>
  );
}

export default function App() {
  const [game, setGame] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [pending, setPending] = useState(null);

  async function sendRequest(actvity, path, options) {
    try {
      setPending(actvity);
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
      setPending(null);
    }
  }

  async function handleNewGameClick() {
    await sendRequest("start", "/games", { method: "POST" });
  }

  async function handleSquareClick(index) {
    await sendRequest("move", `/games/${game.id}/moves`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ position: index }),
    });
  }

  if (game === null) {
    return (
      <main className="card">
        <h1>Tic-Tac-Toe</h1>
        <NewGameButton pending={pending} onClick={handleNewGameClick} />
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
        disabled={game.winner !== null || game.is_draw || pending !== null}
      />
      <NewGameButton pending={pending} onClick={handleNewGameClick} />
      <ErrorMessage msg={errorMsg} />
    </main>
  );
}
