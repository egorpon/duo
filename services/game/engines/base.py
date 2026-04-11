from abc import ABC, abstractmethod
from typing import Any, Generic, Self, TypeVar

from pydantic import BaseModel

TState = TypeVar('TState', bound=BaseModel)
TMove = TypeVar('TMove', bound=BaseModel)
TPlayerView = TypeVar('TPlayerView', bound=BaseModel)


class GameEngine(ABC, Generic[TState, TMove, TPlayerView]):
    state: TState

    def __init__(self, state: TState) -> None:
        self.state = state

    @abstractmethod
    def get_winner(self) -> int | None: ...

    @abstractmethod
    def is_draw(self) -> bool: ...

    def is_game_over(self) -> bool:
        return self.is_draw() or self.get_winner() is not None

    @abstractmethod
    def is_move_possible(self, move: TMove) -> bool: ...

    @abstractmethod
    def make_move(self, move: TMove) -> None: ...

    @abstractmethod
    def get_player_view(self, player_id: int) -> TPlayerView: ...

    @classmethod
    @abstractmethod
    def new_game(cls, p1: int, p2: int) -> Self: ...

    @classmethod
    @abstractmethod
    def load_game(cls, state: dict[str, Any]) -> Self: ...

