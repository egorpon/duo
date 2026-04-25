from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from grpc import StatusCode, aio

from generated import auth_pb2
from services.api.dependencies import UserServiceDep
from services.api.schemas.auth import (
    JsonWebToken,
    UserLoginRequest,
    UserRegisterRequest,
)

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
        if exc.code() == StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='User already exists',
            )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Failed to register. Try again later',
        )


@router.post('/login/')
async def user_login(
    data: UserLoginRequest,
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
        if exc.code() == StatusCode.UNAUTHENTICATED:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid email or password',
            )

        if exc.code() == StatusCode.INVALID_ARGUMENT:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Invalid email or password',
            )

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Internal error',
        )
