"""
Integration tests for the Ashby SDK using real API calls.

These tests require a valid ASHBY_API_KEY environment variable.
They are designed to:
1. Be non-destructive (mostly read-only operations)
2. Clean up any resources they create
3. Use existing resources where possible

Run with:
    pytest tests/test_integration.py -m integration
    
Run only safe (read-only) tests:
    pytest tests/test_integration.py -m "integration and not writes"
"""

import os
import pytest

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


@pytest.fixture(scope="module")
def live_client():
    """
    Create a real Ashby client for integration tests.
    
    Skips if ASHBY_API_KEY is not set.
    Uses module scope to reuse the client across tests.
    """
    api_key = os.getenv("ASHBY_API_KEY")
    if not api_key:
        pytest.skip("ASHBY_API_KEY not set - skipping integration tests")
    return AshbyClient(api_key=api_key)


@pytest.fixture(scope="module")
def sample_candidate_id(live_client):
    """Get a sample candidate ID for tests that need one."""
    candidates = live_client.candidates.list(limit=1)
    if not candidates:
        pytest.skip("No candidates found in Ashby - skipping test")
    return candidates[0].id


@pytest.fixture(scope="module")
def sample_application_id(live_client):
    """Get a sample application ID for tests that need one."""
    applications = live_client.applications.list(limit=1)
    if not applications:
        pytest.skip("No applications found in Ashby - skipping test")
    return applications[0].id


# ---------------------------------------------------------------------------
# Read-Only Tests (Safe to run)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestSourcesIntegration:
    """Integration tests for sources resource."""

    def test_list_sources(self, live_client):
        """Test listing sources from real API."""
        sources = live_client.sources.list()
        
        assert isinstance(sources, list)
        # Most Ashby instances have at least one source
        if sources:
            assert isinstance(sources[0], Source)
            assert sources[0].id
            assert sources[0].name


@pytest.mark.integration
class TestArchiveReasonsIntegration:
    """Integration tests for archive_reasons resource."""

    def test_list_archive_reasons(self, live_client):
        """Test listing archive reasons from real API."""
        reasons = live_client.archive_reasons.list()
        
        assert isinstance(reasons, list)
        if reasons:
            assert isinstance(reasons[0], ArchiveReason)
            assert reasons[0].id
            assert reasons[0].name


@pytest.mark.integration
class TestCloseReasonsIntegration:
    """Integration tests for close_reasons resource."""

    def test_list_close_reasons(self, live_client):
        """Test listing close reasons from real API."""
        reasons = live_client.close_reasons.list()
        
        assert isinstance(reasons, list)
        if reasons:
            assert isinstance(reasons[0], CloseReason)


@pytest.mark.integration
class TestCandidateTagsIntegration:
    """Integration tests for candidate_tags resource."""

    def test_list_candidate_tags(self, live_client):
        """Test listing candidate tags from real API."""
        tags = live_client.candidate_tags.list()
        
        assert isinstance(tags, list)
        if tags:
            assert isinstance(tags[0], Tag)
            assert tags[0].id
            assert tags[0].title


@pytest.mark.integration
class TestDepartmentsIntegration:
    """Integration tests for departments resource."""

    def test_list_departments(self, live_client):
        """Test listing departments from real API."""
        depts = live_client.departments.list()
        
        assert isinstance(depts, list)
        if depts:
            assert isinstance(depts[0], Department)
            assert depts[0].id
            assert depts[0].name

    def test_get_department(self, live_client):
        """Test getting a single department."""
        depts = live_client.departments.list(limit=1)
        if not depts:
            pytest.skip("No departments found")
        
        dept = live_client.departments.get(depts[0].id)
        assert dept.id == depts[0].id


@pytest.mark.integration
class TestLocationsIntegration:
    """Integration tests for locations resource."""

    def test_list_locations(self, live_client):
        """Test listing locations from real API."""
        locations = live_client.locations.list()
        
        assert isinstance(locations, list)
        if locations:
            assert isinstance(locations[0], Location)
            assert locations[0].id
            assert locations[0].name


@pytest.mark.integration
class TestUsersIntegration:
    """Integration tests for users resource."""

    def test_list_users(self, live_client):
        """Test listing users from real API."""
        users = live_client.users.list()
        
        assert isinstance(users, list)
        # Every Ashby instance should have at least one user
        assert len(users) >= 1
        assert isinstance(users[0], User)
        assert users[0].id
        assert users[0].email


@pytest.mark.integration
class TestCustomFieldsIntegration:
    """Integration tests for custom_fields resource."""

    def test_list_custom_fields(self, live_client):
        """Test listing custom fields from real API."""
        fields = live_client.custom_fields.list()
        
        assert isinstance(fields, list)
        if fields:
            assert isinstance(fields[0], CustomFieldDefinition)
            assert fields[0].id
            assert fields[0].title


@pytest.mark.integration
class TestProjectsIntegration:
    """Integration tests for projects resource."""

    def test_list_projects(self, live_client):
        """Test listing projects from real API."""
        projects = live_client.projects.list()
        
        assert isinstance(projects, list)
        if projects:
            assert isinstance(projects[0], Project)


@pytest.mark.integration
class TestOffersIntegration:
    """Integration tests for offers resource."""

    def test_list_offers(self, live_client):
        """Test listing offers from real API."""
        offers = live_client.offers.list()
        
        assert isinstance(offers, list)
        if offers:
            assert isinstance(offers[0], Offer)


@pytest.mark.integration
class TestInterviewsIntegration:
    """Integration tests for interviews resource."""

    def test_list_interviews(self, live_client):
        """Test listing interviews from real API."""
        interviews = live_client.interviews.list()
        
        assert isinstance(interviews, list)
        if interviews:
            assert isinstance(interviews[0], Interview)


