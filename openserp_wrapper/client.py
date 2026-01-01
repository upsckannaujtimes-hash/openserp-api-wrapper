"""
Synchronous OpenSerp API client
"""

import time
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .cache import Cache, InMemoryCache
from .rate_limiter import RateLimiter
from .exceptions import (
    OpenSerpConnectionError,
    OpenSerpTimeoutError,
    OpenSerpAPIError,
    OpenSerpValidationError,
)


class OpenSerpClient:
    """Synchronous client for OpenSerp API

    Args:
        base_url: OpenSerp server URL (default: http://localhost:7000)
        timeout: Request timeout in seconds (default: 30)
        cache: Cache implementation (default: InMemoryCache)
        cache_ttl: Cache time-to-live in seconds (default: 3600)
        rate_limiter: Rate limiter instance (default: None)
        verify_ssl: Verify SSL certificates (default: True)
    """

    def __init__(
        self,
        base_url: str = "http://localhost:7000",
        timeout: int = 30,
        cache: Optional[Cache] = None,
        cache_ttl: int = 3600,
        rate_limiter: Optional[RateLimiter] = None,
        verify_ssl: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.cache = cache or InMemoryCache()
        self.cache_ttl = cache_ttl
        self.rate_limiter = rate_limiter
        self.verify_ssl = verify_ssl
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def search(
        self,
        text: str,
        engines: Optional[List[str]] = None,
        limit: int = 10,
        offset: int = 0,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        language: Optional[str] = None,
        sort: str = "relevance",
    ) -> Dict[str, Any]:
        """Search across OpenSerp engines

        Args:
            text: Search query
            engines: List of search engines to query
            limit: Number of results to return (1-100)
            offset: Result offset for pagination
            date_from: Start date in YYYYMMDD format
            date_to: End date in YYYYMMDD format
            language: Language code (e.g., 'EN', 'ES', 'FR')
            sort: Sort order ('relevance' or 'date')

        Returns:
            Search results dictionary

        Raises:
            OpenSerpValidationError: If input validation fails
            OpenSerpConnectionError: If connection fails
            OpenSerpAPIError: If API returns an error
        """

        # Validate input
        if not text or not isinstance(text, str):
            raise OpenSerpValidationError("Search text must be a non-empty string")
        if not 1 <= limit <= 100:
            raise OpenSerpValidationError("Limit must be between 1 and 100")
        if offset < 0:
            raise OpenSerpValidationError("Offset must be non-negative")

        # Check rate limit
        if self.rate_limiter:
            self.rate_limiter.wait()

        # Check cache
        cache_key = self._generate_cache_key(text, engines, limit, offset)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result

        # Build request
        params = {
            "text": text,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }

        if engines:
            params["engines"] = ",".join(engines)
        if date_from and date_to:
            params["date"] = f"{date_from}..{date_to}"
        elif date_from:
            params["date_from"] = date_from
        elif date_to:
            params["date_to"] = date_to
        if language:
            params["lang"] = language

        try:
            response = self.session.get(
                urljoin(self.base_url, "/mega/search"),
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

            # Handle HTTP errors
            if response.status_code == 429:
                raise OpenSerpConnectionError(
                    "Rate limited by OpenSerp server", "RATE_LIMIT"
                )
            elif response.status_code >= 400:
                raise OpenSerpAPIError(
                    f"API error: {response.text}",
                    status_code=response.status_code,
                )

            result = response.json()

            # Cache result
            self.cache.set(cache_key, result, ttl=self.cache_ttl)

            return result

        except requests.exceptions.Timeout as e:
            raise OpenSerpTimeoutError(f"Request timeout after {self.timeout}s") from e
        except requests.exceptions.ConnectionError as e:
            raise OpenSerpConnectionError(
                f"Failed to connect to {self.base_url}"
            ) from e
        except requests.exceptions.RequestException as e:
            raise OpenSerpConnectionError(f"Request error: {str(e)}") from e

    def search_engines(self) -> List[str]:
        """Get list of available search engines

        Returns:
            List of available engine names
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, "/engines"),
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            response.raise_for_status()
            return response.json().get("engines", [])
        except Exception as e:
            raise OpenSerpConnectionError(f"Failed to fetch engines: {str(e)}") from e

    def clear_cache(self) -> None:
        """Clear all cached results"""
        self.cache.clear()

    def close(self) -> None:
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    @staticmethod
    def _generate_cache_key(
        text: str,
        engines: Optional[List[str]] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> str:
        """Generate cache key from search parameters"""
        engine_str = ",".join(sorted(engines)) if engines else "all"
        return f"search:{text}:{engine_str}:{limit}:{offset}"
