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
            # Adding newly implemented methods
            'get_custom_fields': 'get_custom_fields',
            'get_project_issues_count': 'get_project_issues_count',
            'get_all_project_issues': 'get_project_issues',
            'get_issue_remotelinks': 'get_issue_remotelinks',
            'get_issue_remote_links': 'get_issue_remotelinks',
            'get_issue_remote_link_by_id': 'get_issue_remote_link_by_id',
            'create_or_update_issue_remote_links': 'create_or_update_issue_remote_link'
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

    def get_project_issues_count(self, project_id_or_key: str) -> int:
        """
        Legacy method to get the number of issues in a project.
        
        Args:
            project_id_or_key: Project ID or key
            
        Returns:
            Number of issues in the project
        """
        warnings.warn(
            "The method get_project_issues_count is maintained for backward compatibility.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_project_issues_count(project_id_or_key)
    
    def get_all_project_issues(
        self, 
        project: str, 
        fields: Union[str, List[str]] = "*all", 
        start: int = 0, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Legacy method to get all issues in a project.
        
        Args:
            project: Project key
            fields: Fields to include
            start: Start index
            limit: Maximum number of issues to return
            
        Returns:
            List of issues
        """
        warnings.warn(
            "The method get_all_project_issues is deprecated. Use get_project_issues instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_project_issues(project, fields=fields, start_at=start, max_results=limit)
    
    def get_issue_remotelinks(
        self, 
        issue_id_or_key: str, 
        global_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Legacy method to get remote links for an issue.
        
        Args:
            issue_id_or_key: Issue ID or key
            global_id: Filter by global ID
            
        Returns:
            List of remote links
        """
        warnings.warn(
            "The method get_issue_remotelinks is maintained for backward compatibility.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_issue_remotelinks(issue_id_or_key, global_id)
    
    def get_issue_remote_links(
        self, 
        issue_id_or_key: str, 
        global_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Legacy method to get remote links for an issue.
        
        Args:
            issue_id_or_key: Issue ID or key
            global_id: Filter by global ID
            
        Returns:
            List of remote links
        """
        warnings.warn(
            "The method get_issue_remote_links is deprecated. Use get_issue_remotelinks instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_issue_remotelinks(issue_id_or_key, global_id)
    
    def get_issue_remote_link_by_id(
        self, 
        issue_id_or_key: str, 
        link_id: str
    ) -> Dict[str, Any]:
        """
        Legacy method to get a specific remote link for an issue.
        
        Args:
            issue_id_or_key: Issue ID or key
            link_id: Remote link ID
            
        Returns:
            Remote link details
        """
        warnings.warn(
            "The method get_issue_remote_link_by_id is maintained for backward compatibility.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_issue_remote_link_by_id(issue_id_or_key, link_id)
    
    def create_or_update_issue_remote_links(
        self,
        issue_id_or_key: str,
        link_url: str,
        title: str,
        global_id: Optional[str] = None,
        relationship: Optional[str] = None,
        icon_url: Optional[str] = None,
        icon_title: Optional[str] = None,
        status_resolved: bool = False,
        application: dict = {},
    ) -> Dict[str, Any]:
        """
        Legacy method to create or update a remote link for an issue.
        
        Args:
            issue_id_or_key: Issue ID or key
            link_url: URL of the remote link
            title: Title of the remote link
            global_id: Global ID for the remote link (used for updates)
            relationship: Relationship of the link to the issue
            icon_url: URL of an icon for the link
            icon_title: Title for the icon
            status_resolved: Whether the remote link is resolved
            application: Application information
            
        Returns:
            Created or updated remote link
        """
        warnings.warn(
            "The method create_or_update_issue_remote_links is deprecated. "
            "Use create_or_update_issue_remote_link instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().create_or_update_issue_remote_link(
            issue_id_or_key=issue_id_or_key,
            link_url=link_url,
            title=title,
            global_id=global_id,
            relationship=relationship,
            icon_url=icon_url,
            icon_title=icon_title,
            status_resolved=status_resolved
        )
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Legacy method to get all projects.
        
        Returns:
            List of all projects
        """
        warnings.warn(
            "The method get_projects is deprecated. Use get_all_projects instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return list(super().get_all_projects()) 