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
    - client.candidates - Candidate profiles (with search and add_tag)
    - client.interview_stages - Interview stages/hiring funnel
    - client.surveys - Questionnaire/form submissions
    - client.files - File downloads (resumes, etc.)
    - client.job_postings - Job posting details with descriptions
    - client.notes - Candidate notes
    - client.feedback - Interview feedback/scorecards
    - client.sources - Candidate sources
    - client.archive_reasons - Archive/rejection reasons
    - client.close_reasons - Job close reasons
    - client.departments - Organization departments
    - client.locations - Office locations
    - client.users - Team members
    - client.candidate_tags - Candidate tags
    - client.custom_fields - Custom field definitions
    - client.projects - Talent pools
    - client.offers - Job offers
    - client.interviews - Scheduled interviews
    - client.interview_schedules - Interview schedules
    - client.hiring_team_roles - Hiring team roles

Convenience Methods:
    - client.get_job_funnel(job_id) - Get all stages for a job
    - client.get_application_stage(app_id) - Get current stage
    - client.move_application_to_stage(app_id, stage_id) - Move candidate in funnel

For full documentation, see: https://github.com/deepweather/ashby_python_sdk
"""

from .client import AshbyClient
from .models import (
    Application,
    ApplicationFormSubmission,
    ArchiveReason,
    Candidate,
    CloseReason,
    CustomField,
    CustomFieldDefinition,
    Department,
    EmailAddress,
    Feedback,
    File,
    HiringTeamMember,
    HiringTeamRole,
    Interview,
    InterviewSchedule,
    InterviewStage,
    Job,
    JobPosting,
    Link,
    Location,
    Note,
    Offer,
    PhoneNumber,
    Project,
    Source,
    Tag,
    User,
)
from .exceptions import (
    AshbyError,
    AshbyAPIError,
    AshbyAuthError,
    AshbyNotFoundError,
    AshbyRateLimitError,
)

__version__ = "0.4.1"

__all__ = [
    # Main client
    "AshbyClient",
    # Core models
    "Job",
    "JobPosting",
    "Application",
    "Candidate",
    "File",
    "Note",
    "ApplicationFormSubmission",
    "InterviewStage",
    # New models (v0.4.0)
    "Source",
    "ArchiveReason",
    "CloseReason",
    "Department",
    "Location",
    "User",
    "HiringTeamRole",
    "CustomFieldDefinition",
    "Project",
    "Offer",
    "Interview",
    "InterviewSchedule",
    "Feedback",
    # Metadata models
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
