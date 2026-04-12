from __future__ import annotations

"""Type-safe Jira issue models with fluent builders.

Quick start:
    from atlassian.models.jira import task, serialize

    issue = (
        task()
        .project("PROJ")
        .summary("My task")
        .priority("High")
        .build()
    )
    jira.issue_create(fields=serialize(issue)["fields"])
"""

from atlassian.models.jira.adf import ADFBuilder, InlineNode, MentionNode, TextNode
from atlassian.models.jira.builders import (
    EpicBuilder,
    IssueBuilder,
    StoryBuilder,
    SubTaskBuilder,
    TaskBuilder,
    BugBuilder,
    bug,
    epic,
    story,
    subtask,
    task,
)
from atlassian.models.jira.fields import (
    Component,
    CustomField,
    IssueFields,
    IssueLink,
    IssueType,
    Parent,
    Priority,
    PriorityLevel,
    Project,
    User,
    Version,
)
from atlassian.models.jira.issues import (
    Bug,
    Epic,
    JiraIssue,
    Story,
    SubTask,
    Task,
    get_issue_type_registry,
    issue_type_for,
)
from atlassian.models.jira.comment import Comment, Visibility
from atlassian.models.jira.serializer import FieldMapping, bulk_serialize, serialize, to_fields_dict
from atlassian.models.jira.transition import Transition, TransitionBuilder
from atlassian.models.jira.update import UpdateBuilder, UpdatePayload
from atlassian.models.jira.validation import ValidationError, validate, validate_or_raise

__all__ = [
    "ADFBuilder",
    "Bug",
    "BugBuilder",
    "Comment",
    "Component",
    "CustomField",
    "Epic",
    "EpicBuilder",
    "FieldMapping",
    "InlineNode",
    "IssueBuilder",
    "IssueFields",
    "IssueLink",
    "IssueType",
    "JiraIssue",
    "MentionNode",
    "Parent",
    "Priority",
    "PriorityLevel",
    "Project",
    "Story",
    "StoryBuilder",
    "SubTask",
    "SubTaskBuilder",
    "Task",
    "TaskBuilder",
    "TextNode",
    "Transition",
    "TransitionBuilder",
    "UpdateBuilder",
    "UpdatePayload",
    "User",
    "ValidationError",
    "Version",
    "Visibility",
    "bug",
    "bulk_serialize",
    "epic",
    "get_issue_type_registry",
    "issue_type_for",
    "serialize",
    "story",
    "subtask",
    "task",
    "to_fields_dict",
    "validate",
    "validate_or_raise",
]
