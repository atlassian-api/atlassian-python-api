from __future__ import annotations

import datetime
import re

import pytest

from atlassian.models.jira.adf import ADFBuilder, MentionNode, TextNode
from atlassian.models.jira.builders import (
    EpicBuilder,
    IssueBuilder,
    SubTaskBuilder,
    bug,
    epic,
    story,
    subtask,
    task,
)
from atlassian.models.jira.comment import Comment, Visibility
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
from atlassian.models.jira.serializer import FieldMapping, bulk_serialize, serialize, to_fields_dict
from atlassian.models.jira.transition import Transition, TransitionBuilder
from atlassian.models.jira.update import UpdateBuilder, UpdatePayload
from atlassian.models.jira.validation import validate, validate_or_raise


def test_project_key_only_to_dict():
    p = Project(key="ABC")
    assert p.to_dict() == {"key": "ABC"}


def test_project_id_only_to_dict():
    p = Project(id="10000")
    assert p.to_dict() == {"id": "10000"}


def test_project_both_prefers_key_in_to_dict():
    p = Project(key="ABC", id="10000")
    assert p.to_dict() == {"key": "ABC"}


def test_project_neither_raises():
    with pytest.raises(ValueError, match="key' or 'id"):
        Project()


def test_issue_type_name_only():
    it = IssueType(name="Bug")
    assert it.to_dict() == {"name": "Bug"}


def test_issue_type_id_only():
    it = IssueType(id="10001")
    assert it.to_dict() == {"id": "10001"}


def test_issue_type_neither_raises():
    with pytest.raises(ValueError, match="name' or 'id"):
        IssueType()


def test_priority_creation_and_to_dict():
    assert Priority(name="High").to_dict() == {"name": "High"}
    assert Priority(id="2").to_dict() == {"id": "2"}


def test_priority_from_level():
    p = Priority.from_level(PriorityLevel.MEDIUM)
    assert p.name == "Medium"
    assert p.to_dict() == {"name": "Medium"}


def test_priority_neither_raises():
    with pytest.raises(ValueError, match="name' or 'id"):
        Priority()


def test_issue_type_both_name_and_id_prefers_name_in_to_dict():
    assert IssueType(name="Task", id="3").to_dict() == {"name": "Task"}


def test_user_cloud_and_server_to_dict():
    assert User(account_id="acc-1").to_dict() == {"accountId": "acc-1"}
    assert User(name="jdoe").to_dict() == {"name": "jdoe"}


def test_user_neither_raises():
    with pytest.raises(ValueError, match="account_id"):
        User()


def test_component_version_parent_to_dict():
    assert Component(name="UI").to_dict() == {"name": "UI"}
    assert Version(name="1.0").to_dict() == {"name": "1.0"}
    assert Parent(key="FOO-1").to_dict() == {"key": "FOO-1"}


def test_component_version_parent_neither_raises():
    with pytest.raises(ValueError, match="name' or 'id"):
        Component()
    with pytest.raises(ValueError, match="name' or 'id"):
        Version()
    with pytest.raises(ValueError, match="key' or 'id"):
        Parent()


def test_issue_link_outward_to_dict():
    link = IssueLink("Blocks", outward_issue="A-1")
    assert link.to_dict() == {
        "type": {"name": "Blocks"},
        "outwardIssue": {"key": "A-1"},
    }


def test_issue_link_inward_to_dict():
    link = IssueLink("Duplicate", inward_issue="B-2")
    assert link.to_dict() == {
        "type": {"name": "Duplicate"},
        "inwardIssue": {"key": "B-2"},
    }


def test_issue_link_both_to_dict():
    link = IssueLink("Relates", outward_issue="A-1", inward_issue="B-2")
    d = link.to_dict()
    assert d["outwardIssue"] == {"key": "A-1"}
    assert d["inwardIssue"] == {"key": "B-2"}


def test_issue_link_neither_raises():
    with pytest.raises(ValueError, match="outward_issue|inward_issue"):
        IssueLink("Blocks")


