"""Candidates API resource."""

from __future__ import annotations

from .base import BaseResource
from ..models import Candidate


class CandidatesResource(BaseResource):
    """API resource for candidates."""

    def list(self, limit: int = 100) -> list[Candidate]:
        """
        List all candidates.

        Args:
            limit: Results per page (default 100)

        Returns:
            List of Candidate objects
        """
        return [
            Candidate.from_dict(c) for c in self._paginate("candidate.list", limit=limit)
        ]

    def get(self, candidate_id: str) -> Candidate:
        """
        Get a candidate by ID.

        Args:
            candidate_id: The candidate ID

        Returns:
            Candidate object
        """
        response = self._request("candidate.info", {"id": candidate_id})
        return Candidate.from_dict(response.get("results", {}))
