from jwt import ExpiredSignatureError
from rest_framework_jwt.settings import api_settings as settings


def check_staff(user):
    return user.profile.type == 1


def check_student(user):
    return user.profile.type == 0


def sign_token(user):
    jwt_payload_handler = settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def decode_token(token):
    decode_payload_handler = settings.JWT_DECODE_HANDLER
    try:
        user = decode_payload_handler(token)
    except ExpiredSignatureError:
        return -1
    return user['username']
