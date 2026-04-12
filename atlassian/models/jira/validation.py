from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from atlassian.models.jira.issues import JiraIssue, SubTask


@dataclass
class ValidationError:
    field_name: str
    message: str


def validate(issue: JiraIssue) -> list[ValidationError]:
    """Validate an issue before serialization. Returns empty list if valid."""
    errors: list[ValidationError] = []
    f = issue.fields

    if not f.project:
        errors.append(ValidationError("project", "Project is required"))
    if not f.summary:
        errors.append(ValidationError("summary", "Summary is required"))
    if not f.issue_type:
        errors.append(ValidationError("issuetype", "Issue type is required"))

    if isinstance(issue, SubTask) and not f.parent:
        errors.append(ValidationError("parent", "Sub-task requires a parent issue"))

    if f.summary and len(f.summary) > 255:
        errors.append(ValidationError("summary", "Summary must be 255 characters or fewer"))

    if f.story_points is not None and f.story_points < 0:
        errors.append(ValidationError("story_points", "Story points cannot be negative"))

    if f.due_date is not None and not isinstance(f.due_date, datetime.date):
        errors.append(ValidationError("duedate", "due_date must be a datetime.date"))

    if f.description and isinstance(f.description, dict):
        if f.description.get("type") != "doc" or f.description.get("version") != 1:
            errors.append(ValidationError(
                "description",
                "ADF description must have type='doc' and version=1",
            ))

    return errors


def validate_or_raise(issue: JiraIssue) -> None:
    """Validate and raise ValueError if any errors found."""
    errors = validate(issue)
    if errors:
        details = "; ".join(f"{e.field_name}: {e.message}" for e in errors)
        raise ValueError(f"Issue validation failed: {details}")
