# coding=utf-8
"""
Tempo Server Accounts API module.
"""

from .base import TempoServerBase


class Accounts(TempoServerBase):
    """
    Tempo Server Accounts API client.

    Reference: https://www.tempo.io/server-api-documentation/accounts
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Accounts, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_accounts(self, **kwargs):
        """Get all accounts."""
        return self.parent.get("", **kwargs)

    def get_account(self, account_id, **kwargs):
        """Get account by ID."""
        return self.parent.get(f"{account_id}", **kwargs)

    def create_account(self, data, **kwargs):
        """Create a new account."""
        return self.parent.post("", data=data, **kwargs)

    def update_account(self, account_id, data, **kwargs):
        """Update an existing account."""
        return self.parent.put(f"{account_id}", data=data, **kwargs)

    def delete_account(self, account_id, **kwargs):
        """Delete an account."""
        return self.parent.delete(f"{account_id}", **kwargs)
