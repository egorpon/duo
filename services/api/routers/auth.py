import grpc
from fastapi import APIRouter

from api.schemas.auth import JsonWebToken, UserRegisterRequest
from generated import auth_pb2, auth_pb2_grpc

router = APIRouter()

channel = grpc.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.UserServiceStub(channel)


@router.post('/register/')
async def user_register(data: UserRegisterRequest) -> JsonWebToken:
    resp = stub.UserCreate(
        auth_pb2.UserCreateRequest(
            email='email@email.com', password='strongpassword'
        )
    )
    print('response:', resp)
    return JsonWebToken(
        access_token='token' + data.email,
        token_type='Bearer',
        issued_at=123.1,
        expired_at=12.1,
    )


@router.post('/login/')
async def user_login(data: UserRegisterRequest) -> JsonWebToken:
    return JsonWebToken(
        access_token='token' + data.email,
        token_type='Bearer',
        issued_at=123.1,
        expired_at=12.1,
    )
