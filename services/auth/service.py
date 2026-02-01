from typing import override

from grpc import ServicerContext

from generated import auth_pb2_grpc
from generated.auth_pb2 import (
    JWT,
    UserCreateRequest,
    UserDisplay,
    UserLoginRequest,
)


class UserService(auth_pb2_grpc.UserServiceServicer):
    @override
    async def UserCreate(
        self, request: UserCreateRequest, context: ServicerContext
    ) -> JWT:
        print('UserCreate', request, context)
        return JWT(
            access_token='TokenCreate',
            token_type='Bearer',
            issued_at=1.1,
            expired_at=1.1,
        )

    @override
    async def UserLogin(
        self, request: UserLoginRequest, context: ServicerContext
    ) -> JWT:
        return JWT(
            access_token='TokenLogin',
            token_type='Bearer',
            issued_at=1.1,
            expired_at=1.1,
        )

    @override
    async def GetUserData(
        self, request: JWT, context: ServicerContext
    ) -> UserDisplay:
        return UserDisplay(
            id=1,
            email='test@example.com',
            name='nickname',
        )
