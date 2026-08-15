# coding=utf-8
"""
Tempo Server Budgets API module.
"""

from .base import TempoServerBase


class Budgets(TempoServerBase):
    """
    Tempo Server Budgets API client.

    Reference: https://www.tempo.io/server-api-documentation/budgets
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Budgets, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_budgets(self, **kwargs):
        """Get all budgets."""
        return self.parent.get("", **kwargs)

    def get_budget(self, budget_id, **kwargs):
        """Get budget by ID."""
        return self.parent.get(f"{budget_id}", **kwargs)

    def create_budget(self, data, **kwargs):
        """Create a new budget."""
        return self.parent.post("", data=data, **kwargs)

    def update_budget(self, budget_id, data, **kwargs):
        """Update an existing budget."""
        return self.parent.put(f"{budget_id}", data=data, **kwargs)

    def delete_budget(self, budget_id, **kwargs):
        """Delete a budget."""
        return self.parent.delete(f"{budget_id}", **kwargs)

    def get_budget_allocations(self, budget_id, **kwargs):
        """Get budget allocations."""
        return self.parent.get(f"{budget_id}/allocations", **kwargs)
