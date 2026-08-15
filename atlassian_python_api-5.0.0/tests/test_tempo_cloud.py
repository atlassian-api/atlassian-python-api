# coding=utf-8
"""
Test cases for Tempo Cloud API client.
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

    # Schedule Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_schedules(self, mock_get, tempo_cloud):
        """Test get_schedules method."""
        mock_get.return_value = [{"id": 1, "name": "Test Schedule"}]
        result = tempo_cloud.get_schedules()
        mock_get.assert_called_once_with("schedules", **{})
        assert result == [{"id": 1, "name": "Test Schedule"}]

    @patch.object(TempoCloud, "get")
    def test_get_schedule(self, mock_get, tempo_cloud):
        """Test get_schedule method."""
        mock_get.return_value = {"id": 1, "name": "Test Schedule"}
        result = tempo_cloud.get_schedule(1)
        mock_get.assert_called_once_with("schedules/1", **{})
        assert result == {"id": 1, "name": "Test Schedule"}

    @patch.object(TempoCloud, "post")
    def test_create_schedule(self, mock_post, tempo_cloud):
        """Test create_schedule method."""
        schedule_data = {"name": "New Schedule", "userId": 1}
        mock_post.return_value = {"id": 2, "name": "New Schedule", "userId": 1}
        result = tempo_cloud.create_schedule(schedule_data)
        mock_post.assert_called_once_with("schedules", data=schedule_data, **{})
        assert result == {"id": 2, "name": "New Schedule", "userId": 1}

    @patch.object(TempoCloud, "put")
    def test_update_schedule(self, mock_put, tempo_cloud):
        """Test update_schedule method."""
        schedule_data = {"name": "Updated Schedule"}
        mock_put.return_value = {"id": 1, "name": "Updated Schedule"}
        result = tempo_cloud.update_schedule(1, schedule_data)
        mock_put.assert_called_once_with("schedules/1", data=schedule_data, **{})
        assert result == {"id": 1, "name": "Updated Schedule"}

    @patch.object(TempoCloud, "delete")
    def test_delete_schedule(self, mock_delete, tempo_cloud):
        """Test delete_schedule method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_schedule(1)
        mock_delete.assert_called_once_with("schedules/1", **{})
        assert result == {"success": True}

    # User Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_users(self, mock_get, tempo_cloud):
        """Test get_users method."""
        mock_get.return_value = [{"id": 1, "name": "Test User"}]
        result = tempo_cloud.get_users()
        mock_get.assert_called_once_with("users", **{})
        assert result == [{"id": 1, "name": "Test User"}]

    @patch.object(TempoCloud, "get")
    def test_get_user(self, mock_get, tempo_cloud):
        """Test get_user method."""
        mock_get.return_value = {"id": 1, "name": "Test User"}
        result = tempo_cloud.get_user(1)
        mock_get.assert_called_once_with("users/1", **{})
        assert result == {"id": 1, "name": "Test User"}

    @patch.object(TempoCloud, "get")
    def test_get_user_schedule(self, mock_get, tempo_cloud):
        """Test get_user_schedule method."""
        mock_get.return_value = {"id": 1, "userId": 1}
        result = tempo_cloud.get_user_schedule(1)
        mock_get.assert_called_once_with("users/1/schedule", **{})
        assert result == {"id": 1, "userId": 1}

    @patch.object(TempoCloud, "get")
    def test_get_user_worklogs(self, mock_get, tempo_cloud):
        """Test get_user_worklogs method."""
        mock_get.return_value = [{"id": 1, "userId": 1}]
        result = tempo_cloud.get_user_worklogs(1)
        mock_get.assert_called_once_with("users/1/worklogs", **{})
        assert result == [{"id": 1, "userId": 1}]

    # Team Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_teams(self, mock_get, tempo_cloud):
        """Test get_teams method."""
        mock_get.return_value = [{"id": 1, "name": "Test Team"}]
        result = tempo_cloud.get_teams()
        mock_get.assert_called_once_with("teams", **{})
        assert result == [{"id": 1, "name": "Test Team"}]

    @patch.object(TempoCloud, "get")
    def test_get_team(self, mock_get, tempo_cloud):
        """Test get_team method."""
        mock_get.return_value = {"id": 1, "name": "Test Team"}
        result = tempo_cloud.get_team(1)
        mock_get.assert_called_once_with("teams/1", **{})
        assert result == {"id": 1, "name": "Test Team"}

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

    # Project Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_projects(self, mock_get, tempo_cloud):
        """Test get_projects method."""
        mock_get.return_value = [{"id": 1, "name": "Test Project"}]
        result = tempo_cloud.get_projects()
        mock_get.assert_called_once_with("projects", **{})
        assert result == [{"id": 1, "name": "Test Project"}]

    @patch.object(TempoCloud, "get")
    def test_get_project(self, mock_get, tempo_cloud):
        """Test get_project method."""
        mock_get.return_value = {"id": 1, "name": "Test Project"}
        result = tempo_cloud.get_project(1)
        mock_get.assert_called_once_with("projects/1", **{})
        assert result == {"id": 1, "name": "Test Project"}

    @patch.object(TempoCloud, "get")
    def test_get_project_worklogs(self, mock_get, tempo_cloud):
        """Test get_project_worklogs method."""
        mock_get.return_value = [{"id": 1, "projectId": 1}]
        result = tempo_cloud.get_project_worklogs(1)
        mock_get.assert_called_once_with("projects/1/worklogs", **{})
        assert result == [{"id": 1, "projectId": 1}]

    # Activity Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_activities(self, mock_get, tempo_cloud):
        """Test get_activities method."""
        mock_get.return_value = [{"id": 1, "name": "Test Activity"}]
        result = tempo_cloud.get_activities()
        mock_get.assert_called_once_with("activities", **{})
        assert result == [{"id": 1, "name": "Test Activity"}]

    @patch.object(TempoCloud, "get")
    def test_get_activity(self, mock_get, tempo_cloud):
        """Test get_activity method."""
        mock_get.return_value = {"id": 1, "name": "Test Activity"}
        result = tempo_cloud.get_activity(1)
        mock_get.assert_called_once_with("activities/1", **{})
        assert result == {"id": 1, "name": "Test Activity"}

    @patch.object(TempoCloud, "post")
    def test_create_activity(self, mock_post, tempo_cloud):
        """Test create_activity method."""
        activity_data = {"name": "New Activity"}
        mock_post.return_value = {"id": 2, "name": "New Activity"}
        result = tempo_cloud.create_activity(activity_data)
        mock_post.assert_called_once_with("activities", data=activity_data, **{})
        assert result == {"id": 2, "name": "New Activity"}

    @patch.object(TempoCloud, "put")
    def test_update_activity(self, mock_put, tempo_cloud):
        """Test update_activity method."""
        activity_data = {"name": "Updated Activity"}
        mock_put.return_value = {"id": 1, "name": "Updated Activity"}
        result = tempo_cloud.update_activity(1, activity_data)
        mock_put.assert_called_once_with("activities/1", data=activity_data, **{})
        assert result == {"id": 1, "name": "Updated Activity"}

    @patch.object(TempoCloud, "delete")
    def test_delete_activity(self, mock_delete, tempo_cloud):
        """Test delete_activity method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_activity(1)
        mock_delete.assert_called_once_with("activities/1", **{})
        assert result == {"success": True}

    # Customer Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_customers(self, mock_get, tempo_cloud):
        """Test get_customers method."""
        mock_get.return_value = [{"id": 1, "name": "Test Customer"}]
        result = tempo_cloud.get_customers()
        mock_get.assert_called_once_with("customers", **{})
        assert result == [{"id": 1, "name": "Test Customer"}]

    @patch.object(TempoCloud, "get")
    def test_get_customer(self, mock_get, tempo_cloud):
        """Test get_customer method."""
        mock_get.return_value = {"id": 1, "name": "Test Customer"}
        result = tempo_cloud.get_customer(1)
        mock_get.assert_called_once_with("customers/1", **{})
        assert result == {"id": 1, "name": "Test Customer"}

    @patch.object(TempoCloud, "post")
    def test_create_customer(self, mock_post, tempo_cloud):
        """Test create_customer method."""
        customer_data = {"name": "New Customer"}
        mock_post.return_value = {"id": 2, "name": "New Customer"}
        result = tempo_cloud.create_customer(customer_data)
        mock_post.assert_called_once_with("customers", data=customer_data, **{})
        assert result == {"id": 2, "name": "New Customer"}

    @patch.object(TempoCloud, "put")
    def test_update_customer(self, mock_put, tempo_cloud):
        """Test update_customer method."""
        customer_data = {"name": "Updated Customer"}
        mock_put.return_value = {"id": 1, "name": "Updated Customer"}
        result = tempo_cloud.update_customer(1, customer_data)
        mock_put.assert_called_once_with("customers/1", data=customer_data, **{})
        assert result == {"id": 1, "name": "Updated Customer"}

    @patch.object(TempoCloud, "delete")
    def test_delete_customer(self, mock_delete, tempo_cloud):
        """Test delete_customer method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_customer(1)
        mock_delete.assert_called_once_with("customers/1", **{})
        assert result == {"success": True}

    # Holiday Management Tests
    @patch.object(TempoCloud, "get")
    def test_get_holidays(self, mock_get, tempo_cloud):
        """Test get_holidays method."""
        mock_get.return_value = [{"id": 1, "name": "Test Holiday"}]
        result = tempo_cloud.get_holidays()
        mock_get.assert_called_once_with("holidays", **{})
        assert result == [{"id": 1, "name": "Test Holiday"}]

    @patch.object(TempoCloud, "get")
    def test_get_holiday(self, mock_get, tempo_cloud):
        """Test get_holiday method."""
        mock_get.return_value = {"id": 1, "name": "Test Holiday"}
        result = tempo_cloud.get_holiday(1)
        mock_get.assert_called_once_with("holidays/1", **{})
        assert result == {"id": 1, "name": "Test Holiday"}

    @patch.object(TempoCloud, "post")
    def test_create_holiday(self, mock_post, tempo_cloud):
        """Test create_holiday method."""
        holiday_data = {"name": "New Holiday", "date": "2024-01-01"}
        mock_post.return_value = {"id": 2, "name": "New Holiday", "date": "2024-01-01"}
        result = tempo_cloud.create_holiday(holiday_data)
        mock_post.assert_called_once_with("holidays", data=holiday_data, **{})
        assert result == {"id": 2, "name": "New Holiday", "date": "2024-01-01"}

    @patch.object(TempoCloud, "put")
    def test_update_holiday(self, mock_put, tempo_cloud):
        """Test update_holiday method."""
        holiday_data = {"name": "Updated Holiday"}
        mock_put.return_value = {"id": 1, "name": "Updated Holiday"}
        result = tempo_cloud.update_holiday(1, holiday_data)
        mock_put.assert_called_once_with("holidays/1", data=holiday_data, **{})
        assert result == {"id": 1, "name": "Updated Holiday"}

    @patch.object(TempoCloud, "delete")
    def test_delete_holiday(self, mock_delete, tempo_cloud):
        """Test delete_holiday method."""
        mock_delete.return_value = {"success": True}
        result = tempo_cloud.delete_holiday(1)
        mock_delete.assert_called_once_with("holidays/1", **{})
        assert result == {"success": True}

    # Report Generation Tests
    @patch.object(TempoCloud, "post")
    def test_generate_report(self, mock_post, tempo_cloud):
        """Test generate_report method."""
        mock_post.return_value = {"reportId": "123"}
        result = tempo_cloud.generate_report("timesheet", {"dateFrom": "2024-01-01"})
        mock_post.assert_called_once_with("reports/timesheet", data={"dateFrom": "2024-01-01"}, **{})
        assert result == {"reportId": "123"}

    @patch.object(TempoCloud, "get")
    def test_get_report_status(self, mock_get, tempo_cloud):
        """Test get_report_status method."""
        mock_get.return_value = {"status": "completed"}
        result = tempo_cloud.get_report_status("123")
        mock_get.assert_called_once_with("reports/123/status", **{})
        assert result == {"status": "completed"}

    @patch.object(TempoCloud, "get")
    def test_download_report(self, mock_get, tempo_cloud):
        """Test download_report method."""
        mock_get.return_value = {"content": "report data"}
        result = tempo_cloud.download_report("123")
        mock_get.assert_called_once_with("reports/123/download", **{})
        assert result == {"content": "report data"}

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
