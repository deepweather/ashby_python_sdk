"""Application feedback (scorecards) API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import BaseResource

if TYPE_CHECKING:
    from ..models import Feedback


class FeedbackResource(BaseResource):
    """API resource for application feedback / interview scorecards."""

    def list_for_application(self, application_id: str) -> list[Feedback]:
        """
        Get all interview scorecards and feedback for an application.
        
        Each feedback submission contains:
        - formDefinition: The structure of the feedback form
        - submittedValues: Responses including scores and recommendations
        - Interview context: Links to associated interviews and events
        
        Args:
            application_id: The application ID
            
        Returns:
            List of Feedback objects
        """
        from ..models import Feedback
        
        response = self._request(
            "applicationFeedback.list",
            {"applicationId": application_id}
        )
        return [Feedback.from_dict(f) for f in response.get("results", [])]
