"""Interview stages API resource."""

from __future__ import annotations

from .base import BaseResource
from ..models import InterviewStage


class InterviewStagesResource(BaseResource):
    """API resource for interview stages (hiring funnel stages)."""

    def list(
        self,
        interview_plan_id: str,
        limit: int = 100,
    ) -> list[InterviewStage]:
        """
        List all interview stages for an interview plan.

        Args:
            interview_plan_id: The interview plan ID (required)
            limit: Results per page (default 100)

        Returns:
            List of InterviewStage objects
        """
        data = {"interviewPlanId": interview_plan_id}
        stages = []
        for s in self._paginate("interviewStage.list", data, limit):
            stage = InterviewStage.from_dict(s)
            if stage:
                stages.append(stage)
        return stages

    def get(self, stage_id: str) -> InterviewStage:
        """
        Get an interview stage by ID.

        Args:
            stage_id: The interview stage ID

        Returns:
            InterviewStage object
        """
        response = self._request("interviewStage.info", {"interviewStageId": stage_id})
        return InterviewStage.from_dict(response.get("results", {}))

    def list_for_job(self, job_id: str) -> list[InterviewStage]:
        """
        Get all interview stages for a specific job.

        This returns the stages in the job's interview plan/funnel.

        Args:
            job_id: The job ID

        Returns:
            List of InterviewStage objects ordered by stage order
        """
        # First get the job to find its interview plan
        job_response = self._request("job.info", {"id": job_id})
        job_data = job_response.get("results", {})

        plan_id = job_data.get("defaultInterviewPlanId")
        if not plan_id:
            # Try interviewPlanIds if no default
            plan_ids = job_data.get("interviewPlanIds", [])
            if plan_ids:
                plan_id = plan_ids[0]

        if not plan_id:
            return []

        stages = self.list(interview_plan_id=plan_id)
        # Sort by order if available
        return sorted(stages, key=lambda s: s.order_in_stage_group or 0)
