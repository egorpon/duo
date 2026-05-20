from services.game.engines.tic_tac_toe import Move, TicTacToe, TicTacToeState

P1 = 1
P2 = 2


def test_full_game_until_winner():
    engine = TicTacToe(
        state=TicTacToeState(
            current_player='x',
            players={'x': P1, 'o': P2},
            board=[
                [None, None, None],
                [None, None, None],
                [None, None, None],
            ],
        )
    )
    assert engine.get_winner() is None
    engine.make_move(Move(coordinate=(1, 1)))
    assert engine.state.current_player == 'o'
    engine.make_move(Move(coordinate=(1, 0)))
    engine.make_move(Move(coordinate=(0, 0)))
    engine.make_move(Move(coordinate=(1, 2)))
    engine.make_move(Move(coordinate=(2, 2)))
    assert engine.get_winner() == P1
