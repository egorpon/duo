from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

TState = TypeVar('TState', bound=BaseModel)
TMove = TypeVar('TMove', bound=BaseModel)
TPlayerView = TypeVar('TPlayerView', bound=BaseModel)


class GameEngine(ABC, Generic[TState, TMove, TPlayerView]):
    state: TState

    def __init__(self, state: TState) -> None:
        self.state = state

    @abstractmethod
    def make_move(self, move: TMove) -> None: ...

    @abstractmethod
    def is_move_possible(self, move: TMove) -> bool: ...

    @abstractmethod
    def get_winner(self) -> int | None: ...

    @abstractmethod
    def is_draw(self) -> bool: ...

    @abstractmethod
    def is_game_over(self) -> bool: ...

    @abstractmethod
    def get_player_view(self, player_id: int) -> TPlayerView: ...
