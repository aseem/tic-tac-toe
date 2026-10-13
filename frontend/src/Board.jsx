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

export default function Board({ board, onSquareClick, gameOver, requestPending }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square
          key={index}
          value={value}
          disabled={gameOver || value !== null || requestPending}
          onClick={() => onSquareClick(index)}
        />
      ))}
    </div>
  );
}
