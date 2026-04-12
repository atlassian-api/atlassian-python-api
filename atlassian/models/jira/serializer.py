from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from atlassian.models.jira.fields import IssueFields, IssueLink
from atlassian.models.jira.issues import JiraIssue


@dataclass
class FieldMapping:
    """
    Maps well-known model fields to instance-specific Jira custom field IDs.

    Different Jira instances use different custom field IDs for concepts like
    epic link or story points. Override the defaults here.
    """

    epic_link_field: str = "customfield_10014"
    story_points_field: str = "customfield_10028"
    epic_name_field: str = "customfield_10011"


def _ser_entity_fields(f: IssueFields, fields: dict[str, Any]) -> None:
    if f.project:
        fields["project"] = f.project.to_dict()
    if f.issue_type:
        fields["issuetype"] = f.issue_type.to_dict()
    if f.priority:
        fields["priority"] = f.priority.to_dict()
    if f.assignee:
        fields["assignee"] = f.assignee.to_dict()
    if f.reporter:
        fields["reporter"] = f.reporter.to_dict()
    if f.parent:
        fields["parent"] = f.parent.to_dict()


def _ser_scalar_fields(f: IssueFields, fields: dict[str, Any]) -> None:
    if f.summary is not None:
        fields["summary"] = f.summary
    if f.description is not None:
        fields["description"] = f.description
    if f.due_date:
        fields["duedate"] = f.due_date.isoformat()


def _ser_collection_fields(f: IssueFields, fields: dict[str, Any]) -> None:
    if f.labels:
        fields["labels"] = list(f.labels)
    if f.components:
        fields["components"] = [c.to_dict() for c in f.components]
    if f.fix_versions:
        fields["fixVersions"] = [v.to_dict() for v in f.fix_versions]
    if f.affected_versions:
        fields["versions"] = [v.to_dict() for v in f.affected_versions]


def _ser_custom_and_mapped_fields(f: IssueFields, fields: dict[str, Any], mapping: FieldMapping) -> None:
    if f.epic_link:
        fields[mapping.epic_link_field] = f.epic_link
    if f.epic_name:
        fields[mapping.epic_name_field] = f.epic_name
    if f.story_points is not None:
        fields[mapping.story_points_field] = f.story_points
    for cf in f.custom_fields:
        fields[cf.field_id] = cf.value


def _ser_issue_links(links: list[IssueLink]) -> list[dict[str, Any]]:
    """
    Produce the update payload for issue links.

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
    """
    Convert a JiraIssue into the dict that Jira.create_issue() expects.

    Returns a dict with top-level keys "fields" and optionally "update".
    """
    if mapping is None:
        mapping = FieldMapping()

    f = issue.fields
    fields = {}
    update = {}

    _ser_entity_fields(f, fields)
    _ser_scalar_fields(f, fields)
    _ser_collection_fields(f, fields)
    _ser_custom_and_mapped_fields(f, fields, mapping)

    if f.issue_links:
        update["issuelinks"] = _ser_issue_links(f.issue_links)

    result = {"fields": fields}
    if update:
        result["update"] = update
    return result


def to_fields_dict(
    issue: JiraIssue,
    *,
    mapping: Optional[FieldMapping] = None,
) -> dict[str, Any]:
    """
    Convenience: returns only the inner fields dict.

    Use with jira.issue_create(fields=to_fields_dict(issue)).
    """
    return serialize(issue, mapping=mapping)["fields"]


def bulk_serialize(
    issues: list[JiraIssue],
    *,
    mapping: Optional[FieldMapping] = None,
) -> list[dict[str, Any]]:
    """
    Serialize a list of issues for Jira.create_issues() bulk endpoint.

    Returns a list of dicts, each with "fields" and optionally "update" keys,
    matching the format expected by POST /rest/api/2/issue/bulk.
    """
    return [serialize(issue, mapping=mapping) for issue in issues]
