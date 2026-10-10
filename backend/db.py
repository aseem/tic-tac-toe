import os
import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, SQLModel, create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///games.db")

# SQLite needs this setting to work with FastAPI's threads; other databases reject it.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)


class Game(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    board: list[str | None] = Field(sa_column=Column(JSON, nullable=False))


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
