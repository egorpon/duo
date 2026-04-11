from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import Any, override

import grpc

from common.exceptions import ExpiredTokenError, InvalidTokenError
from common.token import decode_token
from services.game.config import settings

request_user: ContextVar[int | None] = ContextVar('request_user', default=None)


def get_user_from_token(token_raw: str) -> int | None:
    token = decode_token(
        token=token_raw,
        public_key=settings.public_key,
        algorithm=settings.jwt_algorithm,
    )
    return token.sub


def get_current_user_id() -> int | None:
    return request_user.get()


class AuthInterceptor(grpc.aio.ServerInterceptor):
    @override
    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails],
            Awaitable[grpc.RpcMethodHandler[Any, Any]],
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ):
        handler = await continuation(handler_call_details)

        metadata = dict(handler_call_details.invocation_metadata)
        token = str(metadata.get('authorization', ''))
        if not token:
            return await continuation(handler_call_details)

        try:
            user = get_user_from_token(token_raw=token)
        except (InvalidTokenError, ExpiredTokenError):
            user = None

        if handler.unary_unary is not None:

            async def new_unary_unary(
                request: Any, context: grpc.ServicerContext
            ):
                assert handler.unary_unary is not None
                with request_user.set(user):
                    return await handler.unary_unary(request, context)

            return grpc.unary_unary_rpc_method_handler(
                new_unary_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler
