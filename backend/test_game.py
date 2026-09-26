from game import check_winner

def test_empty_board_has_no_winner():
    board = [None] * 9
    assert check_winner(board) is None

def test_top_row_wins():
    board = ["X", "X", "X",
            None, "O", None,
            "O", None, None]
    assert check_winner(board) == "X"

def test_middle_col_wins():
    board = ["X", "O", "X",
            None, "O", None,
            "X", "O", None]
    assert check_winner(board) == "O"

def test_diagonal_wins():
    board = ["X", "O", "O",
            None, "X", None,
            None, None, "X"]
    assert check_winner(board) == "X"

def test_no_winner():
    board = ["X", "O", "X",
            "X", "X", "O",
             "O", "X", "O"]
    assert check_winner(board) == None