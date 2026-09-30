function Square({value}) {
  return <button className="square">{value}</button>
}

export default function App() {
  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <div className="board">
        <Square value="X"/>
        <Square value="O"/>
        <Square value={null}/>
      </div>
    </main>
  )
}
