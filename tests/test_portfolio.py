# coding=utf-8
"""
Test cases for Portfolio API client.
"""

import unittest
from unittest.mock import patch

from atlassian.portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    """Test cases for Portfolio client initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(
            plan_id="PLAN-001",
            url="https://api.atlassian.com",
            token="test-token",
        )

    def test_init(self):
        """Test Portfolio client initialization."""
        self.assertEqual(self.portfolio.plan_id, "PLAN-001")


class TestPortfolioPlanOperations(unittest.TestCase):
    """Test cases for Portfolio plan operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(
            plan_id="PLAN-001",
            url="https://api.atlassian.com",
            token="test-token",
        )

    @patch.object(Portfolio, "get")
    def test_get_plan(self, mock_get):
        """Test get_plan method."""
        mock_get.return_value = {"name": "Test Plan", "id": "PLAN-001"}
        result = self.portfolio.get_plan()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001.json")
        self.assertEqual(result["name"], "Test Plan")

    @patch.object(Portfolio, "get")
    def test_get_stages(self, mock_get):
        """Test get_stages method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Stage 1"}]}
        result = self.portfolio.get_stages()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/stages.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_teams(self, mock_get):
        """Test get_teams method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Team 1"}]}
        result = self.portfolio.get_teams()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/teams.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_config(self, mock_get):
        """Test get_config method."""
        mock_get.return_value = {"configuration": {"key": "value"}}
        result = self.portfolio.get_config()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/config.json")
        self.assertEqual(result["configuration"]["key"], "value")

    @patch.object(Portfolio, "get")
    def test_get_persons(self, mock_get):
        """Test get_persons method."""
        mock_get.return_value = {"collection": [{"id": "1", "name": "Person 1"}]}
        result = self.portfolio.get_persons()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/persons.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_streams(self, mock_get):
        """Test get_streams method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Stream 1"}]}
        result = self.portfolio.get_streams()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/streams.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_releases(self, mock_get):
        """Test get_releases method (delegates to get_streams)."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Release 1"}]}
        result = self.portfolio.get_releases()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/streams.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_themes(self, mock_get):
        """Test get_themes method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Theme 1"}]}
        result = self.portfolio.get_themes()
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/themes.json")
        self.assertEqual(len(result["collection"]), 1)

    @patch.object(Portfolio, "get")
    def test_get_state(self, mock_get):
        """Test get_state method."""
        mock_get.return_value = {"status": "active"}
        result = self.portfolio.get_state()
        mock_get.assert_called_once_with("rest/roadmap/1.0/scheduling/PLAN-001/state.json")
        self.assertEqual(result["status"], "active")


class TestPortfolioFilters(unittest.TestCase):
    """Test cases for Portfolio filter operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(
            plan_id="PLAN-001",
            url="https://api.atlassian.com",
            token="test-token",
        )

    @patch.object(Portfolio, "get")
    def test_get_filters(self, mock_get):
        """Test get_filters method."""
        mock_get.return_value = [{"id": "1", "name": "Filter 1"}]
        result = self.portfolio.get_filters("test query")
        mock_get.assert_called_once_with(
            "rest/roadmap/1.0/system/filters.json", params={"queryString": "test query"}
        )
        self.assertEqual(len(result), 1)

    @patch.object(Portfolio, "get")
    def test_get_dependencies(self, mock_get):
        """Test get_dependencies method."""
        mock_get.return_value = [{"id": "1", "type": "blocks"}]
        result = self.portfolio.get_dependencies("WI-001", "1.0")
        mock_get.assert_called_once_with("rest/roadmap/1.0/workitems/WI-001/dependencies.json?planVersion=1.0")
        self.assertEqual(len(result), 1)

    @patch.object(Portfolio, "post")
    def test_get_filter(self, mock_post):
        """Test get_filter method."""
        mock_post.return_value = {"data": {"items": [{"id": "1", "title": "Item 1"}]}}
        result = self.portfolio.get_filter(limit=100)
        mock_post.assert_called_once_with(
            "rest/roadmap/1.0/plans/PLAN-001/workitems/filter.json",
            data={"limit": 100},
        )
        self.assertEqual(len(result), 1)

    @patch.object(Portfolio, "post")
    def test_get_jql_issues(self, mock_post):
        """Test get_jql_issues method."""
        mock_post.return_value = {"data": {"items": [{"key": "JIRA-001"}]}}
        result = self.portfolio.get_jql_issues("project = TEST")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "rest/roadmap/1.0/system/import.json")
        data = call_args[1]["data"]
        self.assertEqual(data["planId"], "PLAN-001")
        self.assertEqual(data["query"], "project = TEST")
        self.assertEqual(data["maxResults"], 500)
        self.assertEqual(len(result), 1)


class TestPortfolioEpic(unittest.TestCase):
    """Test cases for Portfolio epic operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(
            plan_id="PLAN-001",
            url="https://api.atlassian.com",
            token="test-token",
        )

    @patch.object(Portfolio, "get")
    def test_get_team_name(self, mock_get):
        """Test get_team_name method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Team 1"}]}
        result = self.portfolio.get_team_name("1")
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/teams.json")
        self.assertEqual(result, "Team 1")

    @patch.object(Portfolio, "get")
    def test_get_stage_name(self, mock_get):
        """Test get_stage_name method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Stage 1"}]}
        result = self.portfolio.get_stage_name("1")
        mock_get.assert_called_once_with("rest/roadmap/1.0/plans/PLAN-001/stages.json")
        self.assertEqual(result, "Stage 1")

    @patch.object(Portfolio, "get")
    def test_get_estimates_dict(self, mock_get):
        """Test get_estimates_dict method."""
        mock_get.return_value = {"collection": [{"id": "1", "title": "Stage 1"}]}
        estimates = {
            "stages": [
                {"targetId": "1", "value": 10},
            ]
        }
        result = self.portfolio.get_estimates_dict(estimates)
        self.assertEqual(result["Stage 1"], 10)

    @patch.object(Portfolio, "get")
    def test_get_epic(self, mock_get):
        """Test get_epic method."""
        # Mock get_stages for stage name lookup in estimates
        mock_get.return_value = {
            "collection": [
                {"id": "1", "title": "Development"},
            ]
        }
        epic = {
            "title": "Test Epic",
            "description": "Epic description",
            "estimates": {
                "stages": [
                    {"targetId": "1", "value": 5},
                ]
            },
            "links": [{"link": "PROJ-123"}],
            "teamId": "1",
        }
        result = self.portfolio.get_epic(epic)
        self.assertEqual(result["title"], "Test Epic")
        self.assertEqual(result["issuekey"], "PROJ-123")
        self.assertEqual(result["team"], "Development")
        self.assertIn("Total", result["estimates"])
        self.assertEqual(result["estimates"]["Total"], 5)


class TestPortfolioImport(unittest.TestCase):
    """Test cases for Portfolio import operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(
            plan_id="PLAN-001",
            url="https://api.atlassian.com",
            token="test-token",
        )

    @patch.object(Portfolio, "post")
    def test_import_workitem(self, mock_post):
        """Test import_workitem method."""
        mock_post.return_value = {"id": "WI-001", "success": True}
        result = self.portfolio.import_workitem({"title": "New Workitem"})
        mock_post.assert_called_once_with(
            "rest/roadmap/1.0/plans/bulk/PLAN-001/workitems.json",
            data={"title": "New Workitem"},
        )
        self.assertEqual(result["id"], "WI-001")


if __name__ == "__main__":
    unittest.main()
