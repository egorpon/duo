import datetime
from typing import Any

import jwt
from pydantic import BaseModel

from auth.config import settings
from auth.exceptions import InvalidTokenError
from auth.models import User

ISSUER = 'duo'


class Token(BaseModel):
    access_token: str
    token_type: str
    issued_at: float
    expired_at: float


def issue_token(user: User) -> Token:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    exp = (now + datetime.timedelta(seconds=settings.jwt_lifetime)).timestamp()
    iat = now.timestamp()
    payload = {
        'sub': user.id,
        'iat': iat,
        'exp': exp,
        'iss': ISSUER,
        'hash': user.hashed_password,
    }

    key = jwt.encode(
        payload=payload,
        key=settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
    return Token(
        access_token=key,
        token_type='Bearer',
        issued_at=iat,
        expired_at=exp,
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.secret_key,
            issuer=ISSUER,
            algorithms=[settings.jwt.algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError('Token expired')
    except (jwt.PyJWTError, jwt.InvalidTokenError):
        raise InvalidTokenError('Invalid token')
