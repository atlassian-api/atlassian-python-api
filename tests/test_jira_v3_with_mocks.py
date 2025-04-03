#!/usr/bin/env python3
"""
Tests for the Jira v3 API with mocked responses.
This tests pagination, error handling, and v3 specific features.
"""

import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from requests import Response
from requests.exceptions import HTTPError

from atlassian.jira.cloud import Jira
from atlassian.jira.cloud import JiraAdapter
from atlassian.jira.cloud import UsersJira
from atlassian.jira.cloud import UsersJiraAdapter
from atlassian.jira.cloud import SoftwareJira
from atlassian.jira.cloud import SoftwareJiraAdapter
from atlassian.jira.cloud import PermissionsJira
from atlassian.jira.cloud import PermissionsJiraAdapter
from atlassian.jira.cloud import SearchJira
from atlassian.jira.cloud import SearchJiraAdapter

from mocks.jira_v3_mock_responses import (
    BOARD_MOCK,
    BOARDS_RESULT,
    COMMENT_MOCK,
    COMMENTS_RESULT,
    COMPONENT_MOCK,
    COMPONENTS_RESULT,
    CURRENT_USER_MOCK,
    ERROR_NOT_FOUND,
    ERROR_PERMISSION_DENIED,
    ERROR_VALIDATION,
    FIELD_MOCK,
    FIELDS_RESULT,
    GROUP_MEMBERS_RESULT,
    GROUP_MOCK,
    GROUPS_RESULT,
    ISSUE_MOCK,
    ISSUE_TYPE_MOCK,
    ISSUE_TYPES_RESULT,
    ISSUES_SEARCH_RESULT,
    PERMISSIONS_RESULT,
    PROJECT_MOCK,
    PROJECTS_RESULT,
    SPRINT_MOCK,
    SPRINTS_RESULT,
    USER_MOCK,
    USERS_RESULT,
    VERSION_MOCK,
    VERSIONS_RESULT,
    get_mock_for_endpoint,
)


class TestJiraV3WithMocks(unittest.TestCase):
    """Test case for Jira v3 API using mock responses."""

    # Add a timeout to prevent test hanging
    TEST_TIMEOUT = 10  # seconds

    def setUp(self):
        """Set up the test case."""
        self.jira = Jira(
            url="https://example.atlassian.net",
            username="username",
            password="password",
        )

        # Create a more explicitly defined mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.reason = "OK"
        self.mock_response.headers = {}
        self.mock_response.raise_for_status.side_effect = None

        # Ensure json method is properly mocked
        self.mock_response.json = MagicMock(return_value={})
        self.mock_response.text = "{}"

        # Create a clean session mock with timeout
        self.jira._session = MagicMock()
        self.jira._session.request = MagicMock(return_value=self.mock_response)
        # Explicitly set timeout parameter
        self.jira.timeout = self.TEST_TIMEOUT

    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        # Get default mock data if none provided
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)

        # Convert mock data to text
        mock_data_text = json.dumps(mock_data)

        # Set up response attributes
        self.mock_response.status_code = status_code
        self.mock_response.text = mock_data_text
        self.mock_response.json.return_value = mock_data

        # Set appropriate reason based on status code
        if status_code == 200:
            self.mock_response.reason = "OK"
        elif status_code == 201:
            self.mock_response.reason = "Created"
        elif status_code == 204:
            self.mock_response.reason = "No Content"
        elif status_code == 400:
            self.mock_response.reason = "Bad Request"
        elif status_code == 403:
            self.mock_response.reason = "Forbidden"
        elif status_code == 404:
            self.mock_response.reason = "Not Found"
        else:
            self.mock_response.reason = "Unknown"

        # Handle pagination headers if applicable
        self.mock_response.headers = {}
        if isinstance(mock_data, dict):
            if "nextPage" in mock_data:
                self.mock_response.headers = {"Link": f'<{mock_data["nextPage"]}>; rel="next"'}

        # Configure raise_for_status behavior
        if status_code >= 400:
            error = HTTPError(f"HTTP Error {status_code}", response=self.mock_response)
            self.mock_response.raise_for_status.side_effect = error
        else:
            self.mock_response.raise_for_status.side_effect = None

        return mock_data

    def test_get_current_user(self):
        """Test retrieving the current user."""
        endpoint = "rest/api/3/myself"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_current_user()

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["accountId"], USER_MOCK["accountId"])

    def test_get_issue_by_id(self):
        """Test retrieving an issue by ID."""
        issue_id = "10001"
        endpoint = f"rest/api/3/issue/{issue_id}"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_issue(issue_id)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], issue_id)

    def test_search_issues_with_pagination(self):
        """Test searching for issues with pagination."""
        endpoint = "rest/api/3/search"
        jql = "project = TEST"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.search_issues(jql, max_results=50)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["issues"]), 2)
        self.assertEqual(result["issues"][0]["key"], "TEST-1")

    def test_error_handling_not_found(self):
        """Test error handling when a resource is not found."""
        issue_id = "nonexistent"
        endpoint = f"rest/api/3/issue/{issue_id}"

        # Mock a 404 error response
        self.mock_response_for_endpoint(endpoint, status_code=404, mock_data=ERROR_NOT_FOUND)

        # Ensure HTTPError is raised
        from atlassian.jira.errors import JiraNotFoundError

        with self.assertRaises(JiraNotFoundError):
            self.jira.get_issue(issue_id)

    def test_error_handling_permission_denied(self):
        """Test error handling when permission is denied."""
        issue_id = "restricted"
        endpoint = f"rest/api/3/issue/{issue_id}"

        # Mock a 403 error response
        self.mock_response_for_endpoint(endpoint, status_code=403, mock_data=ERROR_PERMISSION_DENIED)

        # Ensure HTTPError is raised
        from atlassian.jira.errors import JiraPermissionError

        with self.assertRaises(JiraPermissionError):
            self.jira.get_issue(issue_id)

    def test_error_handling_validation(self):
        """Test error handling when there's a validation error."""
        # Trying to create an issue with invalid data
        endpoint = "rest/api/3/issue"

        # Mock a 400 error response
        self.mock_response_for_endpoint(endpoint, status_code=400, mock_data=ERROR_VALIDATION)

        # Ensure HTTPError is raised
        from atlassian.jira.errors import JiraValueError

        with self.assertRaises(JiraValueError):
            self.jira.create_issue(
                fields={
                    "project": {"key": "TEST"},
                    "issuetype": {"name": "Task"},
                }  # Missing summary, should cause validation error
            )

    def test_get_issue_comments(self):
        """Test retrieving comments for an issue."""
        issue_key = "TEST-1"
        endpoint = f"rest/api/3/issue/{issue_key}/comment"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_issue_comments(issue_key)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["comments"]), 2)

    def test_add_comment(self):
        """Test adding a comment to an issue."""
        issue_key = "TEST-1"
        endpoint = f"rest/api/3/issue/{issue_key}/comment"
        comment_text = "This is a test comment."

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint, mock_data=COMMENT_MOCK)

        # Call the method
        result = self.jira.add_comment(issue_key, comment_text)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], "10001")

    def test_get_all_projects(self):
        """Test retrieving all projects."""
        endpoint = "rest/api/3/project"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_all_projects()

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)

    def test_get_project(self):
        """Test retrieving a project by key."""
        project_key = "TEST"
        endpoint = f"rest/api/3/project/{project_key}"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_project(project_key)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["key"], project_key)

    def test_get_project_components(self):
        """Test retrieving components for a project."""
        project_key = "TEST"
        endpoint = f"rest/api/3/project/{project_key}/component"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_project_components(project_key)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Test Component")

    def test_get_project_versions(self):
        """Test retrieving versions for a project."""
        project_key = "TEST"
        endpoint = f"rest/api/3/project/{project_key}/version"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.jira.get_project_versions(project_key)

        # Verify the request was made
        self.jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "v1.0")


