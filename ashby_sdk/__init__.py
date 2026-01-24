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
    - client.applications - Job applications
    - client.candidates - Candidate profiles
    - client.surveys - Questionnaire/form submissions
    - client.files - File downloads (resumes, etc.)

For full documentation, see: https://github.com/deepweather/ashby_python_sdk
"""

from .client import AshbyClient
from .models import (
    Job,
    Application,
    Candidate,
    File,
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

__version__ = "0.1.0"

__all__ = [
    # Main client
    "AshbyClient",
    # Models
    "Job",
    "Application",
    "Candidate",
    "File",
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
