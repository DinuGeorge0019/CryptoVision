import jwt
import grpc
from config.settings import JWT_SECRET


def check_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_info']['user_id']
    except jwt.ExpiredSignatureError:
        raise grpc.RpcError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise grpc.RpcError('Invalid token. Please log in again.')
