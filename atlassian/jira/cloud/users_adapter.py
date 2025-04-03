"""
Jira Cloud API Adapter for user and group management
This module provides adapters to maintain backward compatibility with existing code
"""

import logging
import warnings
from typing import Any, Dict, List

from atlassian.jira.cloud.users import UsersJira

log = logging.getLogger(__name__)


class UsersJiraAdapter(UsersJira):
    """
    Adapter class for Jira Users API to maintain backward compatibility with the original Jira client.
    This class wraps the new UsersJira implementation and provides methods with the same names and signatures
    as in the original client.
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Users Jira Adapter instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the UsersJira constructor
        """
        super(UsersJiraAdapter, self).__init__(url, username, password, **kwargs)

        # Dictionary mapping legacy method names to new method names
        self._legacy_method_map = {
            "user": "get_user",
            "search_users": "find_users",
            "user_find_by_user_string": "find_users_for_picker",
            "get_all_users": "get_all_users",
            "user_assignable_search": "find_users_assignable_to_issues",
            "user_assignable_multiproject_search": "find_users_assignable_to_projects",
            "get_groups": "get_groups",
            "group": "get_group",
            "create_group": "create_group",
            "remove_group": "delete_group",
            "get_users_from_group": "get_group_members",
            "add_user_to_group": "add_user_to_group",
            "remove_user_from_group": "remove_user_from_group",
            "get_user_columns": "get_user_default_columns",
            "set_user_columns": "set_user_default_columns",
            "reset_user_columns": "reset_user_default_columns",
        }

    # User operations - legacy methods

    def user(
        self, username: str = None, key: str = None, account_id: str = None, expand: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get user details. (Legacy method)

        Args:
            username: Username
            key: User key
            account_id: User account ID
            expand: List of fields to expand

        Returns:
            Dictionary containing user details
        """
        warnings.warn("The 'user' method is deprecated. Use 'get_user' instead.", DeprecationWarning, stacklevel=2)
        return self.get_user(username=username, key=key, account_id=account_id, expand=expand)

    def search_users(
        self,
        query: str,
        start_at: int = 0,
        max_results: int = 50,
        include_active: bool = True,
        include_inactive: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Find users by query. (Legacy method)

        Args:
            query: Search query
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            include_active: Whether to include active users
            include_inactive: Whether to include inactive users

        Returns:
            List of dictionaries containing user information
        """
        warnings.warn(
            "The 'search_users' method is deprecated. Use 'find_users' instead.", DeprecationWarning, stacklevel=2
        )
        return self.find_users(
            query=query,
            start_at=start_at,
            max_results=max_results,
            include_active=include_active,
            include_inactive=include_inactive,
        )

    def user_find_by_user_string(
        self, query: str, start_at: int = 0, max_results: int = 50, show_avatar: bool = True
    ) -> Dict[str, Any]:
        """
        Find users for the user picker. (Legacy method)

        Args:
            query: Search query
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            show_avatar: Whether to include avatar information

        Returns:
            Dictionary containing user information
        """
        warnings.warn(
            "The 'user_find_by_user_string' method is deprecated. Use 'find_users_for_picker' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.find_users_for_picker(
            query=query, start_at=start_at, max_results=max_results, show_avatar=show_avatar
        )

    def user_assignable_search(
        self, query: str, project_keys: str = None, issue_key: str = None, start_at: int = 0, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find users assignable to issues. (Legacy method)

        Args:
            query: Search query
            project_keys: Comma-separated list of project keys
            issue_key: Issue key
            start_at: Index of the first user to return
            max_results: Maximum number of users to return

        Returns:
            List of dictionaries containing user information
        """
        warnings.warn(
            "The 'user_assignable_search' method is deprecated. Use 'find_users_assignable_to_issues' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Convert string of comma-separated project keys to list if provided
        project_keys_list = None
        if project_keys:
            project_keys_list = [key.strip() for key in project_keys.split(",")]

        return self.find_users_assignable_to_issues(
            query=query, project_keys=project_keys_list, issue_key=issue_key, start_at=start_at, max_results=max_results
        )

    def user_assignable_multiproject_search(
        self, query: str, project_keys: str, start_at: int = 0, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find users assignable to projects. (Legacy method)

        Args:
            query: Search query
            project_keys: Comma-separated list of project keys
            start_at: Index of the first user to return
            max_results: Maximum number of users to return

        Returns:
            List of dictionaries containing user information
        """
        warnings.warn(
            "The 'user_assignable_multiproject_search' method is deprecated. Use 'find_users_assignable_to_projects' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        # Convert string of comma-separated project keys to list
        project_keys_list = [key.strip() for key in project_keys.split(",")]

        return self.find_users_assignable_to_projects(
            query=query, project_keys=project_keys_list, start_at=start_at, max_results=max_results
        )

    # Group operations - legacy methods

    def group(self, group_name: str, expand: List[str] = None) -> Dict[str, Any]:
        """
        Get group details. (Legacy method)

        Args:
            group_name: Group name
            expand: List of fields to expand

        Returns:
            Dictionary containing group details
        """
        warnings.warn("The 'group' method is deprecated. Use 'get_group' instead.", DeprecationWarning, stacklevel=2)
        return self.get_group(group_name=group_name, expand=expand)

    def remove_group(self, group_name: str, swap_group: str = None) -> None:
        """
        Delete a group. (Legacy method)

        Args:
            group_name: Group name
            swap_group: Group to transfer restrictions to
        """
        warnings.warn(
            "The 'remove_group' method is deprecated. Use 'delete_group' instead.", DeprecationWarning, stacklevel=2
        )
        return self.delete_group(group_name=group_name, swap_group=swap_group)

    def get_users_from_group(
        self, group_name: str, include_inactive_users: bool = False, start_at: int = 0, max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Get group members. (Legacy method)

        Args:
            group_name: Group name
            include_inactive_users: Whether to include inactive users
            start_at: Index of the first user to return
            max_results: Maximum number of users to return

        Returns:
            Dictionary containing group members information
        """
        warnings.warn(
            "The 'get_users_from_group' method is deprecated. Use 'get_group_members' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_group_members(
            group_name=group_name,
            include_inactive_users=include_inactive_users,
            start_at=start_at,
            max_results=max_results,
        )

    # User column operations - legacy methods

    def get_user_columns(self, username: str = None, account_id: str = None) -> List[Dict[str, Any]]:
        """
        Get user default columns. (Legacy method)

        Args:
            username: Username (deprecated)
            account_id: User account ID

        Returns:
            List of dictionaries containing column information
        """
        warnings.warn(
            "The 'get_user_columns' method is deprecated. Use 'get_user_default_columns' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_user_default_columns(username=username, account_id=account_id)

    def set_user_columns(self, columns: List[str], username: str = None, account_id: str = None) -> None:
        """
        Set user default columns. (Legacy method)

        Args:
            columns: List of column ids
            username: Username (deprecated)
            account_id: User account ID
        """
        warnings.warn(
            "The 'set_user_columns' method is deprecated. Use 'set_user_default_columns' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.set_user_default_columns(columns=columns, username=username, account_id=account_id)

    def reset_user_columns(self, username: str = None, account_id: str = None) -> None:
        """
        Reset user default columns to the system default. (Legacy method)

        Args:
            username: Username (deprecated)
            account_id: User account ID
        """
        warnings.warn(
            "The 'reset_user_columns' method is deprecated. Use 'reset_user_default_columns' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.reset_user_default_columns(username=username, account_id=account_id)
