# coding: utf8
"""Tests for Jira Modules"""

from unittest import TestCase
from unittest.mock import patch

from requests import HTTPError

from atlassian import jira

from .mockup import mockup_server


class TestJira(TestCase):
    def setUp(self):
        self.jira = jira.Jira(f"{mockup_server()}/jira", username="username", password="password", cloud=True)

    def test_get_issue(self):
        """Can retrieve an Issue by ID"""
        resp = self.jira.issue("FOO-123")
        self.assertEqual(resp["key"], "FOO-123")

    @patch.object(jira.Jira, "get")
    def test_get_all_application_roles(self, mock_get):
        """Lists ApplicationRoles from the Server v2 resource."""
        self.jira.get_all_application_roles()

        mock_get.assert_called_once_with("rest/api/2/applicationrole")

    @patch.object(jira.Jira, "get")
    def test_get_application_role(self, mock_get):
        """Gets one ApplicationRole from the Server v2 resource."""
        self.jira.get_application_role("jira-software")

        mock_get.assert_called_once_with("rest/api/2/applicationrole/jira-software")

    @patch.object(jira.Jira, "put")
    def test_update_application_roles_uses_etag_when_provided(self, mock_put):
        roles = [{"key": "jira-software", "groups": ["jira-software-users"]}]

        self.jira.update_application_roles(roles, if_match='"role-version"')

        self.assertEqual(mock_put.call_args.args[0], "rest/api/2/applicationrole")
        self.assertEqual(
            mock_put.call_args.kwargs["data"], '[{"key": "jira-software", "groups": ["jira-software-users"]}]'
        )
        self.assertEqual(
            mock_put.call_args.kwargs["headers"],
            {"Content-Type": "application/json", "Accept": "application/json", "If-Match": '"role-version"'},
        )

    def test_get_issue_not_found(self):
        """Receive HTTP Error when Issue does not exist"""
        with self.assertRaises(HTTPError):
            self.jira.issue("FOO-321")

    @patch.object(jira.Jira, "get")
    def test_get_custom_fields_uses_query_parameter_in_cloud(self, mock_get):
        self.jira.get_custom_fields(search="Customer tier")

        self.assertEqual(
            mock_get.call_args.kwargs["params"], {"query": "Customer tier", "startAt": 1, "maxResults": 50}
        )

    @patch.object(jira.Jira, "get")
    def test_get_all_fields_uses_v3_for_cloud(self, mock_get):
        self.jira.get_all_fields()

        mock_get.assert_called_once_with("rest/api/3/field")

    @patch.object(jira.Jira, "get")
    def test_enhanced_jql_uses_the_cloud_v3_endpoint(self, mock_get):
        self.jira.enhanced_jql(
            "created >= -30d ORDER BY created DESC",
            fields="summary,description",
            nextPageToken="next-token",
            expand="names",
        )

        mock_get.assert_called_once_with(
            "rest/api/3/search/jql",
            params={
                "jql": "created >= -30d ORDER BY created DESC",
                "fields": "summary,description",
                "nextPageToken": "next-token",
                "expand": "names",
            },
        )

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

    def test_pin_issue_comment(self):
        """Can pin a comment on an issue"""
        self.jira.issue_pin_comment("FOO-123", 10000)

    def test_unpin_issue_comment(self):
        """Can unpin a comment on an issue"""
        self.jira.issue_unpin_comment("FOO-123", 10000)

    def test_post_issue_with_invalid_request(self):
        """Post an issue but receive a 400 error response"""
        with self.assertRaises(HTTPError):
            self.jira.create_issue(fields={"issuetype": "foo", "summary": "summary", "project": "project"})

    def test_post_issue_expect_failed_authentication(self):
        """Post an issue but receive a 401 error response"""
        with self.assertRaises(HTTPError):
            self.jira.create_issue(fields={"issuetype": "fail", "summary": "authentication", "project": "project"})

    def test_get_issue_property_keys(self):
        """Can retrieve issue property keys"""
        resp = self.jira.get_issue_property_keys("FOO-123")
        self.assertEqual(resp["keys"][0]["key"], "Bar1")
        self.assertEqual(
            resp["keys"][0]["self"], "https://sample.atlassian.net/rest/api/2/issue/FOO-123/properties/Bar1"
        )

    def test_get_issue_property_keys_not_found(self):
        with self.assertRaises(HTTPError):
            self.jira.get_issue_property_keys("BAR-11")

    def test_set_issue_property_create(self):
        self.jira.set_issue_property("FOO-123", "Bar2New", data={"test.id": "123456", "test.mem": "250M"})

    def test_set_issue_property_update(self):
        self.jira.set_issue_property("FOO-123", "Bar1", data={"test.id": "123456", "test.mem": "250M"})

    def test_get_issue_property(self):
        resp = self.jira.get_issue_property("FOO-123", "Bar1")
        self.assertEqual(resp["value"]["test.id"], "123")
        self.assertEqual(resp["value"]["test.time"], "1m")

    def test_get_issue_property_not_found(self):
        with self.assertRaises(HTTPError):
            self.jira.get_issue_property("FOO-123", "NotFoundBar1")
        with self.assertRaises(HTTPError):
            self.jira.get_issue_property("FOONotFound-123", "NotFoundBar1")

    def test_delete_issue_property(self):
        self.jira.delete_issue_property("FOO-123", "Bar1")

    def test_delete_issue_property_not_found(self):
        with self.assertRaises(HTTPError):
            self.jira.get_issue_property("FOO-123", "NotFoundBar1")
        with self.assertRaises(HTTPError):
            self.jira.get_issue_property("FOONotFound-123", "NotFoundBar1")

    def test_post_issue_remotelink(self):
        """Create a new remote link"""
        resp = self.jira.create_or_update_issue_remote_links(
            "FOO-123",
            "https://confluence.atlassian-python.atlassian.net/display/Test",
            "Unused link text",
        )
        self.assertEqual(resp["id"], 10000)
        self.assertEqual(
            resp["self"], "https://atlassian-python.atlassian.net/rest/api/2/issue/FOO-123/remotelink/10000"
        )
        self.assertDictEqual(resp["application"], {})

    def test_post_issue_remotelink_confluence(self):
        """Create a new Confluence remote link"""
        resp = self.jira.create_or_update_issue_remote_links(
            "FOO-123",
            "https://confluence.atlassian-python.atlassian.net/display/Test",
            "Unused link text",
            global_id="appId=00000000-0000-0000-0000-000000000000&pageId=0",
            application={
                "type": "com.atlassian.confluence",
                "name": "Confluence",
            },
        )
        self.assertEqual(resp["id"], 10000)
        self.assertEqual(
            resp["self"], "https://atlassian-python.atlassian.net/rest/api/2/issue/FOO-123/remotelink/10000"
        )
        self.assertDictEqual(
            resp["application"],
            {
                "type": "com.atlassian.confluence",
                "name": "Confluence",
            },
        )
