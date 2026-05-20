from services.game.engines.tic_tac_toe import TicTacToe, TicTacToeState

P1 = 1
P2 = 2


def test_empty_board():
    state = TicTacToeState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_draw() is False


def test_won_game():
    state = TicTacToeState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            ['x', 'o', 'x'],
            ['x', 'o', 'o'],
            ['x', 'o', 'x'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_draw() is False


def test_actual_draw():
    state = TicTacToeState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            ['x', 'o', 'x'],
            ['o', 'x', 'x'],
            ['o', 'x', 'o'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_draw() is True
