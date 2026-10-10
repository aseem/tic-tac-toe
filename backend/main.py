import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlmodel import Session

from db import Game, SessionDep, create_tables
from game import (
    BOARD_SIZE,
    Board,
    InvalidMoveError,
    apply_move,
    check_winner,
    current_player,
    is_draw,
)

# Comma-separated list of frontend URLs allowed to call this API.
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GameState(BaseModel):
    id: str
    board: Board
    current_player: str
    winner: str | None
    is_draw: bool


class MoveRequest(BaseModel):
    position: int = Field(ge=0, lt=BOARD_SIZE)


def to_game_state(game: Game) -> GameState:
    return GameState(
        id=game.id,
        board=game.board,
        current_player=current_player(game.board),
        winner=check_winner(game.board),
        is_draw=is_draw(game.board),
    )


def get_game_or_404(session: Session, game_id: str) -> Game:
    game = session.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/games", status_code=201)
def create_game(session: SessionDep) -> GameState:
    game = Game(board=[None] * BOARD_SIZE)
    session.add(game)
    session.commit()
    session.refresh(game)
    return to_game_state(game)


@app.get("/games/{game_id}")
def get_game(game_id: str, session: SessionDep) -> GameState:
    game = get_game_or_404(session, game_id)
    return to_game_state(game)


@app.post("/games/{game_id}/moves")
def make_move(game_id: str, move: MoveRequest, session: SessionDep) -> GameState:
    game = get_game_or_404(session, game_id)
    try:
        new_board = apply_move(game.board, move.position)
    except InvalidMoveError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    game.board = new_board
    session.commit()
    return to_game_state(game)
