"""
Jira Cloud API for working with issues
"""

import logging
from typing import Any, Dict

from atlassian.jira.cloud.cloud import CloudJira

log = logging.getLogger(__name__)


class IssuesJira(CloudJira):
    """
    Jira Cloud API for working with issues
    """

    def get_issue(self, issue_id_or_key: str, fields: str = None, expand: str = None) -> Dict[str, Any]:
        """
        Get an issue by ID or key.

        Args:
            issue_id_or_key: Issue ID or key
            fields: Comma-separated list of field names to include
            expand: Expand options to retrieve additional information

        Returns:
            Dictionary containing the issue data
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")

        endpoint = f"rest/api/3/issue/{issue_id_or_key}"
        params = self.validate_params(fields=fields, expand=expand)

        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to retrieve issue {issue_id_or_key}: {e}")
            raise

    def get_create_meta(
        self,
        project_keys: str = None,
        project_ids: str = None,
        issue_type_ids: str = None,
        issue_type_names: str = None,
        expand: str = None,
    ) -> Dict[str, Any]:
        """
        Get metadata for creating issues.

        Args:
            project_keys: Comma-separated list of project keys
            project_ids: Comma-separated list of project IDs
            issue_type_ids: Comma-separated list of issue type IDs
            issue_type_names: Comma-separated list of issue type names
            expand: Additional fields to expand in the response

        Returns:
            Dictionary containing the issue creation metadata
        """
        endpoint = "rest/api/3/issue/createmeta"
        params = {}

        if project_keys:
            params["projectKeys"] = project_keys
        if project_ids:
            params["projectIds"] = project_ids
        if issue_type_ids:
            params["issuetypeIds"] = issue_type_ids
        if issue_type_names:
            params["issuetypeNames"] = issue_type_names
        if expand:
            params["expand"] = expand

        return self.get(endpoint, params=params)

    def create_issue(
        self,
        fields: Dict[str, Any],
        update: Dict[str, Any] = None,
        transition: Dict[str, Any] = None,
        update_history: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a new issue.

        Args:
            fields: Issue fields or a dictionary containing the fields under a 'fields' key
            update: Issue update operations
            transition: Initial transition for the issue
            update_history: Whether to update issue view history

        Returns:
            Dictionary containing the created issue
        """
        endpoint = "rest/api/3/issue"

        # Handle both direct fields dictionary and dictionary with a nested 'fields' key
        actual_fields = fields
        if isinstance(fields, dict) and "fields" in fields:
            actual_fields = fields["fields"]

        data = {"fields": actual_fields}

        if update:
            data["update"] = update
        if transition:
            data["transition"] = transition

        params = {}
        if update_history:
            params["updateHistory"] = "true"

        log.debug(f"Creating issue with data: {data}")
        return self.post(endpoint, data=data, params=params)

    def update_issue(
        self,
        issue_id_or_key: str,
        fields: Dict[str, Any] = None,
        update: Dict[str, Any] = None,
        notify_users: bool = True,
        transition: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Update an issue.

        Args:
            issue_id_or_key: Issue ID or key
            fields: Issue fields to update
            update: Issue update operations in the Atlassian Document Format
            notify_users: Whether to send notification about the update
            transition: Transition to perform during the update

        Returns:
            Empty dictionary if successful
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}"

        data = {}

        # Handle both direct fields dictionary and dictionary with a nested 'fields' key
        if fields:
            actual_fields = fields
            if isinstance(fields, dict) and "fields" in fields:
                actual_fields = fields["fields"]
            data["fields"] = actual_fields

        if update:
            data["update"] = update

        if transition:
            data["transition"] = transition

        params = {"notifyUsers": "true" if notify_users else "false"}

        log.debug(f"Updating issue {issue_id_or_key} with data: {data}")
        return self.put(endpoint, data=data, params=params)

    def delete_issue(self, issue_id_or_key: str, delete_subtasks: bool = False) -> Dict[str, Any]:
        """
        Delete an issue.

        Args:
            issue_id_or_key: Issue ID or key
            delete_subtasks: Whether to delete subtasks of the issue

        Returns:
            Empty dictionary if successful
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}"

        params = {"deleteSubtasks": "true" if delete_subtasks else "false"}

        return self.delete(endpoint, params=params)

    def get_issue_comments(
        self, issue_id_or_key: str, start_at: int = 0, max_results: int = 50, expand: str = None
    ) -> Dict[str, Any]:
        """
        Get comments for an issue.

        Args:
            issue_id_or_key: Issue ID or key
            start_at: Index of the first comment to return
            max_results: Maximum number of comments to return
            expand: Additional fields to expand in the response

        Returns:
            Dictionary containing the issue comments
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}/comment"

        params = {"startAt": start_at, "maxResults": max_results}

        if expand:
            params["expand"] = expand

        return self.get(endpoint, params=params)

    def add_comment(self, issue_id_or_key: str, comment: Dict[str, Any], expand: str = None) -> Dict[str, Any]:
        """
        Add a comment to an issue.

        Args:
            issue_id_or_key: Issue ID or key
            comment: Comment body in Atlassian Document Format. Can be either a direct
                    document format or a dictionary with a 'body' key containing the document.
            expand: Additional fields to expand in the response

        Returns:
            Dictionary containing the created comment
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}/comment"

        # Check if comment already has 'body' key or if the body content is directly provided
        if "body" in comment:
            data = comment
        else:
            data = {"body": comment}

        self.logger.debug(f"Adding comment to issue {issue_id_or_key} with data: {data}")

        params = {}

        if expand:
            params["expand"] = expand

        return self.post(endpoint, data=data, params=params)

    def get_issue_transitions(self, issue_id_or_key: str, expand: str = None) -> Dict[str, Any]:
        """
        Get available transitions for an issue.

        Args:
            issue_id_or_key: Issue ID or key
            expand: Additional fields to expand in the response

        Returns:
            Dictionary containing available transitions
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}/transitions"

        params = {}
        if expand:
            params["expand"] = expand

        return self.get(endpoint, params=params)

    def get_issue_watchers(self, issue_id_or_key: str) -> Dict[str, Any]:
        """
        Get watchers for an issue.

        Args:
            issue_id_or_key: Issue ID or key

        Returns:
            Dictionary containing the issue watchers
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        endpoint = f"rest/api/3/issue/{issue_id_or_key}/watchers"

        return self.get(endpoint)