class TestJiraV3UsersWithMocks(unittest.TestCase):
    """Tests for the Jira v3 Users API using mock responses."""

    def setUp(self):
        """Set up the test case."""
        self.users_jira = UsersJira(
            url="https://example.atlassian.net",
            username="username",
            password="password",
        )

        # Create a more explicitly defined mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.reason = "OK"
        self.mock_response.headers = {}
        self.mock_response.raise_for_status.side_effect = None

        # Ensure json method is properly mocked
        self.mock_response.json = MagicMock(return_value={})
        self.mock_response.text = "{}"

        # Create a clean session mock with timeout
        self.users_jira._session = MagicMock()
        self.users_jira._session.request = MagicMock(return_value=self.mock_response)
        # Explicitly set timeout parameter
        self.users_jira.timeout = 10

    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        # Get default mock data if none provided
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)

        # Convert mock data to text
        mock_data_text = json.dumps(mock_data)

        # Set up response attributes
        self.mock_response.status_code = status_code
        self.mock_response.text = mock_data_text
        self.mock_response.json.return_value = mock_data

        # Configure raise_for_status behavior
        if status_code >= 400:
            error = HTTPError(f"HTTP Error {status_code}", response=self.mock_response)
            self.mock_response.raise_for_status.side_effect = error
        else:
            self.mock_response.raise_for_status.side_effect = None

        return mock_data

    def test_get_user(self):
        """Test retrieving a user by account ID."""
        account_id = "5b10a2844c20165700ede21g"
        endpoint = f"rest/api/3/user"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint, mock_data=USER_MOCK)

        # Call the method
        result = self.users_jira.get_user(account_id=account_id)

        # Verify the request was made
        self.users_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["accountId"], account_id)

    def test_search_users(self):
        """Test searching for users."""
        query = "test"
        endpoint = "rest/api/3/user/search"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint, mock_data=USERS_RESULT)

        # Call the method
        result = self.users_jira.find_users(query)

        # Verify the request was made
        self.users_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)

    def test_get_groups(self):
        """Test retrieving all groups."""
        endpoint = "rest/api/3/groups"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.users_jira.get_groups()

        # Verify the request was made
        self.users_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["groups"]), 2)
        self.assertEqual(result["groups"][0]["name"], "test-group")

    def test_get_group(self):
        """Test retrieving a group by name."""
        group_name = "test-group"
        endpoint = "rest/api/3/group"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.users_jira.get_group(group_name)

        # Verify the request was made
        self.users_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["name"], group_name)

    def test_get_group_members(self):
        """Test retrieving members of a group."""
        group_name = "test-group"
        endpoint = "rest/api/3/group/member"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.users_jira.get_group_members(group_name)

        # Verify the request was made
        self.users_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["values"]), 2)
        self.assertEqual(result["values"][0]["displayName"], "Test User")


