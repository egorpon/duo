from fastapi import APIRouter
from grpc import aio

from api.schemas.auth import JsonWebToken, UserRegisterRequest
from generated import auth_pb2, auth_pb2_grpc

router = APIRouter()

channel = aio.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.UserServiceStub(channel)


@router.post('/register/')
async def user_register(data: UserRegisterRequest) -> JsonWebToken:
    resp = await stub.UserCreate(
        auth_pb2.UserCreateRequest(
            email=data.email, password=data.password.get_secret_value()
        ),
        timeout=2,
    )
    return JsonWebToken(
        access_token=resp.access_token,
        token_type=resp.token_type,
        issued_at=resp.issued_at,
        expired_at=resp.expired_at,
    )


@router.post('/login/')
async def user_login(data: UserRegisterRequest) -> JsonWebToken:
    return JsonWebToken(
        access_token='token' + data.email,
        token_type='Bearer',
        issued_at=123.1,
        expired_at=12.1,
    )
