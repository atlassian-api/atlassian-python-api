from unittest import TestCase
from unittest.mock import patch

from atlassian import Jira, JiraCloud, JiraServer, JiraServiceManagement, JiraSoftware, ServiceDesk, create_jira_cloud
from atlassian.jira import Jira as PackageJira


class TestJiraCloudClients(TestCase):
    def test_legacy_clients_keep_their_defaults(self):
        jira = Jira("https://example.atlassian.net")
        service_desk = ServiceDesk("https://example.atlassian.net")

        self.assertEqual(jira.api_version, "2")
        self.assertFalse(jira.cloud)
        self.assertFalse(service_desk.cloud)
        self.assertIs(Jira, JiraServer)
        self.assertIs(PackageJira, JiraServer)

    def test_core_client_defaults_to_v3_and_forces_cloud_mode(self):
        jira = JiraCloud("https://example.atlassian.net", cloud=False)

        self.assertEqual(jira.api_version, 3)
        self.assertTrue(jira.cloud)
        self.assertEqual(jira.endpoint("issue/ABC-1"), "rest/api/3/issue/ABC-1")
        self.assertEqual(jira.endpoint("issue/ABC-1", api_version=2), "rest/api/2/issue/ABC-1")

    def test_core_client_rejects_unsupported_versions(self):
        with self.assertRaisesRegex(ValueError, "must be 2 or 3"):
            JiraCloud("https://example.atlassian.net", api_version=1)

    def test_core_factory_is_explicit_and_versioned(self):
        jira = create_jira_cloud("https://example.atlassian.net", api_version="2")

        self.assertIsInstance(jira, JiraCloud)
        self.assertEqual(jira.api_version, 2)

    def test_core_methods_cover_the_supplied_v3_document(self):
        jira = JiraCloud("https://example.atlassian.net")

        with patch.object(jira, "get", return_value={}) as get:
            jira.get_issue("ABC-1", fields="summary")
        get.assert_called_once_with("rest/api/3/issue/ABC-1", params={"fields": "summary"}, data=None)

    def test_core_methods_honor_the_selected_v2_route(self):
        jira = JiraCloud("https://example.atlassian.net", api_version=2)

        with patch.object(jira, "get", return_value={}) as get:
            jira.get_issue("ABC-1")
        get.assert_called_once_with("rest/api/2/issue/ABC-1", params=None, data=None)

    def test_core_client_supports_enhanced_jql_at_v3(self):
        jira = JiraCloud("https://example.atlassian.net", api_version=2)

        with patch.object(jira, "get", return_value={"issues": [], "isLast": True}) as get:
            jira.enhanced_jql(
                "project = EXAMPLE ORDER BY key DESC",
                fields=["summary", "description"],
                nextPageToken="next-token",
                limit=100,
                expand="names",
            )

        get.assert_called_once_with(
            "rest/api/3/search/jql",
            params={
                "jql": "project = EXAMPLE ORDER BY key DESC",
                "fields": "summary,description",
                "nextPageToken": "next-token",
                "maxResults": 100,
                "expand": "names",
            },
        )

    def test_core_client_enhanced_jql_collects_cursor_pages(self):
        jira = JiraCloud("https://example.atlassian.net")

        with patch.object(
            jira,
            "enhanced_jql",
            side_effect=[
                {"issues": [{"key": "EXAMPLE-1"}], "nextPageToken": "next", "isLast": False},
                {"issues": [{"key": "EXAMPLE-2"}], "isLast": True},
            ],
        ):
            issues = jira.enhanced_jql_get_list_of_tickets("project = EXAMPLE")

        self.assertEqual([issue["key"] for issue in issues], ["EXAMPLE-1", "EXAMPLE-2"])

    def test_software_client_builds_each_documented_api_root(self):
        jira = JiraSoftware("https://example.atlassian.net", cloud=False)

        self.assertTrue(jira.cloud)
        self.assertEqual(jira.endpoint("agile", "board/42/sprint"), "rest/agile/1.0/board/42/sprint")
        self.assertEqual(jira.endpoint("software", "board/42/backlog"), "rest/software/1.0/board/42/backlog")
        self.assertEqual(jira.endpoint("devinfo", "bulk"), "rest/devinfo/0.10/bulk")
        self.assertEqual(jira.endpoint("builds", "bulk"), "rest/builds/0.1/bulk")
        with patch.object(jira, "get", return_value={}) as get:
            jira.get_all_boards(max_results=10)
        get.assert_called_once_with("rest/agile/1.0/board", params={"maxResults": 10}, data=None)

    def test_software_client_rejects_unknown_api_root(self):
        jira = JiraSoftware("https://example.atlassian.net")

        with self.assertRaisesRegex(ValueError, "Unsupported Jira Software API"):
            jira.endpoint("api/3", "issue")

    def test_jsm_client_is_independent_from_the_legacy_service_desk_client(self):
        service_management = JiraServiceManagement("https://example.atlassian.net", cloud=False)

        self.assertNotIsInstance(service_management, ServiceDesk)
        self.assertTrue(service_management.cloud)
        self.assertEqual(service_management.endpoint("request/ABC-1"), "rest/servicedeskapi/request/ABC-1")
        with patch.object(service_management, "get", return_value={}) as get:
            service_management.get_customer_request_by_id_or_key("ABC-1")
        get.assert_called_once_with("rest/servicedeskapi/request/ABC-1", params=None, data=None)

    def test_legacy_service_desk_lists_pages_of_service_desks(self):
        service_desk = ServiceDesk("https://example.atlassian.net")

        with patch.object(service_desk, "get", return_value={"values": []}) as get:
            result = service_desk.get_service_desks(start=50, limit=25)

        self.assertEqual(result, [])
        get.assert_called_once_with(
            "rest/servicedeskapi/servicedesk",
            headers=service_desk.experimental_headers,
            params={"start": 50, "limit": 25},
        )
