function Square({ value }) {
  return <button className="square">{value}</button>;
}

export default function Board({ board }) {
  return (
    <div className="board">
      {board.map((value, index) => (
        <Square key={index} value={value} />
      ))}
    </div>
  );
}
