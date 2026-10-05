import Board from "./Board.jsx";
import { useState } from "react";

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
  const [board, setBoard] = useState(Array(9).fill(null));
  const currentPlayer =
    board.filter((v) => v == "X").length ===
    board.filter((v) => v == "O").length
      ? "X"
      : "O";

  function handleSquareClick(index) {
    if (board[index] === "X" || board[index] == "O") return;

    const newBoard = [...board];
    newBoard[index] = currentPlayer;
    setBoard(newBoard);
  }

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Status winner={null} isDraw={false} currentPlayer={currentPlayer} />
      <Board board={board} onSquareClick={handleSquareClick} />
    </main>
  );
}
