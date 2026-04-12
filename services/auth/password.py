from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Return hashed password"""

    return _hasher.hash(password)


def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the provided password matches the hashed password.
    """
    try:
        return _hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
