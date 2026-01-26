"""
Pytest configuration and shared fixtures for Ashby SDK tests.

This file configures:
1. Custom markers for test categorization
2. Shared fixtures used across test modules
3. Test collection and reporting settings
"""

import pytest


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests requiring real API (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers",
        "writes: marks tests that write/modify data in Ashby (use with caution)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically skip integration tests unless explicitly requested.
    
    This prevents accidentally running integration tests when running
    the full test suite.
    """
    # Check if we're running integration tests explicitly
    markers = config.getoption("-m", default="")
    
    # If 'integration' is not in the marker expression and we're not 
    # running all tests explicitly, skip integration tests
    if "integration" not in markers and markers != "":
        skip_integration = pytest.mark.skip(
            reason="Integration tests not selected (use -m integration)"
        )
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


# ---------------------------------------------------------------------------
# Shared Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def api_key():
    """
    Provide a test API key for mock tests.
    
    This is NOT a real API key - it's just used for testing the client
    initialization without making real API calls.
    """
    return "test_api_key_for_mock_tests_only"
