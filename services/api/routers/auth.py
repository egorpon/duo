from fastapi import APIRouter
from grpc import aio

from api.schemas.auth import JsonWebToken, UserRegisterRequest
from generated import auth_pb2, auth_pb2_grpc

router = APIRouter()

channel = aio.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.UserServiceStub(channel)


@router.post('/register/')
async def user_register(data: UserRegisterRequest) -> JsonWebToken:
    resp = await stub.CreateUser(
        auth_pb2.CreateUserRequest(
            email=data.email,
            password=data.password.get_secret_value(),
        ),
        timeout=2,
    )
    return JsonWebToken(
        access_token=resp.access_token,
        token_type='Bearer',
        issued_at=resp.issued_at.ToDatetime().timestamp(),
        expires_at=resp.expires_at.ToDatetime().timestamp(),
    )


@router.post('/login/')
async def user_login(data: UserRegisterRequest) -> JsonWebToken:
    resp = await stub.LoginUser(
        auth_pb2.LoginUserRequest(
            email=data.email,
            password=data.password.get_secret_value(),
        ),
        timeout=2,
    )
    return JsonWebToken(
        access_token=resp.access_token,
        token_type='Bearer',
        issued_at=resp.issued_at.ToDatetime().timestamp(),
        expires_at=resp.expires_at.ToDatetime().timestamp(),
    )
