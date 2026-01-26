"""API resource classes."""

from .base import BaseResource
from .generic import GenericResource
from .jobs import JobsResource
from .applications import ApplicationsResource
from .candidates import CandidatesResource
from .interview_stages import InterviewStagesResource
from .surveys import SurveysResource
from .files import FilesResource
from .job_postings import JobPostingsResource
from .notes import NotesResource
from .feedback import FeedbackResource

__all__ = [
    "BaseResource",
    "GenericResource",
    "JobsResource",
    "ApplicationsResource",
    "CandidatesResource",
    "InterviewStagesResource",
    "SurveysResource",
    "FilesResource",
    "JobPostingsResource",
    "NotesResource",
    "FeedbackResource",
]
