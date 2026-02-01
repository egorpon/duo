import asyncio

from grpc import aio

from auth.service import UserService
from generated import auth_pb2_grpc


async def serve() -> None:
    server = aio.server()
    auth_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    port = server.add_insecure_port('localhost:50051')
    print('running server on port:', port)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
