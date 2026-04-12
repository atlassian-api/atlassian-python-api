from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Type, Union

from atlassian.models.jira.fields import (
    Component,
    Priority,
    PriorityLevel,
    User,
    Version,
    _NameIdEntity,
)


@dataclass
class UpdatePayload:
    issue_key: str
    fields: dict[str, Any] = field(default_factory=dict)
    update: dict[str, Any] = field(default_factory=dict)


class UpdateBuilder:  # pylint: disable=too-many-public-methods
    """Fluent builder for Jira issue update payloads.

    Produces the dict format expected by Jira.issue_update() and
    Jira.update_issue_field().

    Example:
        payload = (
            UpdateBuilder("PLAT-123")
            .set_summary("New title")
            .set_priority("Critical")
            .add_labels("hotfix")
            .remove_label("stale")
            .add_comment("Fixed in PR #42")
            .build()
        )
        jira.issue_update(payload.issue_key, payload.fields, update=payload.update)

    """

    def __init__(self, issue_key: str) -> None:
        """Initialize the builder for the given issue key."""
        self._issue_key = issue_key
        self._fields: dict[str, Any] = {}
        self._update: dict[str, list[dict[str, Any]]] = {}

    def _add_op(self, field_name: str, operation: str, value: Any) -> UpdateBuilder:
        self._update.setdefault(field_name, []).append({operation: value})
        return self

    def _entity_op(self, field_name: str, operation: str, entity: _NameIdEntity) -> UpdateBuilder:
        return self._add_op(field_name, operation, entity.to_dict())

    def _set_entity_list(
        self, field_name: str, entity_cls: Type[_NameIdEntity], names: tuple[str, ...]
    ) -> UpdateBuilder:
        self._fields[field_name] = [entity_cls(name=n).to_dict() for n in names]
        return self

    def set_summary(self, text: str) -> UpdateBuilder:
        self._fields["summary"] = text
        return self

    def set_description(self, text: Union[str, dict[str, Any]]) -> UpdateBuilder:
        self._fields["description"] = text
        return self

    def set_priority(
        self,
        name: Optional[str] = None,
        *,
        id_: Optional[str] = None,
        level: Optional[PriorityLevel] = None,
    ) -> UpdateBuilder:
        if level is not None:
            p = Priority.from_level(level)
        else:
            p = Priority(name=name, id=id_)
        self._fields["priority"] = p.to_dict()
        return self

    def set_assignee(self, *, account_id: Optional[str] = None, name: Optional[str] = None) -> UpdateBuilder:
        self._fields["assignee"] = User(account_id=account_id, name=name).to_dict()
        return self

    def unassign(self) -> UpdateBuilder:
        self._fields["assignee"] = None
        return self

    def set_reporter(self, *, account_id: Optional[str] = None, name: Optional[str] = None) -> UpdateBuilder:
        self._fields["reporter"] = User(account_id=account_id, name=name).to_dict()
        return self

    def set_labels(self, *labels: str) -> UpdateBuilder:
        self._fields["labels"] = list(labels)
        return self

    def add_labels(self, *labels: str) -> UpdateBuilder:
        for label in labels:
            self._add_op("labels", "add", label)
        return self

    def remove_label(self, label: str) -> UpdateBuilder:
        return self._add_op("labels", "remove", label)

    def set_components(self, *names: str) -> UpdateBuilder:
        return self._set_entity_list("components", Component, names)

    def add_component(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("components", "add", Component(name=name, id=id_))

    def remove_component(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("components", "remove", Component(name=name, id=id_))

    def set_fix_versions(self, *names: str) -> UpdateBuilder:
        return self._set_entity_list("fixVersions", Version, names)

    def add_fix_version(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("fixVersions", "add", Version(name=name, id=id_))

    def remove_fix_version(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("fixVersions", "remove", Version(name=name, id=id_))

    def set_affected_versions(self, *names: str) -> UpdateBuilder:
        return self._set_entity_list("versions", Version, names)

    def add_affected_version(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("versions", "add", Version(name=name, id=id_))

    def remove_affected_version(self, name: Optional[str] = None, *, id_: Optional[str] = None) -> UpdateBuilder:
        return self._entity_op("versions", "remove", Version(name=name, id=id_))

    def set_due_date(self, date: str) -> UpdateBuilder:
        self._fields["duedate"] = date
        return self

    def clear_due_date(self) -> UpdateBuilder:
        self._fields["duedate"] = None
        return self

    def set_custom_field(self, field_id: str, value: Any) -> UpdateBuilder:
        self._fields[field_id] = value
        return self

    def add_comment(self, body: Union[str, dict[str, Any]]) -> UpdateBuilder:
        return self._add_op("comment", "add", {"body": body})

    def add_issue_link(
        self,
        link_type: str,
        *,
        outward: Optional[str] = None,
        inward: Optional[str] = None,
    ) -> UpdateBuilder:
        link: dict[str, Any] = {"type": {"name": link_type}}
        if outward:
            link["outwardIssue"] = {"key": outward}
        if inward:
            link["inwardIssue"] = {"key": inward}
        return self._add_op("issuelinks", "add", link)

    def build(self) -> UpdatePayload:
        return UpdatePayload(
            issue_key=self._issue_key,
            fields=dict(self._fields),
            update=dict(self._update),
        )

    def build_dict(self) -> dict[str, Any]:
        """Return the raw dict payload for direct use with issue_update()."""
        result: dict[str, Any] = {}
        if self._fields:
            result["fields"] = dict(self._fields)
        if self._update:
            result["update"] = dict(self._update)
        return result
