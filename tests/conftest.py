# coding=utf-8
"""
Pytest configuration and fixtures for Tempo tests.
"""

import pytest
from unittest.mock import Mock, patch

# Import mockup server for testing
from .mockup import mockup_server


@pytest.fixture(scope="session")
def mock_server_url():
    """Fixture providing the mock server URL."""
    return mockup_server()


@pytest.fixture
def mock_response():
    """Fixture providing a mock response object."""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"success": True}
    mock_resp.text = '{"success": true}'
    mock_resp.content = b'{"success": true}'
    return mock_resp


@pytest.fixture
def mock_session():
    """Fixture providing a mock session object."""
    with patch("requests.Session") as mock_session:
        mock_session.return_value.request.return_value = Mock()
        yield mock_session


@pytest.fixture
def tempo_cloud_client():
    """Fixture providing a TempoCloud client for testing."""
    from atlassian.tempo import TempoCloud

    return TempoCloud(url="https://test.atlassian.net", token="test-token", cloud=True)


@pytest.fixture
def tempo_server_client():
    """Fixture providing a TempoServer client for testing."""
    from atlassian.tempo import TempoServer

    return TempoServer(url="https://test.atlassian.net", token="test-token", cloud=False)
