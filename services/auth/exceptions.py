from common.exceptions import CommonError


class AuthServiceError(CommonError):
    """Base error class for Auth service exceptions"""


class AuthenticationError(AuthServiceError):
    """Base class for authentication errors"""


class DBError(AuthServiceError):
    """Base class for database related exceptions"""


class EmailAlreadyUsedError(DBError):
    """Raised when email already used by other user"""


class UnsupportedGRPCMethodError(AuthServiceError):
    pass
