from datetime import datetime
from enum import Enum
from typing import Any

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class TimeStampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Game(TimeStampedModel, table=True):
    class Type(str, Enum):
        TIC_TAC_TOE = 'tic_tac_toe'

    class Result(str, Enum):
        TBD = 'tbd'
        DRAW = 'draw'
        P1_WON = 'p1_won'
        P2_WON = 'p2_won'

    class Status(str, Enum):
        IN_QUEUE = 'in_queue'
        IN_PROGRESS = 'in_progress'
        ABANDONED = 'abandoned'
        FINISHED = 'finished'

    id: int | None = Field(default=None, primary_key=True, index=True)

    type: Type = Field(default=Type.TIC_TAC_TOE, max_length=16)
    result: Result = Field(default=Result.TBD, max_length=6)
    status: Status = Field(default=Status.IN_QUEUE, max_length=16)

    player1: int = Field(index=True, gt=0)
    player2: int = Field(index=True, gt=0)
    current_player: int = Field(
        description='ID of a player that should perform a move'
    )

    turn_number: int = Field(default=0)
    state: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    moves: list[GameMove] = Relationship(back_populates='game')


class GameMove(TimeStampedModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)

    game_id: int = Field(foreign_key='game.id', nullable=False)

    player_id: int = Field(gt=0)
    turn_number: int = Field(gt=0)

    move_data: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON)
    )

    game: Game = Relationship(back_populates='moves')
