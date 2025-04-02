#!/usr/bin/env python3
"""
Integration tests for the Jira v3 API.
These tests require a real Jira instance to run against.
"""

import os
import unittest
from dotenv import load_dotenv

from atlassian.jira import (
    get_jira_instance, 
    get_users_jira_instance,
    get_issues_jira_instance,
    get_software_jira_instance,
    get_permissions_jira_instance,
    get_search_jira_instance
)


class JiraV3IntegrationTestCase(unittest.TestCase):
    """Base class for all Jira v3 integration tests."""

    @classmethod
    def setUpClass(cls):
        """Set up the test case."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get credentials from environment variables
        cls.jira_url = os.environ.get("JIRA_URL")
        cls.jira_username = os.environ.get("JIRA_USERNAME")
        cls.jira_api_token = os.environ.get("JIRA_API_TOKEN")
        cls.jira_project_key = os.environ.get("JIRA_PROJECT_KEY", "TEST")

        if not all([cls.jira_url, cls.jira_username, cls.jira_api_token]):
            raise unittest.SkipTest(
                "JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN environment variables must be set"
            )

        # Create Jira instances
        cls.jira = get_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )
        
        # Create specialized Jira instances
        cls.users_jira = get_users_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )
        
        cls.issues_jira = get_issues_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )
        
        cls.software_jira = get_software_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )
        
        cls.permissions_jira = get_permissions_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )
        
        cls.search_jira = get_search_jira_instance(
            url=cls.jira_url,
            username=cls.jira_username,
            password=cls.jira_api_token,
            api_version=3,
            legacy_mode=False
        )


class TestJiraV3Integration(JiraV3IntegrationTestCase):
    """Integration tests for the core Jira v3 functionality."""

    def test_get_current_user(self):
        """Test retrieving the current user."""
        current_user = self.jira.get_current_user()
        
        # Verify that the response contains expected fields
        self.assertIn("accountId", current_user)
        self.assertIn("displayName", current_user)
        self.assertIn("emailAddress", current_user)

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        projects = self.jira.get_all_projects()
        
        # Verify that projects are returned
        self.assertIsInstance(projects, list)
        self.assertTrue(len(projects) > 0, "No projects returned")
        
        # Verify project structure
        first_project = projects[0]
        self.assertIn("id", first_project)
        self.assertIn("key", first_project)
        self.assertIn("name", first_project)

    def test_get_project(self):
        """Test retrieving a specific project."""
        project = self.jira.get_project(self.jira_project_key)
        
        # Verify project data
        self.assertEqual(project["key"], self.jira_project_key)
        self.assertIn("id", project)
        self.assertIn("name", project)
        
    def test_search_issues(self):
        """Test searching for issues."""
        jql = f"project = {self.jira_project_key} ORDER BY created DESC"
        search_results = self.jira.search_issues(jql, max_results=10)
        
        # Verify search results structure
        self.assertIn("issues", search_results)
        self.assertIn("total", search_results)
        
        # If there are any issues, verify their structure
        if search_results["total"] > 0:
            first_issue = search_results["issues"][0]
            self.assertIn("id", first_issue)
            self.assertIn("key", first_issue)
            self.assertIn("fields", first_issue)


class TestJiraV3UsersIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Users API."""
    
    def test_get_user(self):
        """Test retrieving user information."""
        # First get current user to get an account ID
        current_user = self.jira.get_current_user()
        account_id = current_user["accountId"]
        
        # Get user by account ID
        user = self.users_jira.get_user(account_id=account_id)
        
        # Verify user structure
        self.assertEqual(user["accountId"], account_id)
        self.assertIn("displayName", user)
        self.assertIn("emailAddress", user)

    def test_find_users(self):
        """Test searching for users."""
        # Get current user to use display name as search query
        current_user = self.jira.get_current_user()
        query = current_user["displayName"].split()[0]  # Use first name as query
        
        # Search for users
        users = self.users_jira.find_users(query)
        
        # Verify users are returned
        self.assertIsInstance(users, list)
        self.assertTrue(len(users) > 0, "No users found")
        
        # Verify user structure
        self.assertIn("accountId", users[0])
        self.assertIn("displayName", users[0])
        
    def test_get_groups(self):
        """Test retrieving groups."""
        groups = self.users_jira.get_groups()
        
        # Verify groups are returned
        self.assertIn("groups", groups)
        
        # If there are any groups, verify their structure
        if len(groups["groups"]) > 0:
            first_group = groups["groups"][0]
            self.assertIn("name", first_group)
            self.assertIn("groupId", first_group)


