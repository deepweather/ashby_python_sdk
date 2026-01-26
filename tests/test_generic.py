"""
Mock tests for the Ashby SDK generic resources and new endpoints.

These tests use the `responses` library to mock HTTP requests,
allowing us to test the SDK without making real API calls.

Run with: pytest tests/test_generic.py
"""

import pytest
import responses

from ashby_sdk import AshbyClient
from ashby_sdk.models import (
    ArchiveReason,
    Candidate,
    CloseReason,
    CustomFieldDefinition,
    Department,
    Feedback,
    HiringTeamRole,
    Interview,
    InterviewSchedule,
    Location,
    Offer,
    Project,
    Source,
    Tag,
    User,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_client():
    """Create an Ashby client with a fake API key for testing."""
    return AshbyClient(api_key="test_api_key_12345")


# ---------------------------------------------------------------------------
# Generic Resource Tests - List Only Endpoints
# ---------------------------------------------------------------------------


class TestSourcesResource:
    """Tests for the sources (list-only) resource."""

    @responses.activate
    def test_list_sources(self, mock_client):
        """Test listing all sources."""
        responses.post(
            "https://api.ashbyhq.com/source.list",
            json={
                "success": True,
                "results": [
                    {"id": "src_1", "name": "LinkedIn", "type": "Sourcing"},
                    {"id": "src_2", "name": "Referral", "type": "Referral"},
                ],
                "moreDataAvailable": False,
            },
        )

        sources = mock_client.sources.list()
        
        assert len(sources) == 2
        assert isinstance(sources[0], Source)
        assert sources[0].id == "src_1"
        assert sources[0].name == "LinkedIn"
        assert sources[1].name == "Referral"

    @responses.activate
    def test_sources_get_not_supported(self, mock_client):
        """Test that get() raises NotImplementedError for sources."""
        with pytest.raises(NotImplementedError, match="does not support .info"):
            mock_client.sources.get("src_1")


class TestArchiveReasonsResource:
    """Tests for the archive_reasons resource."""

    @responses.activate
    def test_list_archive_reasons(self, mock_client):
        """Test listing archive reasons."""
        responses.post(
            "https://api.ashbyhq.com/archiveReason.list",
            json={
                "success": True,
                "results": [
                    {"id": "ar_1", "text": "Not qualified", "reasonType": "Rejection"},
                    {"id": "ar_2", "text": "Withdrew", "reasonType": "Withdrawal"},
                ],
                "moreDataAvailable": False,
            },
        )

        reasons = mock_client.archive_reasons.list()
        
        assert len(reasons) == 2
        assert isinstance(reasons[0], ArchiveReason)
        assert reasons[0].name == "Not qualified"
        assert reasons[1].reason_type == "Withdrawal"


class TestCandidateTagsResource:
    """Tests for the candidate_tags resource."""

    @responses.activate
    def test_list_candidate_tags(self, mock_client):
        """Test listing candidate tags."""
        responses.post(
            "https://api.ashbyhq.com/candidateTag.list",
            json={
                "success": True,
                "results": [
                    {"id": "tag_1", "title": "VIP"},
                    {"id": "tag_2", "title": "Urgent"},
                ],
                "moreDataAvailable": False,
            },
        )

        tags = mock_client.candidate_tags.list()
        
        assert len(tags) == 2
        assert isinstance(tags[0], Tag)
        assert tags[0].title == "VIP"


# ---------------------------------------------------------------------------
# Generic Resource Tests - List + Get Endpoints
# ---------------------------------------------------------------------------


class TestDepartmentsResource:
    """Tests for the departments resource (list + get)."""

    @responses.activate
    def test_list_departments(self, mock_client):
        """Test listing departments."""
        responses.post(
            "https://api.ashbyhq.com/department.list",
            json={
                "success": True,
                "results": [
                    {"id": "dept_1", "name": "Engineering", "parentId": None},
                    {"id": "dept_2", "name": "Frontend", "parentId": "dept_1"},
                ],
                "moreDataAvailable": False,
            },
        )

        depts = mock_client.departments.list()
        
        assert len(depts) == 2
        assert isinstance(depts[0], Department)
        assert depts[0].name == "Engineering"
        assert depts[1].parent_id == "dept_1"

    @responses.activate
    def test_get_department(self, mock_client):
        """Test getting a single department."""
        responses.post(
            "https://api.ashbyhq.com/department.info",
            json={
                "success": True,
                "results": {"id": "dept_1", "name": "Engineering", "parentId": None},
            },
        )

        dept = mock_client.departments.get("dept_1")
        
        assert isinstance(dept, Department)
        assert dept.id == "dept_1"
        assert dept.name == "Engineering"


class TestLocationsResource:
    """Tests for the locations resource."""

    @responses.activate
    def test_list_locations(self, mock_client):
        """Test listing locations."""
        responses.post(
            "https://api.ashbyhq.com/location.list",
            json={
                "success": True,
                "results": [
                    {"id": "loc_1", "name": "San Francisco", "isRemote": False},
                    {"id": "loc_2", "name": "Remote", "isRemote": True},
                ],
                "moreDataAvailable": False,
            },
        )

        locations = mock_client.locations.list()
        
        assert len(locations) == 2
        assert locations[0].is_remote is False
        assert locations[1].is_remote is True


class TestUsersResource:
    """Tests for the users resource."""

    @responses.activate
    def test_list_users(self, mock_client):
        """Test listing users."""
        responses.post(
            "https://api.ashbyhq.com/user.list",
            json={
                "success": True,
                "results": [
                    {
                        "id": "user_1",
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "john@example.com",
                        "globalRole": "Admin",
                        "isEnabled": True,
                    }
                ],
                "moreDataAvailable": False,
            },
        )

        users = mock_client.users.list()
        
        assert len(users) == 1
        assert isinstance(users[0], User)
        assert users[0].full_name == "John Doe"
        assert users[0].global_role == "Admin"


class TestProjectsResource:
    """Tests for the projects (talent pools) resource."""

    @responses.activate
    def test_list_projects(self, mock_client):
        """Test listing projects."""
        responses.post(
            "https://api.ashbyhq.com/project.list",
            json={
                "success": True,
                "results": [
                    {"id": "proj_1", "name": "ML Engineers Pool", "isArchived": False},
                ],
                "moreDataAvailable": False,
            },
        )

        projects = mock_client.projects.list()
        
        assert len(projects) == 1
        assert isinstance(projects[0], Project)
        assert projects[0].name == "ML Engineers Pool"


class TestOffersResource:
    """Tests for the offers resource."""

    @responses.activate
    def test_list_offers(self, mock_client):
        """Test listing offers."""
        responses.post(
            "https://api.ashbyhq.com/offer.list",
            json={
                "success": True,
                "results": [
                    {
                        "id": "offer_1",
                        "applicationId": "app_1",
                        "status": "Sent",
                        "startDate": "2024-02-01",
                    }
                ],
                "moreDataAvailable": False,
            },
        )

        offers = mock_client.offers.list()
        
        assert len(offers) == 1
        assert isinstance(offers[0], Offer)
        assert offers[0].status == "Sent"


# ---------------------------------------------------------------------------
# Candidate Search and Add Tag Tests
# ---------------------------------------------------------------------------


class TestCandidateSearch:
    """Tests for candidate search functionality."""

    @responses.activate
    def test_search_by_email(self, mock_client):
        """Test searching candidates by email."""
        responses.post(
            "https://api.ashbyhq.com/candidate.search",
            json={
                "success": True,
                "results": [
                    {"id": "cand_1", "name": "John Doe"},
                ],
            },
        )

        candidates = mock_client.candidates.search(email="john@example.com")
        
        assert len(candidates) == 1
        assert isinstance(candidates[0], Candidate)
        assert candidates[0].name == "John Doe"

    @responses.activate
    def test_search_by_name(self, mock_client):
        """Test searching candidates by name."""
        responses.post(
            "https://api.ashbyhq.com/candidate.search",
            json={
                "success": True,
                "results": [
                    {"id": "cand_1", "name": "John Doe"},
                    {"id": "cand_2", "name": "John Smith"},
                ],
            },
        )

        candidates = mock_client.candidates.search(name="John")
        
        assert len(candidates) == 2

    @responses.activate
    def test_search_by_email_and_name(self, mock_client):
        """Test searching candidates by both email and name."""
        responses.post(
            "https://api.ashbyhq.com/candidate.search",
            json={
                "success": True,
                "results": [{"id": "cand_1", "name": "John Doe"}],
            },
        )

        candidates = mock_client.candidates.search(
            email="john@example.com", name="John"
        )
        
        assert len(candidates) == 1

    def test_search_requires_parameter(self, mock_client):
        """Test that search requires at least one parameter."""
        with pytest.raises(ValueError, match="At least one of email or name"):
            mock_client.candidates.search()


class TestCandidateAddTag:
    """Tests for adding tags to candidates."""

    @responses.activate
    def test_add_tag_to_candidate(self, mock_client):
        """Test adding a tag to a candidate."""
        responses.post(
            "https://api.ashbyhq.com/candidate.addTag",
            json={
                "success": True,
                "results": {
                    "id": "cand_1",
                    "name": "John Doe",
                    "tags": [{"id": "tag_1", "title": "VIP"}],
                },
            },
        )

        candidate = mock_client.candidates.add_tag("cand_1", "tag_1")
        
        assert isinstance(candidate, Candidate)
        assert len(candidate.tags) == 1
        assert candidate.tags[0].title == "VIP"


# ---------------------------------------------------------------------------
# Feedback Resource Tests
# ---------------------------------------------------------------------------


class TestFeedbackResource:
    """Tests for the feedback (scorecards) resource."""

    @responses.activate
    def test_list_feedback_for_application(self, mock_client):
        """Test listing feedback for an application."""
        responses.post(
            "https://api.ashbyhq.com/applicationFeedback.list",
            json={
                "success": True,
                "results": [
                    {
                        "id": "fb_1",
                        "applicationId": "app_1",
                        "interviewId": "int_1",
                        "submittedAt": "2024-01-15T10:00:00Z",
                        "submitter": {
                            "id": "user_1",
                            "firstName": "Jane",
                            "lastName": "Recruiter",
                            "email": "jane@example.com",
                        },
                        "submittedValues": [
                            {
                                "field": {"title": "Overall Recommendation"},
                                "value": "Strong Hire",
                            },
                            {
                                "field": {"title": "Technical Skills"},
                                "value": 4,
                            },
                        ],
                    }
                ],
            },
        )

        feedback_list = mock_client.feedback.list_for_application("app_1")
        
        assert len(feedback_list) == 1
        fb = feedback_list[0]
        assert isinstance(fb, Feedback)
        assert fb.application_id == "app_1"
        assert fb.overall_recommendation == "Strong Hire"
        assert fb.get_score("Technical Skills") == 4
        assert fb.submitter.full_name == "Jane Recruiter"


# ---------------------------------------------------------------------------
# Pagination Tests
# ---------------------------------------------------------------------------


class TestPagination:
    """Tests for pagination handling in generic resources."""

    @responses.activate
    def test_pagination_fetches_all_pages(self, mock_client):
        """Test that list() fetches all pages."""
        # First page
        responses.post(
            "https://api.ashbyhq.com/source.list",
            json={
                "success": True,
                "results": [{"id": "src_1", "name": "LinkedIn"}],
                "moreDataAvailable": True,
                "nextCursor": "cursor_1",
            },
        )
        # Second page
        responses.post(
            "https://api.ashbyhq.com/source.list",
            json={
                "success": True,
                "results": [{"id": "src_2", "name": "Referral"}],
                "moreDataAvailable": False,
            },
        )

        sources = mock_client.sources.list()
        
        assert len(sources) == 2
        assert sources[0].name == "LinkedIn"
        assert sources[1].name == "Referral"
        # Verify two requests were made
        assert len(responses.calls) == 2


# ---------------------------------------------------------------------------
# Error Handling Tests
# ---------------------------------------------------------------------------


class TestErrorHandling:
    """Tests for error handling."""

    @responses.activate
    def test_api_error(self, mock_client):
        """Test handling of API errors."""
        from ashby_sdk.exceptions import AshbyAPIError
        
        responses.post(
            "https://api.ashbyhq.com/source.list",
            json={
                "success": False,
                "errors": ["invalid_request"],
                "errorInfo": {"message": "Invalid request"},
            },
        )

        with pytest.raises(AshbyAPIError, match="Invalid request"):
            mock_client.sources.list()

    @responses.activate
    def test_auth_error_401(self, mock_client):
        """Test handling of 401 authentication error."""
        from ashby_sdk.exceptions import AshbyAuthError
        
        responses.post(
            "https://api.ashbyhq.com/source.list",
            status=401,
        )

        with pytest.raises(AshbyAuthError, match="Invalid or missing API key"):
            mock_client.sources.list()

    @responses.activate
    def test_auth_error_403(self, mock_client):
        """Test handling of 403 permission error."""
        from ashby_sdk.exceptions import AshbyAuthError
        
        responses.post(
            "https://api.ashbyhq.com/source.list",
            status=403,
        )

        with pytest.raises(AshbyAuthError, match="does not have permission"):
            mock_client.sources.list()
