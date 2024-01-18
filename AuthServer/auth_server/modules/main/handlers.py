
from .services import AuthentificationService
from protos.auth_proto import auth_pb2_grpc


def grpc_handlers(server):
    auth_pb2_grpc.add_AuthenticationServicer_to_server(AuthentificationService.as_servicer(), server)