@pytest.mark.integration
class TestInterviewSchedulesIntegration:
    """Integration tests for interview_schedules resource."""

    def test_list_interview_schedules(self, live_client):
        """Test listing interview schedules from real API."""
        schedules = live_client.interview_schedules.list()
        
        assert isinstance(schedules, list)
        if schedules:
            assert isinstance(schedules[0], InterviewSchedule)


@pytest.mark.integration
class TestHiringTeamRolesIntegration:
    """Integration tests for hiring_team_roles resource."""

    def test_list_hiring_team_roles(self, live_client):
        """Test listing hiring team roles from real API."""
        roles = live_client.hiring_team_roles.list()
        
        assert isinstance(roles, list)
        if roles:
            assert isinstance(roles[0], HiringTeamRole)


# ---------------------------------------------------------------------------
# Candidate Search Tests (Read-Only)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestCandidateSearchIntegration:
    """Integration tests for candidate search."""

    def test_search_by_name(self, live_client, sample_candidate_id):
        """Test searching candidates by name."""
        # Get the sample candidate's name
        candidate = live_client.candidates.get(sample_candidate_id)
        name_part = candidate.name.split()[0] if candidate.name else None
        
        if not name_part:
            pytest.skip("Sample candidate has no name")
        
        # Search for candidates with that name
        results = live_client.candidates.search(name=name_part)
        
        assert isinstance(results, list)
        # Should find at least the original candidate
        assert len(results) >= 1

    def test_search_by_email(self, live_client, sample_candidate_id):
        """Test searching candidates by email."""
        candidate = live_client.candidates.get(sample_candidate_id)
        
        if not candidate.email:
            pytest.skip("Sample candidate has no email")
        
        results = live_client.candidates.search(email=candidate.email)
        
        assert isinstance(results, list)
        assert len(results) >= 1
        # The search should return the same candidate
        assert any(c.id == candidate.id for c in results)


# ---------------------------------------------------------------------------
# Feedback Tests (Read-Only)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestFeedbackIntegration:
    """Integration tests for feedback resource."""

    def test_list_feedback_for_application(self, live_client, sample_application_id):
        """Test listing feedback for an application."""
        feedback_list = live_client.feedback.list_for_application(sample_application_id)
        
        assert isinstance(feedback_list, list)
        # Feedback may or may not exist for this application
        if feedback_list:
            fb = feedback_list[0]
            assert isinstance(fb, Feedback)
            assert fb.application_id == sample_application_id


# ---------------------------------------------------------------------------
# Write Tests (These modify data - use with caution)
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.writes
class TestCandidateAddTagIntegration:
    """
    Integration tests for adding tags to candidates.
    
    WARNING: These tests modify data. They are designed to be safe:
    - Only adds tags that already exist (doesn't create new tags)
    - Only uses existing candidates
    - Tags are generally harmless metadata
    
    CLEANUP NOTE: The Ashby API does NOT have a candidate.removeTag endpoint,
    so tags added by this test cannot be automatically cleaned up.
    The test prints what was added so you can manually remove it if needed.
    
    Run with: pytest tests/test_integration.py -m "integration and writes"
    Skip with: pytest tests/test_integration.py -m "integration and not writes"
    """

    def test_add_existing_tag_to_candidate(self, live_client, sample_candidate_id):
        """Test adding an existing tag to a candidate."""
        # Get available tags
        tags = live_client.candidate_tags.list()
        if not tags:
            pytest.skip("No tags available in Ashby")
        
        # Get the candidate's current tags
        candidate = live_client.candidates.get(sample_candidate_id)
        existing_tag_ids = {t.id for t in candidate.tags}
        
        # Find a tag that's not already on the candidate
        new_tag = None
        for tag in tags:
            if tag.id not in existing_tag_ids:
                new_tag = tag
                break
        
        if not new_tag:
            pytest.skip("All tags already on candidate - no cleanup needed")
        
        # Log what we're about to do for manual cleanup reference
        print(f"\n[CLEANUP INFO] Adding tag '{new_tag.title}' (id: {new_tag.id}) "
              f"to candidate '{candidate.name}' (id: {sample_candidate_id})")
        print(f"[CLEANUP INFO] To manually remove: Go to candidate in Ashby UI and remove the tag")
        
        # Add the tag
        updated = live_client.candidates.add_tag(sample_candidate_id, new_tag.id)
        
        assert isinstance(updated, Candidate)
        # Verify the tag was added
        updated_tag_ids = {t.id for t in updated.tags}
        assert new_tag.id in updated_tag_ids, "Tag was not added to candidate"


# ---------------------------------------------------------------------------
# Backward Compatibility Tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestBackwardCompatibility:
    """Tests to ensure existing SDK methods still work."""

    def test_jobs_list(self, live_client):
        """Test that jobs.list() still works."""
        jobs = live_client.jobs.list()
        assert isinstance(jobs, list)

    def test_candidates_list(self, live_client):
        """Test that candidates.list() still works."""
        candidates = live_client.candidates.list(limit=5)
        assert isinstance(candidates, list)

    def test_applications_list(self, live_client):
        """Test that applications.list() still works."""
        applications = live_client.applications.list(limit=5)
        assert isinstance(applications, list)

    def test_interview_stages_list(self, live_client):
        """Test that interview_stages work."""
        jobs = live_client.jobs.list(status=["Open"], limit=1)
        if not jobs:
            pytest.skip("No open jobs found")
        
        stages = live_client.interview_stages.list_for_job(jobs[0].id)
        assert isinstance(stages, list)