class TestJiraV3IssuesIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Issues API."""
    
    def test_get_issue_types(self):
        """Test retrieving issue types."""
        issue_types = self.issues_jira.get_issue_types()
        
        # Verify issue types are returned
        self.assertIsInstance(issue_types, list)
        self.assertTrue(len(issue_types) > 0, "No issue types returned")
        
        # Verify issue type structure
        first_issue_type = issue_types[0]
        self.assertIn("id", first_issue_type)
        self.assertIn("name", first_issue_type)
        self.assertIn("description", first_issue_type)

    def test_create_and_get_issue(self):
        """Test creating and retrieving an issue."""
        # Create a new issue
        issue_data = {
            "fields": {
                "project": {"key": self.jira_project_key},
                "summary": "Test issue created by integration test",
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "This is a test issue created by the integration test."
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Task"}
            }
        }
        
        try:
            created_issue = self.issues_jira.create_issue(issue_data)
            
            # Verify created issue structure
            self.assertIn("id", created_issue)
            self.assertIn("key", created_issue)
            self.assertTrue(created_issue["key"].startswith(self.jira_project_key))
            
            # Get the created issue
            issue_key = created_issue["key"]
            retrieved_issue = self.issues_jira.get_issue(issue_key)
            
            # Verify retrieved issue structure
            self.assertEqual(retrieved_issue["key"], issue_key)
            self.assertEqual(retrieved_issue["fields"]["summary"], "Test issue created by integration test")
            
            # Clean up - delete the created issue
            self.issues_jira.delete_issue(issue_key)
        except Exception as e:
            self.fail(f"Failed to create or retrieve issue: {str(e)}")


class TestJiraV3SoftwareIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Software API."""
    
    def test_get_all_boards(self):
        """Test retrieving all boards."""
        try:
            boards = self.software_jira.get_all_boards()
            
            # Verify boards are returned
            self.assertIn("values", boards)
            
            # If there are any boards, verify their structure
            if len(boards["values"]) > 0:
                first_board = boards["values"][0]
                self.assertIn("id", first_board)
                self.assertIn("name", first_board)
                self.assertIn("type", first_board)
        except Exception as e:
            # Some Jira instances might not have Software (board functionality)
            if "404" in str(e):
                self.skipTest("Jira Software (board functionality) not available on this instance")
            else:
                raise


class TestJiraV3PermissionsIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Permissions API."""
    
    def test_get_my_permissions(self):
        """Test retrieving permissions for the current user."""
        permissions = self.permissions_jira.get_my_permissions()
        
        # Verify permissions are returned
        self.assertIn("permissions", permissions)
        
        # Check for common permissions
        permission_keys = permissions["permissions"].keys()
        common_permissions = ["BROWSE_PROJECTS", "CREATE_ISSUES", "ASSIGNABLE_USER"]
        
        for permission in common_permissions:
            if permission in permission_keys:
                self.assertIn("key", permissions["permissions"][permission])
                self.assertIn("name", permissions["permissions"][permission])
                self.assertIn("type", permissions["permissions"][permission])


class TestJiraV3SearchIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Search API."""
    
    def test_search_issues(self):
        """Test searching for issues."""
        jql = f"project = {self.jira_project_key} ORDER BY created DESC"
        search_results = self.search_jira.search_issues(jql, max_results=10)
        
        # Verify search results structure
        self.assertIn("issues", search_results)
        self.assertIn("total", search_results)
        
        # If there are any issues, verify their structure
        if search_results["total"] > 0:
            first_issue = search_results["issues"][0]
            self.assertIn("id", first_issue)
            self.assertIn("key", first_issue)
            self.assertIn("fields", first_issue)

    def test_get_field_reference_data(self):
        """Test retrieving field reference data for JQL."""
        field_reference_data = self.search_jira.get_field_reference_data()
        
        # Verify field reference data structure
        self.assertIn("visibleFieldNames", field_reference_data)
        self.assertIn("jqlReservedWords", field_reference_data)


if __name__ == "__main__":
    unittest.main() 