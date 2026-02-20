from typing import override

from grpc import ServicerContext

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
    def CreateUser(
        self, request: CreateUserRequest, context: ServicerContext
    ) -> AuthResponse: ...

    @override
    def LoginUser(
        self, request: LoginUserRequest, context: ServicerContext
    ) -> AuthResponse: ...

    @override
    def UpdateUserEmail(
        self, request: UpdateUserEmailRequest, context: ServicerContext
    ) -> User: ...

    @override
    def UpdateUserPassword(
        self, request: UpdateUserPasswordRequest, context: ServicerContext
    ) -> AuthResponse: ...

    @override
    def GetCurrentUser(
        self, request: None, context: ServicerContext
    ) -> User: ...

    @override
    def GetUserById(
        self, request: GetUserByIdRequest, context: ServicerContext
    ) -> User: ...
