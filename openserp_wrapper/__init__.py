"""
OpenSerp API Wrapper - A comprehensive wrapper for multi-engine search API

Version: 1.0.0
Author: OpenSerp Wrapper Team
License: MIT
"""

from .client import OpenSerpClient
from .async_client import AsyncOpenSerpClient
from .cache import Cache, InMemoryCache, RedisCache
from .rate_limiter import RateLimiter
from .exceptions import (
    OpenSerpException,
    OpenSerpConnectionError,
    OpenSerpTimeoutError,
    OpenSerpAPIError,
    OpenSerpValidationError,
)

__version__ = "1.0.0"
__author__ = "OpenSerp Wrapper Team"
__license__ = "MIT"

__all__ = [
    "OpenSerpClient",
    "AsyncOpenSerpClient",
    "Cache",
    "InMemoryCache",
    "RedisCache",
    "RateLimiter",
    "OpenSerpException",
    "OpenSerpConnectionError",
    "OpenSerpTimeoutError",
    "OpenSerpAPIError",
    "OpenSerpValidationError",
]
