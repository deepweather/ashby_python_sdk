"""Candidates API resource."""

from __future__ import annotations

from typing import Optional

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

    def search(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
    ) -> list[Candidate]:
        """
        Search for candidates by email and/or name.
        
        Results are limited to 100. If you need more, use list() with pagination.
        When multiple parameters are provided, they are combined with AND.
        
        Args:
            email: Email address to search for
            name: Name to search for
            
        Returns:
            List of matching Candidate objects (max 100)
            
        Example:
            # Find by email
            candidates = client.candidates.search(email="john@example.com")
            
            # Find by name
            candidates = client.candidates.search(name="John Doe")
            
            # Find by both (AND)
            candidates = client.candidates.search(email="john@example.com", name="John")
        """
        data = {}
        if email:
            data["email"] = email
        if name:
            data["name"] = name
        
        if not data:
            raise ValueError("At least one of email or name must be provided")
        
        response = self._request("candidate.search", data)
        return [Candidate.from_dict(c) for c in response.get("results", [])]

    def add_tag(self, candidate_id: str, tag_id: str) -> Candidate:
        """
        Add a tag to a candidate.
        
        Args:
            candidate_id: The candidate ID
            tag_id: The tag ID to add (use client.candidate_tags.list() to get available tags)
            
        Returns:
            Updated Candidate object
            
        Example:
            # Get available tags
            tags = client.candidate_tags.list()
            
            # Add first tag to candidate
            if tags:
                updated = client.candidates.add_tag("cand_123", tags[0].id)
        """
        response = self._request(
            "candidate.addTag",
            {"candidateId": candidate_id, "tagId": tag_id}
        )
        return Candidate.from_dict(response.get("results", {}))
