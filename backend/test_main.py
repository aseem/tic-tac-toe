import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from db import get_session
from main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",  # no filename = in memory
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # one shared connection, or each would get its own empty database
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def game_id(client) -> str:
    """Create a fresh game and return its id."""
    return client.post("/games").json()["id"]


def play(client, game_id, *positions):
    """Plays all the moves in *positions and returns the response from the last move."""
    *setup, last = positions
    for p in setup:
        response = client.post(f"/games/{game_id}/moves", json={"position": p})
        assert response.status_code == 200, response.json()
    return client.post(f"/games/{game_id}/moves", json={"position": last})


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_game(client):
    response = client.post("/games")
    assert response.status_code == 201
    data = response.json()
    assert data["board"] == [None] * 9
    assert data["current_player"] == "X"
    assert data["winner"] is None
    assert data["is_draw"] is False


def test_get_unknown_game_returns_404(client):
    response = client.get("/games/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_first_move_places_x(client, game_id):
    response = client.post(f"/games/{game_id}/moves", json={"position": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["board"][4] == "X"
    assert data["current_player"] == "O"


def test_game_ending_win_x(client, game_id):
    response = play(client, game_id, 0, 1, 3, 4, 6)
    data = response.json()
    assert data["winner"] == "X"
    assert data["is_draw"] is False
    assert data["current_player"] == "O"


def test_move_after_game_ending(client, game_id):
    response = play(client, game_id, 0, 1, 3, 4, 6, 7)
    assert response.status_code == 400
    assert response.json()["detail"] == "The game is already over"


def test_move_on_taken_square(client, game_id):
    response = play(client, game_id, 0, 0)
    assert response.status_code == 400
    assert response.json()["detail"] == "The position is already taken"


def test_invalid_position(client, game_id):
    response = play(client, game_id, -1)
    assert response.status_code == 422

    response = play(client, game_id, 9)
    assert response.status_code == 422


def test_move_on_unknown_game(client):
    response = play(client, "foo", 0)
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_state_persistence(client, game_id):
    play(client, game_id, 0, 1, 2, 3)
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
