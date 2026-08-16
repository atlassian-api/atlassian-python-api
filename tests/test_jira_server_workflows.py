from unittest import TestCase
from unittest.mock import patch

from atlassian import JiraServer


class TestJiraServerWorkflows(TestCase):
    def test_get_workflow_transition_rule_configurations_uses_v2_route(self):
        jira = JiraServer("https://jira.example.com")

        with patch.object(jira, "get", return_value={"values": []}) as get:
            result = jira.get_workflow_transition_rule_configurations(
                start_at=10,
                max_results=25,
                types=["postfunction", "validator"],
                workflow_names="Release workflow",
                draft=False,
            )

        self.assertEqual(result, {"values": []})
        get.assert_called_once_with(
            "rest/api/2/workflow/rule/config",
            params={
                "startAt": 10,
                "maxResults": 25,
                "types": ["postfunction", "validator"],
                "workflowNames": "Release workflow",
                "draft": False,
            },
        )

    def test_bulk_issue_collects_server_pages(self):
        jira = JiraServer("https://jira.example.com")
        first_page = {"issues": [{"key": "DEMO-1"}], "startAt": 0, "maxResults": 1, "total": 2}
        second_page = {"issues": [{"key": "DEMO-2"}], "startAt": 1, "maxResults": 1, "total": 2}

        with patch.object(jira, "jql", side_effect=[first_page, second_page]) as jql:
            result, missing_issues = jira.bulk_issue(["DEMO-1", "DEMO-2"], fields=["summary"], limit=1)

        self.assertEqual([issue["key"] for issue in result["issues"]], ["DEMO-1", "DEMO-2"])
        self.assertEqual(missing_issues, [])
        self.assertEqual(
            jql.call_args_list,
            [
                (("key in (DEMO-1, DEMO-2)",), {"fields": ["summary"], "start": 0, "limit": 1}),
                (("key in (DEMO-1, DEMO-2)",), {"fields": ["summary"], "start": 1, "limit": 1}),
            ],
        )
