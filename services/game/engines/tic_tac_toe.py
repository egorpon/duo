from typing import Any, Literal

from pydantic import BaseModel, ValidationError

type Turn = Literal['x', 'o']


BOARD_LEN = 3


class GameState(BaseModel):
    current_player: int
    player1: int
    player2: int
    board: list[list[Turn | None]]

    def model_post_init(self, context: Any, /) -> None:
        if len(self.board) != BOARD_LEN:
            raise ValidationError(f'Invalid board length: {len(self.board)}')

        for row in self.board:
            if len(row) != BOARD_LEN:
                raise ValidationError(f'Invalid board length: {len(row)}')


class TicTacToe:
    """Main class to handle all actions related to the Tic Tac Toe game"""

    state: GameState

    def __init__(self, state: GameState) -> None:
        self.state = state

    def is_win(self) -> bool:
        """Checks if game is won or not"""

        b = self.state.board
        return any(
            [
                b[0][0] == b[0][1] == b[0][2] and b[0][0] is not None,
                b[1][0] == b[1][1] == b[1][2] and b[1][0] is not None,
                b[2][0] == b[2][1] == b[2][2] and b[2][0] is not None,
                b[0][0] == b[1][0] == b[2][0] and b[0][0] is not None,
                b[0][1] == b[1][1] == b[2][1] and b[0][1] is not None,
                b[0][2] == b[1][2] == b[2][2] and b[0][2] is not None,
                b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None,
                b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None,
            ]
        )

    def get_winner(self) -> int | None:
        return None
