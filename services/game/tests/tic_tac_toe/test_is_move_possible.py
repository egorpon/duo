from services.game.engines.tic_tac_toe import Move, TicTacToe, TicTacToeState

P1 = 1
P2 = 2


def test_valid_move():
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
    assert engine.is_move_possible(Move(turn='x', coordinate=(0, 0))) is True


def test_wrong_player_making_turn():
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
    assert engine.is_move_possible(Move(turn='o', coordinate=(0, 0))) is False


def test_place_already_taken():
    state = TicTacToeState(
        current_player='o',
        players={'x': P1, 'o': P2},
        board=[
            [None, None, None],
            [None, 'x', None],
            [None, None, None],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_move_possible(Move(turn='o', coordinate=(1, 1))) is False


def test_already_won():
    state = TicTacToeState(
        current_player='o',
        players={'x': P1, 'o': P2},
        board=[
            ['x', 'o', None],
            [None, 'x', 'o'],
            [None, None, 'x'],
        ],
    )

    engine = TicTacToe(state=state)
    assert engine.is_move_possible(Move(turn='o', coordinate=(1, 0))) is False
