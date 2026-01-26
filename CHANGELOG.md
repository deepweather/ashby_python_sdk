# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-01-26

### Added

- Generic resource system for easy addition of new endpoints
- New resources via generic pattern:
  - `client.sources` - List candidate sources
  - `client.archive_reasons` - List archive/rejection reasons
  - `client.close_reasons` - List job close reasons
  - `client.departments` - List/get departments
  - `client.locations` - List/get locations
  - `client.users` - List/get team members
  - `client.candidate_tags` - List candidate tags
  - `client.custom_fields` - List/get custom field definitions
  - `client.projects` - List/get talent pools
  - `client.offers` - List/get offers
  - `client.interviews` - List/get interviews
  - `client.interview_schedules` - List/get interview schedules
  - `client.hiring_team_roles` - List hiring team roles
- `client.feedback` resource for interview scorecards
  - `list_for_application(application_id)` - Get feedback for an application
- New candidate methods:
  - `client.candidates.search(email, name)` - Search candidates
  - `client.candidates.add_tag(candidate_id, tag_id)` - Add tag to candidate
- New models: `ArchiveReason`, `CloseReason`, `Project`, `Offer`, `Interview`, `InterviewSchedule`, `HiringTeamRole`, `CustomFieldDefinition`, `Feedback`
- Mock tests using `responses` library
- Integration tests with real API (skipped if no API key)
- Test markers: `@pytest.mark.integration`, `@pytest.mark.writes`

### Changed

- `HiringTeamRole` model now handles both string and dict responses from API

## [0.3.0] - 2025-01-24

### Added

- `client.interview_stages` resource for hiring funnel stages
  - `list(job_id)` - List all interview stages, optionally filtered by job
  - `get(stage_id)` - Get a specific interview stage by ID
  - `list_for_job(job_id)` - Get all stages for a job's interview plan (sorted)
- `applications.change_stage(application_id, interview_stage_id)` - Move application to a different stage
- Convenience methods on `AshbyClient`:
  - `get_job_funnel(job_id)` - Get all interview stages for a job
  - `get_application_stage(application_id)` - Get current stage of an application
  - `move_application_to_stage(application_id, stage_id)` - Move candidate through funnel
- Enhanced `InterviewStage` model with additional fields (`type`, `interview_plan_id`, `stage_group_name`, `raw_data`)

## [0.2.0] - 2025-01-25

### Added

- `client.job_postings` resource for job posting details
  - `get(posting_id)` - Get a job posting by ID
  - `list(job_id)` - List job postings, optionally filtered by job
  - `get_for_job(job_id)` - Get the primary posting for a job
  - `get_description(job_id)` - Get plain text job description
- `client.notes` resource for candidate notes
  - `create(candidate_id, note_text)` - Create a note on a candidate
  - `list(candidate_id)` - List notes for a candidate
- `JobPosting` model with description fields (`description_plain`, `description_html`)
- `Note` model for candidate notes
- Convenience methods on `AshbyClient`:
  - `get_job_description(job_id)` - Get job description directly
  - `create_candidate_note(candidate_id, text)` - Create a note directly
- `job_posting_ids` field on `Job` model

## [0.1.0] - 2025-01-24

### Added

- Initial release
- `AshbyClient` for API authentication and requests
- `client.jobs` resource for job listings and details
- `client.applications` resource for application management
- `client.candidates` resource for candidate profiles
- `client.surveys` resource for questionnaire/form submissions
- `client.files` resource for file downloads (resumes, etc.)
- Typed data models: `Job`, `Application`, `Candidate`, `File`, etc.
- Automatic pagination for list endpoints
- Support for both `applicationFormSubmissions` and `surveySubmission` data sources
- Custom exceptions: `AshbyError`, `AshbyAPIError`, `AshbyAuthError`, `AshbyNotFoundError`
- Full type hints with `py.typed` marker
- Automatic `.env` file loading for API key

[Unreleased]: https://github.com/deepweather/ashby_python_sdk/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/deepweather/ashby_python_sdk/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/deepweather/ashby_python_sdk/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/deepweather/ashby_python_sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/deepweather/ashby_python_sdk/releases/tag/v0.1.0
