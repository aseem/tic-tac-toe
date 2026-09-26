# The 8 ways to win: 3 rows, 3 columns, 2 diagonals
# fmt: off
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]
# fmt: on


def check_winner(board: list[str | None]) -> str | None:
    """Return "X" or "O" if that player has three in a row, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: list[str | None]) -> bool:
    """Return True only when the board is full and there is no winner."""
    return None not in board and check_winner(board) is None
        
