"""
Data models for Ashby API responses.

These are lightweight dataclasses that wrap API responses
and provide convenient access to common fields.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class User:
    """Represents a user in Ashby."""

    id: str
    first_name: str
    last_name: str
    email: str
    global_role: Optional[str] = None
    is_enabled: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id", ""),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            email=data.get("email", ""),
            global_role=data.get("globalRole"),
            is_enabled=data.get("isEnabled"),
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class HiringTeamMember:
    """A member of a job's hiring team."""

    user_id: str
    first_name: str
    last_name: str
    email: str
    role: str

    @classmethod
    def from_dict(cls, data: dict) -> "HiringTeamMember":
        return cls(
            user_id=data.get("userId", ""),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            email=data.get("email", ""),
            role=data.get("role", ""),
        )


@dataclass
class Department:
    """Represents a department."""

    id: str
    name: str
    parent_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            parent_id=data.get("parentId"),
        )


@dataclass
class Location:
    """Represents a location."""

    id: str
    name: str
    is_remote: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Location":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            is_remote=data.get("isRemote", False),
        )


@dataclass
class File:
    """Represents a file (resume, attachment, etc.)."""

    id: str
    name: str
    handle: str

    @classmethod
    def from_dict(cls, data: dict) -> "File":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            handle=data.get("handle", ""),
        )

    @classmethod
    def from_handle_obj(cls, data: dict) -> Optional["File"]:
        """Create from a resumeFileHandle object."""
        if not data:
            return None
        if isinstance(data, str):
            return cls(id="", name="", handle=data)
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            handle=data.get("handle", ""),
        )


@dataclass
class InterviewStage:
    """Represents an interview stage."""

    id: str
    name: str
    order_in_stage_group: Optional[int] = None
    stage_group_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional["InterviewStage"]:
        if not data:
            return None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            order_in_stage_group=data.get("orderInStageGroup"),
            stage_group_id=data.get("stageGroupId"),
        )


@dataclass
class Source:
    """Represents a candidate source."""

    id: str
    name: str
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Source"]:
        if not data:
            return None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=data.get("type"),
        )


@dataclass
class Tag:
    """Represents a candidate tag."""

    id: str
    title: str

    @classmethod
    def from_dict(cls, data: dict) -> "Tag":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
        )


@dataclass
class EmailAddress:
    """Represents an email address."""

    value: str
    type: str
    is_primary: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Optional["EmailAddress"]:
        if not data:
            return None
        return cls(
            value=data.get("value", ""),
            type=data.get("type", ""),
            is_primary=data.get("isPrimary", False),
        )


@dataclass
class PhoneNumber:
    """Represents a phone number."""

    value: str
    type: str
    is_primary: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Optional["PhoneNumber"]:
        if not data:
            return None
        return cls(
            value=data.get("value", ""),
            type=data.get("type", ""),
            is_primary=data.get("isPrimary", False),
        )


@dataclass
class Link:
    """Represents a candidate link (LinkedIn, portfolio, etc.)."""

    url: str
    type: str

    @classmethod
    def from_dict(cls, data: dict) -> "Link":
        return cls(
            url=data.get("url", ""),
            type=data.get("type", ""),
        )


@dataclass
class CustomField:
    """Represents a custom field value."""

    id: str
    title: str
    value: Any

    @classmethod
    def from_dict(cls, data: dict) -> "CustomField":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            value=data.get("value"),
        )


@dataclass
class FormFieldSubmission:
    """A single field submission in an application form."""

    field_id: str
    field_title: str
    field_type: str
    value: Any
    
    @classmethod
    def from_dict(cls, data: dict) -> "FormFieldSubmission":
        field_info = data.get("field", {})
        return cls(
            field_id=field_info.get("id", ""),
            field_title=field_info.get("title", ""),
            field_type=field_info.get("type", ""),
            value=data.get("value"),
        )


@dataclass
class ApplicationFormSubmission:
    """Application form submission data."""

    id: str
    fields: list[FormFieldSubmission] = field(default_factory=list)
    raw_data: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> Optional["ApplicationFormSubmission"]:
        if not data:
            return None
        fields = [
            FormFieldSubmission.from_dict(f)
            for f in data.get("formSubmissionValue", [])
        ]
        return cls(
            id=data.get("id", ""),
            fields=fields,
            raw_data=data,
        )

    def get_field_value(self, field_title: str) -> Any:
        """Get a field value by title (case-insensitive)."""
        title_lower = field_title.lower()
        for field in self.fields:
            if field.field_title.lower() == title_lower:
                return field.value
        return None


