from datetime import datetime, timedelta

import jwt
from pydantic import BaseModel

from common.token import ISSUER, TokenDetails
from common.token import decode_token as _decode_token
from services.auth.config import settings
from services.auth.db.models import User


class Token(BaseModel):
    access_token: str
    token_type: str
    issued_at: datetime
    expires_at: datetime


def issue_token(user: User) -> Token:
    now = datetime.now()
    exp = now + timedelta(seconds=settings.jwt_lifetime)
    payload = {
        'sub': str(user.id),
        'iat': now.timestamp(),
        'exp': exp.timestamp(),
        'iss': ISSUER,
    }

    key = jwt.encode(
        payload=payload,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )
    return Token(
        access_token=key,
        token_type='Bearer',
        issued_at=now,
        expires_at=exp,
    )


def decode_token(token: str) -> TokenDetails:
    return _decode_token(
        token=token,
        public_key=settings.public_key,
        algorithm=settings.jwt_algorithm,
    )
