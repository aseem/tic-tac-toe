function Square({value}) {
  return <button className="square">{value}</button>
}

function Board({ board }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square key={index} value={value} />
      ))}
    </div>
  )
}

export default function App() {
  const board = ["X", "O", null,
                null, "X", null,
                null, null, "O"]
  
  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <Board board={board} />
    </main>
  )
}
