import pytest
from pydantic_core import ValidationError

from services.game.engines.tic_tac_toe import GameState


def test_valid_size():
    GameState(
        current_player=1,
        player1=1,
        player2=2,
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

def test_too_many_rows():
    with pytest.raises(ValidationError):
        GameState(
            current_player=1,
            player1=1,
            player2=2,
            board=[
                [None, None, None],
                [None, None, None],
                [None, None, None],
                [],
            ],
        )

def test_too_many_columns():
    with pytest.raises(ValidationError):
        GameState(
            current_player=1,
            player1=1,
            player2=2,
            board=[
                [None, None, None, None],
                [None, None, None],
                [None, None, None],
            ],
        )
