import asyncio
import logging
import signal

from grpc import aio

from generated import auth_pb2_grpc
from services.auth.config import settings
from services.auth.interceptors import AuthInterceptor
from services.auth.service import UserService

logger = logging.getLogger('duo.auth')

if settings.sentry_dsn:
    import os

    import sentry_sdk
    from sentry_sdk.integrations.asyncpg import AsyncPGIntegration
    from sentry_sdk.integrations.grpc import GRPCIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        send_default_pii=True,
        auto_enabling_integrations=False,
        traces_sample_rate=0,
        environment=os.getenv('SENTRY_ENVIRONMENT', 'production'),
        release=os.getenv('SENTRY_RELEASE'),
        integrations=[
            AsyncPGIntegration(),
            GRPCIntegration(),
            LoggingIntegration(),
            SqlalchemyIntegration(),
        ],
    )


async def serve() -> None:
    interceptors = (AuthInterceptor(),)
    server = aio.server(interceptors=interceptors)
    auth_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    port = server.add_insecure_port(settings.server_url)
    await server.start()
    logger.info('running server on port: %s', port)

    stop_event = asyncio.Event()

    def handle_signal():
        logger.info('Shutdown signal received')
        stop_event.set()

    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGTERM, handle_signal)
        loop.add_signal_handler(signal.SIGINT, handle_signal)
    except NotImplementedError:
        # windows does not have this function
        pass

    await stop_event.wait()

    logger.info('Shutting down gracefully')
    await server.stop(grace=5)
    logger.info('Shutdown complete')


if __name__ == '__main__':
    asyncio.run(serve())
