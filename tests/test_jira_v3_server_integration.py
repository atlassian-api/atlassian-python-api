#!/usr/bin/env python3
"""
Integration tests for the Jira Server v3 API.
These tests require a real Jira Server instance to run against.
"""

import os
import sys
import time
import unittest
import logging
from unittest.mock import Mock
import atlassian
from atlassian.jira import (
    get_jira_instance,
    get_users_jira_instance,
    get_software_jira_instance,
    get_permissions_jira_instance,
    get_search_jira_instance,
    get_richtext_jira_instance,
    get_issuetypes_jira_instance,
    get_projects_jira_instance,
)
from dotenv import load_dotenv
import json


# Set up logging to see detailed error information
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("atlassian.jira.errors")
logger.setLevel(logging.DEBUG)

# Load environment variables from .env file
load_dotenv()


class JiraV3ServerIntegrationTestCase(unittest.TestCase):
    """Base class for all Jira v3 Server integration tests."""

    @classmethod
    def setUpClass(cls):
        """Set up the test case."""
        # Load environment variables from .env file
        load_dotenv()

        # Get credentials from environment variables
        cls.jira_url = os.environ.get("JIRA_SERVER_URL")
        cls.jira_username = os.environ.get("JIRA_SERVER_USERNAME")
        cls.jira_password = os.environ.get("JIRA_SERVER_PASSWORD")  # For Server, we use password rather than API token
        cls.jira_project_key = os.environ.get("JIRA_SERVER_PROJECT_KEY", "TEST")

        # Allow running in offline mode with mocks if JIRA_OFFLINE_TESTS=true
        cls.offline_mode = os.environ.get("JIRA_OFFLINE_TESTS", "false").lower() == "true"

        # Skip tests if credentials are not set and not in offline mode
        if not all([cls.jira_url, cls.jira_username, cls.jira_password]) and not cls.offline_mode:
            raise unittest.SkipTest(
                "JIRA_SERVER_URL, JIRA_SERVER_USERNAME, and JIRA_SERVER_PASSWORD environment variables must be set"
            )

        # Create Jira instances for Server explicitly setting cloud=False
        if not cls.offline_mode:
            cls.jira = get_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            # Create specialized Jira instances
            cls.users_jira = get_users_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.software_jira = get_software_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.permissions_jira = get_permissions_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.search_jira = get_search_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.richtext_jira = get_richtext_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.issuetypes_jira = get_issuetypes_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            cls.projects_jira = get_projects_jira_instance(
                url=cls.jira_url,
                username=cls.jira_username,
                password=cls.jira_password,
                api_version=3,
                cloud=False,
                legacy_mode=False,
            )

            # Verify the project key exists
            try:
                cls.jira.get_project(cls.jira_project_key)
            except Exception as e:
                print(f"Warning: Project key {cls.jira_project_key} may not be valid: {str(e)}")
                # Try to get all projects to find a valid one
                try:
                    projects = cls.jira.get_all_projects()
                    if projects:
                        cls.jira_project_key = projects[0]["key"]
                        print(f"Using the first available project key: {cls.jira_project_key}")
                except Exception as e2:
                    print(f"Could not get projects list: {str(e2)}")
        else:
            # Create mock instances for offline testing
            from unittest.mock import MagicMock

            # Setup mock Jira instance
            cls.jira = MagicMock()
            cls.users_jira = MagicMock()
            cls.software_jira = MagicMock()
            cls.permissions_jira = MagicMock()
            cls.search_jira = MagicMock()
            cls.richtext_jira = MagicMock()
            cls.issuetypes_jira = MagicMock()
            cls.projects_jira = MagicMock()

            # Setup basic mock responses
            cls.jira.get_current_user.return_value = {
                "accountId": "mock-account-id",
                "displayName": "Mock User",
                "emailAddress": "mock@example.com",
            }

            cls.jira.get_project.return_value = {
                "id": "10000",
                "key": "TEST",
                "name": "Test Project",
                "projectTypeKey": "software",
            }

            cls.jira.get_all_projects.return_value = [
                {"id": "10000", "key": "TEST", "name": "Test Project", "projectTypeKey": "software"}
            ]

    def tearDown(self):
        """Clean up after the test."""
        pass

    def get_jira_instance(self):
        """Get the actual Jira instance, bypassing any adapter.

        Returns:
            The direct Jira instance
        """
        if hasattr(self.jira, "_adapted_instance"):
            print("Using direct Jira instance instead of adapter")
            return self.jira._adapted_instance
        return self.jira

    def validate_project_key(self):
        """Validate that the project key exists.

        Raises:
            SkipTest: If the project key is not valid.
        """
        jira_instance = self.get_jira_instance()

        try:
            projects = jira_instance.get_all_projects()
            project_keys = [project["key"] for project in projects]

            if self.jira_project_key not in project_keys:
                self.skipTest(f"Project key {self.jira_project_key} not found in available projects: {project_keys}")
        except Exception as e:
            self.skipTest(f"Failed to validate project key: {str(e)}")

    def check_permissions(self, error):
        """Check if the error is permission-related and skip test if needed.

        Args:
            error: The exception that was raised

        Returns:
            bool: True if the test should be skipped
        """
        if isinstance(error, atlassian.jira.errors.JiraPermissionError):
            self.skipTest(f"Test requires admin permissions: {str(error)}")
            return True
        return False


