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
