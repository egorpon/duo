from common.exceptions import CommonError


class ApiServiceError(CommonError):
    """Base error class for Api service exceptions"""


class AlreadyConnectedError(CommonError):
    pass


class ConnectionLimitError(CommonError):
    pass
