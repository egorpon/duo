import json
from typing import Any, override

from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode
from grpc.aio import ServicerContext

from generated import game_pb2, game_pb2_grpc
from services.game.db.crud import get_game_move_by_id, get_game_moves
from services.game.db.models import GameMove


def _game_move_to_proto(move: GameMove) -> game_pb2.GameMove:
    assert move.id is not None
    return game_pb2.GameMove(
        id=move.id,
        game_id=move.game_id,
        player_id=move.player_id,
        turn_number=move.turn_number,
        move_data=json.dumps(move.move_data),
        created_at=Timestamp().FromDatetime(move.created_at),
        updated_at=Timestamp().FromDatetime(move.updated_at),
    )


class GameMoveService(game_pb2_grpc.GameMoveServiceServicer):
    @override
    async def GetMoveById(
        self,
        request: game_pb2.GetMoveByIdRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.GameMove:
        move = await get_game_move_by_id(id=request.move_id)
        if move is None:
            await context.abort(code=StatusCode.NOT_FOUND)
        return _game_move_to_proto(move)

    @override
    async def GetMovesForGame(
        self,
        request: game_pb2.GetMovesForGameRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.ListMoveResponse:
        moves = await get_game_moves(game_id=request.game_id)
        return game_pb2.ListMoveResponse(
            moves=(_game_move_to_proto(m) for m in moves)
        )
