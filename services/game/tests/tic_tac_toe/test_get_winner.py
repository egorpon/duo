from services.game.engines.tic_tac_toe import GameState, TicTacToe

P1 = 1
P2 = 2


def test_empty_board():
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
    assert engine.get_winner() is None


def test_winner_is_p1():
    state = GameState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            ['x', None, 'o'],
            [None, 'x', 'o'],
            [None, None, 'x'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.get_winner() == P1


def test_winner_is_p2():
    state = GameState(
        current_player='x',
        players={'x': P1, 'o': P2},
        board=[
            ['o', 'o', 'o'],
            ['x', 'x', 'o'],
            [None, 'x', 'x'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.get_winner() == P2
