"""
Jira Cloud API implementation for Jira API v3
"""

import json
import logging
from typing import Any, Dict, Generator, List, Optional, Union

from atlassian.jira.base import JiraBase

log = logging.getLogger(__name__)


class Jira(JiraBase):
    """
    Jira Cloud API implementation for Jira API v3
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Jira Cloud instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the JiraBase constructor
        """
        kwargs["cloud"] = True
        api_version = kwargs.pop("api_version", 3)
        super(Jira, self).__init__(url, username, password, api_version=api_version, **kwargs)

    def _get_paged_resources(
        self, 
        endpoint: str, 
        resource_key: str = None, 
        params: dict = None, 
        data: dict = None,
        absolute: bool = False
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Generic method to retrieve paged resources from Jira Cloud API.

        Args:
            endpoint: The API endpoint to retrieve resources from
            resource_key: The key to extract resources from the response
            params: Query parameters for the request
            data: POST data for the request
            absolute: If True, endpoint is treated as an absolute URL

        Returns:
            Generator yielding resources
        """
        if params is None:
            params = {}

        # Ensure required pagination parameters
        if "startAt" not in params:
            params["startAt"] = 0
        if "maxResults" not in params and "limit" not in params:
            params["maxResults"] = 50

        while True:
            response = self.get(endpoint, params=params, data=data, absolute=absolute)
            
            # Extract resources based on the response format
            resources = []
            if resource_key and isinstance(response, dict):
                resources = response.get(resource_key, [])
            elif isinstance(response, dict) and "values" in response:
                resources = response.get("values", [])
            elif isinstance(response, list):
                resources = response
            else:
                # If no resources found or format not recognized
                resources = [response] if response else []
            
            # Yield each resource
            for resource in resources:
                yield resource
                
            # Check for pagination indicators
            if isinstance(response, dict):
                # Check different pagination indicators
                is_last = response.get("isLast", False)
                next_page = response.get("nextPage")
                total = response.get("total", 0)
                max_results = response.get("maxResults", 0)
                start_at = response.get("startAt", 0)
                
                # Exit if explicitly marked as last page
                if is_last:
                    break
                    
                # Exit if next page URL is not provided and we've reached the end
                if next_page is None:
                    # Check if we've reached the end based on counts
                    if total > 0 and start_at + len(resources) >= total:
                        break
                    # If no next page and no resources, we're done
                    if not resources:
                        break
                    # Otherwise, calculate next page start
                    params["startAt"] = start_at + max_results
                else:
                    # Use the nextPage URL directly
                    endpoint = next_page
                    absolute = True
                    # Parameters are included in the URL
                    params = {}
            else:
                # If response is not a dict, we can't determine pagination
                break
                
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
        endpoint = self.get_endpoint("issue_by_id", id=issue_id_or_key)
        params = {}
        
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand
            
        return self.get(endpoint, params=params)
        
    def create_issue(
        self, 
        fields: Dict[str, Any], 
        update: Dict[str, Any] = None, 
        transition: Dict[str, Any] = None,
        update_history: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new issue.

        Args:
            fields: Issue fields
            update: Issue update operations
            transition: Initial transition for the issue
            update_history: Whether to update issue view history

        Returns:
            Dictionary containing the created issue
        """
        endpoint = self.get_endpoint("issue")
        data = {"fields": fields}
        
        if update:
            data["update"] = update
        if transition:
            data["transition"] = transition
            
        params = {}
        if update_history:
            params["updateHistory"] = "true"
            
        return self.post(endpoint, data=data, params=params)
        
    def update_issue(
        self, 
        issue_id_or_key: str, 
        fields: Dict[str, Any] = None, 
        update: Dict[str, Any] = None,
        notify_users: bool = True,
        override_screen_security: bool = False,
        override_editmeta: bool = False
    ) -> None:
        """
        Update an existing issue.

        Args:
            issue_id_or_key: Issue ID or key
            fields: Issue fields to update
            update: Issue update operations
            notify_users: Whether to send notifications about the update
            override_screen_security: Whether to override screen security
            override_editmeta: Whether to override the screen security of the edit meta
        """
        endpoint = self.get_endpoint("issue_by_id", id=issue_id_or_key)
        data = {}
        
        if fields:
            data["fields"] = fields
        if update:
            data["update"] = update
            
        params = {
            "notifyUsers": str(notify_users).lower(),
            "overrideScreenSecurity": str(override_screen_security).lower(),
            "overrideEditableFlag": str(override_editmeta).lower()
        }
        
        return self.put(endpoint, data=data, params=params)
        
    def delete_issue(self, issue_id_or_key: str, delete_subtasks: bool = False) -> None:
        """
        Delete an issue.

        Args:
            issue_id_or_key: Issue ID or key
            delete_subtasks: Whether to delete subtasks of the issue
        """
        endpoint = self.get_endpoint("issue_by_id", id=issue_id_or_key)
        params = {"deleteSubtasks": str(delete_subtasks).lower()}
        
        return self.delete(endpoint, params=params)

    def get_issue_transitions(self, issue_id_or_key: str) -> Dict[str, Any]:
        """
        Get available transitions for an issue.

        Args:
            issue_id_or_key: Issue ID or key

        Returns:
            Dictionary containing the available transitions
        """
        endpoint = self.get_endpoint("issue_transitions", id=issue_id_or_key)
        return self.get(endpoint)
        
    def transition_issue(
        self, 
        issue_id_or_key: str, 
        transition_id: str, 
        fields: Dict[str, Any] = None, 
        update: Dict[str, Any] = None, 
        comment: Dict[str, Any] = None
    ) -> None:
        """
        Transition an issue.

        Args:
            issue_id_or_key: Issue ID or key
            transition_id: Transition ID
            fields: Issue fields to update during transition
            update: Issue update operations
            comment: Comment to add during transition
        """
        endpoint = self.get_endpoint("issue_transitions", id=issue_id_or_key)
        data = {"transition": {"id": transition_id}}
        
        if fields:
            data["fields"] = fields
        if update:
            data["update"] = update
        if comment:
            # Comment can be in ADF format
            data["update"] = data.get("update", {})
            data["update"]["comment"] = [{"add": comment}]
            
        return self.post(endpoint, data=data)

    def add_comment(
        self, 
        issue_id_or_key: str, 
        body: Union[str, Dict[str, Any]], 
        visibility: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Add a comment to an issue.

        Args:
            issue_id_or_key: Issue ID or key
            body: Comment body (string for simple text or dict for ADF)
            visibility: Visibility settings for the comment

        Returns:
            Dictionary containing the created comment
        """
        endpoint = self.get_endpoint("issue_comment", id=issue_id_or_key)
        
        # Convert string body to ADF if needed
        if isinstance(body, str):
            data = {
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": body
                                }
                            ]
                        }
                    ]
                }
            }
        else:
            data = {"body": body}
            
        if visibility:
            data["visibility"] = visibility
            
        return self.post(endpoint, data=data)

    def get_comments(self, issue_id_or_key: str, expand: str = None) -> Generator[Dict[str, Any], None, None]:
        """
        Get comments for an issue.

        Args:
            issue_id_or_key: Issue ID or key
            expand: Expand options to retrieve additional information

        Returns:
            Generator yielding comment dictionaries
        """
        endpoint = self.get_endpoint("issue_comment", id=issue_id_or_key)
        params = {}
        
        if expand:
            params["expand"] = expand
            
        return self._get_paged_resources(endpoint, "comments", params=params)
        
    def get_issue_attachments(self, issue_id_or_key: str) -> List[Dict[str, Any]]:
        """
        Get attachments for an issue.

        Args:
            issue_id_or_key: Issue ID or key

        Returns:
            List of attachment dictionaries
        """
        endpoint = self.get_endpoint("issue_by_id", id=issue_id_or_key)
        params = {"fields": "attachment"}
        
        response = self.get(endpoint, params=params)
        return response.get("fields", {}).get("attachment", [])
        
    def add_attachment(self, issue_id_or_key: str, filename: str, content) -> List[Dict[str, Any]]:
        """
        Add an attachment to an issue.

        Args:
            issue_id_or_key: Issue ID or key
            filename: Name of the file
            content: File content

        Returns:
            List of created attachment dictionaries
        """
        endpoint = self.get_endpoint("issue_attachments", id=issue_id_or_key)
        headers = {"X-Atlassian-Token": "no-check"}
        
        return self.post(endpoint, files={"file": (filename, content)}, headers=headers)
        
    def get_all_projects(self) -> Generator[Dict[str, Any], None, None]:
        """
        Get all projects.

        Returns:
            Generator yielding project dictionaries
        """
        endpoint = self.get_endpoint("project")
        return self._get_paged_resources(endpoint)
        
    def get_project(self, project_id_or_key: str, expand: str = None) -> Dict[str, Any]:
        """
        Get a project by ID or key.

        Args:
            project_id_or_key: Project ID or key
            expand: Expand options to retrieve additional information

        Returns:
            Dictionary containing the project data
        """
        endpoint = self.get_endpoint("project_by_id", id=project_id_or_key)
        params = {}
        
        if expand:
            params["expand"] = expand
            
        return self.get(endpoint, params=params)
        
    def get_project_components(self, project_id_or_key: str) -> Generator[Dict[str, Any], None, None]:
        """
        Get components for a project.

        Args:
            project_id_or_key: Project ID or key

        Returns:
            Generator yielding component dictionaries
        """
        endpoint = self.get_endpoint("project_components", id=project_id_or_key)
        return self._get_paged_resources(endpoint)
        
    def get_project_versions(self, project_id_or_key: str) -> Generator[Dict[str, Any], None, None]:
        """
        Get versions for a project.

        Args:
            project_id_or_key: Project ID or key

        Returns:
            Generator yielding version dictionaries
        """
        endpoint = self.get_endpoint("project_versions", id=project_id_or_key)
        return self._get_paged_resources(endpoint)
        
    def search_issues(
        self, 
        jql: str, 
        start_at: int = 0, 
        max_results: int = 50, 
        fields: List[str] = None, 
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Search for issues using JQL.

        Args:
            jql: JQL query string
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            fields: Fields to include in the results
            expand: Expand options to retrieve additional information

        Returns:
            Dictionary containing the search results
        """
        endpoint = self.get_endpoint("search")
        data = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if fields:
            data["fields"] = fields
        if expand:
            data["expand"] = expand
            
        return self.post(endpoint, data=data)
        
    def get_all_issues(
        self, 
        jql: str, 
        fields: List[str] = None, 
        expand: str = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Get all issues matching a JQL query, handling pagination.

        Args:
            jql: JQL query string
            fields: Fields to include in the results
            expand: Expand options to retrieve additional information

        Returns:
            Generator yielding issue dictionaries
        """
        endpoint = self.get_endpoint("search")
        data = {"jql": jql}
        
        if fields:
            data["fields"] = fields
        if expand:
            data["expand"] = expand
            
        # Use POST for search as it supports larger JQL queries
        for page in self._get_paged_resources(endpoint, "issues", data=data):
            yield page
            
    def add_watcher(self, issue_id_or_key: str, username: str) -> None:
        """
        Add a watcher to an issue.

        Args:
            issue_id_or_key: Issue ID or key
            username: Username of the watcher to add
        """
        endpoint = self.get_endpoint("issue_watchers", id=issue_id_or_key)
        
        # For API v3, we need to use accountId instead of username
        if self.api_version == 3:
            # First get the account ID for the username
            user_endpoint = self.get_endpoint("user_search")
            users = self.get(user_endpoint, params={"query": username})
            
            if not users:
                raise ValueError(f"User '{username}' not found")
                
            account_id = users[0].get("accountId")
            if not account_id:
                raise ValueError(f"Account ID not found for user '{username}'")
                
            return self.post(endpoint, data=f'"{account_id}"')
        else:
            # For API v2, we can use the username directly
            return self.post(endpoint, data=f'"{username}"')
            
    def remove_watcher(self, issue_id_or_key: str, username: str) -> None:
        """
        Remove a watcher from an issue.

        Args:
            issue_id_or_key: Issue ID or key
            username: Username of the watcher to remove
        """
        endpoint = self.get_endpoint("issue_watchers", id=issue_id_or_key)
        
        if self.api_version == 3:
            # First get the account ID for the username
            user_endpoint = self.get_endpoint("user_search")
            users = self.get(user_endpoint, params={"query": username})
            
            if not users:
                raise ValueError(f"User '{username}' not found")
                
            account_id = users[0].get("accountId")
            if not account_id:
                raise ValueError(f"Account ID not found for user '{username}'")
                
            params = {"accountId": account_id}
        else:
            # For API v2, we can use the username directly
            params = {"username": username}
            
        return self.delete(endpoint, params=params)
        
    def get_issue_worklog(self, issue_id_or_key: str) -> Generator[Dict[str, Any], None, None]:
        """
        Get worklog for an issue.

        Args:
            issue_id_or_key: Issue ID or key

        Returns:
            Generator yielding worklog dictionaries
        """
        endpoint = self.get_endpoint("issue_worklog", id=issue_id_or_key)
        return self._get_paged_resources(endpoint, "worklogs")
        
    def add_worklog(
        self, 
        issue_id_or_key: str, 
        time_spent: str = None, 
        time_spent_seconds: int = None,
        comment: Union[str, Dict[str, Any]] = None,
        started: str = None,
        visibility: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Add worklog to an issue.

        Args:
            issue_id_or_key: Issue ID or key
            time_spent: Time spent in Jira format (e.g., "3h 30m")
            time_spent_seconds: Time spent in seconds
            comment: Worklog comment (string for simple text or dict for ADF)
            started: Start date/time in ISO format
            visibility: Visibility settings for the worklog

        Returns:
            Dictionary containing the created worklog
        """
        endpoint = self.get_endpoint("issue_worklog", id=issue_id_or_key)
        data = {}
        
        if time_spent:
            data["timeSpent"] = time_spent
        if time_spent_seconds:
            data["timeSpentSeconds"] = time_spent_seconds
        if started:
            data["started"] = started
            
        # Handle comment
        if comment:
            if isinstance(comment, str) and self.api_version == 3:
                # Convert to ADF for v3
                data["comment"] = {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment
                                }
                            ]
                        }
                    ]
                }
            elif isinstance(comment, dict):
                data["comment"] = comment
            else:
                data["comment"] = comment
                
        if visibility:
            data["visibility"] = visibility
            
        return self.post(endpoint, data=data) 