import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware


from game import (
    BOARD_SIZE,
    Board,
    InvalidMoveError,
    apply_move,
    check_winner,
    current_player,
    is_draw,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Every game lives here, keyed by its id. In-memory only: games are lost
# whenever the server restarts.
games: dict[str, Board] = {}


class GameState(BaseModel):
    id: str
    board: Board
    current_player: str
    winner: str | None
    is_draw: bool


class MoveRequest(BaseModel):
    position: int = Field(ge=0, lt=BOARD_SIZE)


def to_game_state(game_id: str, board: Board) -> GameState:
    """Package a board with everything the frontend needs to display it."""
    return GameState(
        id=game_id,
        board=board,
        current_player=current_player(board),
        winner=check_winner(board),
        is_draw=is_draw(board),
    )


def get_board_or_404(game_id: str) -> Board:
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/games", status_code=201)
def create_game() -> GameState:
    game_id = str(uuid.uuid4())
    games[game_id] = [None] * BOARD_SIZE
    return to_game_state(game_id, games[game_id])


@app.get("/games/{game_id}")
def get_game(game_id: str) -> GameState:
    board = get_board_or_404(game_id)
    return to_game_state(game_id, board)


@app.post("/games/{game_id}/moves")
def make_move(game_id: str, move: MoveRequest) -> GameState:
    board = get_board_or_404(game_id)
    try:
        new_board = apply_move(board, move.position)
    except InvalidMoveError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    games[game_id] = new_board
    return to_game_state(game_id, new_board)
