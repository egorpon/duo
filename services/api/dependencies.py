from typing import Annotated

from fastapi import Depends
from grpc import aio

from api.config import settings
from generated import auth_pb2_grpc

url = str(settings.auth_service_url)
channel = aio.insecure_channel(str(settings.auth_service_url))
stub = auth_pb2_grpc.UserServiceStub(channel)


def get_user_service_stub():
    return stub


UserServiceDep = Annotated[
    auth_pb2_grpc.UserServiceStub, Depends(get_user_service_stub)
]
