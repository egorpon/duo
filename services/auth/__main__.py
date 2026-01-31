from concurrent.futures import ThreadPoolExecutor

import grpc

from auth.client import UserService
from generated import auth_pb2_grpc

if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor(max_workers=1))
    auth_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    port = server.add_insecure_port('localhost:50051')
    print('running server on port:', port)
    server.start()
    server.wait_for_termination()
