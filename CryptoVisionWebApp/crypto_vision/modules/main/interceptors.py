import jwt
import datetime

from grpc_interceptor import ClientCallDetails, ClientInterceptor


class AuthClientInterceptor(ClientInterceptor):
    def __init__(self):
        self.secret = 'hello'
    
    def intercept(
        self,
        method,
        request_or_iterator,
        call_details,
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
        
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'sub': 'user_id'
        }
        
        auth_token = jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
        
        print("SEND TOKEN: ", auth_token)
        
        metadata = []
        if call_details.metadata is not None:
            metadata = list(call_details.metadata)
        metadata.append(('auth_token', auth_token))
        
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            metadata,
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression
        )
        
        return method(request_or_iterator, new_details)