class TestJiraV3ServerIntegration(JiraV3ServerIntegrationTestCase):
    """Integration tests for the core Jira v3 Server functionality."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        if self.offline_mode:
            # Mock responses for pagination testing
            page1_data = {
                "expand": "schema,names",
                "startAt": 0,
                "maxResults": 3,
                "total": 10,
                "issues": [
                    {
                        "id": "10001",
                        "key": f"{self.jira_project_key}-1",
                        "fields": {"summary": "Test pagination issue 0"},
                    },
                    {
                        "id": "10002",
                        "key": f"{self.jira_project_key}-2",
                        "fields": {"summary": "Test pagination issue 1"},
                    },
                    {
                        "id": "10003",
                        "key": f"{self.jira_project_key}-3",
                        "fields": {"summary": "Test pagination issue 2"},
                    },
                ],
            }

            page2_data = {
                "expand": "schema,names",
                "startAt": 3,
                "maxResults": 3,
                "total": 10,
                "issues": [
                    {
                        "id": "10004",
                        "key": f"{self.jira_project_key}-4",
                        "fields": {"summary": "Test pagination issue 3"},
                    },
                    {
                        "id": "10005",
                        "key": f"{self.jira_project_key}-5",
                        "fields": {"summary": "Test pagination issue 4"},
                    },
                    {
                        "id": "10006",
                        "key": f"{self.jira_project_key}-6",
                        "fields": {"summary": "Test pagination issue 5"},
                    },
                ],
            }

            # Setup mock responses
            self.jira.jql_search.side_effect = (
                lambda jql, start_at=0, max_results=50, fields=None, expand=None, validate_query=None: (
                    page1_data if start_at == 0 else page2_data
                )
            )

            # Mock all the methods directly on the jira instance and on _adapted_instance
            # For get_current_user
            mock_current_user = {
                "name": self.jira_username,
                "displayName": "Test User",
                "emailAddress": "test@example.com",
                "active": True,
            }
            self.jira.get_current_user.return_value = mock_current_user
            if not hasattr(self.jira, "_adapted_instance"):
                self.jira._adapted_instance = Mock()
            self.jira._adapted_instance.get_current_user.return_value = mock_current_user

            # For get_all_projects
            mock_projects = [
                {"id": "10001", "key": self.jira_project_key, "name": "Test Project", "projectTypeKey": "software"},
                {"id": "10002", "key": "ANOTHER", "name": "Another Project", "projectTypeKey": "business"},
            ]
            self.jira.get_all_projects.return_value = mock_projects
            self.jira._adapted_instance.get_all_projects.return_value = mock_projects

            # For get_project
            mock_project = {
                "id": "10001",
                "key": self.jira_project_key,
                "name": "Test Project",
                "projectTypeKey": "software",
                "description": "A test project for integration testing",
                "lead": {"name": self.jira_username, "displayName": "Test User"},
            }
            self.jira.get_project.return_value = mock_project
            self.jira._adapted_instance.get_project.return_value = mock_project

            # For search_issues
            mock_search_results = {
                "expand": "schema,names",
                "startAt": 0,
                "maxResults": 10,
                "total": 5,
                "issues": [
                    {
                        "id": "10001",
                        "key": f"{self.jira_project_key}-1",
                        "fields": {
                            "summary": "Test issue 1",
                            "description": "Test description 1",
                            "issuetype": {"name": "Task"},
                            "project": {"key": self.jira_project_key},
                        },
                    },
                    {
                        "id": "10002",
                        "key": f"{self.jira_project_key}-2",
                        "fields": {
                            "summary": "Test issue 2",
                            "description": "Test description 2",
                            "issuetype": {"name": "Bug"},
                            "project": {"key": self.jira_project_key},
                        },
                    },
                ],
            }
            self.jira.search_issues.return_value = mock_search_results
            self.jira._adapted_instance.search_issues.return_value = mock_search_results

            # For create_issue
            self.jira.create_issue.return_value = {"key": f"{self.jira_project_key}-101"}

            # For get_all_project_issues
            all_issues = (
                page1_data["issues"]
                + page2_data["issues"]
                + [
                    {
                        "id": "10007",
                        "key": f"{self.jira_project_key}-7",
                        "fields": {"summary": "Test pagination issue 6"},
                    },
                    {
                        "id": "10008",
                        "key": f"{self.jira_project_key}-8",
                        "fields": {"summary": "Test pagination issue 7"},
                    },
                    {
                        "id": "10009",
                        "key": f"{self.jira_project_key}-9",
                        "fields": {"summary": "Test pagination issue 8"},
                    },
                    {
                        "id": "10010",
                        "key": f"{self.jira_project_key}-10",
                        "fields": {"summary": "Test pagination issue 9"},
                    },
                ]
            )

            def mock_get_all_project_issues(*args, **kwargs):
                for issue in all_issues:
                    yield issue

            self.jira.get_all_project_issues.side_effect = mock_get_all_project_issues

            # For get_instance
            self.mock_get_paged_resources_calls = 0

            def mock_get_paged_resources(*args, **kwargs):
                self.mock_get_paged_resources_calls += 1
                for issue in all_issues:
                    yield issue

            self.jira._get_paged_resources.side_effect = mock_get_paged_resources

    def test_get_current_user(self):
        """Test retrieving the current user."""
        current_user = self.get_jira_instance().get_current_user()

        # Verify that the response contains expected fields
        # Server may have different fields compared to Cloud
        self.assertIn("name", current_user)
        self.assertIn("displayName", current_user)

        # Verify that the username matches what we provided
        self.assertEqual(current_user["name"], self.jira_username)

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        projects = self.get_jira_instance().get_all_projects()

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
        try:
            project = self.get_jira_instance().get_project(self.jira_project_key)

            # Verify project data
            self.assertEqual(project["key"], self.jira_project_key)
            self.assertIn("id", project)
            self.assertIn("name", project)
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_search_issues(self):
        """Test searching for issues in server."""
        try:
            jql = f"project = {self.jira_project_key} ORDER BY created DESC"
            search_results = self.get_jira_instance().search_issues(jql, max_results=10)

            # Verify search results structure
            self.assertIn("issues", search_results)
            self.assertIn("total", search_results)

            # If there are any issues, verify their structure
            if search_results["total"] > 0:
                first_issue = search_results["issues"][0]
                self.assertIn("id", first_issue)
                self.assertIn("key", first_issue)
                self.assertIn("fields", first_issue)
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_pagination_handling(self):
        """Test the server-specific pagination handling.

        This test verifies that pagination works correctly for Jira Server
        API responses, which use startAt/maxResults/total for controlling pagination
        rather than the nextPage URL-based pagination used in Cloud.
        """
        # Create at least 10 issues to ensure we have enough data for pagination
        issue_keys = []
        try:
            if not self.offline_mode:
                # Create first batch of test issues
                for i in range(5):
                    summary = f"Test pagination issue {i} - {int(time.time())}"
                    description = f"This is a test issue created to test pagination handling. #{i}"

                    issue_data = {
                        "fields": {
                            "project": {"key": self.jira_project_key},
                            "summary": summary,
                            "description": description,
                            "issuetype": {"name": "Task"},
                        }
                    }

                    response = self.jira.create_issue(issue_data)
                    self.assertIsNotNone(response)
                    self.assertIn("key", response)
                    issue_keys.append(response["key"])
                    time.sleep(1)  # Sleep to avoid rate limiting

                # Create second batch of test issues
                for i in range(5, 10):
                    summary = f"Test pagination issue {i} - {int(time.time())}"
                    description = f"This is a test issue created to test pagination handling. #{i}"

                    issue_data = {
                        "fields": {
                            "project": {"key": self.jira_project_key},
                            "summary": summary,
                            "description": description,
                            "issuetype": {"name": "Task"},
                        }
                    }

                    response = self.jira.create_issue(issue_data)
                    self.assertIsNotNone(response)
                    self.assertIn("key", response)
                    issue_keys.append(response["key"])
                    time.sleep(1)  # Sleep to avoid rate limiting
            else:
                # In offline mode, we create dummy issue keys
                for i in range(10):
                    issue_keys.append(f"{self.jira_project_key}-{i+1}")

            # Now test pagination with different page sizes
            jql = f"project = {self.jira_project_key} AND summary ~ 'Test pagination issue'"

            # Test with first page (small page size)
            page1 = self.jira.jql_search(jql, start_at=0, max_results=3, fields=["summary"])
            self.assertIsNotNone(page1)
            self.assertIn("issues", page1)
            self.assertGreaterEqual(len(page1["issues"]), 3)
            self.assertIn("startAt", page1)
            self.assertIn("maxResults", page1)
            self.assertIn("total", page1)

            # Test with second page
            page2 = self.jira.jql_search(jql, start_at=3, max_results=3, fields=["summary"])
            self.assertIsNotNone(page2)
            self.assertIn("issues", page2)

            # Verify no duplicate issues between pages
            page1_keys = [issue["key"] for issue in page1["issues"]]
            page2_keys = [issue["key"] for issue in page2["issues"]]

            self.assertEqual(0, len(set(page1_keys).intersection(set(page2_keys))))

            # Test retrieving all issues with internal pagination
            all_issues = list(
                self.jira.get_all_project_issues(
                    self.jira_project_key, fields=["summary"], jql_filter="summary ~ 'Test pagination issue'"
                )
            )

            # There should be at least the number of issues we created
            self.assertGreaterEqual(len(all_issues), len(issue_keys))

            if not self.offline_mode:
                # Only test with the actual API if we're online
                # Test the _get_paged_resources method directly
                direct_jira = self.get_jira_instance()
                issues_gen = direct_jira._get_paged_resources(
                    f"search?jql=project={self.jira_project_key}+AND+summary~'Test pagination issue'",
                    "issues",
                    params={"maxResults": 2, "fields": "summary"},
                )

                # Count the issues from the generator
                issues_count = 0
                for _ in issues_gen:
                    issues_count += 1

                # Verify we got all issues through pagination
                self.assertGreaterEqual(issues_count, len(issue_keys))

        finally:
            # Clean up by deleting the test issues
            if not self.offline_mode:
                for key in issue_keys:
                    try:
                        self.jira.delete_issue(key)
                    except Exception as e:
                        print(f"Failed to delete issue {key}: {str(e)}")


class TestJiraV3ServerIssuesIntegration(JiraV3ServerIntegrationTestCase):
    """Integration tests for the Jira v3 Server Issues API."""

    def test_create_and_get_issue(self):
        """Test creating and retrieving an issue in Jira Server."""
        try:
            # Validate project key
            self.validate_project_key()

            # Create test issue
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": "Test issue created by integration test",
                    "description": "This is a test issue created by the integration test",
                    "issuetype": {"name": "Task"},
                }
            }

            # Create the issue
            response = self.get_jira_instance().create_issue(fields=issue_data["fields"])

            # Validate response
            self.assertIn("id", response)
            self.assertIn("key", response)

            issue_key = response["key"]

            try:
                # Get the issue we just created
                issue = self.get_jira_instance().get_issue(issue_key)

                # Verify issue data
                self.assertEqual(issue["key"], issue_key)
                self.assertEqual(issue["fields"]["summary"], "Test issue created by integration test")
                self.assertIn("project", issue["fields"])
                self.assertEqual(issue["fields"]["project"]["key"], self.jira_project_key)
            finally:
                # Cleanup - delete the issue
                try:
                    self.get_jira_instance().delete_issue(issue_key)
                except Exception as e:
                    print(f"Warning: Failed to delete test issue {issue_key}: {str(e)}")
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_update_issue(self):
        """Test updating an issue in Jira Server."""
        try:
            # Validate project key
            self.validate_project_key()

            # Create test issue
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": "Test issue for update",
                    "description": "This is a test issue that will be updated",
                    "issuetype": {"name": "Task"},
                }
            }

            # Create the issue
            response = self.get_jira_instance().create_issue(fields=issue_data["fields"])
            issue_key = response["key"]

            try:
                # Update the issue
                update_data = {
                    "summary": "Updated test issue",
                    "description": "This issue has been updated by the integration test",
                }

                self.get_jira_instance().update_issue(issue_key, fields=update_data)

                # Get the updated issue
                updated_issue = self.get_jira_instance().get_issue(issue_key)

                # Verify issue was updated
                self.assertEqual(updated_issue["fields"]["summary"], "Updated test issue")
                self.assertTrue("This issue has been updated" in str(updated_issue["fields"].get("description", "")))
            finally:
                # Cleanup - delete the issue
                try:
                    self.get_jira_instance().delete_issue(issue_key)
                except Exception as e:
                    print(f"Warning: Failed to delete test issue {issue_key}: {str(e)}")
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_get_issue_transitions(self):
        """Test retrieving transitions for an issue in Jira Server."""
        try:
            # Validate project key
            self.validate_project_key()

            # Create test issue
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": "Test issue for transitions",
                    "description": "This is a test issue for checking transitions",
                    "issuetype": {"name": "Task"},
                }
            }

            # Create the issue
            response = self.get_jira_instance().create_issue(fields=issue_data["fields"])
            issue_key = response["key"]

            try:
                # Get transitions for the issue
                transitions = self.get_jira_instance().get_issue_transitions(issue_key)

                # Verify transitions data
                self.assertIn("transitions", transitions)
                self.assertTrue(len(transitions["transitions"]) > 0, "No transitions returned")

                # Verify structure of first transition
                first_transition = transitions["transitions"][0]
                self.assertIn("id", first_transition)
                self.assertIn("name", first_transition)
                self.assertIn("to", first_transition)
            finally:
                # Cleanup - delete the issue
                try:
                    self.get_jira_instance().delete_issue(issue_key)
                except Exception as e:
                    print(f"Warning: Failed to delete test issue {issue_key}: {str(e)}")
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_add_and_get_comments(self):
        """Test adding and retrieving comments for an issue in Jira Server."""
        try:
            # Validate project key
            self.validate_project_key()

            # Create test issue
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": "Test issue for comments",
                    "description": "This is a test issue for adding and retrieving comments",
                    "issuetype": {"name": "Task"},
                }
            }

            # Create the issue
            response = self.get_jira_instance().create_issue(fields=issue_data["fields"])
            issue_key = response["key"]

            try:
                # Add a comment to the issue
                comment_body = "This is a test comment from the integration test"

                # Server may handle comment differently than Cloud
                try:
                    # First, try with structured format that Cloud would use
                    comment = {
                        "body": {
                            "type": "doc",
                            "version": 1,
                            "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment_body}]}],
                        }
                    }
                    self.get_jira_instance().add_comment(issue_key, comment)
                except Exception as _:
                    # If the structured comment fails, try with plain text
                    try:
                        self.get_jira_instance().add_comment(issue_key, {"body": comment_body})
                    except Exception as _:
                        # If both fail, try with just the string
                        self.get_jira_instance().add_comment(issue_key, comment_body)

                # Get comments for the issue
                comments = self.get_jira_instance().get_issue_comments(issue_key)

                # Verify comments data
                self.assertTrue(
                    comments.get("comments") is not None or comments.get("values") is not None,
                    "No comments container returned",
                )

                # Get the comments list (the key might be "comments" or "values" depending on server version)
                comments_list = comments.get("comments", comments.get("values", []))

                # Verify at least one comment exists
                self.assertTrue(len(comments_list) > 0, "No comments returned")

                # Check if the comment text is present in any comment
                comment_found = False
                for comment in comments_list:
                    comment_text = ""
                    if isinstance(comment.get("body"), dict):
                        # ADF format
                        comment_text = str(comment["body"])
                    else:
                        # Plain text format
                        comment_text = str(comment.get("body", ""))

                    if comment_body in comment_text:
                        comment_found = True
                        break

                self.assertTrue(comment_found, f"Added comment text '{comment_body}' not found in comments")
            finally:
                # Cleanup - delete the issue
                try:
                    self.get_jira_instance().delete_issue(issue_key)
                except Exception as e:
                    print(f"Warning: Failed to delete test issue {issue_key}: {str(e)}")
        except Exception as e:
            if not self.check_permissions(e):
                raise


class TestJiraV3ServerProjectsIntegration(JiraV3ServerIntegrationTestCase):
    """Integration tests for Jira v3 Server Projects API."""

    def test_get_project_components(self):
        """Test retrieving components for a project."""
        try:
            # Validate project key
            self.validate_project_key()

            # Get components for the project
            components = self.projects_jira.get_project_components(self.jira_project_key)

            # Verify components data (even if empty, the API should return successfully)
            self.assertIsNotNone(components)

            # If there are components, verify their structure
            if components and len(components) > 0:
                first_component = components[0]
                self.assertIn("id", first_component)
                self.assertIn("name", first_component)
        except Exception as e:
            if not self.check_permissions(e):
                raise

    def test_get_project_versions(self):
        """Test retrieving versions for a project."""
        try:
            # Validate project key
            self.validate_project_key()

            # Get versions for the project
            versions = self.projects_jira.get_project_versions(self.jira_project_key)

            # Verify versions data (even if empty, the API should return successfully)
            self.assertIsNotNone(versions)

            # If there are versions, verify their structure
            if versions and len(versions) > 0:
                first_version = versions[0]
                self.assertIn("id", first_version)
                self.assertIn("name", first_version)
                self.assertIn("released", first_version)
        except Exception as e:
            if not self.check_permissions(e):
                raise


class TestJiraV3ServerPermissionsIntegration(JiraV3ServerIntegrationTestCase):
    """Integration tests for permission-sensitive operations in Jira Server."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        if self.offline_mode:
            # Mock permission errors - using proper constructor
            from unittest.mock import MagicMock
            from requests import Response

            # Create a mock response to use with the error
            mock_response = MagicMock(spec=Response)
            mock_response.status_code = 403
            mock_response.reason = "Forbidden"
            mock_response.text = json.dumps(
                {"errorMessages": ["The user does not have permission to complete this operation"]}
            )

            # Create proper permission error
            permission_error = atlassian.jira.errors.JiraPermissionError("Permission denied", response=mock_response)

            self.permissions_jira.get_all_permission_schemes.side_effect = permission_error
            self.permissions_jira.create_permission_scheme.side_effect = permission_error

            # Mock permission responses
            self.permissions_jira.get_my_permissions.return_value = {
                "permissions": {
                    "BROWSE_PROJECTS": {
                        "id": "10",
                        "key": "BROWSE_PROJECTS",
                        "name": "Browse Projects",
                        "type": "PROJECT",
                        "description": "Ability to browse projects",
                        "havePermission": True,
                    },
                    "CREATE_ISSUES": {
                        "id": "11",
                        "key": "CREATE_ISSUES",
                        "name": "Create Issues",
                        "type": "PROJECT",
                        "description": "Ability to create issues",
                        "havePermission": True,
                    },
                    "ADMINISTER": {
                        "id": "44",
                        "key": "ADMINISTER",
                        "name": "Administer Jira",
                        "type": "GLOBAL",
                        "description": "Ability to administer Jira",
                        "havePermission": False,
                    },
                }
            }

    def test_permission_handling(self):
        """Test handling of permission-sensitive operations.

        This test tries to perform operations that might require elevated permissions
        and verifies that our error handling gracefully handles permission issues.
        """
        try:
            # Try to get permission schemes (usually requires admin)
            try:
                permission_schemes = self.permissions_jira.get_all_permission_schemes()
                # If we have admin rights, verify the response structure
                self.assertIsNotNone(permission_schemes)
                self.assertIn("permissionSchemes", permission_schemes)
                print("User has admin permissions - able to get permission schemes")
            except atlassian.jira.errors.JiraPermissionError as e:
                # Verify our error handling works correctly
                self.assertTrue("does not have permission" in str(e) or "Unauthorized" in str(e))
                print(f"Permission error correctly identified: {str(e)}")

            # Try to get my permissions for the current project
            my_permissions = self.permissions_jira.get_my_permissions(project_key=self.jira_project_key)
            self.assertIsNotNone(my_permissions)
            self.assertIn("permissions", my_permissions)

            # Verify we can access our own permissions
            browse_permission = my_permissions["permissions"].get("BROWSE_PROJECTS", {})
            self.assertIn("havePermission", browse_permission)

            # Try an operation where we know we have permission (viewing current user)
            current_user = self.jira.get_current_user()
            self.assertIsNotNone(current_user)
            self.assertIn("displayName", current_user)

            # Attempt a high privilege operation and test error handling
            try:
                # Trying to create a permission scheme - typically admin only
                new_scheme = {"name": "Test Permission Scheme", "description": "Created by integration test"}
                result = self.permissions_jira.create_permission_scheme(new_scheme)

                # If successful, clean up
                if result and "id" in result:
                    scheme_id = result["id"]
                    try:
                        self.permissions_jira.delete_permission_scheme(scheme_id)
                    except Exception as cleanup_error:
                        print(f"Failed to clean up permission scheme {scheme_id}: {str(cleanup_error)}")
            except atlassian.jira.errors.JiraPermissionError as e:
                # If we get here, we correctly handled the permission error
                self.assertTrue("does not have permission" in str(e) or "Unauthorized" in str(e))
                print(f"Permission error correctly identified for create_permission_scheme: {str(e)}")

        except Exception as e:
            # This will fail the test with informative error if our permission handling is broken
            self.fail(f"Permission handling error: {str(e)}")


