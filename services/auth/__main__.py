import asyncio
import logging
import signal

from grpc import aio

from auth.interceptors import AuthInterceptor
from auth.service import UserService
from generated import auth_pb2_grpc

logger = logging.getLogger('duo.auth')


async def serve() -> None:
    interceptors = (AuthInterceptor(),)
    server = aio.server(interceptors=interceptors)
    auth_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    port = server.add_insecure_port('localhost:50051')
    await server.start()
    logger.info('running server on port: %s', port)

    stop_event = asyncio.Event()

    def handle_signal():
        logger.info('Shutdown signal received')
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, handle_signal)
    loop.add_signal_handler(signal.SIGINT, handle_signal)

    await stop_event.wait()

    logger.info('Shutting down gracefully')
    await server.stop(grace=5)
    logger.info('Shutdown complete')


if __name__ == '__main__':
    asyncio.run(serve())
