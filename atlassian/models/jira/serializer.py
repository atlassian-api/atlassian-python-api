from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from atlassian.models.jira.fields import (
    Component,
    CustomField,
    IssueFields,
    IssueLink,
    IssueType,
    Parent,
    Priority,
    Project,
    User,
    Version,
)
from atlassian.models.jira.issues import JiraIssue


@dataclass
class FieldMapping:
    """Maps well-known model fields to instance-specific Jira custom field IDs.

    Different Jira instances use different custom field IDs for concepts like
    epic link or story points. Override the defaults here.
    """
    epic_link_field: str = "customfield_10014"
    story_points_field: str = "customfield_10028"
    epic_name_field: str = "customfield_10011"


def _ser_project(p: Project) -> dict[str, Any]:
    return p.to_dict()


def _ser_issue_type(it: IssueType) -> dict[str, Any]:
    return it.to_dict()


def _ser_priority(p: Priority) -> dict[str, Any]:
    return p.to_dict()


def _ser_user(u: User) -> dict[str, Any]:
    return u.to_dict()


def _ser_component(c: Component) -> dict[str, Any]:
    return c.to_dict()


def _ser_version(v: Version) -> dict[str, Any]:
    return v.to_dict()


def _ser_parent(p: Parent) -> dict[str, Any]:
    return p.to_dict()


def _ser_issue_links(links: list[IssueLink]) -> list[dict[str, Any]]:
    """Produce the update payload for issue links.

    Issue links go into the `update.issuelinks` block as "add" operations,
    not into the top-level `fields` dict.
    """
    result: list[dict[str, Any]] = []
    for link in links:
        entry: dict[str, Any] = {"add": {"type": {"name": link.link_type}}}
        if link.outward_issue:
            entry["add"]["outwardIssue"] = {"key": link.outward_issue}
        if link.inward_issue:
            entry["add"]["inwardIssue"] = {"key": link.inward_issue}
        result.append(entry)
    return result


def serialize(
    issue: JiraIssue,
    *,
    mapping: Optional[FieldMapping] = None,
) -> dict[str, Any]:
    """Convert a JiraIssue into the dict that Jira.create_issue() expects.

    Returns a dict with top-level keys "fields" and optionally "update".
    """
    if mapping is None:
        mapping = FieldMapping()

    f = issue.fields
    fields: dict[str, Any] = {}
    update: dict[str, Any] = {}

    if f.project:
        fields["project"] = _ser_project(f.project)
    if f.issue_type:
        fields["issuetype"] = _ser_issue_type(f.issue_type)
    if f.summary is not None:
        fields["summary"] = f.summary

    if f.description is not None:
        fields["description"] = f.description

    if f.priority:
        fields["priority"] = _ser_priority(f.priority)
    if f.assignee:
        fields["assignee"] = _ser_user(f.assignee)
    if f.reporter:
        fields["reporter"] = _ser_user(f.reporter)
    if f.parent:
        fields["parent"] = _ser_parent(f.parent)
    if f.due_date:
        fields["duedate"] = f.due_date.isoformat()

    if f.labels:
        fields["labels"] = list(f.labels)
    if f.components:
        fields["components"] = [_ser_component(c) for c in f.components]
    if f.fix_versions:
        fields["fixVersions"] = [_ser_version(v) for v in f.fix_versions]
    if f.affected_versions:
        fields["versions"] = [_ser_version(v) for v in f.affected_versions]

    if f.epic_link:
        fields[mapping.epic_link_field] = f.epic_link
    if f.epic_name:
        fields[mapping.epic_name_field] = f.epic_name
    if f.story_points is not None:
        fields[mapping.story_points_field] = f.story_points

    for cf in f.custom_fields:
        fields[cf.field_id] = cf.value

    if f.issue_links:
        update["issuelinks"] = _ser_issue_links(f.issue_links)

    result: dict[str, Any] = {"fields": fields}
    if update:
        result["update"] = update
    return result


def to_fields_dict(
    issue: JiraIssue,
    *,
    mapping: Optional[FieldMapping] = None,
) -> dict[str, Any]:
    """Convenience: returns only the inner fields dict.

    Use with jira.issue_create(fields=to_fields_dict(issue)).
    """
    return serialize(issue, mapping=mapping)["fields"]


def bulk_serialize(
    issues: list[JiraIssue],
    *,
    mapping: Optional[FieldMapping] = None,
) -> list[dict[str, Any]]:
    """Serialize a list of issues for Jira.create_issues() bulk endpoint.

    Returns a list of dicts, each with "fields" and optionally "update" keys,
    matching the format expected by POST /rest/api/2/issue/bulk.
    """
    return [serialize(issue, mapping=mapping) for issue in issues]
