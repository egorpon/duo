"""
Service-wide exceptions
"""


class CommonError(Exception):
    """
    Common error class for all service exceptions
    """


class JWTError(CommonError):
    """Base class for JWT related errors"""


class InvalidTokenError(JWTError):
    """Raised when got invalid JWT"""


class ExpiredTokenError(JWTError):
    """Raised when got expired JWT"""
