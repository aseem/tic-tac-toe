Board = list[str | None]

# The 8 ways to win: 3 rows, 3 columns, 2 diagonals
# fmt: off
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]
# fmt: on


class InvalidMoveError(ValueError):
    """Raised when a move breaks the rules of the game."""


def check_winner(board: Board) -> str | None:
    """Return "X" or "O" if that player has three in a row, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: Board) -> bool:
    """Return True only when the board is full and there is no winner."""
    return None not in board and check_winner(board) is None


def current_player(board: Board) -> str:
    """Return whose turn it is.  X goes first, so equal counts mean X's turn"""
    return "X" if board.count("X") == board.count("O") else "O"


def apply_move(board: Board, position: int) -> Board:
    """Return a new board with the current player's mark at position.

    Raises InvalidMoveError if the move breaks the rules.
    """

    if check_winner(board) is not None or is_draw(board):
        raise InvalidMoveError("The game is already over")

    if not 0 <= position < len(board):
        raise InvalidMoveError("Position is invalid")

    if board[position] is not None:
        raise InvalidMoveError("The position is already taken")

    new_board = board.copy()
    new_board[position] = current_player(board)
    return new_board
