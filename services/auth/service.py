from datetime import datetime
from typing import override

from grpc import ServicerContext

from auth.password import check_password
from auth.queries import get_user_by_email, user_create
from auth.token import issue_token
from generated import auth_pb2_grpc
from generated.auth_pb2 import (
    AuthResponse,
    CreateUserRequest,
    GetUserByIdRequest,
    LoginUserRequest,
    UpdateUserEmailRequest,
    UpdateUserPasswordRequest,
    User,
)


class UserService(auth_pb2_grpc.UserServiceServicer):
    @override
    async def CreateUser(
        self, request: CreateUserRequest, context: ServicerContext
    ) -> AuthResponse:
        user = await user_create(email=request.email, password=request.email)
        token = issue_token(user=user)
        return AuthResponse(
            access_token=token.access_token,
            expires_at=token.expires_at,
            issued_at=token.issued_at,
        )

    @override
    async def LoginUser(
        self, request: LoginUserRequest, context: ServicerContext
    ) -> AuthResponse:
        user = await get_user_by_email(email=request.email)
        now = datetime.now()
        if not user:
            # TODO: handle error appropriately
            return AuthResponse(
                access_token='x',
                expires_at=now,
                issued_at=now,
            )

        if not check_password(request.password, user.hashed_password):
            # TODO: handle error appropriately
            return AuthResponse(
                access_token='',
                expires_at=now,
                issued_at=now,
            )

        token = issue_token(user=user)
        return AuthResponse(
            access_token=token.access_token,
            expires_at=token.expires_at,
            issued_at=token.issued_at,
        )

    @override
    async def UpdateUserEmail(
        self, request: UpdateUserEmailRequest, context: ServicerContext
    ) -> User: ...

    @override
    async def UpdateUserPassword(
        self, request: UpdateUserPasswordRequest, context: ServicerContext
    ) -> AuthResponse: ...

    @override
    async def GetCurrentUser(
        self, request: None, context: ServicerContext
    ) -> User: ...

    @override
    async def GetUserById(
        self, request: GetUserByIdRequest, context: ServicerContext
    ) -> User: ...
