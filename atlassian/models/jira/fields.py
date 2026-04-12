from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union


class PriorityLevel(Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"


@dataclass(frozen=True)
class Project:
    key: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.key and not self.id:
            raise ValueError("Project requires either 'key' or 'id'")

    def to_dict(self) -> dict[str, Any]:
        if self.key:
            return {"key": self.key}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        return cls(key=data.get("key"), id=data.get("id"))


@dataclass(frozen=True)
class IssueType:
    name: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name and not self.id:
            raise ValueError("IssueType requires either 'name' or 'id'")

    def to_dict(self) -> dict[str, Any]:
        if self.name:
            return {"name": self.name}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IssueType:
        return cls(name=data.get("name"), id=data.get("id"))


@dataclass(frozen=True)
class Priority:
    name: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name and not self.id:
            raise ValueError("Priority requires either 'name' or 'id'")

    @classmethod
    def from_level(cls, level: PriorityLevel) -> Priority:
        return cls(name=level.value)

    def to_dict(self) -> dict[str, Any]:
        if self.name:
            return {"name": self.name}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Priority:
        return cls(name=data.get("name"), id=data.get("id"))


@dataclass(frozen=True)
class User:
    account_id: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.account_id and not self.name:
            raise ValueError("User requires either 'account_id' (Cloud) or 'name' (Server)")

    def to_dict(self) -> dict[str, Any]:
        if self.account_id:
            return {"accountId": self.account_id}
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(account_id=data.get("accountId"), name=data.get("name"))


@dataclass(frozen=True)
class Component:
    name: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name and not self.id:
            raise ValueError("Component requires either 'name' or 'id'")

    def to_dict(self) -> dict[str, Any]:
        if self.name:
            return {"name": self.name}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Component:
        return cls(name=data.get("name"), id=data.get("id"))


@dataclass(frozen=True)
class Version:
    name: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name and not self.id:
            raise ValueError("Version requires either 'name' or 'id'")

    def to_dict(self) -> dict[str, Any]:
        if self.name:
            return {"name": self.name}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Version:
        return cls(name=data.get("name"), id=data.get("id"))


@dataclass(frozen=True)
class Parent:
    key: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.key and not self.id:
            raise ValueError("Parent requires either 'key' or 'id'")

    def to_dict(self) -> dict[str, Any]:
        if self.key:
            return {"key": self.key}
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Parent:
        return cls(key=data.get("key"), id=data.get("id"))


@dataclass(frozen=True)
class IssueLink:
    link_type: str
    outward_issue: Optional[str] = None
    inward_issue: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.outward_issue and not self.inward_issue:
            raise ValueError("IssueLink requires either 'outward_issue' or 'inward_issue'")

    def to_dict(self) -> dict[str, Any]:
        entry: dict[str, Any] = {"type": {"name": self.link_type}}
        if self.outward_issue:
            entry["outwardIssue"] = {"key": self.outward_issue}
        if self.inward_issue:
            entry["inwardIssue"] = {"key": self.inward_issue}
        return entry


@dataclass(frozen=True)
class CustomField:
    field_id: str
    value: Any

    def __post_init__(self) -> None:
        if not self.field_id:
            raise ValueError("CustomField requires a 'field_id'")


@dataclass
class IssueFields:
    project: Optional[Project] = None
    issue_type: Optional[IssueType] = None
    summary: Optional[str] = None
    description: Optional[Union[str, dict[str, Any]]] = None
    priority: Optional[Priority] = None
    labels: list[str] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    assignee: Optional[User] = None
    reporter: Optional[User] = None
    parent: Optional[Parent] = None
    epic_link: Optional[str] = None
    epic_name: Optional[str] = None
    fix_versions: list[Version] = field(default_factory=list)
    affected_versions: list[Version] = field(default_factory=list)
    due_date: Optional[datetime.date] = None
    story_points: Optional[float] = None
    issue_links: list[IssueLink] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, mapping: Optional[Any] = None) -> IssueFields:
        """Parse a Jira REST API fields dict into an IssueFields instance.

        Handles the standard Jira field keys (issuetype, fixVersions, etc.)
        and maps them back to Python attribute names.

        Note: this is a partial deserialization. ``custom_fields`` and
        ``issue_links`` are not reconstructed (their schema varies per
        instance). Use ``serialize()`` output for the authoritative format.
        """
        from atlassian.models.jira.serializer import FieldMapping

        if mapping is None:
            mapping = FieldMapping()

        fields = cls()
        if "project" in data and data["project"]:
            fields.project = Project.from_dict(data["project"])
        if "issuetype" in data and data["issuetype"]:
            fields.issue_type = IssueType.from_dict(data["issuetype"])
        if "summary" in data:
            fields.summary = data["summary"]
        if "description" in data:
            fields.description = data["description"]
        if "priority" in data and data["priority"]:
            fields.priority = Priority.from_dict(data["priority"])
        if "labels" in data:
            fields.labels = list(data["labels"])
        if "components" in data:
            fields.components = [Component.from_dict(c) for c in data["components"]]
        if "assignee" in data and data["assignee"]:
            fields.assignee = User.from_dict(data["assignee"])
        if "reporter" in data and data["reporter"]:
            fields.reporter = User.from_dict(data["reporter"])
        if "parent" in data and data["parent"]:
            fields.parent = Parent.from_dict(data["parent"])
        if "fixVersions" in data:
            fields.fix_versions = [Version.from_dict(v) for v in data["fixVersions"]]
        if "versions" in data:
            fields.affected_versions = [Version.from_dict(v) for v in data["versions"]]
        if "duedate" in data and data["duedate"]:
            fields.due_date = datetime.date.fromisoformat(data["duedate"])
        if mapping.epic_link_field in data:
            fields.epic_link = data[mapping.epic_link_field]
        if mapping.epic_name_field in data:
            fields.epic_name = data[mapping.epic_name_field]
        if mapping.story_points_field in data and data[mapping.story_points_field] is not None:
            fields.story_points = data[mapping.story_points_field]
        return fields
