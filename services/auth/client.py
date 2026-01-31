from typing import override

from generated import auth_pb2, auth_pb2_grpc


class UserService(auth_pb2_grpc.UserServiceServicer):
    @override
    def UserCreate(self, request, context):
        print('UserCreate', request, context)
        return auth_pb2.JWT(
            access_token='TokenCreate',
            token_type='Bearer',
            issued_at=1.1,
            expired_at=1.1,
        )

    @override
    def UserLogin(self, request, context):
        return auth_pb2.JWT(
            access_token='TokenLogin',
            token_type='Bearer',
            issued_at=1.1,
            expired_at=1.1,
        )

    @override
    def GetUserData(self, request, context):
        return auth_pb2.UserDisplay(
            id=1,
            email='test@example.com',
            name='nickname',
        )
