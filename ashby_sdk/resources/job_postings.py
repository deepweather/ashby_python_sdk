"""Job postings API resource."""

from __future__ import annotations

from typing import Optional

from .base import BaseResource
from ..models import JobPosting


class JobPostingsResource(BaseResource):
    """API resource for job postings (with descriptions)."""

    def list(
        self,
        job_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[JobPosting]:
        """
        List all job postings.

        Args:
            job_id: Filter by job ID (optional)
            limit: Results per page (default 100)

        Returns:
            List of JobPosting objects
        """
        data = {}
        if job_id:
            data["jobId"] = job_id
        return [
            JobPosting.from_dict(p) for p in self._paginate("jobPosting.list", data, limit)
        ]

    def get(self, posting_id: str) -> JobPosting:
        """
        Get a job posting by ID.

        Args:
            posting_id: The job posting ID

        Returns:
            JobPosting object with description
        """
        response = self._request("jobPosting.info", {"jobPostingId": posting_id})
        return JobPosting.from_dict(response.get("results", {}))

    def get_for_job(self, job_id: str) -> Optional[JobPosting]:
        """
        Get the primary job posting for a job with full details.

        This method first lists postings for the job, then fetches the
        full details (including description) for the first posting.

        Args:
            job_id: The job ID

        Returns:
            JobPosting object with description, or None if no postings exist
        """
        postings = self.list(job_id=job_id)
        if not postings:
            return None
        # Fetch full details including description
        return self.get(postings[0].id)

    def get_description(self, job_id: str) -> Optional[str]:
        """
        Get the job description for a job.

        Convenience method that fetches the job posting and returns
        the plain text description.

        Args:
            job_id: The job ID

        Returns:
            Plain text job description or None
        """
        posting = self.get_for_job(job_id)
        return posting.description if posting else None
