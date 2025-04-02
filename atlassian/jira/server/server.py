"""
Jira Server API implementation for Jira API v2
"""

import logging
from typing import Any, Dict, Generator, List, Optional, Union

from atlassian.jira.base import JiraBase

log = logging.getLogger(__name__)


class Jira(JiraBase):
    """
    Jira Server API implementation for Jira API v2
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Jira Server instance.

        Args:
            url: Jira Server URL
            username: Username for authentication
            password: Password for authentication
            kwargs: Additional arguments to pass to the JiraBase constructor
        """
        kwargs["cloud"] = False
        api_version = kwargs.pop("api_version", 2)
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
        Generic method to retrieve paged resources from Jira Server API.
        Server pagination works differently than Cloud pagination.

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
        if "maxResults" not in params:
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
                total = response.get("total", 0)
                max_results = response.get("maxResults", 0)
                start_at = response.get("startAt", 0)
                
                # Exit if we've reached the end based on counts
                if total > 0 and start_at + len(resources) >= total:
                    break
                # If no more resources, we're done
                if not resources:
                    break
                # Otherwise, calculate next page start
                params["startAt"] = start_at + max_results
            else:
                # If response is not a dict, we can't determine pagination
                break

    # Placeholder for server-specific implementations
    # These will be implemented in Phase 2

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

    def get_all_projects(self) -> Generator[Dict[str, Any], None, None]:
        """
        Get all projects.

        Returns:
            Generator yielding project dictionaries
        """
        endpoint = self.get_endpoint("project")
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