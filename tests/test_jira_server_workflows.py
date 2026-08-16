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
