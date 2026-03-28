from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from grpc import aio

from generated import auth_pb2_grpc
from services.api.config import settings

channel = aio.insecure_channel(str(settings.auth_service_url))
stub: auth_pb2_grpc.UserServiceAsyncStub = auth_pb2_grpc.UserServiceStub(
    channel
)


def get_user_service_stub() -> auth_pb2_grpc.UserServiceStub:
    return stub


# stub is actually async at runtime, but type checker thins its sync
if TYPE_CHECKING:
    UserServiceDep = Annotated[
        'auth_pb2_grpc.UserServiceAsyncStub',  # pyright: ignore[reportGeneralTypeIssues]
        Depends(get_user_service_stub),
    ]
else:
    UserServiceDep = Annotated[
        auth_pb2_grpc.UserServiceStub, Depends(get_user_service_stub)
    ]
