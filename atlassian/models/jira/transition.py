from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Transition:
    """
    Represents a Jira issue status transition.

    Used with Jira.set_issue_status(issue_key, status_name, fields=..., update=...).
    """

    issue_key: str
    status: str
    fields: dict[str, Any] = field(default_factory=dict)
    update: dict[str, Any] = field(default_factory=dict)
    resolution: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate required fields and apply resolution."""
        if not self.issue_key:
            raise ValueError("Transition requires an 'issue_key'")
        if not self.status:
            raise ValueError("Transition requires a 'status'")
        if self.resolution:
            self.fields["resolution"] = {"name": self.resolution}

    def as_args(self) -> dict[str, Any]:
        """
        Return keyword arguments for Jira.set_issue_status().

        Usage:
            t = Transition("PLAT-123", "Done", resolution="Fixed")
            jira.set_issue_status(**t.as_args())
        """
        args: dict[str, Any] = {
            "issue_key": self.issue_key,
            "status_name": self.status,
        }
        if self.fields:
            args["fields"] = self.fields
        if self.update:
            args["update"] = self.update
        return args


class TransitionBuilder:
    """Fluent builder for issue transitions."""

    def __init__(self, issue_key: str, status: str) -> None:
        """Initialize the builder with issue key and target status."""
        self._issue_key = issue_key
        self._status = status
        self._fields: dict[str, Any] = {}
        self._update: dict[str, Any] = {}
        self._resolution: Optional[str] = None

    def resolution(self, name: str) -> TransitionBuilder:
        self._resolution = name
        return self

    def set_field(self, field_name: str, value: Any) -> TransitionBuilder:
        self._fields[field_name] = value
        return self

    def set_custom_field(self, field_id: str, value: Any) -> TransitionBuilder:
        self._fields[field_id] = value
        return self

    def build(self) -> Transition:
        return Transition(
            issue_key=self._issue_key,
            status=self._status,
            fields=dict(self._fields),
            update=dict(self._update),
            resolution=self._resolution,
        )
