# coding=utf-8
"""
Test cases for Tempo Cloud API client using pytest.
"""

import pytest
from unittest.mock import patch

from atlassian.tempo import TempoCloud


@pytest.fixture
def tempo_cloud():
    """Fixture for TempoCloud client."""
    return TempoCloud(url="https://test.atlassian.net", token="test-token", cloud=True)


class TestTempoCloud:
    """Test cases for TempoCloud client."""

    def test_init_defaults(self):
        """Test TempoCloud client initialization with default values."""
        tempo = TempoCloud(url="https://test.atlassian.net", token="test-token")
        assert tempo.api_version == "1"
        assert tempo.api_root == "rest/tempo-timesheets/4"

    def test_init_custom_values(self):
        """Test TempoCloud client initialization with custom values."""
        tempo = TempoCloud(
            url="https://test.atlassian.net", token="test-token", api_version="2", api_root="custom/api/root"
        )
        assert tempo.api_version == "2"
        assert tempo.api_root == "custom/api/root"

    # Account Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_accounts(self, mock_get, tempo_cloud):
        """Test get_accounts method."""
        mock_get.return_value = [{"id": 1, "name": "Test Account"}]
        result = tempo_cloud.get_accounts()
        mock_get.assert_called_once_with("accounts", **{})
        assert result == [{"id": 1, "name": "Test Account"}]

    @patch.object(TempoCloud, "get")
    def test_get_account(self, mock_get, tempo_cloud):
        """Test get_account method."""
        mock_get.return_value = {"id": 1, "name": "Test Account"}
        result = tempo_cloud.get_account(1)
        mock_get.assert_called_once_with("accounts/1", **{})
        assert result == {"id": 1, "name": "Test Account"}

    @patch.object(TempoCloud, "post")
    def test_create_account(self, mock_post, tempo_cloud):
        """Test create_account method."""
        account_data = {"name": "New Account", "key": "NEW"}
        mock_post.return_value = {"id": 2, "name": "New Account", "key": "NEW"}
        result = tempo_cloud.create_account(account_data)
        mock_post.assert_called_once_with("accounts", data=account_data, **{})
        assert result == {"id": 2, "name": "New Account", "key": "NEW"}

    @patch.object(TempoCloud, "put")
    def test_update_account(self, mock_put, tempo_cloud):
        """Test update_account method."""
        account_data = {"name": "Updated Account"}
        mock_put.return_value = {"id": 1, "name": "Updated Account"}
        result = tempo_cloud.update_account(1, account_data)
        mock_put.assert_called_once_with("accounts/1", data=account_data, **{})
        assert result == {"id": 1, "name": "Updated Account"}

    @patch.object(TempoCloud, "delete")
    def test_delete_account(self, mock_delete, tempo_cloud):
        """Test delete_account method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_account(1)
        mock_delete.assert_called_once_with("accounts/1", **{})
        assert result == {"success": True}

    # Worklog Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_worklogs(self, mock_get, tempo_cloud):
        """Test get_worklogs method."""
        mock_get.return_value = [{"id": 1, "timeSpentSeconds": 3600}]
        result = tempo_cloud.get_worklogs()
        mock_get.assert_called_once_with("worklogs", **{})
        assert result == [{"id": 1, "timeSpentSeconds": 3600}]

    @patch.object(TempoCloud, "get")
    def test_get_worklog(self, mock_get, tempo_cloud):
        """Test get_worklog method."""
        mock_get.return_value = {"id": 1, "timeSpentSeconds": 3600}
        result = tempo_cloud.get_worklog(1)
        mock_get.assert_called_once_with("worklogs/1", **{})
        assert result == {"id": 1, "timeSpentSeconds": 3600}

    @patch.object(TempoCloud, "post")
    def test_create_worklog(self, mock_post, tempo_cloud):
        """Test create_worklog method."""
        worklog_data = {"issueKey": "TEST-1", "timeSpentSeconds": 3600}
        mock_post.return_value = {"id": 2, "issueKey": "TEST-1", "timeSpentSeconds": 3600}
        result = tempo_cloud.create_worklog(worklog_data)
        mock_post.assert_called_once_with("worklogs", data=worklog_data, **{})
        assert result == {"id": 2, "issueKey": "TEST-1", "timeSpentSeconds": 3600}

    @patch.object(TempoCloud, "put")
    def test_update_worklog(self, mock_put, tempo_cloud):
        """Test update_worklog method."""
        worklog_data = {"timeSpentSeconds": 7200}
        mock_put.return_value = {"id": 1, "timeSpentSeconds": 7200}
        result = tempo_cloud.update_worklog(1, worklog_data)
        mock_put.assert_called_once_with("worklogs/1", data=worklog_data, **{})
        assert result == {"id": 1, "timeSpentSeconds": 7200}

    @patch.object(TempoCloud, "delete")
    def test_delete_worklog(self, mock_delete, tempo_cloud):
        """Test delete_worklog method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_worklog(1)
        mock_delete.assert_called_once_with("worklogs/1", **{})
        assert result == {"success": True}

    # Team Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_teams(self, mock_get, tempo_cloud):
        """Test get_teams method."""
        mock_get.return_value = [{"id": 1, "name": "Test Team"}]
        result = tempo_cloud.get_teams()
        mock_get.assert_called_once_with("teams", **{})
        assert result == [{"id": 1, "name": "Test Team"}]

    @patch.object(TempoCloud, "post")
    def test_create_team(self, mock_post, tempo_cloud):
        """Test create_team method."""
        team_data = {"name": "New Team"}
        mock_post.return_value = {"id": 2, "name": "New Team"}
        result = tempo_cloud.create_team(team_data)
        mock_post.assert_called_once_with("teams", data=team_data, **{})
        assert result == {"id": 2, "name": "New Team"}

    @patch.object(TempoCloud, "put")
    def test_update_team(self, mock_put, tempo_cloud):
        """Test update_team method."""
        team_data = {"name": "Updated Team"}
        mock_put.return_value = {"id": 1, "name": "Updated Team"}
        result = tempo_cloud.update_team(1, team_data)
        mock_put.assert_called_once_with("teams/1", data=team_data, **{})
        assert result == {"id": 1, "name": "Updated Team"}

    @patch.object(TempoCloud, "delete")
    def test_delete_team(self, mock_delete, tempo_cloud):
        """Test delete_team method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_team(1)
        mock_delete.assert_called_once_with("teams/1", **{})
        assert result == {"success": True}

    @patch.object(TempoCloud, "get")
    def test_get_team_members(self, mock_get, tempo_cloud):
        """Test get_team_members method."""
        mock_get.return_value = [{"id": 1, "name": "Member 1"}]
        result = tempo_cloud.get_team_members(1)
        mock_get.assert_called_once_with("teams/1/members", **{})
        assert result == [{"id": 1, "name": "Member 1"}]

    @patch.object(TempoCloud, "post")
    def test_add_team_member(self, mock_post, tempo_cloud):
        """Test add_team_member method."""
        mock_post.return_value = {"success": True}
        result = tempo_cloud.add_team_member(1, 2)
        mock_post.assert_called_once_with("teams/1/members", data={"userId": 2}, **{})
        assert result == {"success": True}

    @patch.object(TempoCloud, "delete")
    def test_remove_team_member(self, mock_delete, tempo_cloud):
        """Test remove_team_member method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.remove_team_member(1, 2)
        mock_delete.assert_called_once_with("teams/1/members/2", **{})
        assert result == {"success": True}

    # Utility Methods Tests
    @patch.object(TempoCloud, "get")
    def test_get_metadata(self, mock_get, tempo_cloud):
        """Test get_metadata method."""
        mock_get.return_value = {"version": "1.0.0"}
        result = tempo_cloud.get_metadata()
        mock_get.assert_called_once_with("metadata", **{})
        assert result == {"version": "1.0.0"}

    @patch.object(TempoCloud, "get")
    def test_get_health(self, mock_get, tempo_cloud):
        """Test get_health method."""
        mock_get.return_value = {"status": "healthy"}
        result = tempo_cloud.get_health()
        mock_get.assert_called_once_with("health", **{})
        assert result == {"status": "healthy"}
