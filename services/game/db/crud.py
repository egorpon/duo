from collections.abc import Sequence
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from common.game import Result, Status, Type
from common.models import model_update
from services.game.db.engine import get_session_ctx
from services.game.db.models import Game, GameMove


async def get_game_by_id(
    session: AsyncSession | None = None,
    *,
    id: int,
) -> Game | None:
    async with get_session_ctx(session=session) as s:
        query = select(Game).where(Game.id == id)
        return (await s.exec(query)).first()


async def game_create(  # noqa: PLR0913
    session: AsyncSession | None = None,
    *,
    type: Type = Type.TIC_TAC_TOE,
    result: Result = Result.TBD,
    status: Status = Status.IN_QUEUE,
    player1: int,
    player2: int | None = None,
    current_player: int | None = None,
    turn_number: int = 0,
    state: dict[str, Any] | None = None,
) -> Game:
    if state is None:
        state = dict()
    async with get_session_ctx(session) as s:
        game = Game(
            type=type,
            result=result,
            status=status,
            player1=player1,
            player2=player2,
            current_player=current_player,
            turn_number=turn_number,
            state=state,
        )
        s.add(game)
        await s.commit()
        await s.refresh(game)
        return game


async def game_update(
    session: AsyncSession | None = None,
    *,
    game: Game,
    **fields: Any,
) -> Game:
    game, updates = model_update(model=game, **fields)
    if not updates:
        return game

    async with get_session_ctx(session) as s:
        s.add(Game)
        await s.commit()
        await s.refresh(game)
        return game


async def get_game_move_by_id(
    session: AsyncSession | None = None,
    *,
    id: int,
) -> GameMove | None:
    async with get_session_ctx(session=session) as s:
        query = select(GameMove).where(GameMove.id == id)
        return (await s.exec(query)).first()


async def get_game_moves(
    session: AsyncSession | None = None,
    *,
    game_id: int,
) -> Sequence[GameMove]:
    async with get_session_ctx(session=session) as s:
        query = select(GameMove).where(GameMove.game_id == game_id)
        return (await s.exec(query)).all()


async def game_move_create(
    session: AsyncSession | None = None,
    *,
    game_id: int,
    player_id: int,
    turn_number: int,
    move_data: dict[str, Any] | None = None,
) -> GameMove:
    if move_data is None:
        move_data = dict()
    async with get_session_ctx(session) as s:
        move = GameMove(
            game_id=game_id,
            player_id=player_id,
            turn_number=turn_number,
            move_data=move_data,
        )
        s.add(move)
        await s.commit()
        await s.refresh(move)
        return move
