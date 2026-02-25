from typing import Any, override

from grpc.aio import ServicerContext, StatusCode

from auth.exceptions import EmailAlreadyUsedError
from auth.password import check_password
from auth.queries import get_user_by_email, get_user_by_id, user_create
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
        self,
        request: CreateUserRequest,
        context: ServicerContext[Any, Any],
    ) -> AuthResponse:
        try:
            user = await user_create(
                email=request.email, password=request.email
            )
        except EmailAlreadyUsedError:
            await context.abort(
                code=StatusCode.ALREADY_EXISTS, details='Email already used'
            )

        token = issue_token(user=user)
        return AuthResponse(
            access_token=token.access_token,
            expires_at=token.expires_at,
            issued_at=token.issued_at,
        )

    @override
    async def LoginUser(
        self, request: LoginUserRequest, context: ServicerContext[Any, Any]
    ) -> AuthResponse:
        user = await get_user_by_email(email=request.email)
        if user is None:
            await context.abort(
                code=StatusCode.NOT_FOUND,
                details='User not found',
            )

        if not check_password(request.password, user.hashed_password):
            await context.abort(  
                code=StatusCode.INVALID_ARGUMENT,
                details='Invalid password',
            )

        token = issue_token(user=user)
        return AuthResponse(
            access_token=token.access_token,
            expires_at=token.expires_at,
            issued_at=token.issued_at,
        )

    @override
    async def UpdateUserEmail(
        self,
        request: UpdateUserEmailRequest,
        context: ServicerContext[Any, Any],
    ) -> User: ...

    @override
    async def UpdateUserPassword(
        self,
        request: UpdateUserPasswordRequest,
        context: ServicerContext[Any, Any],
    ) -> AuthResponse: ...

    @override
    async def GetCurrentUser(
        self, request: None, context: ServicerContext[Any, Any]
    ) -> User: ...

    @override
    async def GetUserById(
        self, request: GetUserByIdRequest, context: ServicerContext[Any, Any]
    ) -> User:
        user = await get_user_by_id(id=request.id)
        if user is None:
            await context.abort(  
                code=StatusCode.NOT_FOUND,
                details='User not found',
            )

        return User(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
