"""
Ashby API Client

Main client class for interacting with the Ashby ATS API.
"""

import os
import base64
from typing import Generator, Optional, TypeVar, Callable

import requests
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

from .exceptions import AshbyAPIError, AshbyAuthError, AshbyNotFoundError
from .models import Job, Application, Candidate, File

T = TypeVar("T")


class BaseResource:
    """Base class for API resources."""

    def __init__(self, client: "AshbyClient"):
        self._client = client

    def _request(self, endpoint: str, data: Optional[dict] = None) -> dict:
        return self._client._request(endpoint, data)

    def _paginate(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        limit: int = 100,
    ) -> Generator[dict, None, None]:
        return self._client._paginate(endpoint, data, limit)


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


class SurveysResource(BaseResource):
    """API resource for survey/questionnaire submissions."""

    def list(
        self,
        survey_type: str = "Questionnaire",
        limit: int = 100,
    ):
        """
        List all survey submissions of a given type.

        Args:
            survey_type: Type of survey (default "Questionnaire")
            limit: Results per page (default 100)

        Returns:
            List of survey submission dicts
        """
        return list(self._paginate(
            "surveySubmission.list",
            {"surveyType": survey_type},
            limit
        ))

    def get_for_candidate(
        self,
        candidate_id: str,
        survey_type: str = "Questionnaire",
    ):
        """
        Get all survey submissions for a specific candidate.

        Args:
            candidate_id: The candidate ID
            survey_type: Type of survey (default "Questionnaire")

        Returns:
            List of survey submissions for this candidate
        """
        all_surveys = self.list(survey_type=survey_type)
        return [s for s in all_surveys if s.get("candidateId") == candidate_id]

    def parse_submission(self, submission: dict) -> dict:
        """
        Parse a survey or application form submission into a readable format.

        Works for both surveySubmission and applicationFormSubmissions data.

        Args:
            submission: Raw submission dict (from survey or application form)

        Returns:
            Dict with field titles mapped to values
        """
        # Build field ID -> title mapping
        field_map = {}
        form_def = submission.get("formDefinition", {})
        for section in form_def.get("sections", []):
            for field_def in section.get("fields", []):
                field = field_def.get("field", {})
                field_id = field.get("id")
                field_title = field.get("title")
                field_path = field.get("path", "")
                if field_id:
                    field_map[field_id] = field_title
                if field_path:
                    field_map[field_path] = field_title

        # Map submitted values to titles
        result = {
            "submitted_at": submission.get("submittedAt"),
            "candidate_id": submission.get("candidateId"),
            "application_id": submission.get("applicationId"),
            "survey_type": submission.get("surveyType"),
            "form_id": submission.get("id"),
            "answers": {},
        }

        # System fields to skip (these are basic info, not questionnaire answers)
        skip_fields = {
            "_systemfield_resume",
            "_systemfield_pre_parsed_resume",
            "_systemfield_name",
            "_systemfield_email",
            "_systemfield_phone",
        }

        submitted = submission.get("submittedValues", {})
        for field_key, value in submitted.items():
            title = field_map.get(field_key, field_key)

            # Skip system fields that contain basic candidate info
            if field_key in skip_fields:
                continue
            if field_key.startswith("_systemfield_") and field_key not in field_map:
                continue

            # Format value
            if isinstance(value, dict):
                if "text" in value:
                    value = value.get("text")
                elif "name" in value:
                    value = value.get("name")
            elif isinstance(value, bool):
                value = "Yes" if value else "No"
            elif isinstance(value, list):
                value = ", ".join(
                    str(v.get("name", v) if isinstance(v, dict) else v) for v in value
                )

            result["answers"][title] = value

        return result


class FilesResource(BaseResource):
    """API resource for files."""

    def get_url(self, file_handle: str) -> str:
        """
        Get the download URL for a file.

        Args:
            file_handle: The file handle string

        Returns:
            Signed URL for downloading the file
        """
        response = self._request("file.info", {"fileHandle": file_handle})
        return response.get("results", {}).get("url", "")

    def download(self, file_handle: str) -> tuple[bytes, str]:
        """
        Download a file by its handle.

        Args:
            file_handle: The file handle string

        Returns:
            Tuple of (file content bytes, filename)
        """
        url = self.get_url(file_handle)
        if not url:
            raise AshbyNotFoundError(f"Could not get URL for file handle")

        response = requests.get(url)
        response.raise_for_status()

        # Try to get filename from content-disposition header
        content_disp = response.headers.get("content-disposition", "")
        filename = "downloaded_file"
        if "filename=" in content_disp:
            filename = content_disp.split("filename=")[-1].strip('"')

        return response.content, filename


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

        # Initialize resource endpoints
        self.jobs = JobsResource(self)
        self.applications = ApplicationsResource(self)
        self.candidates = CandidatesResource(self)
        self.surveys = SurveysResource(self)
        self.files = FilesResource(self)

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
            message = error_info.get("message") if error_info else str(errors)
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

    # Convenience methods for common operations

    def get_application_with_candidate(self, application_id: str) -> Application:
        """
        Get an application with full candidate details populated.

        Args:
            application_id: The application ID

        Returns:
            Application with candidate field populated
        """
        application = self.applications.get(application_id)
        if application.candidate_id:
            application.candidate = self.candidates.get(application.candidate_id)
        return application

    def download_resume(self, candidate: Candidate) -> Optional[tuple[bytes, str]]:
        """
        Download a candidate's resume if available.

        Args:
            candidate: Candidate object

        Returns:
            Tuple of (file content, filename) or None if no resume
        """
        if not candidate.resume_handle:
            return None
        return self.files.download(candidate.resume_handle)
