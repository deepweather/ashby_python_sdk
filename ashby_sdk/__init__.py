"""
Ashby SDK - Python client for the Ashby ATS API.

A clean, typed Python SDK for interacting with the Ashby Applicant Tracking System API.

Basic Usage:
    >>> from ashby_sdk import AshbyClient
    >>> client = AshbyClient()  # Uses ASHBY_API_KEY env var
    >>> jobs = client.jobs.list(status=["Open"])
    >>> for job in jobs:
    ...     print(job.title)

Resources:
    - client.jobs - Job postings
    - client.applications - Job applications (with change_stage support)
    - client.candidates - Candidate profiles
    - client.interview_stages - Interview stages/hiring funnel
    - client.surveys - Questionnaire/form submissions
    - client.files - File downloads (resumes, etc.)
    - client.job_postings - Job posting details with descriptions
    - client.notes - Candidate notes

Convenience Methods:
    - client.get_job_funnel(job_id) - Get all stages for a job
    - client.get_application_stage(app_id) - Get current stage
    - client.move_application_to_stage(app_id, stage_id) - Move candidate in funnel

For full documentation, see: https://github.com/deepweather/ashby_python_sdk
"""

from .client import AshbyClient
from .models import (
    Job,
    JobPosting,
    Application,
    Candidate,
    File,
    Note,
    ApplicationFormSubmission,
    InterviewStage,
    Source,
    User,
    HiringTeamMember,
    Tag,
    Link,
    CustomField,
    EmailAddress,
    PhoneNumber,
)
from .exceptions import (
    AshbyError,
    AshbyAPIError,
    AshbyAuthError,
    AshbyNotFoundError,
    AshbyRateLimitError,
)

__version__ = "0.3.0"

__all__ = [
    # Main client
    "AshbyClient",
    # Models
    "Job",
    "JobPosting",
    "Application",
    "Candidate",
    "File",
    "Note",
    "ApplicationFormSubmission",
    "InterviewStage",
    "Source",
    "User",
    "HiringTeamMember",
    "Tag",
    "Link",
    "CustomField",
    "EmailAddress",
    "PhoneNumber",
    # Exceptions
    "AshbyError",
    "AshbyAPIError",
    "AshbyAuthError",
    "AshbyNotFoundError",
    "AshbyRateLimitError",
]
