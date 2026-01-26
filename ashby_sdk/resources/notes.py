"""Notes API resource."""

from __future__ import annotations

from .base import BaseResource
from ..models import Note


class NotesResource(BaseResource):
    """API resource for candidate notes."""

    def create(
        self,
        candidate_id: str,
        note_text: str,
        note_type: str = "text/plain",
    ) -> Note:
        """
        Create a note on a candidate.

        Args:
            candidate_id: The candidate ID
            note_text: The note content
            note_type: "text/plain" or "text/html" (default "text/plain")

        Returns:
            Note object with the created note
        """
        response = self._request(
            "candidate.createNote",
            {
                "candidateId": candidate_id,
                "note": note_text,
                "type": note_type,
            }
        )
        return Note.from_dict(response.get("results", {}))

    def list(
        self,
        candidate_id: str,
        limit: int = 100,
    ) -> list[Note]:
        """
        List all notes for a candidate.

        Args:
            candidate_id: The candidate ID
            limit: Results per page (default 100)

        Returns:
            List of Note objects
        """
        return [
            Note.from_dict(n)
            for n in self._paginate(
                "candidate.listNotes",
                {"candidateId": candidate_id},
                limit
            )
        ]
