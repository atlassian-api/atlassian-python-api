# coding=utf-8
"""
Tempo Server Timesheets API module.
"""

from .base import TempoServerBase


class Timesheets(TempoServerBase):
    """
    Tempo Server Timesheets API client.

    Reference: https://www.tempo.io/server-api-documentation/timesheets
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Timesheets, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_timesheets(self, **kwargs):
        """Get all timesheets."""
        return self.parent.get("", **kwargs)

    def get_timesheet(self, timesheet_id, **kwargs):
        """Get timesheet by ID."""
        return self.parent.get(f"{timesheet_id}", **kwargs)

    def create_timesheet(self, data, **kwargs):
        """Create a new timesheet."""
        return self.parent.post("", data=data, **kwargs)

    def update_timesheet(self, timesheet_id, data, **kwargs):
        """Update an existing timesheet."""
        return self.parent.put(f"{timesheet_id}", data=data, **kwargs)

    def delete_timesheet(self, timesheet_id, **kwargs):
        """Delete a timesheet."""
        return self.parent.delete(f"{timesheet_id}", **kwargs)

    def get_timesheet_entries(self, timesheet_id, **kwargs):
        """Get timesheet entries."""
        return self.parent.get(f"{timesheet_id}/entries", **kwargs)

    def submit_timesheet(self, timesheet_id, **kwargs):
        """Submit a timesheet for approval."""
        return self.parent.post(f"{timesheet_id}/submit", **kwargs)

    def approve_timesheet(self, timesheet_id, **kwargs):
        """Approve a timesheet."""
        return self.parent.post(f"{timesheet_id}/approve", **kwargs)

    def reject_timesheet(self, timesheet_id, reason, **kwargs):
        """Reject a timesheet."""
        return self.parent.post(f"{timesheet_id}/reject", data={"reason": reason}, **kwargs)
