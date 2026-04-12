from __future__ import annotations

import datetime
from typing import Any, Generic, Optional, Type, TypeVar, Union

from atlassian.models.jira.adf import ADFBuilder, InlineNode
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
from atlassian.models.jira.issues import Bug, Epic, JiraIssue, Story, SubTask, Task
from atlassian.models.jira.serializer import FieldMapping, serialize, to_fields_dict
from atlassian.models.jira.validation import validate_or_raise

T = TypeVar("T", bound=JiraIssue)


class IssueBuilder(Generic[T]):
    """Fluent, type-safe builder for any JiraIssue subclass."""

    def __init__(self, issue_cls: Type[T]) -> None:
        self._issue_cls = issue_cls
        self._fields = IssueFields()

    def project(self, key: Optional[str] = None, *, id: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.project = Project(key=key, id=id)
        return self

    def summary(self, text: str) -> IssueBuilder[T]:
        self._fields.summary = text
        return self

    def description(self, text: str) -> IssueBuilder[T]:
        self._fields.description = text
        return self

    def description_adf(self, adf: Union[dict[str, Any], ADFBuilder]) -> IssueBuilder[T]:
        if isinstance(adf, ADFBuilder):
            self._fields.description = adf.build()
        else:
            self._fields.description = adf
        return self

    def description_builder(self) -> _ADFBridge[T]:
        return _ADFBridge(self)

    def priority(
        self,
        name: Optional[str] = None,
        *,
        id: Optional[str] = None,
        level: Optional[PriorityLevel] = None,
    ) -> IssueBuilder[T]:
        if level is not None:
            self._fields.priority = Priority.from_level(level)
        else:
            self._fields.priority = Priority(name=name, id=id)
        return self

    def labels(self, *labels: str) -> IssueBuilder[T]:
        self._fields.labels = list(labels)
        return self

    def add_label(self, label: str) -> IssueBuilder[T]:
        self._fields.labels.append(label)
        return self

    def components(self, *names: str) -> IssueBuilder[T]:
        self._fields.components = [Component(name=n) for n in names]
        return self

    def add_component(self, name: Optional[str] = None, *, id: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.components.append(Component(name=name, id=id))
        return self

    def assignee(self, *, account_id: Optional[str] = None, name: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.assignee = User(account_id=account_id, name=name)
        return self

    def reporter(self, *, account_id: Optional[str] = None, name: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.reporter = User(account_id=account_id, name=name)
        return self

    def due_date(self, date: Union[datetime.date, str]) -> IssueBuilder[T]:
        if isinstance(date, str):
            date = datetime.date.fromisoformat(date)
        self._fields.due_date = date
        return self

    def fix_versions(self, *names: str) -> IssueBuilder[T]:
        self._fields.fix_versions = [Version(name=n) for n in names]
        return self

    def add_fix_version(self, name: Optional[str] = None, *, id: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.fix_versions.append(Version(name=name, id=id))
        return self

    def affected_versions(self, *names: str) -> IssueBuilder[T]:
        self._fields.affected_versions = [Version(name=n) for n in names]
        return self

    def parent(self, key: Optional[str] = None, *, id: Optional[str] = None) -> IssueBuilder[T]:
        self._fields.parent = Parent(key=key, id=id)
        return self

    def epic_link(self, epic_key: str) -> IssueBuilder[T]:
        self._fields.epic_link = epic_key
        return self

    def story_points(self, points: float) -> IssueBuilder[T]:
        self._fields.story_points = points
        return self

    def add_link(
        self,
        link_type: str,
        *,
        outward: Optional[str] = None,
        inward: Optional[str] = None,
    ) -> IssueBuilder[T]:
        self._fields.issue_links.append(
            IssueLink(link_type=link_type, outward_issue=outward, inward_issue=inward)
        )
        return self

    def custom_field(self, field_id: str, value: Any) -> IssueBuilder[T]:
        self._fields.custom_fields.append(CustomField(field_id=field_id, value=value))
        return self

    def validate(self) -> IssueBuilder[T]:
        """Validate the current fields and raise ValueError if invalid.

        Can be chained: task().project("P").summary("S").validate().build()
        """
        issue = self._issue_cls()
        issue.fields = self._fields
        type_name = self._issue_cls._issue_type_name
        if type_name:
            issue.fields.issue_type = IssueType(name=type_name)
        validate_or_raise(issue)
        return self

    def build(self) -> T:
        issue = self._issue_cls()
        issue.fields = self._fields
        type_name = self._issue_cls._issue_type_name
        if type_name:
            issue.fields.issue_type = IssueType(name=type_name)
        return issue

    def build_dict(self, *, mapping: Optional[FieldMapping] = None) -> dict[str, Any]:
        """Build the issue and serialize to fields dict for issue_create()."""
        return to_fields_dict(self.build(), mapping=mapping)

    def build_payload(self, *, mapping: Optional[FieldMapping] = None) -> dict[str, Any]:
        """Build the issue and serialize to full payload for create_issue()."""
        return serialize(self.build(), mapping=mapping)


class _ADFBridge(Generic[T]):
    """Bridges IssueBuilder into ADFBuilder, returning control on done()."""

    def __init__(self, parent: IssueBuilder[T]) -> None:
        self._parent = parent
        self._adf = ADFBuilder()

    def paragraph(self, *nodes: InlineNode) -> _ADFBridge[T]:
        self._adf.paragraph(*nodes)
        return self

    def text_paragraph(self, text: str) -> _ADFBridge[T]:
        self._adf.text_paragraph(text)
        return self

    def heading(self, text: str, level: int = 1) -> _ADFBridge[T]:
        self._adf.heading(text, level)
        return self

    def bullet_list(self, items: list[str]) -> _ADFBridge[T]:
        self._adf.bullet_list(items)
        return self

    def ordered_list(self, items: list[str]) -> _ADFBridge[T]:
        self._adf.ordered_list(items)
        return self

    def code_block(self, code: str, language: Optional[str] = None) -> _ADFBridge[T]:
        self._adf.code_block(code, language)
        return self

    def rule(self) -> _ADFBridge[T]:
        self._adf.rule()
        return self

    def blockquote(self, *nodes: InlineNode) -> _ADFBridge[T]:
        self._adf.blockquote(*nodes)
        return self

    def table(self, headers: list[str], rows: list[list[str]]) -> _ADFBridge[T]:
        self._adf.table(headers, rows)
        return self

    def raw_node(self, node: dict[str, Any]) -> _ADFBridge[T]:
        self._adf.raw_node(node)
        return self

    def done(self) -> IssueBuilder[T]:
        self._parent.description_adf(self._adf)
        return self._parent


class TaskBuilder(IssueBuilder[Task]):
    def __init__(self) -> None:
        super().__init__(Task)


class BugBuilder(IssueBuilder[Bug]):
    def __init__(self) -> None:
        super().__init__(Bug)


class StoryBuilder(IssueBuilder[Story]):
    def __init__(self) -> None:
        super().__init__(Story)


class EpicBuilder(IssueBuilder[Epic]):
    def __init__(self) -> None:
        super().__init__(Epic)

    def epic_name(self, name: str) -> EpicBuilder:
        self._fields.epic_name = name
        return self


class SubTaskBuilder(IssueBuilder[SubTask]):
    def __init__(self) -> None:
        super().__init__(SubTask)


def task() -> IssueBuilder[Task]:
    return IssueBuilder(Task)


def bug() -> IssueBuilder[Bug]:
    return IssueBuilder(Bug)


def story() -> IssueBuilder[Story]:
    return IssueBuilder(Story)


def epic() -> EpicBuilder:
    return EpicBuilder()


def subtask() -> SubTaskBuilder:
    return SubTaskBuilder()
