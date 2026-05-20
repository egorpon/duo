import pytest
from pydantic_core import ValidationError

from services.game.engines.tic_tac_toe import TicTacToeState

P1 = 1
P2 = 2


def test_valid_size():
    TicTacToeState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )


def test_too_many_rows():
    with pytest.raises(ValidationError):
        TicTacToeState(
            current_player='x',
            players={'x': P1, 'o': P2},
            board=[
                [None, None, None],
                [None, None, None],
                [None, None, None],
                [],
            ],
        )


def test_too_many_columns():
    with pytest.raises(ValidationError):
        TicTacToeState(
            current_player='x',
            players={'x': P1, 'o': P2},
            board=[
                [None, None, None, None],
                [None, None, None],
                [None, None, None],
            ],
        )
