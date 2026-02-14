"""Tests for the Ashby SDK client."""

import pytest
from unittest.mock import patch, MagicMock

from ashby_sdk import AshbyClient, AshbyAuthError, AshbyAPIError
from ashby_sdk.models import Job, Application, Candidate


class TestAshbyClientInit:
    """Tests for client initialization."""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        client = AshbyClient(api_key="test-key")
        assert client.api_key == "test-key"

    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises error."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(AshbyAuthError):
                AshbyClient(api_key=None)

    def test_init_from_env_var(self):
        """Test initialization from environment variable."""
        with patch.dict("os.environ", {"ASHBY_API_KEY": "env-key"}):
            client = AshbyClient()
            assert client.api_key == "env-key"


class TestJobsResource:
    """Tests for the jobs resource."""

    @pytest.fixture
    def client(self):
        return AshbyClient(api_key="test-key")

    @pytest.fixture
    def mock_response(self):
        return {
            "success": True,
            "results": [
                {
                    "id": "job-123",
                    "title": "Software Engineer",
                    "status": "Open",
                    "employmentType": "FullTime",
                }
            ],
            "moreDataAvailable": False,
        }

    def test_list_jobs(self, client, mock_response):
        """Test listing jobs."""
        with patch.object(client, "_request", return_value=mock_response):
            jobs = client.jobs.list()
            assert len(jobs) == 1
            assert isinstance(jobs[0], Job)
            assert jobs[0].title == "Software Engineer"

    def test_list_jobs_with_status_filter(self, client, mock_response):
        """Test listing jobs with status filter."""
        with patch.object(client, "_request", return_value=mock_response) as mock:
            client.jobs.list(status=["Open", "Closed"])
            call_args = mock.call_args[0]
            assert call_args[1]["status"] == ["Open", "Closed"]


class TestModels:
    """Tests for data models."""

    def test_job_from_dict(self):
        """Test Job model creation from dict."""
        data = {
            "id": "job-123",
            "title": "Engineer",
            "status": "Open",
            "employmentType": "FullTime",
            "hiringTeam": [
                {
                    "userId": "user-1",
                    "firstName": "John",
                    "lastName": "Doe",
                    "email": "john@example.com",
                    "role": "Hiring Manager",
                }
            ],
        }
        job = Job.from_dict(data)
        assert job.id == "job-123"
        assert job.title == "Engineer"
        assert job.status == "Open"
        assert len(job.hiring_team) == 1
        assert job.hiring_team[0].first_name == "John"

    def test_candidate_from_dict(self):
        """Test Candidate model creation from dict."""
        data = {
            "id": "cand-123",
            "name": "Jane Smith",
            "primaryEmailAddress": {"value": "jane@example.com", "type": "Work"},
            "primaryPhoneNumber": {"value": "+1234567890", "type": "Mobile"},
            "resumeFileHandle": {
                "id": "file-1",
                "name": "resume.pdf",
                "handle": "abc123",
            },
            "links": [{"url": "https://linkedin.com/in/jane", "type": "LinkedIn"}],
            "tags": [{"id": "tag-1", "title": "Senior"}],
        }
        candidate = Candidate.from_dict(data)
        assert candidate.id == "cand-123"
        assert candidate.name == "Jane Smith"
        assert candidate.email == "jane@example.com"
        assert candidate.phone == "+1234567890"
        assert candidate.resume_handle == "abc123"
        assert len(candidate.links) == 1
        assert len(candidate.tags) == 1

    def test_application_from_dict(self):
        """Test Application model creation from dict."""
        data = {
            "id": "app-123",
            "status": "Active",
            "candidate": {"id": "cand-1", "name": "John Doe"},
            "jobId": "job-1",
            "isArchived": False,
            "currentInterviewStage": {"id": "stage-1", "name": "Phone Screen"},
            "source": {"id": "src-1", "name": "LinkedIn"},
            "createdAt": "2025-01-01T00:00:00Z",
        }
        app = Application.from_dict(data)
        assert app.id == "app-123"
        assert app.status == "Active"
        assert app.candidate_name == "John Doe"
        assert app.stage_name == "Phone Screen"
        assert app.source.name == "LinkedIn"


class TestSurveysParsing:
    """Tests for survey/form submission parsing."""

    @pytest.fixture
    def client(self):
        return AshbyClient(api_key="test-key")

    def test_parse_submission(self, client):
        """Test parsing survey submission."""
        survey = {
            "submittedAt": "2025-01-01T00:00:00Z",
            "candidateId": "cand-123",
            "applicationId": "app-123",
            "surveyType": "Questionnaire",
            "formDefinition": {
                "sections": [
                    {
                        "fields": [
                            {
                                "field": {
                                    "id": "field-1",
                                    "title": "What is your notice period?",
                                    "path": "field-1",
                                }
                            }
                        ]
                    }
                ]
            },
            "submittedValues": {"field-1": "2 weeks"},
        }

        parsed = client.surveys.parse_submission(survey)
        assert parsed["candidate_id"] == "cand-123"
        assert "What is your notice period?" in parsed["answers"]
        assert parsed["answers"]["What is your notice period?"] == "2 weeks"

    def test_parse_submission_with_boolean(self, client):
        """Test parsing submission with boolean value."""
        survey = {
            "formDefinition": {
                "sections": [
                    {
                        "fields": [
                            {"field": {"id": "f1", "title": "Remote OK?", "path": "f1"}}
                        ]
                    }
                ]
            },
            "submittedValues": {"f1": True},
        }

        parsed = client.surveys.parse_submission(survey)
        assert parsed["answers"]["Remote OK?"] == "Yes"