@dataclass
class Job:
    """Represents a job posting."""

    id: str
    title: str
    status: str
    confidential: bool = False
    employment_type: Optional[str] = None
    department_id: Optional[str] = None
    location_id: Optional[str] = None
    hiring_team: list[HiringTeamMember] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    opened_at: Optional[str] = None
    closed_at: Optional[str] = None
    raw_data: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Job":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            status=data.get("status", ""),
            confidential=data.get("confidential", False),
            employment_type=data.get("employmentType"),
            department_id=data.get("departmentId"),
            location_id=data.get("locationId"),
            hiring_team=[
                HiringTeamMember.from_dict(m) for m in data.get("hiringTeam", [])
            ],
            custom_fields=[
                CustomField.from_dict(f) for f in data.get("customFields", [])
            ],
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
            opened_at=data.get("openedAt"),
            closed_at=data.get("closedAt"),
            raw_data=data,
        )


@dataclass
class Candidate:
    """Represents a candidate."""

    id: str
    name: str
    primary_email: Optional[EmailAddress] = None
    primary_phone: Optional[PhoneNumber] = None
    resume_file: Optional[File] = None
    links: list[Link] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    raw_data: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Candidate":
        resume_file = File.from_handle_obj(data.get("resumeFileHandle"))
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            primary_email=EmailAddress.from_dict(data.get("primaryEmailAddress")),
            primary_phone=PhoneNumber.from_dict(data.get("primaryPhoneNumber")),
            resume_file=resume_file,
            links=[Link.from_dict(link) for link in data.get("links", [])],
            tags=[Tag.from_dict(tag) for tag in data.get("tags", [])],
            custom_fields=[
                CustomField.from_dict(f) for f in data.get("customFields", [])
            ],
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
            raw_data=data,
        )

    @property
    def email(self) -> Optional[str]:
        return self.primary_email.value if self.primary_email else None

    @property
    def phone(self) -> Optional[str]:
        return self.primary_phone.value if self.primary_phone else None

    @property
    def resume_handle(self) -> Optional[str]:
        return self.resume_file.handle if self.resume_file else None


@dataclass
class Application:
    """Represents a job application."""

    id: str
    status: str
    candidate_id: str
    candidate_name: str
    job_id: str
    is_archived: bool = False
    archive_reason: Optional[str] = None
    current_stage: Optional[InterviewStage] = None
    source: Optional[Source] = None
    form_submission: Optional[ApplicationFormSubmission] = None
    form_submissions: list = field(default_factory=list)  # Expanded applicationFormSubmissions
    credited_to: Optional[User] = None
    hired_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    raw_data: dict = field(default_factory=dict)
    
    # Populated when fetching full details
    candidate: Optional[Candidate] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Application":
        candidate_data = data.get("candidate", {})
        archive_reason = data.get("archiveReason")
        if isinstance(archive_reason, dict):
            archive_reason = archive_reason.get("name")
            
        return cls(
            id=data.get("id", ""),
            status=data.get("status", ""),
            candidate_id=candidate_data.get("id", ""),
            candidate_name=candidate_data.get("name", ""),
            job_id=data.get("jobId", ""),
            is_archived=data.get("isArchived", False),
            archive_reason=archive_reason,
            current_stage=InterviewStage.from_dict(data.get("currentInterviewStage")),
            source=Source.from_dict(data.get("source")),
            form_submission=ApplicationFormSubmission.from_dict(
                data.get("applicationFormSubmission")
            ),
            form_submissions=data.get("applicationFormSubmissions", []),
            credited_to=User.from_dict(data["creditedTo"]) if data.get("creditedTo") else None,
            hired_at=data.get("hiredAt"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
            raw_data=data,
        )

    @property
    def stage_name(self) -> Optional[str]:
        return self.current_stage.name if self.current_stage else None

    @property
    def has_form_data(self) -> bool:
        """Check if application has any form submission data."""
        return bool(self.form_submissions) or bool(self.form_submission)
