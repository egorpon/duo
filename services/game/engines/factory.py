from typing import Any

from common.game import Type
from services.game.db.models import Game
from services.game.engines.base import GameEngine
from services.game.engines.tic_tac_toe import TicTacToe
from services.game.exceptions import UnsupportedGameTypeError


def get_game_engine(game: Game) -> type[GameEngine[Any, Any, Any]]:
    if game.type == Type.TIC_TAC_TOE:
        return TicTacToe

    raise UnsupportedGameTypeError(f'Not found game engine for {game.type}')
