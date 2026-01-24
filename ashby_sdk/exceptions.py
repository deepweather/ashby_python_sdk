"""
Custom exceptions for the Ashby SDK.
"""


class AshbyError(Exception):
    """Base exception for all Ashby SDK errors."""

    pass


class AshbyAPIError(AshbyError):
    """Error returned by the Ashby API."""

    def __init__(self, message: str, errors: list[str] | None = None):
        self.errors = errors or []
        super().__init__(message)


class AshbyAuthError(AshbyError):
    """Authentication error (invalid or missing API key)."""

    pass


class AshbyNotFoundError(AshbyError):
    """Resource not found."""

    pass


class AshbyRateLimitError(AshbyError):
    """Rate limit exceeded."""

    pass
