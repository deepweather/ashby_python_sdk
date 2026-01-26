"""Base resource class for API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional

if TYPE_CHECKING:
    from ..client import AshbyClient


class BaseResource:
    """Base class for API resources."""

    def __init__(self, client: AshbyClient) -> None:
        self._client = client

    def _request(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make a request to the API."""
        return self._client._request(endpoint, data)

    def _paginate(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        limit: int = 100,
    ) -> Generator[dict, None, None]:
        """Paginate through API results."""
        return self._client._paginate(endpoint, data, limit)
