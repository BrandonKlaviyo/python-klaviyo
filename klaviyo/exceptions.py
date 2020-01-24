class KlaviyoException(Exception):
    pass


class KlaviyoAuthenticationError(KlaviyoException):
    pass


class KlaviyoRateLimitException(KlaviyoException):
    pass


class KlaviyoServerError(KlaviyoException):
    pass