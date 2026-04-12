from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from atlassian.models.jira.fields import IssueFields, IssueType


_ISSUE_TYPE_REGISTRY: dict[str, type[JiraIssue]] = {}


def get_issue_type_registry() -> dict[str, type[JiraIssue]]:
    return dict(_ISSUE_TYPE_REGISTRY)


def issue_type_for(name: str) -> type[JiraIssue]:
    try:
        return _ISSUE_TYPE_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown issue type '{name}'. " f"Registered: {sorted(_ISSUE_TYPE_REGISTRY)}")


@dataclass
class JiraIssue:
    _issue_type_name: ClassVar[str] = ""

    fields: IssueFields = field(default_factory=IssueFields)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Register subclass in the issue type registry."""
        super().__init_subclass__(**kwargs)
        name = getattr(cls, "_issue_type_name", "")
        if name:
            _ISSUE_TYPE_REGISTRY[name] = cls

    def __post_init__(self) -> None:
        """Stamp issue type from class variable."""
        if self._issue_type_name:
            self.fields.issue_type = IssueType(name=self._issue_type_name)

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, mapping: Any = None) -> JiraIssue:
        """
        Create a JiraIssue from a Jira REST API response dict.

        If a ``fields`` key is present, extracts fields from it.
        Otherwise treats the dict itself as the fields block.

        Note: this is a *partial* deserialization. ``custom_fields`` and
        ``issue_links`` are not reconstructed because their schema varies
        per Jira instance. Use the returned object for inspection or as a
        starting point for updates, not as a lossless round-trip.
        """
        fields_data = data.get("fields", data)
        fields = IssueFields.from_dict(fields_data, mapping=mapping)

        issue_type_name = ""
        if fields.issue_type and fields.issue_type.name:
            issue_type_name = fields.issue_type.name

        issue_cls = _ISSUE_TYPE_REGISTRY.get(issue_type_name, cls)
        issue = issue_cls.__new__(issue_cls)
        issue.fields = fields
        return issue

    def __repr__(self) -> str:
        """Return a concise string representation."""
        parts = [self.__class__.__name__]
        if self.fields.project and self.fields.project.key:
            parts.append(f"project={self.fields.project.key!r}")
        if self.fields.summary:
            summary = self.fields.summary
            if len(summary) > 50:
                summary = summary[:47] + "..."
            parts.append(f"summary={summary!r}")
        if len(parts) == 1:
            return f"{parts[0]}()"
        return f"{parts[0]}({', '.join(parts[1:])})"


@dataclass
class Task(JiraIssue):
    _issue_type_name: ClassVar[str] = "Task"


@dataclass
class Bug(JiraIssue):
    _issue_type_name: ClassVar[str] = "Bug"


@dataclass
class Story(JiraIssue):
    _issue_type_name: ClassVar[str] = "Story"


@dataclass
class Epic(JiraIssue):
    _issue_type_name: ClassVar[str] = "Epic"


@dataclass
class SubTask(JiraIssue):
    _issue_type_name: ClassVar[str] = "Sub-task"
