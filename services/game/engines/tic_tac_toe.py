from typing import Any, Literal

from pydantic import BaseModel, field_validator

from services.game.engines.base import GameEngine
from services.game.exceptions import InvalidMoveError

type Turn = Literal['x', 'o']
type Board = list[list[Turn | None]]

type Coordinate = tuple[int, int]
type Row = tuple[Coordinate, Coordinate, Coordinate]

BOARD_SIZE = 3

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


def make_board() -> Board:
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


class Move(BaseModel):
    turn: Turn
    coordinate: Coordinate


class TicTacToeState(BaseModel):
    current_player: Turn
    players: dict[Turn, int]
    board: Board

    @field_validator('board')
    @classmethod
    def validate_board(cls, board: Board) -> Board:
        if len(board) != BOARD_SIZE:
            raise ValueError(f'Invalid board size: {len(board)}')

        for row in board:
            if len(row) != BOARD_SIZE:
                raise ValueError(f'Invalid board size: {len(row)}')
            for cell in row:
                if cell not in ('x', 'o', None):
                    raise ValueError(f'Invalid cell value: {cell}')
        return board


class TicTacToePlayerView(BaseModel):
    board: Board
    your_turn: bool
    your_symbol: Turn
    winner: int | None
    is_draw: bool


class TicTacToe(GameEngine[TicTacToeState, Move, TicTacToePlayerView]):
    """
    Main class to handle all actions related to the Tic Tac Toe game
    P1 plays with 'x'
    P2 plays with 'o'
    """

    @classmethod
    def new_game(cls, p1: int, p2: int):
        return cls(
            state=TicTacToeState(
                current_player='x',
                players={'x': p1, 'o': p2},
                board=make_board(),
            )
        )

    @classmethod
    def load_game(cls, state: dict[str, Any]):
        return cls(state=TicTacToeState.model_validate(state))

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
        path = self._get_win_path()
        if not path:
            return None

        symbol: Turn | None = self.state.board[path[0][0]][path[0][1]]
        assert symbol is not None  # guaranteed by self._get_win_path
        return self.state.players[symbol]

    def is_draw(self) -> bool:
        if self.get_winner() is not None:
            return False

        for row in self.state.board:
            for value in row:
                if value is None:
                    return False
        return True

    def is_move_possible(self, move: Move) -> bool:
        if self.is_game_over():
            return False

        if self.state.current_player != move.turn:
            return False

        return self.state.board[move.coordinate[0]][move.coordinate[1]] is None

    def make_move(self, move: Move) -> None:
        if not self.is_move_possible(move):
            raise InvalidMoveError('Move is invalid')

        self.state.board[move.coordinate[0]][move.coordinate[1]] = move.turn
        next_player: dict[Turn, Turn] = {'x': 'o', 'o': 'x'}
        self.state.current_player = next_player[move.turn]

    def get_player_view(self, player_id: int) -> TicTacToePlayerView:
        symbol: Turn = next(
            turn for turn, pid in self.state.players.items() if pid == player_id
        )
        return TicTacToePlayerView(
            board=self.state.board,
            your_symbol=symbol,
            your_turn=self.state.current_player == symbol,
            winner=self.get_winner(),
            is_draw=self.is_draw(),
        )
