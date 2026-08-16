"""Structural tests for the complete, concrete Jira Cloud method surface."""

import inspect
from unittest import TestCase

from atlassian.jira.core_methods import JiraCloudCoreMethods
from atlassian.jira.jira_server import Jira as JiraServer
from atlassian.jira.service_management_methods import JiraServiceManagementMethods
from atlassian.jira.software_methods import JiraSoftwareMethods


class RecordingClient:
    """Minimal REST client that records requests made by generated methods."""

    api_version = 3

    def __init__(self):
        self.calls = []

    def resource_url(self, resource, api_root=None, api_version=None):
        return "/".join(str(part).strip("/") for part in (api_root, api_version, resource) if part is not None)

    def __getattr__(self, method):
        if method not in {"get", "post", "put", "delete", "patch"}:
            raise AttributeError(method)

        def request(url, **kwargs):
            self.calls.append((method, url, kwargs))
            return {"method": method, "url": url}

        return request


class TestJiraCloudMethodCoverage(TestCase):
    METHOD_GROUPS = (
        (JiraCloudCoreMethods, 617, "rest/api/3/"),
        (JiraSoftwareMethods, 105, "rest/"),
        (JiraServiceManagementMethods, 75, "rest/servicedeskapi/"),
    )

    @staticmethod
    def _required_arguments(method):
        signature = inspect.signature(method)
        return [
            "value"
            for parameter in list(signature.parameters.values())[1:]
            if parameter.default is inspect.Parameter.empty
            and parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]

    def test_every_documented_method_is_concrete_and_dispatches(self):
        for method_group, expected_count, prefix in self.METHOD_GROUPS:
            methods = [method for _, method in inspect.getmembers(method_group, inspect.isfunction)]
            self.assertEqual(len(methods), expected_count)

            for method in methods:
                client = RecordingClient()
                result = method(client, *self._required_arguments(method))

                self.assertEqual(result["method"], client.calls[0][0])
                self.assertTrue(client.calls[0][1].startswith(prefix))
                self.assertNotIn("{", client.calls[0][1])
                self.assertEqual(client.calls[0][2]["data"], None)

    def test_every_cloud_method_has_a_complete_docstring(self):
        for method_group, _, _ in self.METHOD_GROUPS:
            for _, method in inspect.getmembers(method_group, inspect.isfunction):
                docstring = inspect.getdoc(method)
                self.assertIsNotNone(docstring)
                self.assertIn("Args:", docstring)
                self.assertIn("Returns:", docstring)

    def test_every_public_jira_server_method_has_a_docstring(self):
        methods = inspect.getmembers(JiraServer, inspect.isfunction)
        undocumented = [name for name, method in methods if not name.startswith("_") and not inspect.getdoc(method)]

        self.assertEqual(undocumented, [])
