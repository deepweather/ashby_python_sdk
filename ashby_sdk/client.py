"""
Ashby API Client

Main client class for interacting with the Ashby ATS API.
"""

from __future__ import annotations

import os
import base64
from typing import Generator, Optional

import requests
from dotenv import load_dotenv

from .exceptions import AshbyAPIError, AshbyAuthError
from .models import (
    Application,
    ArchiveReason,
    Candidate,
    CloseReason,
    CustomFieldDefinition,
    Department,
    Feedback,
    HiringTeamRole,
    Interview,
    InterviewSchedule,
    InterviewStage,
    Location,
    Note,
    Offer,
    Project,
    Source,
    Tag,
    User,
)
from .resources import (
    JobsResource,
    ApplicationsResource,
    CandidatesResource,
    InterviewStagesResource,
    SurveysResource,
    FilesResource,
    JobPostingsResource,
    NotesResource,
    GenericResource,
    FeedbackResource,
)

# Load .env file if present
load_dotenv()


# ---------------------------------------------------------------------------
# Generic Resource Registry
# ---------------------------------------------------------------------------
# Configuration-driven endpoint registration.
# Adding a new simple endpoint is just one line here.
#
# Format: "attribute_name": (endpoint_prefix, model_class, supports_get)
#
# Example: "sources": ("source", Source, False)
#   -> Creates client.sources with .list() method
#   -> Calls source.list endpoint
#   -> Deserializes to Source model
#   -> supports_get=False means .get() raises NotImplementedError
#
SIMPLE_RESOURCES: dict[str, tuple[type, str, bool]] = {
    # Hiring Process Metadata (read-only list endpoints)
    "sources": (Source, "source", False),
    "archive_reasons": (ArchiveReason, "archiveReason", False),
    "close_reasons": (CloseReason, "closeReason", False),
    "candidate_tags": (Tag, "candidateTag", False),
    "hiring_team_roles": (HiringTeamRole, "hiringTeamRole", False),
    
    # Organization (list + get endpoints)
    "departments": (Department, "department", True),
    "locations": (Location, "location", True),
    "users": (User, "user", True),
    
    # Custom fields (list + get)
    "custom_fields": (CustomFieldDefinition, "customField", True),
    
    # Projects / Talent pools (list + get)
    "projects": (Project, "project", True),
    
    # Offers (list + get)
    "offers": (Offer, "offer", True),
    
    # Interviews (list + get)  
    "interviews": (Interview, "interview", True),
    "interview_schedules": (InterviewSchedule, "interviewSchedule", True),
}


class AshbyClient:
    """
    Client for interacting with the Ashby API.

    Usage:
        client = AshbyClient(api_key="your-key")
        # or set ASHBY_API_KEY environment variable

        jobs = client.jobs.list(status=["Open"])
        applications = client.applications.list(job_id="...")
        candidate = client.candidates.get(candidate_id="...")
    """

    BASE_URL = "https://api.ashbyhq.com"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Ashby client.

        Args:
            api_key: Ashby API key. If not provided, reads from ASHBY_API_KEY env var.

        Raises:
            AshbyAuthError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("ASHBY_API_KEY")
        if not self.api_key:
            raise AshbyAuthError(
                "API key is required. Provide it as argument or set ASHBY_API_KEY env var."
            )

        # Basic auth: API key as username, empty password
        credentials = f"{self.api_key}:"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self._headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Initialize specialized resource endpoints
        self.jobs = JobsResource(self)
        self.applications = ApplicationsResource(self)
        self.candidates = CandidatesResource(self)
        self.interview_stages = InterviewStagesResource(self)
        self.surveys = SurveysResource(self)
        self.files = FilesResource(self)
        self.job_postings = JobPostingsResource(self)
        self.notes = NotesResource(self)
        self.feedback = FeedbackResource(self)
        
        # Initialize generic resources from registry
        # This allows adding new endpoints with just one line in SIMPLE_RESOURCES
        for attr_name, (model_class, endpoint, supports_get) in SIMPLE_RESOURCES.items():
            setattr(self, attr_name, GenericResource(self, endpoint, model_class, supports_get))

    def _request(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """
        Make a POST request to the Ashby API.

        Args:
            endpoint: API endpoint (e.g., "job.list")
            data: Request body data

        Returns:
            Response JSON

        Raises:
            AshbyAuthError: If authentication fails
            AshbyAPIError: If the API returns an error
        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.post(url, headers=self._headers, json=data or {})

        if response.status_code == 401:
            raise AshbyAuthError("Invalid or missing API key")
        if response.status_code == 403:
            raise AshbyAuthError("API key does not have permission for this endpoint")

        response.raise_for_status()

        result = response.json()
        if not result.get("success", False):
            errors = result.get("errors", [])
            error_info = result.get("errorInfo", {})
            message = error_info.get("message") if error_info else None
            if not message and errors:
                message = str(errors)
            if not message:
                message = f"Unknown error (response: {result})"
            raise AshbyAPIError(f"API error: {message}", errors=errors)

        return result

    def _paginate(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        limit: int = 100,
    ) -> Generator[dict, None, None]:
        """
        Paginate through all results from a list endpoint.

        Args:
            endpoint: API endpoint
            data: Additional request parameters
            limit: Number of results per page

        Yields:
            Individual result items
        """
        request_data = data.copy() if data else {}
        request_data["limit"] = limit
        cursor = None

        while True:
            if cursor:
                request_data["cursor"] = cursor

            response = self._request(endpoint, request_data)

            for item in response.get("results", []):
                yield item

            if not response.get("moreDataAvailable", False):
                break

            cursor = response.get("nextCursor")

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def get_application_with_candidate(self, application_id: str) -> Application:
        """Get an application with full candidate details populated."""
        application = self.applications.get(application_id)
        if application.candidate_id:
            application.candidate = self.candidates.get(application.candidate_id)
        return application

    def download_resume(self, candidate: Candidate) -> Optional[tuple[bytes, str]]:
        """Download a candidate's resume if available."""
        if not candidate.resume_handle:
            return None
        return self.files.download(candidate.resume_handle)

    def get_job_description(self, job_id: str) -> Optional[str]:
        """Get the job description for a job."""
        return self.job_postings.get_description(job_id)

    def create_candidate_note(
        self,
        candidate_id: str,
        note_text: str,
        note_type: str = "text/plain",
    ) -> Note:
        """Create a note on a candidate."""
        return self.notes.create(candidate_id, note_text, note_type)

    def get_application_stage(self, application_id: str) -> Optional[InterviewStage]:
        """Get the current interview stage for an application."""
        application = self.applications.get(application_id)
        return application.current_stage

    def move_application_to_stage(
        self,
        application_id: str,
        interview_stage_id: str,
    ) -> Application:
        """Move an application to a different interview stage."""
        return self.applications.change_stage(application_id, interview_stage_id)

    def get_job_funnel(self, job_id: str) -> list[InterviewStage]:
        """Get all interview stages (funnel steps) for a job."""
        return self.interview_stages.list_for_job(job_id)