def test_custom_field_empty_id_raises():
    with pytest.raises(ValueError, match="field_id"):
        CustomField(field_id="", value=1)


def test_adf_empty_doc_structure():
    doc = ADFBuilder().build()
    assert doc == {"version": 1, "type": "doc", "content": []}


def test_adf_paragraph_and_text_paragraph():
    b = ADFBuilder()
    b.paragraph(TextNode("a"), TextNode("b"))
    b.text_paragraph("c")
    doc = b.build()
    assert doc["content"][0] == {
        "type": "paragraph",
        "content": [
            {"type": "text", "text": "a"},
            {"type": "text", "text": "b"},
        ],
    }
    assert doc["content"][1] == {
        "type": "paragraph",
        "content": [{"type": "text", "text": "c"}],
    }


def test_adf_heading_levels():
    doc = ADFBuilder().heading("T", level=3).build()
    assert doc["content"][0] == {
        "type": "heading",
        "attrs": {"level": 3},
        "content": [{"type": "text", "text": "T"}],
    }


def test_adf_heading_invalid_level():
    with pytest.raises(ValueError, match="Heading level"):
        ADFBuilder().heading("x", level=0)


def test_adf_bullet_and_ordered_list():
    doc = (
        ADFBuilder()
        .bullet_list(["a", "b"])
        .ordered_list(["c"])
        .build()
    )
    assert doc["content"][0]["type"] == "bulletList"
    assert doc["content"][1]["type"] == "orderedList"
    assert len(doc["content"][0]["content"]) == 2


def test_adf_code_block_with_and_without_language():
    d1 = ADFBuilder().code_block("x = 1").build()["content"][0]
    assert d1["type"] == "codeBlock"
    assert "attrs" not in d1
    d2 = ADFBuilder().code_block("print()", language="python").build()["content"][0]
    assert d2["attrs"] == {"language": "python"}


def test_adf_rule():
    assert ADFBuilder().rule().build()["content"][0] == {"type": "rule"}


def test_adf_text_marks():
    node = (
        TextNode("hi")
        .bold()
        .italic()
        .code()
        .link("https://e.example")
        .strike()
    )
    assert node.to_dict() == {
        "type": "text",
        "text": "hi",
        "marks": [
            {"type": "strong"},
            {"type": "em"},
            {"type": "code"},
            {"type": "link", "attrs": {"href": "https://e.example"}},
            {"type": "strike"},
        ],
    }


def test_adf_mention_node():
    assert MentionNode("acc", "Bob").to_dict() == {
        "type": "mention",
        "attrs": {"id": "acc", "text": "Bob"},
    }
    assert MentionNode("acc").to_dict()["attrs"]["text"] == ""


def test_adf_table():
    doc = ADFBuilder().table(["H"], [["c"]]).build()
    tbl = doc["content"][0]
    assert tbl["type"] == "table"
    assert tbl["attrs"] == {"isNumberColumnEnabled": False, "layout": "default"}
    assert len(tbl["content"]) == 2


def test_adf_blockquote():
    doc = ADFBuilder().blockquote(TextNode("q")).build()
    bq = doc["content"][0]
    assert bq["type"] == "blockquote"
    assert bq["content"][0]["type"] == "paragraph"


def test_adf_raw_node_escape_hatch():
    raw = {"type": "extension", "attrs": {"foo": "bar"}}
    doc = ADFBuilder().raw_node(raw).build()
    assert doc["content"][0] == raw


def test_issue_classes_and_issue_type_name():
    assert Task._issue_type_name == "Task"
    assert Bug._issue_type_name == "Bug"
    assert Story._issue_type_name == "Story"
    assert Epic._issue_type_name == "Epic"
    assert SubTask._issue_type_name == "Sub-task"


def test_post_init_stamps_issue_type():
    t = Task()
    assert t.fields.issue_type == IssueType(name="Task")


def test_registry_has_five_types():
    reg = get_issue_type_registry()
    assert set(reg.keys()) == {"Task", "Bug", "Story", "Epic", "Sub-task"}
    assert reg["Task"] is Task


