from common.exceptions import CommonError


class GameError(CommonError):
    """Base error for Game service"""


class InvalidMoveError(CommonError):
    """Raised when move is impossible to make"""
