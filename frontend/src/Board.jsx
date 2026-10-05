function Square({ value, onClick }) {
  return (
    <button className={value ? `square ${value}` : "square"} onClick={onClick}>
      {value}
    </button>
  );
}

export default function Board({ board, onSquareClick }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square
          key={index}
          value={value}
          onClick={() => onSquareClick(index)}
        />
      ))}
    </div>
  );
}
