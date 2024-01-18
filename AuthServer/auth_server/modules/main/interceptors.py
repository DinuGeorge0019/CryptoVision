
# import jwt
import grpc
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException

class AuthServerInterceptor(ServerInterceptor):
    def __init__(self):
        self.secret = 'hello'
        
    def intercept(
        self,
        method,
        request,
        context,
        method_name,
    ):
        """Override this method to implement a custom interceptor.
         You should call method(request, context) to invoke the
         next handler (either the RPC method implementation, or the
         next interceptor in the list).
         Args:
             method: The next interceptor, or method implementation.
             request: The RPC request, as a protobuf message.
             context: The ServicerContext pass by gRPC to the service.
             method_name: A string of the form
                 "/protobuf.package.Service/Method"
         Returns:
             This should generally return the result of
             method(request, context), which is typically the RPC
             method response, as a protobuf message. The interceptor
             is free to modify this in some way, however.
         """
        try:
            print("AuthServerInterceptor.intercept")
            
            # metadata = dict(context.invocation_metadata())
            
            # if 'auth_token' not in metadata:
            #     raise grpc.RpcError('NO AUTH TOKEN')
                
            # try:
                
            #     print("RECEIVED TOKEN: ", metadata['auth_token'])
                
            #     payload = jwt.decode(metadata['auth_token'], self.secret, algorithms=['HS256'])
            # except jwt.ExpiredSignatureError:
            #     raise grpc.RpcError('Signature expired. Please log in again.')
            # except jwt.InvalidTokenError:
            #     raise grpc.RpcError('Invalid token. Please log in again.')
            
            return method(request, context)
        
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
