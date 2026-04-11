from typing import Any, override

from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode
from grpc.aio import ServicerContext

from generated import game_pb2, game_pb2_grpc
from services.game.db.crud import game_create, game_update, get_game_by_id
from services.game.db.models import Game
from services.game.engines.factory import get_game_engine
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


def game_to_proto(game: Game) -> game_pb2.Game:
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
        return game_to_proto(game)

    @override
    async def JoinGame(
        self,
        request: game_pb2.JoinGameRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.JoinGameResponse:
        # initialize game state for 2 new players
        game = await get_game_by_id(id=request.game_id)
        if game is None:
            await context.abort(
                code=StatusCode.NOT_FOUND,
                details=f'Not found game with id {request.game_id}',
            )

        assert game.player2 is not None
        engine = get_game_engine(game=game).new_game(
            p1=game.player1, p2=request.player_id
        )
        game = await game_update(
            game=game,
            player2=request.player_id,
            status=Game.Status.IN_PROGRESS,
            state=engine.state.model_dump(),
        )

        assert game.player2 is not None
        return game_pb2.JoinGameResponse(
            game=game_to_proto(game),
            player1_view=engine.get_player_view(game.player1),
            player2_view=engine.get_player_view(game.player2),
        )

    @override
    async def MakeGameAbandoned(
        self,
        request: game_pb2.MakeGameAbandonedRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.Game:
        game = await get_game_by_id(id=request.game_id)
        if game is None:
            await context.abort(code=StatusCode.NOT_FOUND)

        game = await game_update(game=game, status=Game.Status.ABANDONED)
        return game_to_proto(game=game)

    @override
    async def GetGameById(
        self,
        request: game_pb2.GetGameByIdRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.Game:
        game = await get_game_by_id(id=request.game_id)
        if game is None:
            await context.abort(code=StatusCode.NOT_FOUND)
        return game_to_proto(game=game)

    @override
    async def MakeMove(
        self,
        request: game_pb2.MakeMoveRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.MakeMoveResponse:
        game = await get_game_by_id(id=request.game_id)
        if game is None:
            await context.abort(code=StatusCode.NOT_FOUND)

        if game.status != Game.Status.IN_PROGRESS:
            await context.abort(code=StatusCode.FAILED_PRECONDITION)

        if request.player_id != game.current_player:
            await context.abort(code=StatusCode.INVALID_ARGUMENT)

        engine_class = get_game_engine(game)
        move = engine_class.load_move(request.move_data)
        engine = engine_class.load_game(game.state)

        if not engine.is_move_possible(move):
            await context.abort(code=StatusCode.INVALID_ARGUMENT)

        engine.make_move(move=move)
        winner = engine.get_winner()
        is_draw = engine.is_draw()
        status = game.status
        result = game.result

        if is_draw:
            result = Game.Result.DRAW
            status = Game.Status.FINISHED

        if winner:
            status = Game.Status.FINISHED
            if winner == game.player1:
                result = Game.Result.P1_WON
            else:
                result = Game.Result.P1_WON

        await game_update(
            game=game,
            state=engine.state.model_dump(),
            current_player=engine.get_current_player(),
            status=status,
            result=result,
            turn_number=game.turn_number + 1,
        )

        assert game.player2 is not None
        return game_pb2.MakeMoveResponse(
            game=game_to_proto(game),
            player1_view=engine.get_player_view(game.player1),
            player2_view=engine.get_player_view(game.player2),
        )

    @override
    async def GetPlayerView(
        self,
        request: game_pb2.GetPlayerViewRequest,
        context: ServicerContext[Any, Any],
    ) -> game_pb2.GamePlayerView: ...
