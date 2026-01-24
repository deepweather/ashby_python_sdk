# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/deepweather/ashby_python_sdk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/deepweather/ashby_python_sdk/releases/tag/v0.1.0
