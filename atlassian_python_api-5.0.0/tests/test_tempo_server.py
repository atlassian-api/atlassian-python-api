# coding=utf-8
"""
Test cases for Tempo Server API clients.
"""

import unittest
from unittest.mock import patch

from atlassian.tempo import TempoServer


class TestTempoServer(unittest.TestCase):
    """Test cases for base TempoServer client."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token", cloud=False)

    def test_init_defaults(self):
        """Test TempoServer client initialization with default values."""
        tempo = TempoServer(url="https://test.atlassian.net", token="test-token")
        self.assertEqual(tempo.api_version, "1")
        self.assertEqual(tempo.api_root, "rest/tempo-core/1")

    def test_init_custom_values(self):
        """Test TempoServer client initialization with custom values."""
        tempo = TempoServer(
            url="https://test.atlassian.net", token="test-token", api_version="2", api_root="custom/api/root"
        )
        self.assertEqual(tempo.api_version, "2")
        self.assertEqual(tempo.api_root, "custom/api/root")

    def test_specialized_modules_exist(self):
        """Test that specialized modules are properly initialized."""
        self.assertIsNotNone(self.tempo.accounts)
        self.assertIsNotNone(self.tempo.teams)
        self.assertIsNotNone(self.tempo.planner)
        self.assertIsNotNone(self.tempo.budgets)
        self.assertIsNotNone(self.tempo.timesheets)
        self.assertIsNotNone(self.tempo.servlet)
        self.assertIsNotNone(self.tempo.events)

    @patch.object(TempoServer, "get")
    def test_get_health(self, mock_get):
        """Test get_health method."""
        mock_get.return_value = {"status": "healthy"}
        result = self.tempo.get_health()
        mock_get.assert_called_once_with("health", **{})
        self.assertEqual(result, {"status": "healthy"})

    @patch.object(TempoServer, "get")
    def test_get_metadata(self, mock_get):
        """Test get_metadata method."""
        mock_get.return_value = {"version": "1.0.0"}
        result = self.tempo.get_metadata()
        mock_get.assert_called_once_with("metadata", **{})
        self.assertEqual(result, {"version": "1.0.0"})


class TestTempoServerAccounts(unittest.TestCase):
    """Test cases for TempoServer accounts module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_accounts(self, mock_get):
        """Test get_accounts method."""
        mock_get.return_value = [{"id": 1, "name": "Test Account"}]
        result = self.tempo.accounts.get_accounts()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "name": "Test Account"}])

    @patch.object(TempoServer, "get")
    def test_get_account(self, mock_get):
        """Test get_account method."""
        mock_get.return_value = {"id": 1, "name": "Test Account"}
        result = self.tempo.accounts.get_account(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "name": "Test Account"})


class TestTempoServerTeams(unittest.TestCase):
    """Test cases for TempoServer teams module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_teams(self, mock_get):
        """Test get_teams method."""
        mock_get.return_value = [{"id": 1, "name": "Test Team"}]
        result = self.tempo.teams.get_teams()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "name": "Test Team"}])

    @patch.object(TempoServer, "get")
    def test_get_team(self, mock_get):
        """Test get_team method."""
        mock_get.return_value = {"id": 1, "name": "Test Team"}
        result = self.tempo.teams.get_team(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "name": "Test Team"})


class TestTempoServerPlanner(unittest.TestCase):
    """Test cases for TempoServer planner module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_plans(self, mock_get):
        """Test get_plans method."""
        mock_get.return_value = [{"id": 1, "name": "Test Plan"}]
        result = self.tempo.planner.get_plans()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "name": "Test Plan"}])

    @patch.object(TempoServer, "get")
    def test_get_plan(self, mock_get):
        """Test get_plan method."""
        mock_get.return_value = {"id": 1, "name": "Test Plan"}
        result = self.tempo.planner.get_plan(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "name": "Test Plan"})


class TestTempoServerBudgets(unittest.TestCase):
    """Test cases for TempoServer budgets module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_budgets(self, mock_get):
        """Test get_budgets method."""
        mock_get.return_value = [{"id": 1, "name": "Test Budget"}]
        result = self.tempo.budgets.get_budgets()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "name": "Test Budget"}])

    @patch.object(TempoServer, "get")
    def test_get_budget(self, mock_get):
        """Test get_budget method."""
        mock_get.return_value = {"id": 1, "name": "Test Budget"}
        result = self.tempo.budgets.get_budget(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "name": "Test Budget"})


class TestTempoServerTimesheets(unittest.TestCase):
    """Test cases for TempoServer timesheets module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_timesheets(self, mock_get):
        """Test get_timesheets method."""
        mock_get.return_value = [{"id": 1, "name": "Test Timesheet"}]
        result = self.tempo.timesheets.get_timesheets()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "name": "Test Timesheet"}])

    @patch.object(TempoServer, "get")
    def test_get_timesheet(self, mock_get):
        """Test get_timesheet method."""
        mock_get.return_value = {"id": 1, "name": "Test Timesheet"}
        result = self.tempo.timesheets.get_timesheet(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "name": "Test Timesheet"})


class TestTempoServerServlet(unittest.TestCase):
    """Test cases for TempoServer servlet module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_worklogs(self, mock_get):
        """Test get_worklogs method."""
        mock_get.return_value = [{"id": 1, "timeSpentSeconds": 3600}]
        result = self.tempo.servlet.get_worklogs()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "timeSpentSeconds": 3600}])

    @patch.object(TempoServer, "get")
    def test_get_worklog(self, mock_get):
        """Test get_worklog method."""
        mock_get.return_value = {"id": 1, "timeSpentSeconds": 3600}
        result = self.tempo.servlet.get_worklog(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "timeSpentSeconds": 3600})


class TestTempoServerEvents(unittest.TestCase):
    """Test cases for TempoServer events module."""

    def setUp(self):
        """Set up test fixtures."""
        self.tempo = TempoServer(url="https://test.atlassian.net", token="test-token")

    @patch.object(TempoServer, "get")
    def test_get_events(self, mock_get):
        """Test get_events method."""
        mock_get.return_value = [{"id": 1, "type": "worklog_created"}]
        result = self.tempo.events.get_events()
        mock_get.assert_called_once_with("", **{})
        self.assertEqual(result, [{"id": 1, "type": "worklog_created"}])

    @patch.object(TempoServer, "get")
    def test_get_event(self, mock_get):
        """Test get_event method."""
        mock_get.return_value = {"id": 1, "type": "worklog_created"}
        result = self.tempo.events.get_event(1)
        mock_get.assert_called_once_with("1", **{})
        self.assertEqual(result, {"id": 1, "type": "worklog_created"})


if __name__ == "__main__":
    unittest.main()