def test_issue_type_for_known_and_unknown():
    assert issue_type_for("Story") is Story
    with pytest.raises(ValueError, match="Unknown issue type"):
        issue_type_for("Unknown")


def test_serialize_minimal_fields_shape():
    issue = Task()
    issue.fields = IssueFields(
        project=Project(key="P"),
        summary="S",
        issue_type=IssueType(name="Task"),
    )
    assert serialize(issue) == {
        "fields": {
            "project": {"key": "P"},
            "issuetype": {"name": "Task"},
            "summary": "S",
        }
    }


def test_serialize_issue_links_update_block():
    issue = Task()
    issue.fields = IssueFields(
        project=Project(key="P"),
        summary="S",
        issue_type=IssueType(name="Task"),
        issue_links=[IssueLink("Blocks", outward_issue="X-1")],
    )
    out = serialize(issue)
    assert out["update"] == {
        "issuelinks": [
            {
                "add": {
                    "type": {"name": "Blocks"},
                    "outwardIssue": {"key": "X-1"},
                },
            },
        ],
    }


def test_to_fields_dict_strips_wrapper():
    issue = Task()
    issue.fields.project = Project(key="K")
    issue.fields.summary = "Hi"
    d = to_fields_dict(issue)
    assert d == serialize(issue)["fields"]
    assert "update" not in to_fields_dict(issue)


def test_field_mapping_overrides_epic_link_and_story_points_keys():
    issue = Task()
    issue.fields.project = Project(key="P")
    issue.fields.summary = "S"
    issue.fields.epic_link = "E-1"
    issue.fields.story_points = 3.5
    m = FieldMapping(epic_link_field="customfield_9001", story_points_field="customfield_9002")
    fields = serialize(issue, mapping=m)["fields"]
    assert fields["customfield_9001"] == "E-1"
    assert fields["customfield_9002"] == 3.5


def test_serialize_all_field_types_and_custom_fields():
    due = datetime.date(2026, 4, 1)
    issue = Task()
    issue.fields = IssueFields(
        project=Project(key="PR"),
        issue_type=IssueType(name="Task"),
        summary="Sum",
        description="plain",
        priority=Priority.from_level(PriorityLevel.HIGH),
        labels=["l1"],
        components=[Component(name="C1")],
        assignee=User(account_id="a1"),
        reporter=User(name="rep"),
        parent=Parent(key="P-9"),
        fix_versions=[Version(name="2.0")],
        affected_versions=[Version(name="1.0")],
        due_date=due,
        story_points=2.0,
        custom_fields=[CustomField("customfield_50000", {"x": 1})],
    )
    f = serialize(issue)["fields"]
    assert f["project"] == {"key": "PR"}
    assert f["issuetype"] == {"name": "Task"}
    assert f["summary"] == "Sum"
    assert f["description"] == "plain"
    assert f["priority"] == {"name": "High"}
    assert f["labels"] == ["l1"]
    assert f["components"] == [{"name": "C1"}]
    assert f["assignee"] == {"accountId": "a1"}
    assert f["reporter"] == {"name": "rep"}
    assert f["parent"] == {"key": "P-9"}
    assert f["fixVersions"] == [{"name": "2.0"}]
    assert f["versions"] == [{"name": "1.0"}]
    assert f["duedate"] == "2026-04-01"
    assert f["customfield_50000"] == {"x": 1}


def test_serialize_omits_empty_optional_lists_and_none_fields():
    issue = Task()
    issue.fields.project = Project(key="P")
    issue.fields.summary = "S"
    keys = set(serialize(issue)["fields"].keys())
    assert "labels" not in keys
    assert "components" not in keys
    assert "assignee" not in keys
    assert "duedate" not in keys


def test_issue_builder_chaining_and_build_types():
    b: IssueBuilder[Task] = task()
    b.project(key="X").summary("Y").priority(level=PriorityLevel.LOW).labels("a").due_date("2026-01-02")
    issue = b.build()
    assert isinstance(issue, Task)
    assert issue.fields.project == Project(key="X")
    assert issue.fields.summary == "Y"
    assert issue.fields.priority == Priority.from_level(PriorityLevel.LOW)
    assert issue.fields.labels == ["a"]
    assert issue.fields.due_date == datetime.date(2026, 1, 2)


