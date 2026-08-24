from unittest.mock import patch

import pytest

from atlassian import Jira, JiraCloud, JiraServer


def test_server_add_version_accepts_payload_and_uses_v2():
    jira = JiraServer("https://jira.example.com")
    payload = {"name": "TestVersion", "description": "Description", "released": False}

    with patch.object(jira, "post", return_value={"id": "10001"}) as post:
        result = jira.add_version(project_key="TST", project_id=10000, version=payload)

    assert result == {"id": "10001"}
    post.assert_called_once_with(
        "rest/api/2/version",
        data={
            "name": "TestVersion",
            "description": "Description",
            "released": False,
            "project": "TST",
            "projectId": 10000,
        },
    )


def test_cloud_compatibility_add_version_uses_v3_and_project_id():
    jira = Jira("https://example.atlassian.net", cloud=True)

    with patch.object(jira, "post") as post:
        jira.add_version(project_key="TST", project_id="10000", version="TestVersion")

    post.assert_called_once_with(
        "rest/api/3/version",
        data={"name": "TestVersion", "archived": False, "released": False, "projectId": 10000},
    )


def test_server_accepts_project_key_when_project_id_repeats_the_key():
    jira = JiraServer("https://jira.example.com")

    with patch.object(jira, "post") as post:
        jira.add_version(project_key="TST", project_id="TST", version={"name": "TestVersion"})

    post.assert_called_once_with("rest/api/2/version", data={"name": "TestVersion", "project": "TST"})


def test_cloud_core_add_version_uses_v3():
    jira = JiraCloud("https://example.atlassian.net")

    with patch.object(jira, "post") as post:
        jira.add_version(10000, {"name": "TestVersion"})

    post.assert_called_once_with("rest/api/3/version", data={"name": "TestVersion", "projectId": 10000})


def test_cloud_add_version_requires_numeric_project_id():
    jira = JiraCloud("https://example.atlassian.net")

    with pytest.raises((TypeError, ValueError)):
        jira.add_version("TST", "TestVersion")
