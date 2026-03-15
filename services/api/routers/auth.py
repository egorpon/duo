from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from grpc import StatusCode, aio

from api.dependencies import UserServiceDep
from api.schemas.auth import (
    JsonWebToken,
    UserRegisterRequest,
)
from generated import auth_pb2

router = APIRouter(tags=['auth'])


@router.post('/register/')
async def user_register(
    data: UserRegisterRequest,
    stub: UserServiceDep,
) -> JsonWebToken:
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
        if exc.code == StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='User already exists',
            )
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Failed to register. Try again later',
        )


@router.post('/login/')
async def user_login(
    data: UserRegisterRequest,
    stub: UserServiceDep,
) -> JsonWebToken:
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
        if exc.code == StatusCode.INTERNAL:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Internal error',
            )

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Invalid email or password',
        )