def test_factory_functions_return_expected_builder_types():
    assert isinstance(task(), IssueBuilder)
    assert isinstance(bug(), IssueBuilder)
    assert isinstance(story(), IssueBuilder)
    assert isinstance(epic(), EpicBuilder)
    assert isinstance(subtask(), SubTaskBuilder)


def test_build_dict_and_build_payload():
    b = story().project(key="S").summary("st")
    assert isinstance(b.build(), Story)
    d = b.build_dict()
    assert "fields" not in d
    assert d["summary"] == "st"
    payload = b.build_payload()
    assert set(payload.keys()) == {"fields"}
    assert payload["fields"]["summary"] == "st"


def test_adf_bridge_description_builder_done():
    issue = (
        bug()
        .project(key="P")
        .summary("S")
        .description_builder()
        .text_paragraph("Hello")
        .done()
        .build()
    )
    desc = issue.fields.description
    assert isinstance(desc, dict)
    assert desc["type"] == "doc"
    assert desc["version"] == 1
    assert desc["content"][0]["type"] == "paragraph"


def test_epic_builder_epic_name_sets_field():
    issue = epic().project(key="E").summary("Epic").epic_name("My Epic").build()
    assert issue.fields.epic_name == "My Epic"
    fields = to_fields_dict(issue)
    assert fields["customfield_10011"] == "My Epic"


def test_epic_builder_epic_name_respects_field_mapping():
    issue = epic().project(key="E").summary("Epic").epic_name("My Epic").build()
    mapping = FieldMapping(epic_name_field="customfield_99999")
    fields = to_fields_dict(issue, mapping=mapping)
    assert fields["customfield_99999"] == "My Epic"
    assert "customfield_10011" not in fields


def test_subtask_builder_parent_method():
    issue = subtask().project(key="P").summary("Sub").parent(key="P-1").build()
    assert issue.fields.parent == Parent(key="P-1")


def test_builder_custom_field_in_serialize():
    payload = (
        task()
        .project(key="P")
        .summary("S")
        .custom_field("customfield_70000", [1, 2])
        .build_payload()
    )
    assert payload["fields"]["customfield_70000"] == [1, 2]


def test_validate_empty_for_complete_task():
    issue = task().project(key="P").summary("OK").build()
    assert validate(issue) == []


def test_validate_missing_project_summary_issue_type():
    issue = JiraIssue()
    issue.fields = IssueFields()
    errs = validate(issue)
    names = {e.field_name for e in errs}
    assert names == {"project", "summary", "issuetype"}


def test_validate_subtask_without_parent():
    issue = subtask().project(key="P").summary("S").build()
    names = [e.field_name for e in validate(issue)]
    assert "parent" in names


def test_validate_summary_too_long():
    issue = task().project(key="P").summary("x" * 256).build()
    msgs = [e.message for e in validate(issue) if e.field_name == "summary"]
    assert any("255" in m for m in msgs)


def test_validate_negative_story_points():
    issue = task().project(key="P").summary("S").story_points(-1).build()
    assert any(e.field_name == "story_points" for e in validate(issue))


def test_validate_invalid_adf_structure():
    issue = task().project(key="P").summary("S").build()
    issue.fields.description = {"type": "wrong", "version": 1}
    assert any(e.field_name == "description" for e in validate(issue))


def test_validate_or_raise_joins_errors():
    issue = JiraIssue()
    issue.fields = IssueFields()
    with pytest.raises(ValueError, match=re.compile("project:|summary:|issuetype:", re.DOTALL)):
        validate_or_raise(issue)


def test_e2e_task_builder_serialize_matches_api_shape():
    payload = (
        task()
        .project(key="DEMO")
        .summary("Do work")
        .priority(level=PriorityLevel.MEDIUM)
        .assignee(account_id="712345:abc")
        .due_date("2026-12-31")
        .build_payload()
    )
    assert payload == {
        "fields": {
            "project": {"key": "DEMO"},
            "issuetype": {"name": "Task"},
            "summary": "Do work",
            "priority": {"name": "Medium"},
            "assignee": {"accountId": "712345:abc"},
            "duedate": "2026-12-31",
        },
    }


