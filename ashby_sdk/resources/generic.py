"""Generic resource class for simple list/get endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

from .base import BaseResource

if TYPE_CHECKING:
    from ..client import AshbyClient


class GenericResource(BaseResource):
    """
    Generic resource for simple list/get endpoints.
    
    This class handles the common patterns:
    - list(): Paginated list with optional filters
    - get(id): Fetch single resource by ID
    
    Usage:
        # In client.py:
        self.sources = GenericResource(self, "source", Source, supports_get=False)
        self.departments = GenericResource(self, "department", Department, supports_get=True)
        
        # Then use:
        sources = client.sources.list()
        dept = client.departments.get("dept_123")
    """

    def __init__(
        self,
        client: AshbyClient,
        endpoint: str,
        model_class: type,
        supports_get: bool = False,
        id_param: Optional[str] = None,
    ) -> None:
        """
        Initialize a generic resource.
        
        Args:
            client: The Ashby client instance
            endpoint: API endpoint name (e.g., "source", "department")
            model_class: The model class to deserialize results into
            supports_get: Whether this endpoint supports .info (get by ID)
            id_param: Parameter name for the ID in .info calls (e.g., "departmentId").
                     If not provided, defaults to "{endpoint}Id".
        """
        super().__init__(client)
        self._endpoint = endpoint
        self._model = model_class
        self._supports_get = supports_get
        # Ashby uses {endpoint}Id for most .info endpoints (e.g., departmentId, locationId)
        self._id_param = id_param or f"{endpoint}Id"

    def list(self, limit: int = 100, **filters: Any) -> list:
        """
        List all resources of this type.
        
        Args:
            limit: Results per page (default 100)
            **filters: Optional filters to pass to the API
            
        Returns:
            List of model instances
        """
        # Filter out None values from filters
        data = {k: v for k, v in filters.items() if v is not None}
        return [
            self._model.from_dict(item)
            for item in self._paginate(f"{self._endpoint}.list", data, limit)
        ]

    def get(self, id: str) -> Any:
        """
        Get a single resource by ID.
        
        Args:
            id: The resource ID
            
        Returns:
            Model instance
            
        Raises:
            NotImplementedError: If this endpoint doesn't support get
        """
        if not self._supports_get:
            raise NotImplementedError(
                f"The {self._endpoint} endpoint does not support .info (get by ID)"
            )
        response = self._request(f"{self._endpoint}.info", {self._id_param: id})
        return self._model.from_dict(response.get("results", {}))

    @property
    def endpoint(self) -> str:
        """Return the endpoint name."""
        return self._endpoint

    @property
    def model(self) -> type:
        """Return the model class."""
        return self._model
