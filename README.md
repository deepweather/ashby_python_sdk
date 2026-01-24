# Ashby SDK

[![PyPI version](https://badge.fury.io/py/ashby-sdk.svg)](https://badge.fury.io/py/ashby-sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/ashby-sdk.svg)](https://pypi.org/project/ashby-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the [Ashby](https://www.ashbyhq.com/) ATS (Applicant Tracking System) API.

## Installation

```bash
pip install ashby-sdk
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add ashby-sdk
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
| Jobs | Read | `job.list`, `job.info` |
| Candidates | Read | `application.list`, `application.info`, `candidate.info`, `file.info`, `surveySubmission.list` |

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

## Data Models

All responses are wrapped in typed dataclasses:

| Model | Description |
|-------|-------------|
| `Job` | Job posting with title, status, hiring team |
| `Application` | Job application with status, stage, forms |
| `Candidate` | Candidate with contact info, resume, links |
| `File` | File with download handle |
| `InterviewStage` | Pipeline stage |
| `Source` | Application source |
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
| `client.applications.list()` | `POST /application.list` |
| `client.applications.get()` | `POST /application.info` |
| `client.candidates.list()` | `POST /candidate.list` |
| `client.candidates.get()` | `POST /candidate.info` |
| `client.surveys.list()` | `POST /surveySubmission.list` |
| `client.files.get_url()` | `POST /file.info` |

See [Ashby API Documentation](https://developers.ashbyhq.com/reference) for full API details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [PyPI Package](https://pypi.org/project/ashby-sdk/)
- [GitHub Repository](https://github.com/deepweather/ashby_python_sdk)
- [Ashby API Documentation](https://developers.ashbyhq.com/reference)
- [Ashby Website](https://www.ashbyhq.com/)
