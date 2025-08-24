# coding=utf-8
"""
Tempo Server Teams API module.
"""

from .base import TempoServerBase


class Teams(TempoServerBase):
    """
    Tempo Server Teams API client.

    Reference: https://www.tempo.io/server-api-documentation/teams
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Teams, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_teams(self, **kwargs):
        """Get all teams."""
        return self.parent.get("", **kwargs)

    def get_team(self, team_id, **kwargs):
        """Get team by ID."""
        return self.parent.get(f"{team_id}", **kwargs)

    def create_team(self, data, **kwargs):
        """Create a new team."""
        return self.parent.post("", data=data, **kwargs)

    def update_team(self, team_id, data, **kwargs):
        """Update an existing team."""
        return self.parent.put(f"{team_id}", data=data, **kwargs)

    def delete_team(self, team_id, **kwargs):
        """Delete a team."""
        return self.parent.delete(f"{team_id}", **kwargs)

    def get_team_members(self, team_id, **kwargs):
        """Get team members."""
        return self.parent.get(f"{team_id}/members", **kwargs)

    def add_team_member(self, team_id, user_id, **kwargs):
        """Add member to team."""
        return self.parent.post(f"{team_id}/members", data={"userId": user_id}, **kwargs)

    def remove_team_member(self, team_id, user_id, **kwargs):
        """Remove member from team."""
        return self.parent.delete(f"{team_id}/members/{user_id}", **kwargs)