def test_e2e_bug_with_adf_description_in_fields():
    adf = ADFBuilder().heading("Title").text_paragraph("Body").build()
    fields = bug().project(key="B").summary("Crash").description_adf(adf).build_dict()
    assert fields["description"] == adf
    assert fields["description"]["type"] == "doc"
    assert fields["description"]["version"] == 1


def test_e2e_epic_custom_field_mapping():
    mapping = FieldMapping(
        epic_link_field="customfield_80001",
        story_points_field="customfield_80002",
    )
    fields = (
        epic()
        .project(key="E")
        .summary("Roadmap")
        .epic_link("E-100")
        .story_points(8)
        .custom_field("customfield_91000", "extra")
        .build_dict(mapping=mapping)
    )
    assert fields["customfield_80001"] == "E-100"
    assert fields["customfield_80002"] == 8
    assert fields["customfield_91000"] == "extra"
    assert fields["issuetype"] == {"name": "Epic"}


def test_update_builder_set_summary():
    p = UpdateBuilder("PLAT-1").set_summary("New title").build()
    assert isinstance(p, UpdatePayload)
    assert p.issue_key == "PLAT-1"
    assert p.fields["summary"] == "New title"


def test_update_builder_set_priority():
    p = UpdateBuilder("PLAT-2").set_priority("Critical").build()
    assert p.fields["priority"] == {"name": "Critical"}


def test_update_builder_add_and_remove_labels():
    p = (
        UpdateBuilder("PLAT-3")
        .add_labels("a", "b")
        .remove_label("stale")
        .build()
    )
    assert p.update["labels"] == [
        {"add": "a"},
        {"add": "b"},
        {"remove": "stale"},
    ]


def test_update_builder_set_assignee_and_unassign():
    assigned = UpdateBuilder("PLAT-4").set_assignee(account_id="acc-9").build()
    assert assigned.fields["assignee"] == {"accountId": "acc-9"}
    unassigned = UpdateBuilder("PLAT-4").unassign().build()
    assert unassigned.fields["assignee"] is None


def test_update_builder_add_component():
    p = UpdateBuilder("PLAT-5").add_component("UI").build()
    assert p.update["components"] == [{"add": {"name": "UI"}}]


def test_update_builder_add_comment():
    p = UpdateBuilder("PLAT-6").add_comment("note").build()
    assert p.update["comment"] == [{"add": {"body": "note"}}]


def test_update_builder_add_issue_link():
    p = UpdateBuilder("PLAT-7").add_issue_link("Blocks", outward="OTHER-1").build()
    assert p.update["issuelinks"] == [
        {
            "add": {
                "type": {"name": "Blocks"},
                "outwardIssue": {"key": "OTHER-1"},
            },
        },
    ]


def test_update_builder_build_dict_format():
    d = (
        UpdateBuilder("PLAT-8")
        .set_summary("S")
        .add_labels("x")
        .build_dict()
    )
    assert d == {
        "fields": {"summary": "S"},
        "update": {"labels": [{"add": "x"}]},
    }


def test_transition_basic():
    t = Transition("FOO-1", "In Progress")
    assert t.issue_key == "FOO-1"
    assert t.status == "In Progress"
    assert t.fields == {}
    assert t.update == {}
    assert t.resolution is None


def test_transition_with_resolution():
    t = Transition("FOO-2", "Done", resolution="Fixed")
    assert t.resolution == "Fixed"
    assert t.fields["resolution"] == {"name": "Fixed"}


def test_transition_as_args():
    t = Transition("FOO-3", "Done", fields={"customfield_1": "v"}, update={"comment": []})
    assert t.as_args() == {
        "issue_key": "FOO-3",
        "status_name": "Done",
        "fields": {"customfield_1": "v"},
        "update": {"comment": []},
    }


