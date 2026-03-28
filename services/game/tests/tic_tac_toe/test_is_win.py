from services.game.engines.tic_tac_toe import GameState, TicTacToe


def test_empty_board():
    state = GameState(
        current_player=1,
        player1=1,
        player2=2,
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_win() is False

def test_win_by_diagonal():
    state = GameState(
        current_player=1,
        player1=1,
        player2=2,
        board=[
            ['x', None, 'o'],
            [None, 'x', 'o'],
            [None, None, 'x'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_win() is True
