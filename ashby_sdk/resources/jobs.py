"""Jobs API resource."""

from __future__ import annotations

from typing import Optional

from .base import BaseResource
from ..models import Job


class JobsResource(BaseResource):
    """API resource for jobs."""

    def list(
        self,
        status: Optional[list[str]] = None,
        limit: int = 100,
    ) -> list[Job]:
        """
        List all jobs.

        Args:
            status: Filter by status (e.g., ["Open", "Closed", "Draft", "Archived"])
            limit: Results per page (default 100)

        Returns:
            List of Job objects
        """
        data = {}
        if status:
            data["status"] = status
        return [Job.from_dict(j) for j in self._paginate("job.list", data, limit)]

    def get(self, job_id: str) -> Job:
        """
        Get a job by ID.

        Args:
            job_id: The job ID

        Returns:
            Job object
        """
        response = self._request("job.info", {"id": job_id})
        return Job.from_dict(response.get("results", {}))