def test_transition_builder_chain():
    t = (
        TransitionBuilder("FOO-4", "Done")
        .resolution("Won't Do")
        .set_field("timeSpent", "1h")
        .build()
    )
    assert isinstance(t, Transition)
    assert t.resolution == "Won't Do"
    assert t.fields["resolution"] == {"name": "Won't Do"}
    assert t.fields["timeSpent"] == "1h"


def test_comment_plain_text():
    c = Comment("hello")
    assert c.body == "hello"
    assert c.visibility is None


def test_comment_with_visibility():
    vis = Visibility("role", "Developers")
    c = Comment("secret", visibility=vis)
    assert c.visibility == vis


def test_comment_as_args():
    c = Comment("body", visibility=Visibility("group", "jira-users"))
    assert c.as_args() == {
        "comment": "body",
        "visibility": {"type": "group", "value": "jira-users"},
    }


def test_visibility_invalid_type_raises():
    with pytest.raises(ValueError, match="role' or 'group"):
        Visibility("team", "x")


def test_project_from_dict():
    assert Project.from_dict({"key": "ABC"}) == Project(key="ABC")
    assert Project.from_dict({"id": "9"}) == Project(id="9")


def test_user_from_dict_cloud_and_server():
    assert User.from_dict({"accountId": "a1"}) == User(account_id="a1")
    assert User.from_dict({"name": "jdoe"}) == User(name="jdoe")


def test_issue_fields_from_dict_round_trip():
    issue = (
        task()
        .project(key="RT")
        .summary("Round trip")
        .priority(level=PriorityLevel.HIGH)
        .labels("l1", "l2")
        .build()
    )
    raw_fields = serialize(issue)["fields"]
    parsed = IssueFields.from_dict(raw_fields)
    assert parsed.project == Project(key="RT")
    assert parsed.summary == "Round trip"
    assert parsed.priority == Priority(name="High")
    assert parsed.labels == ["l1", "l2"]
    assert parsed.issue_type == IssueType(name="Task")


def test_jira_issue_from_dict_returns_correct_type():
    data = {
        "project": {"key": "P"},
        "summary": "Bug body",
        "issuetype": {"name": "Bug"},
    }
    issue = JiraIssue.from_dict(data)
    assert isinstance(issue, Bug)
    assert issue.fields.summary == "Bug body"


def test_jira_issue_from_dict_with_fields_wrapper():
    data = {
        "fields": {
            "project": {"key": "P"},
            "summary": "Wrapped",
            "issuetype": {"name": "Task"},
        },
    }
    issue = JiraIssue.from_dict(data)
    assert isinstance(issue, Task)
    assert issue.fields.project == Project(key="P")


def test_jira_issue_repr():
    issue = JiraIssue()
    issue.fields = IssueFields(project=Project(key="DEMO"), summary="Short title")
    assert repr(issue) == "JiraIssue(project='DEMO', summary='Short title')"
    issue.fields.summary = "y" * 60
    assert repr(issue) == "JiraIssue(project='DEMO', summary='" + "y" * 47 + "...')"


def test_builder_validate_passes_for_valid_issue():
    b = task().project(key="P").summary("OK").validate()
    issue = b.build()
    assert validate(issue) == []


def test_builder_validate_raises_for_invalid_issue():
    with pytest.raises(ValueError, match="Issue validation failed"):
        task().summary("Missing project").validate()


def test_bulk_serialize_produces_list():
    i1 = task().project(key="P").summary("One").build()
    i2 = task().project(key="P").summary("Two").build()
    out = bulk_serialize([i1, i2])
    assert isinstance(out, list)
    assert len(out) == 2
    assert out[0]["fields"]["summary"] == "One"
    assert out[1]["fields"]["summary"] == "Two"


def test_bulk_serialize_with_mapping():
    mapping = FieldMapping(epic_link_field="customfield_777")
    issue = task().project(key="P").summary("S").epic_link("E-99").build()
    out = bulk_serialize([issue], mapping=mapping)
    assert out[0]["fields"]["customfield_777"] == "E-99"
