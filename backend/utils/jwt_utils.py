import jwt
import datetime
from config import DEFAULT_JWT_TOKEN_HOURS, JWT_ALGORITHM, SECRET_KEY

def generate_token(user_id=None, role=None, extra_claims=None, expires_in_hours=None):
    payload = {}

    if user_id is not None:
        payload["user_id"] = user_id
    if role is not None:
        payload["role"] = role
    if extra_claims:
        payload.update(extra_claims)

    expiry_hours = expires_in_hours or DEFAULT_JWT_TOKEN_HOURS
    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=expiry_hours)

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
