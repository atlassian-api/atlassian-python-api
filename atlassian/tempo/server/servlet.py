# coding=utf-8
"""
Tempo Server Servlet API module.
"""

from .base import TempoServerBase


class Servlet(TempoServerBase):
    """
    Tempo Server Servlet API client.

    Reference: https://www.tempo.io/server-api-documentation/servlet
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Servlet, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_worklogs(self, **kwargs):
        """Get all worklogs."""
        return self.parent.get("", **kwargs)

    def get_worklog(self, worklog_id, **kwargs):
        """Get worklog by ID."""
        return self.parent.get(f"{worklog_id}", **kwargs)

    def create_worklog(self, data, **kwargs):
        """Create a new worklog."""
        return self.parent.post("", data=data, **kwargs)

    def update_worklog(self, worklog_id, data, **kwargs):
        """Update an existing worklog."""
        return self.parent.put(f"{worklog_id}", data=data, **kwargs)

    def delete_worklog(self, worklog_id, **kwargs):
        """Delete a worklog."""
        return self.parent.delete(f"{worklog_id}", **kwargs)

    def get_worklog_attributes(self, worklog_id, **kwargs):
        """Get worklog attributes."""
        return self.parent.get(f"{worklog_id}/attributes", **kwargs)

    def update_worklog_attributes(self, worklog_id, data, **kwargs):
        """Update worklog attributes."""
        return self.parent.put(f"{worklog_id}/attributes", data=data, **kwargs)
