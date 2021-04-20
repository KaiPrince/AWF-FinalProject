import jwt
from jwt import InvalidTokenError

# TODO: get from .env
secret = "our secret <3"


def issue_jwt_token(payload):
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except InvalidTokenError:
        return False
