class AuthServiceError(Exception):
    """Base error class for Auth service exeptions"""


class InvalidTokenError(AuthServiceError):
    """Raised when got invalid JWT"""
