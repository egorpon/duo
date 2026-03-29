import pytest

from services.game.engines.tic_tac_toe import GameState, Move, TicTacToe
from services.game.exceptions import InvalidMoveError

P1 = 1
P2 = 2


def test_making_move_updates_state():
    state = GameState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    engine.make_move(Move(turn='x', coordinate=(0, 0)))
    assert state.current_player == 'o'
    assert state.board[0][0] == 'x'


def test_invalid_move_does_not_change_state():
    state = GameState(
        current_player='o',
        players={'x': P1, 'o': P2},
        board=[
            ['x', None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    with pytest.raises(InvalidMoveError):
        engine.make_move(Move(turn='o', coordinate=(0, 0)))

    assert state.current_player == 'o'
    assert state.board[0][0] == 'x'


def test_multiple_moves():
    state = GameState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    engine.make_move(Move(turn='x', coordinate=(0, 0)))
    engine.make_move(Move(turn='o', coordinate=(1, 1)))
    engine.make_move(Move(turn='x', coordinate=(2, 2)))
    engine.make_move(Move(turn='o', coordinate=(1, 0)))

    assert state.current_player == 'x'
    assert state.board[0][0] == 'x'
    assert state.board[1][1] == 'o'
    assert state.board[2][2] == 'x'
    assert state.board[1][0] == 'o'
