"""Tests for Requirement Yogi clients."""

import inspect
from unittest import TestCase
from unittest.mock import Mock

from atlassian import YogiConfluenceCloud, YogiConfluenceDC, YogiJiraCloud, YogiJiraDC
from atlassian.yogi.cloud import YogiCloud


class TestYogiCloud(TestCase):
    def test_cloud_clients_have_all_documented_operations(self):
        """Every supplied Cloud Swagger operation is concrete and callable."""
        methods = [
            (name, method)
            for name, method in inspect.getmembers(YogiCloud, inspect.isfunction)
            if method.__module__ == "atlassian.yogi.cloud" and name != "__init__"
        ]
        self.assertEqual(len(methods), 128)
        for client_type in (YogiJiraCloud, YogiConfluenceCloud):
            client = client_type()
            for name, method in methods:
                transports = {verb: Mock(return_value={}) for verb in ("get", "post", "put", "delete")}
                for verb, transport in transports.items():
                    setattr(client, verb, transport)
                arguments = {
                    parameter.name: "value"
                    for parameter in list(inspect.signature(method).parameters.values())[1:]
                    if parameter.default is inspect.Parameter.empty
                    and parameter.kind is not inspect.Parameter.VAR_KEYWORD
                }
                getattr(client, name)(**arguments)
                calls = [transport.call_args for transport in transports.values() if transport.called]
                self.assertEqual(len(calls), 1, name)
                self.assertNotIn("{", calls[0].args[0], name)


class TestYogiDataCenter(TestCase):
    def test_jira_routes(self):
        """Jira Data Center methods use the public Requirement Yogi routes."""
        client = YogiJiraDC("https://jira.example.com")
        client.get = Mock(return_value={})
        client.post = Mock(return_value={})
        client.put = Mock(return_value={})
        client.get_issue_links("PROJ-1", relationship="implements")
        client.create_issue_links("PROJ-1", [])
        client.sync_issues(["PROJ-1"])
        self.assertEqual(client.get.call_args.args[0], "rest/reqs/1/issuelinks/PROJ-1")
        self.assertEqual(client.post.call_args.args[0], "rest/reqs/1/issuelinks/PROJ-1")
        self.assertEqual(client.put.call_args.args[0], "rest/reqs/1/sync")

    def test_confluence_routes(self):
        """Confluence Data Center methods use the public Requirement Yogi routes."""
        client = YogiConfluenceDC("https://confluence.example.com")
        client.get = Mock(return_value={})
        client.post = Mock(return_value={})
        client.search_requirements("ENG", query="REQ")
        client.create_baseline("ENG", {"name": "v1"})
        self.assertEqual(client.get.call_args.args[0], "rest/reqs/1/requirement2/ENG")
        self.assertEqual(client.post.call_args.args[0], "rest/reqs/1/baseline/ENG/1/create")