class TestJiraV3AdapterWithMocks(unittest.TestCase):
    """Tests for the Jira v3 Adapter (legacy compatibility) using mock responses."""

    def setUp(self):
        """Set up the test case."""
        self.jira_adapter = JiraAdapter(
            url="https://example.atlassian.net",
            username="username",
            password="password",
        )

        # Create a more explicitly defined mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.reason = "OK"
        self.mock_response.headers = {}
        self.mock_response.raise_for_status.side_effect = None

        # Ensure json method is properly mocked
        self.mock_response.json = MagicMock(return_value={})
        self.mock_response.text = "{}"

        # Create a clean session mock with timeout
        self.jira_adapter._session = MagicMock()
        self.jira_adapter._session.request = MagicMock(return_value=self.mock_response)
        # Explicitly set timeout parameter
        self.jira_adapter.timeout = 10

    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        # Get default mock data if none provided
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)

        # Convert mock data to text
        mock_data_text = json.dumps(mock_data)

        # Set up response attributes
        self.mock_response.status_code = status_code
        self.mock_response.text = mock_data_text
        self.mock_response.json.return_value = mock_data

        # Configure raise_for_status behavior
        if status_code >= 400:
            error = HTTPError(f"HTTP Error {status_code}", response=self.mock_response)
            self.mock_response.raise_for_status.side_effect = error
        else:
            self.mock_response.raise_for_status.side_effect = None

        return mock_data

    def test_legacy_get_issue(self):
        """Test retrieving an issue using the legacy method name."""
        issue_key = "TEST-1"
        endpoint = f"rest/api/3/issue/{issue_key}"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint, mock_data=ISSUE_MOCK)

        # Call the method
        result = self.jira_adapter.issue(issue_key)

        # Verify the request was made
        self.jira_adapter._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["key"], issue_key)

    def test_legacy_search_issues(self):
        """Test searching for issues using the legacy method name."""
        jql = "project = TEST"
        endpoint = "rest/api/3/search"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint, mock_data=ISSUES_SEARCH_RESULT)

        # Call the method
        result = self.jira_adapter.jql(jql)

        # Verify the request was made
        self.jira_adapter._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["issues"]), 2)


class TestJiraV3SoftwareWithMocks(unittest.TestCase):
    """Tests for the Jira v3 Software API using mock responses."""

    def setUp(self):
        """Set up the test case."""
        self.software_jira = SoftwareJira(
            url="https://example.atlassian.net",
            username="username",
            password="password",
        )

        # Create a more explicitly defined mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.reason = "OK"
        self.mock_response.headers = {}
        self.mock_response.raise_for_status.side_effect = None

        # Ensure json method is properly mocked
        self.mock_response.json = MagicMock(return_value={})
        self.mock_response.text = "{}"

        # Create a clean session mock with timeout
        self.software_jira._session = MagicMock()
        self.software_jira._session.request = MagicMock(return_value=self.mock_response)
        # Explicitly set timeout parameter
        self.software_jira.timeout = 10

    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        # Get default mock data if none provided
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)

        # Convert mock data to text
        mock_data_text = json.dumps(mock_data)

        # Set up response attributes
        self.mock_response.status_code = status_code
        self.mock_response.text = mock_data_text
        self.mock_response.json.return_value = mock_data

        # Configure raise_for_status behavior
        if status_code >= 400:
            error = HTTPError(f"HTTP Error {status_code}", response=self.mock_response)
            self.mock_response.raise_for_status.side_effect = error
        else:
            self.mock_response.raise_for_status.side_effect = None

        return mock_data

    def test_get_all_boards(self):
        """Test retrieving all boards."""
        endpoint = "rest/agile/1.0/board"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.software_jira.get_all_boards()

        # Verify the request was made
        self.software_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["values"]), 2)
        self.assertEqual(result["values"][0]["name"], "Test Board")

    def test_get_board(self):
        """Test retrieving a board by ID."""
        board_id = 1
        endpoint = f"rest/agile/1.0/board/{board_id}"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.software_jira.get_board(board_id)

        # Verify the request was made
        self.software_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], board_id)

    def test_get_board_sprints(self):
        """Test retrieving sprints for a board."""
        board_id = 1
        endpoint = f"rest/agile/1.0/board/{board_id}/sprint"

        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)

        # Call the method
        result = self.software_jira.get_board_sprints(board_id)

        # Verify the request was made
        self.software_jira._session.request.assert_called_once()

        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result["values"]), 2)
        self.assertEqual(result["values"][0]["name"], "Sprint 1")


if __name__ == "__main__":
    unittest.main()
