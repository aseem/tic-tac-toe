import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_game():
    response = client.post("/games")
    assert response.status_code == 201
    data = response.json()
    assert data["board"] == [None] * 9
    assert data["current_player"] == "X"
    assert data["winner"] is None
    assert data["is_draw"] is False


def test_get_unknown_game_returns_404():
    response = client.get("/games/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


@pytest.fixture
def game_id() -> str:
    """Create a fresh game and return its id."""
    return client.post("/games").json()["id"]


def play(game_id, *positions):
    """Plays all the moves in *positions and returns the response from the last move."""
    *setup, last = positions
    for p in setup:
        response = client.post(f"/games/{game_id}/moves", json={"position": p})
        assert response.status_code == 200, response.json()
    return client.post(f"/games/{game_id}/moves", json={"position": last})


def test_first_move_places_x(game_id):
    response = client.post(f"/games/{game_id}/moves", json={"position": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["board"][4] == "X"
    assert data["current_player"] == "O"


def test_game_ending_win_x(game_id):
    response = play(game_id, 0, 1, 3, 4, 6)
    data = response.json()
    assert data["winner"] == "X"
    assert data["is_draw"] is False
    assert data["current_player"] == "O"


def test_move_after_game_ending(game_id):
    response = play(game_id, 0, 1, 3, 4, 6, 7)
    assert response.status_code == 400
    assert response.json()["detail"] == "The game is already over"


def test_move_on_taken_square(game_id):
    response = play(game_id, 0, 0)
    assert response.status_code == 400
    assert response.json()["detail"] == "The position is already taken"


def test_invalid_position(game_id):
    response = play(game_id, -1)
    assert response.status_code == 422

    response = play(game_id, 9)
    assert response.status_code == 422


def test_move_on_unknown_game():
    response = play("foo", 0)
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_state_persistence(game_id):
    play(game_id, 0, 1, 2, 3)
    response = client.get(f"/games/{game_id}")
    assert response.json()["board"] == [
        "X",
        "O",
        "X",
        "O",
        None,
        None,
        None,
        None,
        None,
    ]
