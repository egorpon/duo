class AuthServiceError(Exception):
    """Base error class for Auth service exeptions"""


class InvalidTokenError(AuthServiceError):
    """Raised when got invalid JWT"""


class DBError(AuthServiceError):
    """Base class for database related exceptions"""


class EmailAlreadyUsedError(DBError):
    """Raised when email already used by other user"""
