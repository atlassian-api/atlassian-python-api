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
        """Can retrieve an Issue by ID"""
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

    def test_get_issue_comments(self):
        """Can retrieve issue comments"""
        resp = self.jira.issue_get_comments("FOO-123")
        self.assertEqual(len(resp["comments"]), 2)
        self.assertEqual(resp["total"], 2)

    def test_get_issue_comment(self):
        """Can retrieve issue comments"""
        resp = self.jira.issue_get_comment("FOO-123", 10000)
        self.assertEqual(resp["body"], "Some Text comment")
        self.assertEqual(resp["id"], "10000")

    def test_get_issue_comment_not_found(self):
        """Get comment on issue by id, but not found"""
        with self.assertRaises(HTTPError):
            self.jira.epic_issues("BAR-11")

    def test_post_issue_with_invalid_request(self):
        """Post an issue but receive a 400 error response"""
        with self.assertRaises(HTTPError):
            self.jira.create_issue(fields={"issuetype": "foo", "summary": "summary", "project": "project"})
