# Ashby SDK

[![PyPI version](https://badge.fury.io/py/ashby.svg)](https://badge.fury.io/py/ashby)
[![Python versions](https://img.shields.io/pypi/pyversions/ashby.svg)](https://pypi.org/project/ashby/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the [Ashby](https://www.ashbyhq.com/) ATS (Applicant Tracking System) API.

## Installation

```bash
pip install ashby
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add ashby
```

## Quick Start

```python
from ashby_sdk import AshbyClient

# Initialize client (uses ASHBY_API_KEY from environment)
client = AshbyClient()

# Or provide API key directly
client = AshbyClient(api_key="your-api-key")

# List all open jobs
jobs = client.jobs.list(status=["Open"])
for job in jobs:
    print(f"{job.title} ({job.status})")

# Get candidates for a job
applications = client.applications.list(job_id=jobs[0].id)
for app in applications:
    print(f"{app.candidate_name}: {app.status}")

# Get candidate details
candidate = client.candidates.get(applications[0].candidate_id)
print(f"Email: {candidate.email}")
print(f"Phone: {candidate.phone}")

# Download resume
if candidate.resume_handle:
    content, filename = client.files.download(candidate.resume_handle)
    with open(filename, "wb") as f:
        f.write(content)
```

## Authentication

Set your Ashby API key via environment variable:

```bash
export ASHBY_API_KEY=your-api-key
```

Or use a `.env` file (automatically loaded):

```
ASHBY_API_KEY=your-api-key
```

### Required Permissions

Your API key needs these permissions:

| Module | Permission | Endpoints |
|--------|------------|-----------|
| Jobs | Read | `job.list`, `job.info`, `jobPosting.list`, `jobPosting.info`, `interviewStage.list`, `interviewStage.info`, `opening.list` |
| Candidates | Read | `application.list`, `application.info`, `candidate.list`, `candidate.info`, `candidate.search`, `file.info`, `surveySubmission.list`, `applicationFeedback.list`, `project.list` |
| Candidates | Write | `candidate.createNote` (for notes), `candidate.addTag` (for tagging), `application.changeStage` (for moving candidates) |
| Interviews | Read | `interview.list`, `interview.info`, `interviewSchedule.list` |
| Hiring Process | Read | `source.list`, `archiveReason.list`, `closeReason.list`, `candidateTag.list`, `customField.list`, `hiringTeamRole.list` |
| Organization | Read | `department.list`, `department.info`, `location.list`, `location.info`, `user.list`, `user.info` |
| Offers | Read | `offer.list`, `offer.info` |

## Resources

### Jobs

```python
# List jobs (with optional status filter)
jobs = client.jobs.list()
jobs = client.jobs.list(status=["Open", "Closed"])

# Get job details
job = client.jobs.get(job_id="...")
print(job.title, job.status, job.employment_type)
print(job.hiring_team)  # List of HiringTeamMember
```

### Applications

```python
# List applications
apps = client.applications.list()
apps = client.applications.list(job_id="...")

# Get application details
app = client.applications.get(application_id="...")
print(app.status)        # "Active", "Archived", "Hired"
print(app.stage_name)    # Current interview stage
print(app.candidate_name)

# Get with form submissions expanded
app = client.applications.get_with_forms(application_id="...")
for form in app.form_submissions:
    parsed = client.surveys.parse_submission(form)
    print(parsed["answers"])

# Move candidate to a different stage in the funnel
updated_app = client.applications.change_stage(
    application_id="...",
    interview_stage_id="..."
)
print(f"Moved to: {updated_app.stage_name}")
```

### Interview Stages (Hiring Funnel)

```python
# Get all interview stages for a job
stages = client.interview_stages.list_for_job(job_id="...")
for stage in stages:
    print(f"{stage.name} (order: {stage.order_in_stage_group})")

# Or use convenience method
funnel = client.get_job_funnel(job_id="...")
print("Hiring funnel stages:")
for i, stage in enumerate(funnel, 1):
    print(f"  {i}. {stage.name}")

# Get current stage of an application
current_stage = client.get_application_stage(application_id="...")
print(f"Currently at: {current_stage.name}")

# Move candidate to next stage
client.move_application_to_stage(
    application_id="...",
    interview_stage_id=funnel[2].id  # Move to 3rd stage
)

# Get details about a specific stage
stage = client.interview_stages.get(stage_id="...")
print(f"Stage: {stage.name}, Type: {stage.type}")
```

### Candidates

```python
# List all candidates
candidates = client.candidates.list()

# Get candidate details
candidate = client.candidates.get(candidate_id="...")
print(candidate.name)
print(candidate.email)
print(candidate.phone)
print(candidate.links)       # LinkedIn, portfolio, etc.
print(candidate.tags)
print(candidate.resume_file) # File object with handle

# Search candidates by email or name
results = client.candidates.search(email="john@example.com")
results = client.candidates.search(name="John")
results = client.candidates.search(email="john@example.com", name="John")  # AND

# Add a tag to a candidate
tags = client.candidate_tags.list()
if tags:
    updated = client.candidates.add_tag(candidate_id="...", tag_id=tags[0].id)
```

### Questionnaires / Form Submissions

Ashby stores form responses in two places depending on when candidates applied:

```python
# Method 1: Application form submissions (newer candidates)
app = client.applications.get_with_forms(application_id="...")
for form in app.form_submissions:
    parsed = client.surveys.parse_submission(form)
    for question, answer in parsed["answers"].items():
        print(f"Q: {question}")
        print(f"A: {answer}")

# Method 2: Survey submissions (older candidates)
surveys = client.surveys.get_for_candidate(candidate_id="...")
for survey in surveys:
    parsed = client.surveys.parse_submission(survey)
    print(parsed["answers"])

# List all questionnaire submissions
all_surveys = client.surveys.list(survey_type="Questionnaire")
```

### Files

```python
# Get download URL
url = client.files.get_url(file_handle="...")

# Download file
content, filename = client.files.download(file_handle="...")
with open(filename, "wb") as f:
    f.write(content)

# Download candidate resume
if candidate.resume_handle:
    content, filename = client.files.download(candidate.resume_handle)
```

### Job Postings (Descriptions)

```python
# Get job posting details (includes description)
posting = client.job_postings.get(posting_id="...")
print(posting.title)
print(posting.description_plain)
print(posting.description)  # Prefers plain text, falls back to stripped HTML

# Get posting for a job
posting = client.job_postings.get_for_job(job_id="...")

# Get job description directly (convenience method)
description = client.get_job_description(job_id="...")
print(description)

# List all postings for a job
postings = client.job_postings.list(job_id="...")
```

### Notes

```python
# Create a note on a candidate
note = client.notes.create(
    candidate_id="...",
    note_text="Great candidate, recommend for interview.",
    note_type="text/plain"  # or "text/html"
)
print(note.id)

# Or use convenience method
note = client.create_candidate_note(
    candidate_id="...",
    note_text="Interview scheduled."
)

# List notes for a candidate
notes = client.notes.list(candidate_id="...")
for note in notes:
    print(f"{note.created_at}: {note.content}")
```

### Interview Feedback (Scorecards)

```python
# Get interview feedback/scorecards for an application
feedback_list = client.feedback.list_for_application(application_id="...")
for fb in feedback_list:
    print(f"Submitted by: {fb.submitter.full_name}")
    print(f"Recommendation: {fb.overall_recommendation}")
    print(f"Technical score: {fb.get_score('Technical Skills')}")
```

### Organization Data

```python
# Departments
departments = client.departments.list()
dept = client.departments.get(department_id="...")

# Locations
locations = client.locations.list()
loc = client.locations.get(location_id="...")

# Users (team members)
users = client.users.list()
user = client.users.get(user_id="...")
print(user.full_name, user.email, user.global_role)

# Hiring team roles
roles = client.hiring_team_roles.list()
for role in roles:
    print(role.name)  # e.g., "Hiring Manager", "Recruiter"
```

### Hiring Process Metadata

```python
# Sources (where candidates come from)
sources = client.sources.list()
for source in sources:
    print(f"{source.name} ({source.type})")

# Archive reasons (why candidates were rejected)
archive_reasons = client.archive_reasons.list()
for reason in archive_reasons:
    print(f"{reason.name} - {reason.reason_type}")

# Close reasons (why jobs were closed)
close_reasons = client.close_reasons.list()

# Candidate tags
tags = client.candidate_tags.list()

# Custom field definitions
fields = client.custom_fields.list()
field = client.custom_fields.get(custom_field_id="...")
```

### Other Resources

```python
# Projects (talent pools)
projects = client.projects.list()
project = client.projects.get(project_id="...")

# Offers
offers = client.offers.list()
offer = client.offers.get(offer_id="...")

# Interviews
interviews = client.interviews.list()
interview = client.interviews.get(interview_id="...")

# Interview schedules
schedules = client.interview_schedules.list()
schedule = client.interview_schedules.get(interview_schedule_id="...")
```

## Data Models

All responses are wrapped in typed dataclasses:

| Model | Description |
|-------|-------------|
| `Job` | Job posting with title, status, hiring team |
| `JobPosting` | Job posting details with description |
| `Application` | Job application with status, stage, forms |
| `Candidate` | Candidate with contact info, resume, links |
| `Note` | Candidate note with content and author |
| `File` | File with download handle |
| `InterviewStage` | Pipeline stage |
| `Source` | Application source |
| `ArchiveReason` | Reason for archiving/rejecting candidates |
| `CloseReason` | Reason for closing jobs |
| `Department` | Organization department |
| `Location` | Office location |
| `User` | Team member with role |
| `HiringTeamRole` | Role type (Hiring Manager, Recruiter, etc.) |
| `Project` | Talent pool |
| `Offer` | Job offer |
| `Interview` | Scheduled interview |
| `InterviewSchedule` | Interview schedule |
| `Feedback` | Interview scorecard/feedback |
| `CustomFieldDefinition` | Custom field definition |
| `HiringTeamMember` | Hiring team member |
| `Tag`, `Link`, `CustomField` | Candidate metadata |

All models have a `raw_data` property with the complete API response.

## Error Handling

```python
from ashby_sdk import (
    AshbyClient,
    AshbyAPIError,
    AshbyAuthError,
    AshbyNotFoundError,
)

try:
    client = AshbyClient()
    jobs = client.jobs.list()
except AshbyAuthError as e:
    print(f"Authentication failed: {e}")
except AshbyAPIError as e:
    print(f"API error: {e}")
    print(f"Error codes: {e.errors}")
```

## Pagination

Pagination is handled automatically. All `list()` methods fetch all pages:

```python
# This fetches ALL applications (may be thousands)
applications = client.applications.list(job_id="...")

# Adjust page size if needed
applications = client.applications.list(job_id="...", limit=50)
```

## Development

```bash
# Clone the repo
git clone https://github.com/deepweather/ashby_python_sdk.git
cd ashby_python_sdk

# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Run type checker
uv run mypy .
```

## API Reference

| SDK Method | Ashby Endpoint |
|------------|----------------|
| `client.jobs.list()` | `POST /job.list` |
| `client.jobs.get()` | `POST /job.info` |
| `client.job_postings.list()` | `POST /jobPosting.list` |
| `client.job_postings.get()` | `POST /jobPosting.info` |
| `client.applications.list()` | `POST /application.list` |
| `client.applications.get()` | `POST /application.info` |
| `client.applications.change_stage()` | `POST /application.changeStage` |
| `client.interview_stages.list()` | `POST /interviewStage.list` |
| `client.interview_stages.get()` | `POST /interviewStage.info` |
| `client.candidates.list()` | `POST /candidate.list` |
| `client.candidates.get()` | `POST /candidate.info` |
| `client.candidates.search()` | `POST /candidate.search` |
| `client.candidates.add_tag()` | `POST /candidate.addTag` |
| `client.notes.create()` | `POST /candidate.createNote` |
| `client.notes.list()` | `POST /candidate.listNotes` |
| `client.surveys.list()` | `POST /surveySubmission.list` |
| `client.files.get_url()` | `POST /file.info` |
| `client.feedback.list_for_application()` | `POST /applicationFeedback.list` |
| `client.sources.list()` | `POST /source.list` |
| `client.archive_reasons.list()` | `POST /archiveReason.list` |
| `client.close_reasons.list()` | `POST /closeReason.list` |
| `client.departments.list()` | `POST /department.list` |
| `client.departments.get()` | `POST /department.info` |
| `client.locations.list()` | `POST /location.list` |
| `client.locations.get()` | `POST /location.info` |
| `client.users.list()` | `POST /user.list` |
| `client.users.get()` | `POST /user.info` |
| `client.candidate_tags.list()` | `POST /candidateTag.list` |
| `client.custom_fields.list()` | `POST /customField.list` |
| `client.custom_fields.get()` | `POST /customField.info` |
| `client.projects.list()` | `POST /project.list` |
| `client.projects.get()` | `POST /project.info` |
| `client.offers.list()` | `POST /offer.list` |
| `client.offers.get()` | `POST /offer.info` |
| `client.interviews.list()` | `POST /interview.list` |
| `client.interviews.get()` | `POST /interview.info` |
| `client.interview_schedules.list()` | `POST /interviewSchedule.list` |
| `client.interview_schedules.get()` | `POST /interviewSchedule.info` |
| `client.hiring_team_roles.list()` | `POST /hiringTeamRole.list` |

See [Ashby API Documentation](https://developers.ashbyhq.com/reference) for full API details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [PyPI Package](https://pypi.org/project/ashby/)
- [GitHub Repository](https://github.com/deepweather/ashby_python_sdk)
- [Ashby API Documentation](https://developers.ashbyhq.com/reference)
- [Ashby Website](https://www.ashbyhq.com/)
