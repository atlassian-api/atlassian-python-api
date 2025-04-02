"""
Adapter for existing Jira functionality to maintain backward compatibility.
This adapter ensures that code written for the previous Jira implementation will work with the new version.
"""

import logging
import warnings
from typing import Any, Dict, List, Optional, Set, Union, cast

from atlassian.jira.cloud.cloud import Jira as CloudJira

log = logging.getLogger(__name__)


class JiraAdapter(CloudJira):
    """
    Adapter that provides compatibility with the legacy Jira API methods.
    This ensures backward compatibility with existing code.
    """

    def __init__(self, url: str, *args: Any, **kwargs: Any):
        """
        Initialize the JiraAdapter instance.

        Args:
            url: Jira URL
            args: Arguments to pass to CloudJira
            kwargs: Keyword arguments to pass to CloudJira
        """
        super(JiraAdapter, self).__init__(url, *args, **kwargs)
        self._mapped_methods: Set[str] = set()
        self._initialize_method_mapping()

    def _initialize_method_mapping(self) -> None:
        """
        Initialize the mapping for legacy method names to new method names.
        """
        # Map methods that have equivalent functionality but different names
        self._mapped_methods = {
            # Original method name -> New method name
            'get_issue': 'get_issue',
            'issue_add_comment': 'add_comment',
            'issue_edit_comment': 'edit_comment',
            'issue_get_comments': 'get_comments',
            'get_issue_watchers': 'get_issue_watchers',
            'jql': 'search_issues',
            'get_projects': 'get_all_projects',
            'get_project': 'get_project',
            'get_project_components': 'get_project_components',
            'get_project_versions': 'get_project_versions',
            'get_user': 'get_user',
            'myself': 'get_current_user',
            'search_users': 'search_users',
            'get_fields': 'get_fields',
            'get_all_fields': 'get_all_fields',
            'get_priorities': 'get_priorities',
            'get_statuses': 'get_statuses',
            'get_resolutions': 'get_resolutions',
            'get_issue_types': 'get_issue_types',
            'issue_add_attachment': 'add_attachment',
            'issue_get_attachments': 'get_issue_attachments',
            'issue_delete': 'delete_issue',
            'issue_update': 'update_issue',
            'issue_get_transitions': 'get_issue_transitions',
            'issue_transition': 'transition_issue',
            'issue_get_worklog': 'get_issue_worklog',
            'issue_add_worklog': 'add_worklog',
            'assign_issue': 'assign_issue',
            'issue_add_watcher': 'add_watcher',
            'issue_remove_watcher': 'remove_watcher',
            'jql_get': 'get_all_issues',
        }

    def __getattr__(self, name: str) -> Any:
        """
        Handle calls to legacy method names by redirecting to new methods.

        Args:
            name: The method name being accessed

        Returns:
            The requested attribute or method
        """
        # If the method is mapped to a new name, redirect and show a deprecation warning
        if name in self._mapped_methods:
            new_name = self._mapped_methods[name]
            if new_name != name:  # Only show warning if name actually changed
                warnings.warn(
                    f"Method '{name}' is deprecated, use '{new_name}' instead.",
                    DeprecationWarning,
                    stacklevel=2
                )
            return getattr(self, new_name)
        
        # Handle special cases that require more complex adaptation
        if name == 'issue_field_value':
            return self._adapted_issue_field_value
        
        # For unmapped methods, we'll raise an AttributeError
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")

    def _adapted_issue_field_value(self, issue_key: str, field: str) -> Any:
        """
        Adapter for the legacy issue_field_value method.

        Args:
            issue_key: The issue key (e.g. 'JRA-123')
            field: The field name

        Returns:
            The field value
        """
        issue = self.get_issue(issue_key, fields=field)
        if 'fields' in issue and field in issue['fields']:
            return issue['fields'][field]
        return None

    # Legacy API methods that need specific adaptation

    def search(self, jql: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Legacy method for JQL search.

        Args:
            jql: JQL query string
            args: Additional args to pass to search_issues
            kwargs: Additional kwargs to pass to search_issues

        Returns:
            Search results
        """
        return self.search_issues(jql, *args, **kwargs)

    def get_project(self, project_id_or_key: str) -> Dict[str, Any]:
        """
        Get project information.

        Args:
            project_id_or_key: Project ID or key

        Returns:
            Project information
        """
        url = self.get_endpoint("project_by_id", id=project_id_or_key)
        return self.get(url)

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Legacy method to get all projects.

        Returns:
            List of all projects
        """
        return super().get_all_projects()

    def add_watcher(self, issue_key: str, username: str) -> bool:
        """
        Add watcher to an issue.

        Args:
            issue_key: The issue key (e.g. 'JRA-123')
            username: The username to add as a watcher

        Returns:
            True if successful
        """
        url = self.get_endpoint("issue_watchers", id=issue_key)
        
        # Different payload format for v2 vs v3
        data = username
        if self.api_version == 3:
            data = {"accountId": username}
            
        response = self.post(url, data=data)
        return response.status_code == 204  # 204 No Content indicates success

    def remove_watcher(self, issue_key: str, username: str) -> bool:
        """
        Remove watcher from an issue.

        Args:
            issue_key: The issue key (e.g. 'JRA-123')
            username: The username to remove as a watcher

        Returns:
            True if successful
        """
        url = self.get_endpoint("issue_watchers", id=issue_key)
        params = {"username": username}
        if self.api_version == 3:
            params = {"accountId": username}
            
        response = self.delete(url, params=params)
        return response.status_code == 204  # 204 No Content indicates success

    # Additional legacy method adapters will be added in Phase 2 

    def myself(self) -> Dict[str, Any]:
        """
        Legacy method to get current user information.
        
        Returns:
            Dictionary containing the current user data
        """
        warnings.warn(
            "The method myself is deprecated and will be removed in a future version. "
            "Please use get_current_user instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_current_user() 