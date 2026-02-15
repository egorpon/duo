from typing import override

from grpc import ServicerContext

from auth.main import user_create
from auth.token import issue_token
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
        user = await user_create(email=request.email, password=request.password)
        token = issue_token(user)
        return JWT(
            access_token=token.access_token,
            token_type=token.token_type,
            issued_at=token.issued_at,
            expired_at=token.expired_at,
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