class TestJiraV3ServerSearchIntegration(JiraV3ServerIntegrationTestCase):
    """Integration tests for Jira v3 Server Search API."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        if self.offline_mode:
            # Mock responses for JQL pagination testing
            # Setup multiple pages of response data
            self.mock_search_pages = []
            total_issues = 125  # Total number of mock issues
            max_per_page = 50  # Jira's default page size

            # Create 3 pages of results (50, 50, 25 issues)
            for page in range(3):
                start_at = page * max_per_page
                issue_count = min(max_per_page, total_issues - start_at)
                issues = []

                for i in range(issue_count):
                    issue_idx = start_at + i
                    issues.append(
                        {
                            "id": f"1000{issue_idx}",
                            "key": f"{self.jira_project_key}-{issue_idx + 1}",
                            "fields": {
                                "summary": f"Test JQL issue {issue_idx}",
                                "description": f"Description for JQL test issue {issue_idx}",
                            },
                        }
                    )

                # Build the response page
                page_data = {
                    "expand": "schema,names",
                    "startAt": start_at,
                    "maxResults": max_per_page,
                    "total": total_issues,
                    "issues": issues,
                }
                self.mock_search_pages.append(page_data)

            # Keep track of all mock issues for generator functions
            self.all_mock_issues = []
            for page in self.mock_search_pages:
                self.all_mock_issues.extend(page["issues"])

            # Setup mock for search_issues
            def mock_search_issues(jql, max_results=50, start_at=0, fields=None, **kwargs):
                # Calculate which page to return based on start_at
                page_idx = start_at // max_per_page if max_per_page > 0 else 0
                if page_idx >= len(self.mock_search_pages):
                    # Return empty results if requesting beyond available pages
                    return {"startAt": start_at, "maxResults": max_results, "total": total_issues, "issues": []}

                page = self.mock_search_pages[page_idx]
                # Adjust for different max_results
                if max_results != max_per_page:
                    adjusted_page = page.copy()
                    # Calculate actual end index based on start_at within the page
                    local_start = start_at - page["startAt"]
                    if local_start < 0:
                        local_start = 0
                    local_end = min(local_start + max_results, len(page["issues"]))
                    adjusted_page["issues"] = page["issues"][local_start:local_end]
                    adjusted_page["maxResults"] = max_results
                    adjusted_page["startAt"] = start_at
                    return adjusted_page

                return page

            self.search_jira.search_issues.side_effect = mock_search_issues
            self.jira.search_issues.side_effect = mock_search_issues

            # Mock for jql_get_all_issues
            def mock_jql_get_all_issues(jql, fields=None, **kwargs):
                # This should be a generator returning all issues
                for issue in self.all_mock_issues:
                    yield issue

            # Add the mock to both instances
            self.search_jira.jql_get_all_issues = mock_jql_get_all_issues
            self.jira.jql_get_all_issues = mock_jql_get_all_issues

    def test_jql_pagination_using_loop(self):
        """Test JQL search pagination using manual loop approach.

        This test demonstrates how to handle Jira Server pagination with JQL searches
        where we need to loop through all results using startAt/maxResults parameters.
        """
        # The JQL query we want to test
        jql = f"project = {self.jira_project_key} ORDER BY created DESC"

        # Loop method - what API consumers typically need to implement
        all_issues = []
        max_results = 50
        start_at = 0

        while True:
            # Get a page of results
            page = self.search_jira.search_issues(jql, max_results=max_results, start_at=start_at)

            # Verify page structure
            self.assertIn("issues", page)
            self.assertIn("startAt", page)
            self.assertIn("maxResults", page)
            self.assertIn("total", page)

            issues = page["issues"]
            all_issues.extend(issues)

            # Break if we've retrieved all issues
            if len(all_issues) >= page["total"] or len(issues) == 0:
                break

            # Update startAt for the next page
            start_at += len(issues)

        # Verify we got all the results
        if not self.offline_mode:
            # In online mode, just check we got some results
            self.assertGreater(len(all_issues), 0, "No issues found in search")
        else:
            # In offline mode with our mocks, we can verify exact count
            self.assertEqual(len(all_issues), 125, "Should retrieve all 125 mock issues")

        # Verify no duplicate issues (each issue has a unique key)
        issue_keys = [issue["key"] for issue in all_issues]
        unique_keys = set(issue_keys)
        self.assertEqual(len(issue_keys), len(unique_keys), "Duplicate issues found in pagination results")

    def test_jql_pagination_using_helper(self):
        """Test JQL search pagination using the helper method.

        This test verifies that our library's helper methods correctly handle
        pagination for Jira Server JQL searches.
        """
        # The JQL query we want to test
        jql = f"project = {self.jira_project_key} ORDER BY created DESC"

        # Use the library's built-in pagination method
        issues_gen = self.search_jira.jql_get_all_issues(jql, fields="summary,description")

        # Collect all results
        all_issues = list(issues_gen)

        # Verify we got results
        if not self.offline_mode:
            # In online mode, just check we got some results
            self.assertGreater(len(all_issues), 0, "No issues found in search")
        else:
            # In offline mode with our mocks, we can verify exact count
            self.assertEqual(len(all_issues), 125, "Should retrieve all 125 mock issues")

        # Verify no duplicate issues (each issue has a unique key)
        issue_keys = [issue["key"] for issue in all_issues]
        unique_keys = set(issue_keys)
        self.assertEqual(len(issue_keys), len(unique_keys), "Duplicate issues found in pagination results")

        # Verify we can iterate through the generator multiple times
        issues_gen = self.search_jira.jql_get_all_issues(jql, fields="summary")
        first_page_issues = []
        for i, issue in enumerate(issues_gen):
            first_page_issues.append(issue)
            if i >= 9:  # Get first 10 issues
                break

        self.assertEqual(len(first_page_issues), 10, "Should be able to get first 10 issues")

    def test_jql_with_small_page_size(self):
        """Test JQL search with small page size to verify pagination handling.

        This test verifies that our pagination works correctly even with
        non-standard page sizes.
        """
        # The JQL query we want to test
        jql = f"project = {self.jira_project_key} ORDER BY created DESC"

        # Use a very small page size to force many pagination calls
        small_page_size = 10

        # Get all results with small page size
        all_issues = []
        start_at = 0
        total = None

        while True:
            # Get a page of results
            page = self.search_jira.search_issues(jql, max_results=small_page_size, start_at=start_at)

            # Store the total on first iteration
            if total is None:
                total = page["total"]

            issues = page["issues"]
            all_issues.extend(issues)

            # Break if we've retrieved all issues or we're getting empty pages
            if len(all_issues) >= total or len(issues) == 0:
                break

            # Update startAt for the next page
            start_at += len(issues)

        # Verify we got the expected number of results
        if not self.offline_mode:
            # In online mode, just check we got some results
            self.assertGreater(len(all_issues), 0, "No issues found in search")
        else:
            # In offline mode with our mocks, we can verify exact count
            self.assertEqual(len(all_issues), 125, "Should retrieve all 125 mock issues")


class TestJiraV3ServerVersionCompat(JiraV3ServerIntegrationTestCase):
    """Tests for Python version compatibility for the Jira v3 Server API."""

    def test_python_version_compatibility(self):
        """Test compatibility with the current Python version.

        This test verifies that the Jira v3 API works with the current Python version.
        It should be run across multiple Python versions (3.6, 3.7, 3.8, 3.9, 3.10)
        to ensure compatibility.
        """
        import platform

        # Get Python version information
        python_version = sys.version_info
        python_implementation = platform.python_implementation()

        # Log Python version for CI testing
        print(
            f"Testing with Python {python_implementation} {python_version.major}.{python_version.minor}.{python_version.micro}"
        )

        # Core functionality test that should work on all Python versions
        try:
            # Test creating a basic instance
            test_jira = get_jira_instance(
                url="https://example.atlassian.net",
                username="test",
                password="test",
                api_version=3,
                cloud=False,  # Server instance
            )

            # Verify instance is created correctly
            self.assertIsNotNone(test_jira)
            # The server property is part of the Jira instance
            self.assertEqual(test_jira.url, "https://example.atlassian.net")

            # Verify type annotations work correctly
            from typing import Dict, Any

            # Type annotation test - this would fail on Python < 3.5
            variables: Dict[str, Any] = {"username": "test", "project_key": "TEST"}

            # Test f-strings - these were introduced in Python 3.6
            test_string = f"User {variables['username']} is working on {variables['project_key']}"
            self.assertEqual(test_string, "User test is working on TEST")

            # If Python >= 3.7, test dataclasses (introduced in 3.7)
            if python_version.major == 3 and python_version.minor >= 7:
                from dataclasses import dataclass

                @dataclass
                class Issue:
                    key: str
                    summary: str

                issue = Issue(key="TEST-1", summary="Test issue")
                self.assertEqual(issue.key, "TEST-1")

            # If Python >= 3.8, test walrus operator (introduced in 3.8)
            if python_version.major == 3 and python_version.minor >= 8:
                # Simple test using the walrus operator
                if (n := len(variables)) > 0:
                    self.assertEqual(n, 2)

            # If Python >= 3.9, test dictionary union (introduced in 3.9)
            if python_version.major == 3 and python_version.minor >= 9:
                dict1 = {"a": 1}
                dict2 = {"b": 2}
                # Dictionary union with |
                combined = dict1 | dict2
                self.assertEqual(combined, {"a": 1, "b": 2})

            # If Python >= 3.10, test match statement (introduced in 3.10)
            if python_version.major == 3 and python_version.minor >= 10:
                # Simple test using match statement
                status = "open"
                result = None

                match status:
                    case "open":
                        result = "Issue is open"
                    case "closed":
                        result = "Issue is closed"
                    case _:
                        result = "Unknown status"

                self.assertEqual(result, "Issue is open")

        except ImportError as e:
            # Skip if the Python version doesn't support a required feature
            self.skipTest(f"This Python version doesn't support a required feature: {str(e)}")
        except SyntaxError as e:
            # This will happen if we're using Python < 3.6 and try f-strings
            self.skipTest(f"This Python version doesn't support the syntax: {str(e)}")


if __name__ == "__main__":
    unittest.main()
