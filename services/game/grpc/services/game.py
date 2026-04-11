from typing import Any, override

from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode
from grpc.aio import ServicerContext

from generated import game_pb2, game_pb2_grpc
from services.game.db.crud import game_create
from services.game.db.models import Game
from services.game.grpc.interceptors import get_current_user_id

_TYPE_MAP: dict[Game.Type, game_pb2.GameType.ValueType] = {
    Game.Type.TIC_TAC_TOE: game_pb2.TIC_TAC_TOE,
}

_RESULT_MAP: dict[Game.Result, game_pb2.GameResult.ValueType] = {
    Game.Result.TBD: game_pb2.TBD,
    Game.Result.DRAW: game_pb2.DRAW,
    Game.Result.P1_WON: game_pb2.P1_WON,
    Game.Result.P2_WON: game_pb2.P2_WON,
}

_STATUS_MAP: dict[Game.Status, game_pb2.GameStatus.ValueType] = {
    Game.Status.IN_QUEUE: game_pb2.IN_QUEUE,
    Game.Status.IN_PROGRESS: game_pb2.IN_PROGRESS,
    Game.Status.ABANDONED: game_pb2.ABANDONED,
    Game.Status.FINISHED: game_pb2.FINISHED,
}


class GameService(game_pb2_grpc.GameServiceServicer):
    @override
    async def CreateGame(
        self,
        request: game_pb2.CreateGameRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.Game:
        user_id = get_current_user_id()
        if user_id is None:
            await context.abort(code=StatusCode.UNAUTHENTICATED)

        game = await game_create(
            type=Game.Type(request.type),
            player1=user_id,
            current_player=user_id,
            turn_number=1,
        )
        assert game.id is not None
        return game_pb2.Game(
            id=game.id,
            type=_TYPE_MAP[game.type],
            result=_RESULT_MAP[game.result],
            status=_STATUS_MAP[game.status],
            player1=game.player1,
            player2=game.player2,
            current_player=game.current_player,
            turn_number=game.turn_number,
            created_at=Timestamp().FromDatetime(game.created_at),
            updated_at=Timestamp().FromDatetime(game.updated_at),
        )

    @override
    async def JoinGame(
        self,
        request: game_pb2.JoinGameRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.JoinGameResponse: ...

    @override
    async def MakeGameAbandoned(
        self,
        request: game_pb2.MakeGameAbandonedRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.Game: ...

    @override
    async def GetGameById(
        self,
        request: game_pb2.GetGameByIdRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.Game: ...

    @override
    async def MakeMove(
        self,
        request: game_pb2.MakeMoveRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.MakeMoveResponse: ...

    @override
    async def GetPlayerView(
        self,
        request: game_pb2.GetPlayerViewRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.GamePlayerView: ...
