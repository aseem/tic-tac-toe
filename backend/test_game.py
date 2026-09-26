import pytest

from game import InvalidMoveError, apply_move, check_winner, current_player, is_draw


def test_empty_board_has_no_winner():
    board = [None] * 9
    assert check_winner(board) is None
    assert not is_draw(board)


def test_top_row_wins():
    # fmt: off
    board = ["X", "X", "X",
            None, "O", None,
            "O", None, None]
    # fmt: on
    assert check_winner(board) == "X"
    assert not is_draw(board)


def test_middle_col_wins():
    # fmt: off
    board = ["X", "O", "X",
            None, "O", None,
            "X", "O", None]
    # fmt: on
    assert check_winner(board) == "O"
    assert not is_draw(board)


def test_diagonal_wins():
    # fmt: off
    board = ["X", "O", "O",
            None, "X", None,
            None, None, "X"]
    # fmt: on
    assert check_winner(board) == "X"
    assert not is_draw(board)


def test_full_board_no_winner():
    # fmt: off
    board = ["X", "O", "X",
            "X", "X", "O",
            "O", "X", "O"]
    # fmt: on
    assert check_winner(board) is None
    assert is_draw(board)


def test_partly_filled_no_winner():
    # fmt: off
    board = ["X", None, "O",
            None, "X", "X",
            None, None, "O"]
    # fmt: on
    assert check_winner(board) is None
    assert not is_draw(board)


def test_full_board_winner():
    # fmt: off
    board = ["X", "O", "X",
            "O", "X", "O",
            "O", "X", "X"]
    # fmt: on
    assert check_winner(board) == "X"
    assert not is_draw(board)


def test_cannot_move_after_game_over():
    # fmt: off
    board = ["X", "X", "X",
            "O", "O", None,
            None, None, None]
    # fmt: on
    with pytest.raises(InvalidMoveError, match="over"):
        apply_move(board, 8)


def test_apply_move_does_not_change_original_board():
    board = [None] * 9
    new_board = apply_move(board, 4)
    assert new_board[4] == "X"
    assert board[4] is None


def test_second_move_places_O():
    board = [None] * 9
    second_board = apply_move(board, 0)
    assert second_board[0] == "X"
    third_board = apply_move(second_board, 2)
    assert third_board[0] == "X"
    assert third_board[2] == "O"


def test_move_taken_square():
    # fmt: off
    board = ["X", "X", "O",
            "O", "X", None,
            None, None, None]
    # fmt: on
    with pytest.raises(InvalidMoveError, match="taken"):
        apply_move(board, 4)


def test_move_invalid_positions():
    board = [None] * 9
    with pytest.raises(InvalidMoveError, match="invalid"):
        apply_move(board, -1)
    with pytest.raises(InvalidMoveError, match="invalid"):
        apply_move(board, 9)


def test_current_player_O():
    # fmt: off
    board = ["X", "X", "O",
            "O", "X", None,
            None, None, None]
    # fmt: on
    assert current_player(board) == "O"


def test_current_player_X():
    # fmt: off
    board = ["X", "X", "O",
            "O", None, None,
            None, None, None]
    # fmt: on
    assert current_player(board) == "X"