class TestJobPostingsGetForJob:
    """Tests for job posting selection when multiple postings exist."""

    @pytest.fixture
    def client(self):
        return AshbyClient(api_key="test-key")

    def _make_posting_dict(self, posting_id, title, job_id, updated_at):
        return {
            "id": posting_id,
            "title": title,
            "jobId": job_id,
            "locationIds": {},
            "isListed": True,
            "isLive": True,
            "employmentType": "FullTime",
            "updatedAt": updated_at,
        }

    def _make_full_posting_dict(self, posting_id, title, job_id, description):
        return {
            "id": posting_id,
            "title": title,
            "jobId": job_id,
            "locationIds": {},
            "isListed": True,
            "isLive": True,
            "employmentType": "FullTime",
            "descriptionPlain": description,
        }

    def test_single_posting_returns_it(self, client):
        """With one posting, it should be returned directly."""
        list_resp = {
            "success": True,
            "results": [
                self._make_posting_dict("p1", "Engineer", "job-1", "2026-01-01T00:00:00Z"),
            ],
            "moreDataAvailable": False,
        }
        get_resp = {
            "success": True,
            "results": self._make_full_posting_dict("p1", "Engineer", "job-1", "desc"),
        }
        with patch.object(client, "_request", side_effect=[list_resp, get_resp]):
            posting = client.job_postings.get_for_job("job-1")
            assert posting is not None
            assert posting.id == "p1"

    def test_multiple_postings_matches_by_title(self, client):
        """With multiple postings, the one matching job_title should win."""
        list_resp = {
            "success": True,
            "results": [
                self._make_posting_dict("p-wrong", "Customer Success Manager", "job-1", "2026-01-01T00:00:00Z"),
                self._make_posting_dict("p-right", "Key Account Manager", "job-1", "2026-01-02T00:00:00Z"),
            ],
            "moreDataAvailable": False,
        }
        get_resp = {
            "success": True,
            "results": self._make_full_posting_dict("p-right", "Key Account Manager", "job-1", "KAM desc"),
        }
        with patch.object(client, "_request", side_effect=[list_resp, get_resp]):
            posting = client.job_postings.get_for_job("job-1", job_title="Key Account Manager")
            assert posting is not None
            assert posting.id == "p-right"
            assert posting.title == "Key Account Manager"

    def test_multiple_postings_no_title_match_falls_back_to_newest(self, client):
        """Without a title match, the most recently updated posting should be returned."""
        list_resp = {
            "success": True,
            "results": [
                self._make_posting_dict("p-old", "Old Title", "job-1", "2026-01-01T00:00:00Z"),
                self._make_posting_dict("p-new", "New Title", "job-1", "2026-01-10T00:00:00Z"),
            ],
            "moreDataAvailable": False,
        }
        get_resp = {
            "success": True,
            "results": self._make_full_posting_dict("p-new", "New Title", "job-1", "newest desc"),
        }
        with patch.object(client, "_request", side_effect=[list_resp, get_resp]):
            posting = client.job_postings.get_for_job("job-1", job_title="Nonexistent Title")
            assert posting is not None
            assert posting.id == "p-new"

    def test_multiple_postings_no_title_given_falls_back_to_newest(self, client):
        """Without job_title param, the most recently updated posting should be returned."""
        list_resp = {
            "success": True,
            "results": [
                self._make_posting_dict("p-old", "Title A", "job-1", "2026-01-01T00:00:00Z"),
                self._make_posting_dict("p-new", "Title B", "job-1", "2026-01-10T00:00:00Z"),
            ],
            "moreDataAvailable": False,
        }
        get_resp = {
            "success": True,
            "results": self._make_full_posting_dict("p-new", "Title B", "job-1", "B desc"),
        }
        with patch.object(client, "_request", side_effect=[list_resp, get_resp]):
            posting = client.job_postings.get_for_job("job-1")
            assert posting is not None
            assert posting.id == "p-new"

    def test_get_description_resolves_title_automatically(self, client):
        """get_description should look up the job title and match the right posting."""
        # 1st call: job.info -> returns job with title "Key Account Manager"
        job_info_resp = {
            "success": True,
            "results": {
                "id": "job-1",
                "title": "Key Account Manager",
                "status": "Open",
            },
        }
        # 2nd call: jobPosting.list -> returns two postings
        list_resp = {
            "success": True,
            "results": [
                self._make_posting_dict("p-wrong", "Customer Success Manager", "job-1", "2026-01-01T00:00:00Z"),
                self._make_posting_dict("p-right", "Key Account Manager", "job-1", "2026-01-02T00:00:00Z"),
            ],
            "moreDataAvailable": False,
        }
        # 3rd call: jobPosting.info -> returns the matched posting with description
        get_resp = {
            "success": True,
            "results": self._make_full_posting_dict("p-right", "Key Account Manager", "job-1", "The KAM JD"),
        }
        with patch.object(client, "_request", side_effect=[job_info_resp, list_resp, get_resp]):
            description = client.job_postings.get_description("job-1")
            assert description == "The KAM JD"

    def test_no_postings_returns_none(self, client):
        """With no postings, None should be returned."""
        list_resp = {
            "success": True,
            "results": [],
            "moreDataAvailable": False,
        }
        with patch.object(client, "_request", return_value=list_resp):
            posting = client.job_postings.get_for_job("job-1")
            assert posting is None
