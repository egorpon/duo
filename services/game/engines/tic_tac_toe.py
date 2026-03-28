from typing import Any, Literal

from pydantic import BaseModel

type Turn = Literal['x', 'o']
type Board = list[list[Turn | None]]

type Coordinate = tuple[int, int]
type Row = tuple[Coordinate, Coordinate, Coordinate]

class Move(BaseModel):
    turn: Turn
    coordinate: Coordinate


BOARD_SIZE = 3


class GameState(BaseModel):
    current_player: Turn
    players: dict[Turn, int]
    board: Board

    def model_post_init(self, context: Any, /) -> None:
        if len(self.board) != BOARD_SIZE:
            raise ValueError(f'Invalid board size: {len(self.board)}')

        for row in self.board:
            if len(row) != BOARD_SIZE:
                raise ValueError(f'Invalid board size: {len(row)}')


WINNING_COORDS: list[Row] = [
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
]


class TicTacToe:
    """Main class to handle all actions related to the Tic Tac Toe game"""

    state: GameState

    def __init__(self, state: GameState) -> None:
        self.state = state

    @staticmethod
    def _check_win(board: Board, coords: Row) -> bool:
        return (
            board[coords[0][0]][coords[0][1]]
            == board[coords[1][0]][coords[1][1]]
            == board[coords[2][0]][coords[2][1]]
            and board[coords[0][0]][coords[0][1]] is not None
        )

    def _get_win_path(self) -> Row | None:
        for coords in WINNING_COORDS:
            if self._check_win(board=self.state.board, coords=coords):
                return coords

        return None

    def get_winner(self) -> int | None:
        """P1 plays with 'x'
        P2 plays with 'o'
        """
        path = self._get_win_path()
        if not path:
            return None

        symbol: Turn | None = self.state.board[path[0][0]][path[0][1]]
        assert symbol is not None
        return self.state.players[symbol]

    def is_move_possible(self, move: Move) -> bool:
        if self.state.current_player != move.turn:
            return False

        return self.state.board[move.coordinate[0]][move.coordinate[1]] is None

    def make_move(self) -> None:
        pass
