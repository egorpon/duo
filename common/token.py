import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jwt.types import Options
from pydantic import BaseModel

from common.exceptions import ExpiredTokenError, InvalidTokenError

ISSUER = 'duo'


class TokenDetails(BaseModel):
    sub: int
    iat: float
    exp: float
    iss: str


def decode_token(
    *,
    token: str,
    public_key: Ed25519PublicKey,
    algorithm: str,
) -> TokenDetails:
    try:
        result = jwt.decode(
            jwt=token,
            key=public_key,
            issuer=ISSUER,
            algorithms=[algorithm],
            options=Options(verify_signature=True),
        )
        return TokenDetails(**result)
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError('Token expired')
    except (jwt.PyJWTError, jwt.InvalidTokenError):
        raise InvalidTokenError('Invalid token')
