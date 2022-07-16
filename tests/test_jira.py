# coding: utf8
"""Tests for Jira Modules"""
from unittest import TestCase
from atlassian import jira
from .mockup import mockup_server
from requests import HTTPError


class TestJira(TestCase):
    def setUp(self):
        self.jira = jira.Jira("{}/jira".format(mockup_server()), username="username", password="password", cloud=True)

    def test_get_issue(self):
        """Can retrieve an Issue by Id"""
        resp = self.jira.issue("FOO-123")
        self.assertEqual(resp["key"], "FOO-123")

    def test_get_issue_not_found(self):
        """Receive HTTP Error when Issue does not exist"""
        with self.assertRaises(HTTPError):
            self.jira.issue("FOO-321")

    def test_get_epic_issues(self):
        resp = self.jira.epic_issues("BAR-22")
        self.assertIsInstance(resp["issues"], list)

    def test_get_epic_issues_not_found(self):
        with self.assertRaises(HTTPError):
            self.jira.epic_issues("BAR-11")
