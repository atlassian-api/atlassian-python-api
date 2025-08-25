# coding=utf-8
"""
Test cases for Tempo Server API clients using pytest.
"""

import pytest
from unittest.mock import patch

from atlassian.tempo import TempoServer


@pytest.fixture
def tempo_server():
    """Fixture for TempoServer client."""
    return TempoServer(url="https://test.atlassian.net", token="test-token", cloud=False)


class TestTempoServer:
    """Test cases for base TempoServer client."""

    def test_init_defaults(self):
        """Test TempoServer client initialization with default values."""
        tempo = TempoServer(url="https://test.atlassian.net", token="test-token")
        assert tempo.api_version == "1"
        assert tempo.api_root == "rest/tempo-core/1"

    def test_init_custom_values(self):
        """Test TempoServer client initialization with custom values."""
        tempo = TempoServer(
            url="https://test.atlassian.net", token="test-token", api_version="2", api_root="custom/api/root"
        )
        assert tempo.api_version == "2"
        assert tempo.api_root == "custom/api/root"

    def test_specialized_modules_exist(self, tempo_server):
        """Test that specialized modules are properly initialized."""
        assert tempo_server.accounts is not None
        assert tempo_server.teams is not None
        assert tempo_server.planner is not None
        assert tempo_server.budgets is not None
        assert tempo_server.timesheets is not None
        assert tempo_server.servlet is not None
        assert tempo_server.events is not None

    @patch.object(TempoServer, "get")
    def test_get_health(self, mock_get, tempo_server):
        """Test get_health method."""
        mock_get.return_value = {"status": "healthy"}
        result = tempo_server.get_health()
        mock_get.assert_called_once_with("health", **{})
        assert result == {"status": "healthy"}

    @patch.object(TempoServer, "get")
    def test_get_metadata(self, mock_get, tempo_server):
        """Test get_metadata method."""
        mock_get.return_value = {"version": "1.0.0"}
        result = tempo_server.get_metadata()
        mock_get.assert_called_once_with("metadata", **{})
        assert result == {"version": "1.0.0"}


class TestTempoServerAccounts:
    """Test cases for TempoServer accounts module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_accounts(self, mock_get, tempo_server):
        """Test get_accounts method."""
        mock_get.return_value = [{"id": 1, "name": "Test Account"}]
        result = tempo_server.accounts.get_accounts()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "name": "Test Account"}]

    @patch.object(TempoServer, "get")
    def test_get_account(self, mock_get, tempo_server):
        """Test get_account method."""
        mock_get.return_value = {"id": 1, "name": "Test Account"}
        result = tempo_server.accounts.get_account(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "name": "Test Account"}


class TestTempoServerTeams:
    """Test cases for TempoServer teams module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_teams(self, mock_get, tempo_server):
        """Test get_teams method."""
        mock_get.return_value = [{"id": 1, "name": "Test Team"}]
        result = tempo_server.teams.get_teams()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "name": "Test Team"}]

    @patch.object(TempoServer, "get")
    def test_get_team(self, mock_get, tempo_server):
        """Test get_team method."""
        mock_get.return_value = {"id": 1, "name": "Test Team"}
        result = tempo_server.teams.get_team(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "name": "Test Team"}


class TestTempoServerPlanner:
    """Test cases for TempoServer planner module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_plans(self, mock_get, tempo_server):
        """Test get_plans method."""
        mock_get.return_value = [{"id": 1, "name": "Test Plan"}]
        result = tempo_server.planner.get_plans()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "name": "Test Plan"}]

    @patch.object(TempoServer, "get")
    def test_get_plan(self, mock_get, tempo_server):
        """Test get_plan method."""
        mock_get.return_value = {"id": 1, "name": "Test Plan"}
        result = tempo_server.planner.get_plan(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "name": "Test Plan"}


class TestTempoServerBudgets:
    """Test cases for TempoServer budgets module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_budgets(self, mock_get, tempo_server):
        """Test get_budgets method."""
        mock_get.return_value = [{"id": 1, "name": "Test Budget"}]
        result = tempo_server.budgets.get_budgets()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "name": "Test Budget"}]

    @patch.object(TempoServer, "get")
    def test_get_budget(self, mock_get, tempo_server):
        """Test get_budget method."""
        mock_get.return_value = {"id": 1, "name": "Test Budget"}
        result = tempo_server.budgets.get_budget(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "name": "Test Budget"}


class TestTempoServerTimesheets:
    """Test cases for TempoServer timesheets module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_timesheets(self, mock_get, tempo_server):
        """Test get_timesheets method."""
        mock_get.return_value = [{"id": 1, "name": "Test Timesheet"}]
        result = tempo_server.timesheets.get_timesheets()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "name": "Test Timesheet"}]

    @patch.object(TempoServer, "get")
    def test_get_timesheet(self, mock_get, tempo_server):
        """Test get_timesheet method."""
        mock_get.return_value = {"id": 1, "name": "Test Timesheet"}
        result = tempo_server.timesheets.get_timesheet(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "name": "Test Timesheet"}


class TestTempoServerServlet:
    """Test cases for TempoServer servlet module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_worklogs(self, mock_get, tempo_server):
        """Test get_worklogs method."""
        mock_get.return_value = [{"id": 1, "timeSpentSeconds": 3600}]
        result = tempo_server.servlet.get_worklogs()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "timeSpentSeconds": 3600}]

    @patch.object(TempoServer, "get")
    def test_get_worklog(self, mock_get, tempo_server):
        """Test get_worklog method."""
        mock_get.return_value = {"id": 1, "timeSpentSeconds": 3600}
        result = tempo_server.servlet.get_worklog(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "timeSpentSeconds": 3600}


class TestTempoServerEvents:
    """Test cases for TempoServer events module."""

    @pytest.fixture
    def tempo_server(self):
        """Fixture for TempoServer client."""
        return TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_events(self, mock_get, tempo_server):
        """Test get_events method."""
        mock_get.return_value = [{"id": 1, "type": "worklog_created"}]
        result = tempo_server.events.get_events()
        mock_get.assert_called_once_with("", **{})
        assert result == [{"id": 1, "type": "worklog_created"}]

    @patch.object(TempoServer, "get")
    def test_get_event(self, mock_get, tempo_server):
        """Test get_event method."""
        mock_get.return_value = {"id": 1, "type": "worklog_created"}
        result = tempo_server.events.get_event(1)
        mock_get.assert_called_once_with("1", **{})
        assert result == {"id": 1, "type": "worklog_created"}
