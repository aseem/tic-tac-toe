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

  function handleSquareClick(index) {
    const newBoard = [...board];
    newBoard[index] = "X";
    setBoard(newBoard);
  }

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Status winner={null} isDraw={false} currentPlayer="O" />
      <Board board={board} onSquareClick={handleSquareClick} />
    </main>
  );
}
