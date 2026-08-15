# coding=utf-8

from .base import TempoCloudBase


class Cloud(TempoCloudBase):
    """
    Tempo Cloud REST API wrapper
    """

    def __init__(self, url="https://api.tempo.io/", *args, **kwargs):
        # Set default API configuration for Tempo Cloud, but allow overrides
        if "cloud" not in kwargs:
            kwargs["cloud"] = True
        if "api_version" not in kwargs:
            kwargs["api_version"] = "1"
        if "api_root" not in kwargs:
            kwargs["api_root"] = "rest/tempo-timesheets/4"
        super(Cloud, self).__init__(url, *args, **kwargs)

    # Account Management
    def get_accounts(self, **kwargs):
        """Get all accounts."""
        return self.get("accounts", **kwargs)

    def get_account(self, account_id, **kwargs):
        """Get account by ID."""
        return self.get(f"accounts/{account_id}", **kwargs)

    def create_account(self, data, **kwargs):
        """Create a new account."""
        return self.post("accounts", data=data, **kwargs)

    def update_account(self, account_id, data, **kwargs):
        """Update an existing account."""
        return self.put(f"accounts/{account_id}", data=data, **kwargs)

    def delete_account(self, account_id, **kwargs):
        """Delete an account."""
        return self.delete(f"accounts/{account_id}", **kwargs)

    # Worklog Management
    def get_worklogs(self, **kwargs):
        """Get all worklogs."""
        return self.get("worklogs", **kwargs)

    def get_worklog(self, worklog_id, **kwargs):
        """Get worklog by ID."""
        return self.get(f"worklogs/{worklog_id}", **kwargs)

    def create_worklog(self, data, **kwargs):
        """Create a new worklog."""
        return self.post("worklogs", data=data, **kwargs)

    def update_worklog(self, worklog_id, data, **kwargs):
        """Update an existing worklog."""
        return self.put(f"worklogs/{worklog_id}", data=data, **kwargs)

    def delete_worklog(self, worklog_id, **kwargs):
        """Delete a worklog."""
        return self.delete(f"worklogs/{worklog_id}", **kwargs)

    # Schedule Management
    def get_schedules(self, **kwargs):
        """Get all schedules."""
        return self.get("schedules", **kwargs)

    def get_schedule(self, schedule_id, **kwargs):
        """Get schedule by ID."""
        return self.get(f"schedules/{schedule_id}", **kwargs)

    def create_schedule(self, data, **kwargs):
        """Create a new schedule."""
        return self.post("schedules", data=data, **kwargs)

    def update_schedule(self, schedule_id, data, **kwargs):
        """Update an existing schedule."""
        return self.put(f"schedules/{schedule_id}", data=data, **kwargs)

    def delete_schedule(self, schedule_id, **kwargs):
        """Delete a schedule."""
        return self.delete(f"schedules/{schedule_id}", **kwargs)

    # User Management
    def get_users(self, **kwargs):
        """Get all users."""
        return self.get("users", **kwargs)

    def get_user(self, user_id, **kwargs):
        """Get user by ID."""
        return self.get(f"users/{user_id}", **kwargs)

    def get_user_schedule(self, user_id, **kwargs):
        """Get user's schedule."""
        return self.get(f"users/{user_id}/schedule", **kwargs)

    def get_user_worklogs(self, user_id, **kwargs):
        """Get user's worklogs."""
        return self.get(f"users/{user_id}/worklogs", **kwargs)

    # Team Management
    def get_teams(self, **kwargs):
        """Get all teams."""
        return self.get("teams", **kwargs)

    def get_team(self, team_id, **kwargs):
        """Get team by ID."""
        return self.get(f"teams/{team_id}", **kwargs)

    def create_team(self, data, **kwargs):
        """Create a new team."""
        return self.post("teams", data=data, **kwargs)

    def update_team(self, team_id, data, **kwargs):
        """Update an existing team."""
        return self.put(f"teams/{team_id}", data=data, **kwargs)

    def delete_team(self, team_id, **kwargs):
        """Delete a team."""
        return self.delete(f"teams/{team_id}", **kwargs)

    def get_team_members(self, team_id, **kwargs):
        """Get team members."""
        return self.get(f"teams/{team_id}/members", **kwargs)

    def add_team_member(self, team_id, user_id, **kwargs):
        """Add member to team."""
        return self.post(f"teams/{team_id}/members", data={"userId": user_id}, **kwargs)

    def remove_team_member(self, team_id, user_id, **kwargs):
        """Remove member from team."""
        return self.delete(f"teams/{team_id}/members/{user_id}", **kwargs)

    # Project Management
    def get_projects(self, **kwargs):
        """Get all projects."""
        return self.get("projects", **kwargs)

    def get_project(self, project_id, **kwargs):
        """Get project by ID."""
        return self.get(f"projects/{project_id}", **kwargs)

    def get_project_worklogs(self, project_id, **kwargs):
        """Get project worklogs."""
        return self.get(f"projects/{project_id}/worklogs", **kwargs)

    # Activity Management
    def get_activities(self, **kwargs):
        """Get all activities."""
        return self.get("activities", **kwargs)

    def get_activity(self, activity_id, **kwargs):
        """Get activity by ID."""
        return self.get(f"activities/{activity_id}", **kwargs)

    def create_activity(self, data, **kwargs):
        """Create a new activity."""
        return self.post("activities", data=data, **kwargs)

    def update_activity(self, activity_id, data, **kwargs):
        """Update an existing activity."""
        return self.put(f"activities/{activity_id}", data=data, **kwargs)

    def delete_activity(self, activity_id, **kwargs):
        """Delete an activity."""
        return self.delete(f"activities/{activity_id}", **kwargs)

    # Customer Management
    def get_customers(self, **kwargs):
        """Get all customers."""
        return self.get("customers", **kwargs)

    def get_customer(self, customer_id, **kwargs):
        """Get customer by ID."""
        return self.get(f"customers/{customer_id}", **kwargs)

    def create_customer(self, data, **kwargs):
        """Create a new customer."""
        return self.post("customers", data=data, **kwargs)

    def update_customer(self, customer_id, data, **kwargs):
        """Update an existing customer."""
        return self.put(f"customers/{customer_id}", data=data, **kwargs)

    def delete_customer(self, customer_id, **kwargs):
        """Delete a customer."""
        return self.delete(f"customers/{customer_id}", **kwargs)

    # Holiday Management
    def get_holidays(self, **kwargs):
        """Get all holidays."""
        return self.get("holidays", **kwargs)

    def get_holiday(self, holiday_id, **kwargs):
        """Get holiday by ID."""
        return self.get(f"holidays/{holiday_id}", **kwargs)

    def create_holiday(self, data, **kwargs):
        """Create a new holiday."""
        return self.post("holidays", data=data, **kwargs)

    def update_holiday(self, holiday_id, data, **kwargs):
        """Update an existing holiday."""
        return self.put(f"holidays/{holiday_id}", data=data, **kwargs)

    def delete_holiday(self, holiday_id, **kwargs):
        """Delete a holiday."""
        return self.delete(f"holidays/{holiday_id}", **kwargs)

    # Report Generation
    def generate_report(self, report_type, params=None, **kwargs):
        """Generate a report."""
        if params is None:
            params = {}
        return self.post(f"reports/{report_type}", data=params, **kwargs)

    def get_report_status(self, report_id, **kwargs):
        """Get report generation status."""
        return self.get(f"reports/{report_id}/status", **kwargs)

    def download_report(self, report_id, **kwargs):
        """Download a generated report."""
        return self.get(f"reports/{report_id}/download", **kwargs)

    # Utility Methods
    def get_metadata(self, **kwargs):
        """Get API metadata."""
        return self.get("metadata", **kwargs)

    def get_health(self, **kwargs):
        """Get API health status."""
        return self.get("health", **kwargs)
