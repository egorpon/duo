from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

from auth.config import settings
from auth.exceptions import ExpiredTokenError, InvalidTokenError
from auth.models import User

ISSUER = 'duo'


class Token(BaseModel):
    access_token: str
    token_type: str
    issued_at: datetime
    expires_at: datetime


class TokenDetails(BaseModel):
    sub: int
    iat: float
    exp: float
    iss: str
    hash: str


def issue_token(user: User) -> Token:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=settings.jwt_lifetime)
    payload = {
        'sub': str(user.id),
        'iat': now.timestamp(),
        'exp': exp.timestamp(),
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
        issued_at=now,
        expires_at=exp,
    )


def decode_token(token: str) -> TokenDetails:
    try:
        result = jwt.decode(
            jwt=token,
            key=settings.secret_key.get_secret_value(),
            issuer=ISSUER,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenDetails(**result)
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError('Token expired')
    except (jwt.PyJWTError, jwt.InvalidTokenError):
        raise InvalidTokenError('Invalid token')
