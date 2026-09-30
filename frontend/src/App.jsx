function Status({ winner, isDraw, currentPlayer }) {
  if (winner) {
    return <p>Winner: {winner}</p>;
  } else if (isDraw) {
    return <p>The game ended in a tie!</p>;
  }
  return <p>Current Player: {currentPlayer}</p>;
}

function Square({ value }) {
  return <button className="square">{value}</button>;
}

function Board({ board }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square key={index} value={value} />
      ))}
    </div>
  );
}

export default function App() {
  const board = ["X", "O", null, null, "X", null, null, null, "O"];

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Status winner={null} isDraw={false} currentPlayer="O" />
      <Board board={board} />
    </main>
  );
}
