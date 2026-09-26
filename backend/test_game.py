from game import check_winner, is_draw


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
