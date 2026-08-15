# coding=utf-8
"""
Tempo Server Events API module.
"""

from .base import TempoServerBase


class Events(TempoServerBase):
    """
    Tempo Server Events API client.

    Reference:
    - https://github.com/tempo-io/tempo-events-example/blob/master/README.md
    - https://github.com/tempo-io/tempo-client-events/blob/master/README.md
    """

    def __init__(self, url, parent=None, *args, **kwargs):
        super(Events, self).__init__(url, *args, **kwargs)
        self.parent = parent

    def get_events(self, **kwargs):
        """Get all events."""
        return self.parent.get("", **kwargs)

    def get_event(self, event_id, **kwargs):
        """Get event by ID."""
        return self.parent.get(f"{event_id}", **kwargs)

    def create_event(self, data, **kwargs):
        """Create a new event."""
        return self.parent.post("", data=data, **kwargs)

    def update_event(self, event_id, data, **kwargs):
        """Update an existing event."""
        return self.parent.put(f"{event_id}", data=data, **kwargs)

    def delete_event(self, event_id, **kwargs):
        """Delete an event."""
        return self.parent.delete(f"{event_id}", **kwargs)

    def get_event_subscriptions(self, **kwargs):
        """Get event subscriptions."""
        return self.parent.get("subscriptions", **kwargs)

    def create_event_subscription(self, data, **kwargs):
        """Create a new event subscription."""
        return self.parent.post("subscriptions", data=data, **kwargs)

    def delete_event_subscription(self, subscription_id, **kwargs):
        """Delete an event subscription."""
        return self.parent.delete(f"subscriptions/{subscription_id}", **kwargs)
