from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.protobuf.empty_pb2 import Empty
from grpc import aio

from api.schemas.auth import JsonWebToken, UserDisplay, UserRegisterRequest
from generated import auth_pb2, auth_pb2_grpc

router = APIRouter()

channel = aio.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.UserServiceStub(channel)


security = HTTPBearer()

Credentials = Annotated[HTTPAuthorizationCredentials, Depends(security)]


@router.post('/register/')
async def user_register(data: UserRegisterRequest) -> JsonWebToken:
    try:
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
    except aio.AioRpcError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=exc.details()
        )


@router.post('/login/')
async def user_login(data: UserRegisterRequest) -> JsonWebToken:
    try:
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
    except aio.AioRpcError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=exc.details()
        )


@router.get('/user/{user_id}/')
async def user_detail(user_id: int, credentials: Credentials) -> UserDisplay:
    try:
        resp = await stub.GetUserById(
            auth_pb2.GetUserByIdRequest(
                id=user_id,
            ),
            timeout=2,
            metadata=(('authorization', credentials.credentials),),
        )
        return UserDisplay(
            id=resp.id,
            email=resp.email,
            created_at=resp.created_at.ToDatetime().timestamp(),
            updated_at=resp.updated_at.ToDatetime().timestamp(),
        )
    except aio.AioRpcError as exc:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=exc.details()
        )


@router.get('user/me/')
async def user_me(credentials: Credentials) -> UserDisplay:
    try:
        resp = await stub.GetCurrentUser(
            Empty(),
            timeout=2,
            metadata=(('authorization', credentials.credentials),),
        )
        return UserDisplay(
            id=resp.id,
            email=resp.email,
            created_at=resp.created_at.ToDatetime().timestamp(),
            updated_at=resp.updated_at.ToDatetime().timestamp(),
        )
    except aio.AioRpcError as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=exc.details()
        )
