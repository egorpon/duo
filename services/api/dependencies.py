from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from grpc import aio

from generated import auth_pb2_grpc, game_pb2_grpc
from services.api.config import settings

auth_channel = aio.insecure_channel(str(settings.auth_service_url))
auth_stub: auth_pb2_grpc.UserServiceAsyncStub = auth_pb2_grpc.UserServiceStub(
    auth_channel
)

game_channel = aio.insecure_channel(str(settings.game_service_url))
game_stub: game_pb2_grpc.GameServiceAsyncStub = game_pb2_grpc.GameServiceStub(
    game_channel
)
game_move_stub: game_pb2_grpc.GameMoveServiceAsyncStub = (
    game_pb2_grpc.GameMoveServiceStub(game_channel)
)


def get_auth_service_stub() -> auth_pb2_grpc.UserServiceStub:
    return auth_stub


def get_game_service_stub() -> game_pb2_grpc.GameServiceAsyncStub:
    return game_stub


def get_game_move_service_stub() -> game_pb2_grpc.GameMoveServiceAsyncStub:
    return game_move_stub


# stub is actually async at runtime, but type checker thins its sync
if TYPE_CHECKING:
    UserServiceDep = Annotated[
        'auth_pb2_grpc.UserServiceAsyncStub',  # pyright: ignore[reportGeneralTypeIssues]
        Depends(get_auth_service_stub),
    ]
    GameServiceDep = Annotated[
        'game_pb2_grpc.GameServiceAsyncStub',  # pyright: ignore[reportGeneralTypeIssues]
        Depends(get_game_service_stub),
    ]
    GameMoveServiceDep = Annotated[
        'game_pb2_grpc.GameMoveServiceAsyncStub',  # pyright: ignore[reportGeneralTypeIssues]
        Depends(get_game_move_service_stub),
    ]
else:
    UserServiceDep = Annotated[
        auth_pb2_grpc.UserServiceStub, Depends(get_auth_service_stub)
    ]
    GameServiceDep = Annotated[
        game_pb2_grpc.GameServiceStub, Depends(get_game_service_stub)
    ]
    GameMoveServiceDep = Annotated[
        game_pb2_grpc.GameMoveServiceStub,
        Depends(get_game_move_service_stub),
    ]
