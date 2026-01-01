"""
Custom exceptions for OpenSerp wrapper
"""


class OpenSerpException(Exception):
    """Base exception class for all OpenSerp wrapper errors"""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class OpenSerpConnectionError(OpenSerpException):
    """Raised when connection to OpenSerp server fails"""

    pass


class OpenSerpTimeoutError(OpenSerpException):
    """Raised when OpenSerp server request times out"""

    pass


class OpenSerpAPIError(OpenSerpException):
    """Raised when OpenSerp API returns an error"""

    def __init__(self, message: str, status_code: int = None, code: str = None):
        super().__init__(message, code)
        self.status_code = status_code


class OpenSerpValidationError(OpenSerpException):
    """Raised when input validation fails"""

    pass


class OpenSerpRateLimitError(OpenSerpException):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after


class OpenSerpCacheError(OpenSerpException):
    """Raised when cache operations fail"""

    pass
