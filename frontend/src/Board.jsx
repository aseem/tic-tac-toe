function Square({ value, onClick, disabled }) {
  return (
    <button
      className={value ? `square ${value}` : "square"}
      disabled={disabled}
      onClick={onClick}
    >
      {value}
    </button>
  );
}

export default function Board({ board, onSquareClick, disabled }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square
          key={index}
          value={value}
          disabled={disabled || value !== null}
          onClick={() => onSquareClick(index)}
        />
      ))}
    </div>
  );
}
