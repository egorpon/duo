from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from services.game.db.models import Game, GameMove


async def get_game_by_id(
    session: AsyncSession | None = None,
    *,
    id: int,
) -> Game | None:
    pass


async def game_create(  # noqa: PLR0913
    session: AsyncSession | None = None,
    *,
    type: Game.Type = Game.Type.TIC_TAC_TOE,
    result: Game.Result = Game.Result.TBD,
    status: Game.Status = Game.Status.IN_QUEUE,
    player1: int,
    player2: int | None = None,
    current_player: int | None = None,
    turn_number: int = 0,
    state: dict[str, Any] | None = None,
) -> Game: ...


async def game_update(
    session: AsyncSession | None = None,
    *,
    game: Game,
    **fields: Any,
) -> Game: ...


async def get_game_move_by_id(
    session: AsyncSession | None = None,
    *,
    id: int,
) -> GameMove | None: ...


async def get_game_moves(
    session: AsyncSession | None = None,
    *,
    game_id: int,
) -> list[GameMove]: ...


async def game_move_create(
    session: AsyncSession | None = None,
    *,
    game_id: int,
    player_id: int,
    turn_number: int,
    move_data: dict[str, Any] | None = None,
) -> GameMove: ...
