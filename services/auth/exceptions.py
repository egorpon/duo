class AuthServiceError(Exception):
    """Base error class for Auth service exeptions"""


class AuthenticationError(AuthServiceError):
    """Base class for authentication errors"""


class InvalidTokenError(AuthenticationError):
    """Raised when got invalid JWT"""


class ExpiredTokenError(AuthenticationError):
    """Raised when got expired JWT"""


class DBError(AuthServiceError):
    """Base class for database related exceptions"""


class EmailAlreadyUsedError(DBError):
    """Raised when email already used by other user"""
