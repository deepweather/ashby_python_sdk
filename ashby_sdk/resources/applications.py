"""Applications API resource."""

from __future__ import annotations

from typing import Optional

from .base import BaseResource
from ..models import Application


class ApplicationsResource(BaseResource):
    """API resource for applications."""

    def list(
        self,
        job_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[Application]:
        """
        List applications.

        Args:
            job_id: Filter by job ID (optional)
            limit: Results per page (default 100)

        Returns:
            List of Application objects
        """
        data = {}
        if job_id:
            data["jobId"] = job_id
        return [
            Application.from_dict(a) for a in self._paginate("application.list", data, limit)
        ]

    def get(
        self,
        application_id: str,
        expand_forms: bool = False,
    ) -> Application:
        """
        Get an application by ID.

        Args:
            application_id: The application ID
            expand_forms: Whether to expand applicationFormSubmissions

        Returns:
            Application object with full details
        """
        data = {"applicationId": application_id}
        if expand_forms:
            data["expand"] = ["applicationFormSubmissions"]
        response = self._request("application.info", data)
        return Application.from_dict(response.get("results", {}))

    def get_with_forms(self, application_id: str) -> Application:
        """
        Get an application with form submissions expanded.

        Args:
            application_id: The application ID

        Returns:
            Application object with applicationFormSubmissions populated
        """
        return self.get(application_id, expand_forms=True)

    def change_stage(
        self,
        application_id: str,
        interview_stage_id: str,
    ) -> Application:
        """
        Move an application to a different interview stage.

        This changes the candidate's position in the hiring funnel.

        Args:
            application_id: The application ID
            interview_stage_id: The target interview stage ID

        Returns:
            Updated Application object
        """
        response = self._request(
            "application.changeStage",
            {
                "applicationId": application_id,
                "interviewStageId": interview_stage_id,
            }
        )
        return Application.from_dict(response.get("results", {}))

    def archive(
        self,
        application_id: str,
        archive_reason_id: str,
    ) -> Application:
        """
        Archive an application with a reason.

        This marks the candidate as rejected/archived in the hiring process.

        Args:
            application_id: The application ID
            archive_reason_id: The ID of the archive reason

        Returns:
            Updated Application object
        """
        response = self._request(
            "application.update",
            {
                "applicationId": application_id,
                "isArchived": True,
                "archiveReasonId": archive_reason_id,
            }
        )
        return Application.from_dict(response.get("results", {}))
