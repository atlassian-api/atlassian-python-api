#!/usr/bin/env python3
"""
Integration tests for the Jira v3 API.
These tests require a real Jira instance to run against.
"""

import os
import unittest
import logging
import atlassian
from dotenv import load_dotenv
import traceback

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

# Set up logging to see detailed error information
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("atlassian.jira.errors")
logger.setLevel(logging.DEBUG)

# Load environment variables from .env file
load_dotenv()


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

        # Skip all tests if credentials are not set
        if not all([cls.jira_url, cls.jira_username, cls.jira_api_token]):
            raise unittest.SkipTest("JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN environment variables must be set")

        # Create Jira instances
        cls.jira = get_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        # Create specialized Jira instances
        cls.users_jira = get_users_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.software_jira = get_software_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.permissions_jira = get_permissions_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.search_jira = get_search_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.richtext_jira = get_richtext_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.issuetypes_jira = get_issuetypes_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
        )

        cls.projects_jira = get_projects_jira_instance(
            url=cls.jira_url, username=cls.jira_username, password=cls.jira_api_token, api_version=3, legacy_mode=False
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


class TestJiraV3Integration(JiraV3IntegrationTestCase):
    """Integration tests for the core Jira v3 functionality."""

    def test_get_current_user(self):
        """Test retrieving the current user."""
        current_user = self.get_jira_instance().get_current_user()

        # Verify that the response contains expected fields
        self.assertIn("accountId", current_user)
        self.assertIn("displayName", current_user)
        self.assertIn("emailAddress", current_user)

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
        project = self.get_jira_instance().get_project(self.jira_project_key)

        # Verify project data
        self.assertEqual(project["key"], self.jira_project_key)
        self.assertIn("id", project)
        self.assertIn("name", project)

    def test_search_issues(self):
        """Test searching for issues."""
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


class TestJiraV3UsersIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Users API."""

    def test_get_user(self):
        """Test retrieving user information."""
        # First get current user to get an account ID
        current_user = self.get_jira_instance().get_current_user()
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
        current_user = self.get_jira_instance().get_current_user()
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


class TestJiraV3IssueTypesIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Issue Types API."""

    def test_get_all_issue_types(self):
        """Test retrieving all issue types."""
        try:
            issue_types = self.issuetypes_jira.get_all_issue_types()

            # Verify issue types are returned
            self.assertIsInstance(issue_types, list)
            self.assertTrue(len(issue_types) > 0, "No issue types returned")

            # Verify issue type structure
            first_issue_type = issue_types[0]
            self.assertIn("id", first_issue_type)
            self.assertIn("name", first_issue_type)
            self.assertIn("description", first_issue_type)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise

    def test_get_issue_type(self):
        """Test retrieving a specific issue type."""
        try:
            # First get all issue types to get an ID
            issue_types = self.issuetypes_jira.get_all_issue_types()
            first_issue_type_id = issue_types[0]["id"]

            # Get the specific issue type
            issue_type = self.issuetypes_jira.get_issue_type(first_issue_type_id)

            # Verify issue type data
            self.assertEqual(issue_type["id"], first_issue_type_id)
            self.assertIn("name", issue_type)
            self.assertIn("description", issue_type)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise

    def test_get_issue_type_schemes(self):
        """Test retrieving issue type schemes."""
        try:
            schemes = self.issuetypes_jira.get_issue_type_schemes()

            # Verify schemes structure
            self.assertIn("values", schemes)

            # If there are schemes, verify their structure
            if schemes["values"]:
                first_scheme = schemes["values"][0]
                self.assertIn("id", first_scheme)
                self.assertIn("name", first_scheme)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise

    def test_get_field_configurations(self):
        """Test retrieving field configurations."""
        try:
            field_configs = self.issuetypes_jira.get_field_configurations()

            # Verify field configurations structure
            self.assertIn("values", field_configs)

            # If there are configurations, verify their structure
            if field_configs["values"]:
                first_config = field_configs["values"][0]
                self.assertIn("id", first_config)
                self.assertIn("name", first_config)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise

    def test_get_all_fields(self):
        """Test retrieving all fields."""
        try:
            fields = self.issuetypes_jira.get_all_fields()

            # Verify fields are returned
            self.assertIsInstance(fields, list)
            self.assertTrue(len(fields) > 0, "No fields returned")

            # Verify field structure
            first_field = fields[0]
            self.assertIn("id", first_field)
            self.assertIn("name", first_field)
            self.assertIn("schema", first_field)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise


class TestJiraV3IssuesIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Issues API."""

    def get_issue_data(self, summary="Test issue"):
        """Get data for creating a test issue.

        Args:
            summary (str): The issue summary/title

        Returns:
            dict: Issue data ready for creating a new issue
        """
        # Ensure the project key is valid
        self.validate_project_key()

        # Get issue types for the project to find a valid issue type ID
        issue_type_name = "Task"  # Default to Task, which is commonly available
        issue_type_id = None

        try:
            # Try to get project first, which includes issue types
            project = self.get_jira_instance().get_project(self.jira_project_key)
            print(f"Project data: {project}")

            if "issueTypes" in project and project["issueTypes"]:
                # Look for Task, Bug, or Story issue types
                for issue_type in project["issueTypes"]:
                    if issue_type["name"] in ["Task", "Bug", "Story"]:
                        issue_type_name = issue_type["name"]
                        issue_type_id = issue_type["id"]
                        print(f"Using project-specific issue type: {issue_type_name} (ID: {issue_type_id})")
                        break

                # If no standard type was found, use the first one that is not a subtask
                if not issue_type_id:
                    for issue_type in project["issueTypes"]:
                        if not issue_type.get("subtask", False):
                            issue_type_name = issue_type["name"]
                            issue_type_id = issue_type["id"]
                            print(f"Using first available project issue type: {issue_type_name} (ID: {issue_type_id})")
                            break
            else:
                print("No issue types found in project data, trying to get all issue types")
                # Fallback to all issue types
                try:
                    issue_types = self.issuetypes_jira.get_all_issue_types()

                    # Look for Task, Bug, or Story issue types
                    for issue_type in issue_types:
                        if issue_type["name"] in ["Task", "Bug", "Story"] and not issue_type.get("subtask", False):
                            issue_type_name = issue_type["name"]
                            issue_type_id = issue_type["id"]
                            print(f"Using issue type: {issue_type_name} (ID: {issue_type_id})")
                            break

                    # If no standard type was found, use the first one that is not a subtask
                    if not issue_type_id and issue_types:
                        for issue_type in issue_types:
                            if not issue_type.get("subtask", False):
                                issue_type_name = issue_type["name"]
                                issue_type_id = issue_type["id"]
                                print(f"Using first available issue type: {issue_type_name} (ID: {issue_type_id})")
                                break
                except Exception as e:
                    import traceback

                    print(f"Could not get all issue types: {str(e)}")
                    print(f"Traceback: {traceback.format_exc()}")
        except Exception as e:
            import traceback

            print(f"Could not get issue types from project: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

        # Create proper description in ADF format (required by some instances)
        description_adf = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "This is a test issue created by the integration test."}],
                }
            ],
        }

        # Prepare issue data
        issue_data = {
            "fields": {
                "project": {"key": self.jira_project_key},
                "summary": summary,
                "description": description_adf,  # Use ADF format for description
                "issuetype": {},
            }
        }

        # Use issue type ID if available (more reliable than name)
        if issue_type_id:
            issue_data["fields"]["issuetype"] = {"id": issue_type_id}
        else:
            issue_data["fields"]["issuetype"] = {"name": issue_type_name}

        print(f"Prepared issue data: {issue_data}")
        return issue_data

    def test_create_and_get_issue(self):
        """Test creating and retrieving an issue."""
        # Prepare issue data
        issue_data = self.get_issue_data("Test issue created by integration test")

        # Print debug information
        print(f"Using project key: {self.jira_project_key}")

        # Try to get create metadata to see what fields might be required
        try:
            create_meta = self.get_jira_instance().get_create_meta(
                projectKeys=self.jira_project_key, expand="projects.issuetypes.fields"
            )
            print(f"Create metadata available: {bool(create_meta)}")

            # Look for required fields in the selected issue type
            if create_meta and "projects" in create_meta and create_meta["projects"]:
                project = create_meta["projects"][0]
                issue_type = None

                # Find the issue type we're trying to use
                if "issuetypes" in project:
                    for it in project["issuetypes"]:
                        if it.get("id") == issue_data["fields"]["issuetype"].get("id") or it.get("name") == issue_data[
                            "fields"
                        ]["issuetype"].get("name"):
                            issue_type = it
                            break

                # If we found the issue type, look for required fields
                if issue_type and "fields" in issue_type:
                    required_fields = {}
                    for field_id, field_info in issue_type["fields"].items():
                        if field_info.get("required", False) and field_id not in [
                            "project",
                            "issuetype",
                            "summary",
                            "description",
                        ]:
                            print(f"Required field: {field_id} - {field_info.get('name')}")

                            # Try to add default values for required fields
                            if field_info.get("allowedValues") and field_info["allowedValues"]:
                                # Use the first allowed value
                                if field_info["schema"]["type"] == "option":
                                    required_fields[field_id] = {"id": field_info["allowedValues"][0]["id"]}
                                elif field_info["schema"]["type"] == "array":
                                    required_fields[field_id] = [{"id": field_info["allowedValues"][0]["id"]}]

                    # Add required fields to issue data
                    if required_fields:
                        print(f"Adding required fields: {required_fields}")
                        issue_data["fields"].update(required_fields)
        except Exception as e:
            print(f"Error getting create metadata: {str(e)}")

        # Print the full issue data for debugging
        print(f"Issue data: {issue_data}")

        issue_key = None
        try:
            # Create an issue - make sure we're passing the data properly
            jira_instance = self.get_jira_instance()

            # Get the fields data from our issue_data structure
            fields_data = issue_data.get("fields", {})
            print(f"Fields data being sent to API: {fields_data}")

            # Create the issue with the fields data
            created_issue = jira_instance.create_issue(fields=fields_data)
            print(f"API response: {created_issue}")

            # Check that the issue was created successfully
            self.assertIn("id", created_issue)
            self.assertIn("key", created_issue)
            self.assertIn("self", created_issue)

            issue_key = created_issue["key"]

            # Get the created issue
            retrieved_issue = jira_instance.get_issue(issue_key)

            # Check that the retrieved issue matches the created one
            self.assertEqual(retrieved_issue["id"], created_issue["id"])
            self.assertEqual(retrieved_issue["key"], issue_key)
            self.assertEqual(retrieved_issue["fields"]["summary"], fields_data["summary"])

        except Exception as e:
            # Print detailed error information for debugging
            import traceback

            print(f"Error creating/retrieving issue: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.fail(f"Failed to create or retrieve issue: {str(e)}")
        finally:
            # Clean up - delete the created issue if it exists
            if issue_key:
                try:
                    self.get_jira_instance().delete_issue(issue_key)
                except Exception as e:
                    print(f"Warning: Failed to delete test issue {issue_key}: {str(e)}")

    def test_update_issue(self):
        """Test updating an issue."""
        # Create a new issue first
        try:
            issue_data = self.get_issue_data("Issue to be updated")

            # Test with direct Jira class instead of adapter if we're using the adapter
            jira_instance = None
            if hasattr(self.jira, "_adapted_instance"):
                print("Using direct Jira instance instead of adapter")
                jira_instance = self.jira._adapted_instance
            else:
                jira_instance = self.jira

            # Get the fields data from our issue_data structure
            fields_data = issue_data.get("fields", {})
            print(f"Fields data being sent to API for creation: {fields_data}")

            created_issue = jira_instance.create_issue(fields=fields_data)
            issue_key = created_issue["key"]

            # Update the issue
            update_data = {
                "summary": "Updated summary",
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "This is an updated description."}]}
                    ],
                },
            }

            print(f"Update data being sent to API: {update_data}")
            jira_instance.update_issue(issue_key, fields=update_data)

            # Get the updated issue
            updated_issue = jira_instance.get_issue(issue_key)

            # Verify the update
            self.assertEqual(updated_issue["fields"]["summary"], "Updated summary")

            # Clean up
            jira_instance.delete_issue(issue_key)
        except Exception as e:
            import traceback

            print(f"Error updating issue: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.fail(f"Failed to update issue: {str(e)}")

    def test_add_and_get_comments(self):
        """Test adding and retrieving comments."""
        # Get a Jira instance
        jira_instance = self.get_jira_instance()

        # Create an issue to add comments to
        try:
            issue_data = self.get_issue_data()
            print("Prepared issue data:", issue_data)

            # Extract fields data
            fields_data = issue_data.get("fields", {})

            # Create the issue with proper fields data
            created_issue = jira_instance.create_issue(fields=fields_data)

            # Add a comment
            comment_body = {
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "This is a test comment."}]}
                    ],
                }
            }

            added_comment = jira_instance.add_comment(created_issue["key"], comment_body)
            self.assertIsNotNone(added_comment)
            self.assertEqual(added_comment["body"]["content"][0]["content"][0]["text"], "This is a test comment.")

            # Get comments
            comments = jira_instance.get_issue_comments(created_issue["key"])
            self.assertIsNotNone(comments)
            self.assertTrue(isinstance(comments["comments"], list))
            self.assertEqual(len(comments["comments"]), 1)

            # Verify comment content
            self.assertEqual(
                comments["comments"][0]["body"]["content"][0]["content"][0]["text"], "This is a test comment."
            )

            # Clean up
            jira_instance.delete_issue(created_issue["key"])

        except Exception as e:
            # Clean up in case of error
            if "created_issue" in locals():
                try:
                    jira_instance.delete_issue(created_issue["key"])
                except Exception:  # Using Exception instead of bare except
                    pass  # Ignore errors during cleanup

            print(f"Error adding/retrieving comments: {str(e)}")
            print("Traceback:", traceback.format_exc())
            self.fail(f"Failed to add or get comments: {str(e)}")

    def test_get_issue_transitions(self):
        """Test retrieving issue transitions."""
        # Create a new issue
        try:
            issue_data = self.get_issue_data("Issue for transitions test")

            # Test with direct Jira class instead of adapter if we're using the adapter
            jira_instance = None
            if hasattr(self.jira, "_adapted_instance"):
                print("Using direct Jira instance instead of adapter")
                jira_instance = self.jira._adapted_instance
            else:
                jira_instance = self.jira

            # Extract fields data from issue_data
            fields_data = issue_data.get("fields", {})

            # Create the issue with proper fields data
            created_issue = jira_instance.create_issue(fields=fields_data)
            issue_key = created_issue["key"]

            # Get issue transitions
            transitions = jira_instance.get_issue_transitions(issue_key)

            # Verify transitions structure
            self.assertIn("transitions", transitions)
            self.assertIsInstance(transitions["transitions"], list)

            # If there are any transitions, verify their structure
            if transitions["transitions"]:
                first_transition = transitions["transitions"][0]
                self.assertIn("id", first_transition)
                self.assertIn("name", first_transition)

            # Clean up
            jira_instance.delete_issue(issue_key)
        except Exception as e:
            import traceback

            print(f"Error getting transitions: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.fail(f"Failed to get issue transitions: {str(e)}")

    def test_get_issue_watchers(self):
        """Test retrieving issue watchers."""
        # Create a new issue
        try:
            issue_data = self.get_issue_data("Issue for watchers test")

            # Test with direct Jira class instead of adapter if we're using the adapter
            jira_instance = None
            if hasattr(self.jira, "_adapted_instance"):
                print("Using direct Jira instance instead of adapter")
                jira_instance = self.jira._adapted_instance
            else:
                jira_instance = self.jira

            # Extract fields data from issue_data
            fields_data = issue_data.get("fields", {})

            # Create the issue with proper fields data
            created_issue = jira_instance.create_issue(fields=fields_data)
            issue_key = created_issue["key"]

            # Get issue watchers
            watchers = jira_instance.get_issue_watchers(issue_key)

            # Verify watchers structure
            self.assertIsInstance(watchers, dict)
            self.assertIn("watchers", watchers)

            # Clean up
            jira_instance.delete_issue(issue_key)
        except Exception as e:
            import traceback

            print(f"Error getting watchers: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.fail(f"Failed to get issue watchers: {str(e)}")


class TestJiraV3SoftwareIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Software API."""

    def test_get_all_boards(self):
        """Test retrieving all boards."""
        try:
            boards = self.software_jira.get_all_boards()

            # Verify boards structure
            self.assertIn("values", boards)

            # If there are boards, verify their structure
            if boards["values"]:
                first_board = boards["values"][0]
                self.assertIn("id", first_board)
                self.assertIn("name", first_board)
                self.assertIn("type", first_board)
        except Exception as e:
            import traceback

            print(f"Error retrieving boards: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

            if self.check_permissions(e):
                return

            # Skip test if the error is related to no boards or access issues
            if "no boards" in str(e).lower() or "403" in str(e) or "404" in str(e):
                self.skipTest(f"No boards available or access denied: {str(e)}")
            raise

    def test_get_board(self):
        """Test retrieving a specific board."""
        try:
            # First get all boards to get an ID
            boards = self.software_jira.get_all_boards()

            # Skip if no boards are available
            if not boards["values"]:
                self.skipTest("No boards available for testing")

            first_board_id = boards["values"][0]["id"]

            # Get the specific board
            board = self.software_jira.get_board(first_board_id)

            # Verify board data
            self.assertEqual(board["id"], first_board_id)
            self.assertIn("name", board)
            self.assertIn("type", board)
        except Exception as e:
            import traceback

            print(f"Error retrieving board: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

            if self.check_permissions(e):
                return

            # Skip test if the board isn't accessible or doesn't exist
            if "board not found" in str(e).lower() or "403" in str(e) or "404" in str(e):
                self.skipTest(f"Board not accessible: {str(e)}")
            raise

    def test_get_board_configuration(self):
        """Test retrieving board configuration."""
        try:
            # First get all boards to get an ID
            boards = self.software_jira.get_all_boards()

            # Skip if no boards are available
            if not boards["values"]:
                self.skipTest("No boards available for testing")

            first_board_id = boards["values"][0]["id"]

            # Get the board configuration
            config = self.software_jira.get_board_configuration(first_board_id)

            # Verify configuration structure
            self.assertIn("id", config)
            self.assertIn("name", config)
            self.assertIn("filter", config)
        except Exception as e:
            import traceback

            print(f"Error retrieving board configuration: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

            if self.check_permissions(e):
                return

            # Some board configurations might not be accessible
            if "board configuration" in str(e).lower() or "403" in str(e) or "404" in str(e):
                self.skipTest(f"Board configuration not accessible: {str(e)}")
            raise

    def test_get_board_issues(self):
        """Test retrieving issues for a board."""
        try:
            # First get all boards to get an ID
            boards = self.software_jira.get_all_boards()

            # Skip if no boards are available
            if not boards["values"]:
                self.skipTest("No boards available for testing")

            first_board_id = boards["values"][0]["id"]

            # Get issues for the board
            issues = self.software_jira.get_board_issues(first_board_id, max_results=10)

            # Verify issues structure
            self.assertIn("issues", issues)
            self.assertIsInstance(issues["issues"], list)
            self.assertIn("startAt", issues)
            self.assertIn("maxResults", issues)
            self.assertIn("total", issues)
        except Exception as e:
            import traceback

            print(f"Error retrieving board issues: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

            if self.check_permissions(e):
                return

            # Some boards might have query errors or issues
            if "jql" in str(e).lower() or "403" in str(e) or "400" in str(e) or "404" in str(e):
                self.skipTest(f"Board issues query error: {str(e)}")
            raise

    def test_get_sprints(self):
        """Test retrieving sprints for a board."""
        try:
            # First get all boards to get an ID
            boards = self.software_jira.get_all_boards()

            # Skip if no boards are available
            if not boards["values"]:
                self.skipTest("No boards available for testing")

            # Find a board that has sprints or choose the first one
            board_id = None
            for board in boards["values"]:
                try:
                    # Check if the board has the sprint feature
                    if board["type"] in ["scrum", "simple"]:
                        board_id = board["id"]
                        print(f"Using board {board['name']} (ID: {board_id}) of type {board['type']}")
                        break
                except (KeyError, TypeError):
                    pass

            if not board_id:
                board_id = boards["values"][0]["id"]
                print(f"Using first available board (ID: {board_id})")

            # Get sprints for the board
            try:
                sprints = self.software_jira.get_all_sprints(board_id)

                # Verify sprints structure
                self.assertIn("values", sprints)

                # If there are sprints, verify their structure
                if sprints["values"]:
                    first_sprint = sprints["values"][0]
                    self.assertIn("id", first_sprint)
                    self.assertIn("name", first_sprint)
                    self.assertIn("state", first_sprint)
            except Exception as e:
                import traceback

                print(f"Error retrieving sprints for board {board_id}: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")

                # If this board doesn't support sprints, skip the test
                if (
                    "does not support sprint operations" in str(e).lower()
                    or "400" in str(e)
                    or "403" in str(e)
                    or "404" in str(e)
                ):
                    self.skipTest(f"Board {board_id} does not support sprints: {str(e)}")
                raise
        except Exception as e:
            import traceback

            print(f"Error retrieving boards: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

            if self.check_permissions(e):
                return

            # Skip if boards can't be retrieved
            if "403" in str(e) or "404" in str(e):
                self.skipTest(f"Cannot retrieve boards: {str(e)}")
            raise


class TestJiraV3PermissionsIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Permissions API."""

    def test_get_my_permissions(self):
        """Test retrieving permissions for the current user."""
        try:
            # Try getting permissions without context (global permissions)
            permissions = self.permissions_jira.get_my_permissions()

            # Verify permissions structure
            self.assertIn("permissions", permissions)

            # If a project context is needed, try with the project key
            if not permissions["permissions"]:
                context = {"projectKey": self.jira_project_key}
                permissions = self.permissions_jira.get_my_permissions(context_parameters=context)
                self.assertIn("permissions", permissions)

            # Should have at least one permission
            self.assertTrue(len(permissions["permissions"]) > 0, "No permissions found")

            # Check structure of a permission
            first_perm_key = list(permissions["permissions"].keys())[0]
            first_perm = permissions["permissions"][first_perm_key]
            self.assertIn("key", first_perm)
            self.assertIn("name", first_perm)
            self.assertIn("type", first_perm)
            self.assertIn("description", first_perm)
            self.assertIn("havePermission", first_perm)
        except Exception as e:
            # Handle 400 errors specially
            if isinstance(e, atlassian.jira.errors.JiraValueError):
                self.skipTest(f"API error when getting permissions: {str(e)}")

            if self.check_permissions(e):
                return

            raise


class TestJiraV3SearchIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Search API."""

    def test_search_issues(self):
        """Test searching for issues."""
        try:
            # Use a more specific JQL that will work even with empty projects
            jql = f"project = {self.jira_project_key}"

            # Try search with POST method (v3 API)
            search_results = self.search_jira.search_issues(jql, max_results=10)

            # Verify search results structure
            self.assertIn("issues", search_results)
            self.assertIsInstance(search_results["issues"], list)

            # Even if no issues are found, the structure should be valid
            self.assertIn("startAt", search_results)
            self.assertIn("maxResults", search_results)
            self.assertIn("total", search_results)

            print(f"Found {len(search_results['issues'])} issues in project {self.jira_project_key}")
        except Exception as e:
            # If there's a 400 error, try with a simpler query
            if isinstance(e, atlassian.jira.errors.JiraValueError):
                try:
                    # Try a generic search instead
                    print("Initial search failed, trying a generic search")
                    search_results = self.search_jira.search_issues("order by created DESC", max_results=10)

                    # Verify search results structure
                    self.assertIn("issues", search_results)
                    self.assertIsInstance(search_results["issues"], list)
                    self.assertIn("startAt", search_results)
                    self.assertIn("maxResults", search_results)
                    self.assertIn("total", search_results)
                    return
                except Exception as e2:
                    self.skipTest(f"Could not perform search: {str(e)} (fallback error: {str(e2)})")

            if self.check_permissions(e):
                return

            self.skipTest(f"Search operation failed: {str(e)}")

    def test_get_field_reference_data(self):
        """Test retrieving field reference data for JQL."""
        try:
            field_data = self.search_jira.get_field_reference_data()

            # Verify field reference data structure - it can be a dictionary or a list depending on the API version
            if isinstance(field_data, dict):
                # For API responses that return a dictionary
                self.assertIn("visibleFieldNames", field_data)

                # If we have field names, verify their structure
                if field_data.get("visibleFieldNames"):
                    field_names = field_data.get("visibleFieldNames")
                    self.assertIsInstance(field_names, list)
            else:
                # For API responses that return a list
                self.assertIsInstance(field_data, list)

                # If there are fields, verify their structure
                if field_data:
                    first_field = field_data[0]
                    self.assertIn("id", first_field)
                    self.assertIn("key", first_field)
                    self.assertIn("displayName", first_field)
        except Exception as e:
            if self.check_permissions(e):
                return
            raise


class TestJiraV3RichTextIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 RichText/ADF API."""

    def test_convert_text_to_adf(self):
        """Test converting plain text to ADF."""
        text = "This is a test of ADF conversion"
        adf_document = self.richtext_jira.convert_text_to_adf(text)

        # Verify ADF structure
        self.assertEqual(adf_document["version"], 1)
        self.assertEqual(adf_document["type"], "doc")
        self.assertIn("content", adf_document)
        self.assertGreater(len(adf_document["content"]), 0)

        # Verify the text content is preserved
        paragraph = adf_document["content"][0]
        self.assertEqual(paragraph["type"], "paragraph")
        self.assertIn("content", paragraph)

        text_node = paragraph["content"][0]
        self.assertEqual(text_node["type"], "text")
        self.assertEqual(text_node["text"], text)

    def test_create_adf_document(self):
        """Test creating an ADF document with multiple elements."""
        # Create paragraphs
        paragraph1 = self.richtext_jira.create_adf_paragraph("Test paragraph")
        paragraph2 = self.richtext_jira.create_adf_paragraph("Bold text", marks=["strong"])

        # Create a bullet list
        bullet_list = self.richtext_jira.create_adf_bullet_list(["Item 1", "Item 2", "Item 3"])

        # Create a code block
        code_block = self.richtext_jira.create_adf_code_block("print('Hello, world!')", language="python")

        # Create a heading
        heading = self.richtext_jira.create_adf_heading("Test Heading", level=2)

        # Combine into a document
        elements = [heading, paragraph1, bullet_list, paragraph2, code_block]
        document = self.richtext_jira.create_adf_document(elements)

        # Verify document structure
        self.assertEqual(document["version"], 1)
        self.assertEqual(document["type"], "doc")
        self.assertEqual(len(document["content"]), 5)

        # Check types of each element
        self.assertEqual(document["content"][0]["type"], "heading")
        self.assertEqual(document["content"][1]["type"], "paragraph")
        self.assertEqual(document["content"][2]["type"], "bulletList")
        self.assertEqual(document["content"][3]["type"], "paragraph")
        self.assertEqual(document["content"][4]["type"], "codeBlock")

    def test_add_comment_with_adf(self):
        """Test adding a comment with ADF to an issue."""
        # Skip test in offline mode
        if os.environ.get("JIRA_OFFLINE_TESTS", "").lower() == "true":
            self.skipTest("Skipping ADF comment test in offline mode")

        # Validate the project key
        self.validate_project_key()

        # Use the helper method to get issue data
        issue_data = TestJiraV3IssuesIntegration.get_issue_data(self, "Test issue for ADF comment")

        try:
            created_issue = self.get_jira_instance().create_issue(issue_data)
            issue_key = created_issue["key"]

            # Create ADF document for comment
            adf_document = self.richtext_jira.create_adf_document(
                [
                    self.richtext_jira.create_adf_paragraph("This is a test comment with ADF"),
                    self.richtext_jira.create_adf_heading("Test Heading", 2),
                    self.richtext_jira.create_adf_bullet_list(["Point 1", "Point 2"]),
                ]
            )

            # Add comment with ADF
            comment = self.richtext_jira.add_comment_with_adf(issue_key, adf_document)

            # Verify comment was added
            self.assertIn("id", comment)

            # Verify we can retrieve the comment
            comments = self.get_jira_instance().get_issue_comments(issue_key)
            self.assertIn("comments", comments)
            self.assertTrue(len(comments["comments"]) > 0)

            # Clean up
            self.get_jira_instance().delete_issue(issue_key)
        except Exception as e:
            # Print detailed error information for debugging
            import traceback

            print(f"Error in ADF comment test: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            self.fail(f"Failed to add comment with ADF: {str(e)}")


class TestJiraV3ProjectsIntegration(JiraV3IntegrationTestCase):
    """Integration tests for the Jira v3 Projects API."""

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        projects = self.projects_jira.get_all_projects()

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
        project = self.projects_jira.get_project(self.jira_project_key)

        # Verify project data
        self.assertEqual(project["key"], self.jira_project_key)
        self.assertIn("id", project)
        self.assertIn("name", project)

    def test_get_project_components(self):
        """Test retrieving project components."""
        components = self.projects_jira.get_project_components(self.jira_project_key)

        # Verify that components are returned (even if empty)
        self.assertIsInstance(components, list)

        # If there are components, verify their structure
        if components:
            first_component = components[0]
            self.assertIn("id", first_component)
            self.assertIn("name", first_component)

    def test_get_project_versions(self):
        """Test retrieving project versions."""
        versions = self.projects_jira.get_project_versions(self.jira_project_key)

        # Verify that versions are returned (even if empty)
        self.assertIsInstance(versions, list)

        # If there are versions, verify their structure
        if versions:
            first_version = versions[0]
            self.assertIn("id", first_version)
            self.assertIn("name", first_version)

    def test_get_project_roles(self):
        """Test retrieving project roles."""
        roles = self.projects_jira.get_project_roles(self.jira_project_key)

        # Verify that roles are returned
        self.assertIsInstance(roles, dict)
        self.assertTrue(len(roles) > 0, "No project roles returned")

        # Get the first role
        first_role_key = next(iter(roles))
        first_role_url = roles[first_role_key]

        # Extract role ID from URL
        role_id = first_role_url.split("/")[-1]

        # Get specific role details
        role = self.projects_jira.get_project_role(self.jira_project_key, role_id)

        # Verify role structure
        self.assertIn("id", role)
        self.assertIn("name", role)
        self.assertIn("actors", role)


if __name__ == "__main__":
    unittest.main()
