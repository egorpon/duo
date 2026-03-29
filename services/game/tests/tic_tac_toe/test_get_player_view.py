from services.game.engines.tic_tac_toe import (
    Board,
    TicTacToe,
    TicTacToeState,
)

P1 = 1
P2 = 2


def test_get_player_view():
    board: Board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]
    engine = TicTacToe(
        state=TicTacToeState(
            current_player='x',
            players={'x': P1, 'o': P2},
            board=board,
        )
    )
    view = engine.get_player_view(P1)
    assert view.is_draw is False
    assert view.winner is None
    assert view.board == board
    assert view.your_symbol == 'x'
    assert view.your_turn is True

    view = engine.get_player_view(P2)
    assert view.is_draw is False
    assert view.winner is None
    assert view.board == board
    assert view.your_symbol == 'o'
    assert view.your_turn is False
