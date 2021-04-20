import jwt

secret = "our secret <3"


def issue_jwt_token(payload):
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, secret, algorithms=["HS256"])
