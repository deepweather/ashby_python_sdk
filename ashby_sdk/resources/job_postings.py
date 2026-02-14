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
        
        Note:
            The Ashby API does not filter by jobId server-side, so we filter
            client-side if job_id is provided.
        """
        # Note: Ashby API ignores jobId filter, so we fetch all and filter client-side
        all_postings = [
            JobPosting.from_dict(p) for p in self._paginate("jobPosting.list", {}, limit)
        ]
        
        if job_id:
            return [p for p in all_postings if p.job_id == job_id]
        return all_postings

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

    def get_for_job(
        self,
        job_id: str,
        job_title: Optional[str] = None,
    ) -> Optional[JobPosting]:
        """
        Get the best-matching job posting for a job with full details.

        When multiple postings exist for the same job (e.g. different titles
        for internal vs external listings), this method picks the posting
        whose title matches *job_title*.  If no match is found — or no
        *job_title* is given — it falls back to the most-recently-updated
        posting.

        Args:
            job_id: The job ID
            job_title: The canonical job title used for matching.
                       When called via :meth:`get_description` this is
                       looked up automatically.

        Returns:
            JobPosting object with description, or None if no postings exist
        """
        postings = self.list(job_id=job_id)
        if not postings:
            return None

        # Only one posting — no ambiguity
        if len(postings) == 1:
            return self.get(postings[0].id)

        # Try exact title match first
        if job_title:
            for p in postings:
                if p.title == job_title:
                    return self.get(p.id)

        # Fallback: most recently updated posting
        postings.sort(
            key=lambda p: p.updated_at or "",
            reverse=True,
        )
        return self.get(postings[0].id)

    def get_description(self, job_id: str) -> Optional[str]:
        """
        Get the job description for a job.

        Convenience method that fetches the job posting and returns
        the plain text description.  Automatically resolves the correct
        posting when multiple postings exist for the same job by looking
        up the job title via the jobs API.

        Args:
            job_id: The job ID

        Returns:
            Plain text job description or None
        """
        # Look up the canonical job title so we can match the right posting
        job_title: Optional[str] = None
        try:
            from .jobs import JobsResource
            jobs_resource = JobsResource(self._client)
            job = jobs_resource.get(job_id)
            job_title = job.title
        except Exception:
            pass

        posting = self.get_for_job(job_id, job_title=job_title)
        return posting.description if posting else None
