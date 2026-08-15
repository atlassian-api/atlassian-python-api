# coding=utf-8
"""
Tempo Server Planner API module.
"""

from .base import TempoServerBase


class Planner(TempoServerBase):
    """
    Tempo Server Planner API client.

    Reference: https://www.tempo.io/server-api-documentation/planner
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Planner, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_plans(self, **kwargs):
        """Get all plans."""
        return self.parent.get("", **kwargs)

    def get_plan(self, plan_id, **kwargs):
        """Get plan by ID."""
        return self.parent.get(f"{plan_id}", **kwargs)

    def create_plan(self, data, **kwargs):
        """Create a new plan."""
        return self.parent.post("", data=data, **kwargs)

    def update_plan(self, plan_id, data, **kwargs):
        """Update an existing plan."""
        return self.parent.put(f"{plan_id}", data=data, **kwargs)

    def delete_plan(self, plan_id, **kwargs):
        """Delete a plan."""
        return self.parent.delete(f"{plan_id}", **kwargs)

    def get_plan_assignments(self, plan_id, **kwargs):
        """Get plan assignments."""
        return self.parent.get(f"{plan_id}/assignments", **kwargs)
