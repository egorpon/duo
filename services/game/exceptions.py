from common.exceptions import CommonError


class GameError(CommonError):
    """Base error for Game service"""


class InvalidMoveError(GameError):
    """Raised when move is impossible to make"""


class UnsupportedGameTypeError(GameError):
    """No engines for that type of game"""
