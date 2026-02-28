from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import Any, override

import grpc

from auth.exceptions import ExpiredTokenError, InvalidTokenError
from auth.models import User
from auth.queries import get_user_from_token

request_user: ContextVar[User | None] = ContextVar('request_user', default=None)


def get_current_user() -> User | None:
    return request_user.get()


class AuthInterceptor(grpc.aio.ServerInterceptor):  # type: ignore[misc]
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
            user = await get_user_from_token(token=token)
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
