from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Request

from generated import auth_pb2_grpc, game_pb2_grpc


def get_auth_service_stub(request: Request) -> auth_pb2_grpc.UserServiceStub:
    return auth_pb2_grpc.UserServiceStub(request.state.auth_channel)


def get_game_service_stub(request: Request) -> game_pb2_grpc.GameServiceStub:
    return game_pb2_grpc.GameServiceStub(request.state.game_channel)


def get_game_move_service_stub(
    request: Request,
) -> game_pb2_grpc.GameMoveServiceStub:
    return game_pb2_grpc.GameMoveServiceStub(request.state.game_channel)


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
