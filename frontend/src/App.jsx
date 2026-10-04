import Board from "./Board.jsx";

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
  // prettier-ignore
  const board = ["X", "O", null, 
                null, "X", null, 
                null, null, "O"];

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Status winner={null} isDraw={false} currentPlayer="O" />
      <Board board={board} />
    </main>
  );
}
