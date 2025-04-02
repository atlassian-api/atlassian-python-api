"""
Jira Cloud API implementation for user and group management in Jira API v3
"""

import logging
from typing import Any, Dict, List, Optional, Union

from atlassian.jira.cloud.cloud import Jira as CloudJira

log = logging.getLogger(__name__)


class UsersJira(CloudJira):
    """
    Jira Cloud API implementation with user and group management features
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Users Jira Cloud instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the CloudJira constructor
        """
        super(UsersJira, self).__init__(url, username, password, **kwargs)
        
    # User operations
    
    def get_all_users(
        self, 
        start_at: int = 0, 
        max_results: int = 50, 
        include_inactive: bool = False,
        include_active: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all users.
        
        Args:
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            include_inactive: Whether to include inactive users
            include_active: Whether to include active users
            
        Returns:
            List of dictionaries containing user information
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "includeInactive": include_inactive,
            "includeActive": include_active
        }
            
        return self.get("rest/api/3/users/search", params=params)
    
    def get_user(
        self, 
        account_id: str = None,
        username: str = None,
        key: str = None,
        expand: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get user details.
        
        Args:
            account_id: User account ID
            username: Username
            key: User key
            expand: List of fields to expand
            
        Returns:
            Dictionary containing user details
        """
        if not any([account_id, username, key]):
            raise ValueError("At least one of account_id, username, or key must be provided")
            
        params = {}
        
        if account_id:
            params["accountId"] = account_id
            
        if username:
            params["username"] = username
            
        if key:
            params["key"] = key
            
        if expand:
            params["expand"] = ",".join(expand) if isinstance(expand, list) else expand
            
        return self.get("rest/api/3/user", params=params)
    
    def find_users(
        self, 
        query: str, 
        start_at: int = 0, 
        max_results: int = 50, 
        include_active: bool = True, 
        include_inactive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Find users by query.
        
        Args:
            query: Search query
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            include_active: Whether to include active users
            include_inactive: Whether to include inactive users
            
        Returns:
            List of dictionaries containing user information
        """
        params = {
            "query": query,
            "startAt": start_at,
            "maxResults": max_results,
            "includeActive": include_active,
            "includeInactive": include_inactive
        }
            
        return self.get("rest/api/3/user/search", params=params)
    
    def find_users_for_picker(
        self, 
        query: str, 
        start_at: int = 0, 
        max_results: int = 50, 
        show_avatar: bool = True
    ) -> Dict[str, Any]:
        """
        Find users for the user picker.
        
        Args:
            query: Search query
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            show_avatar: Whether to include avatar information
            
        Returns:
            Dictionary containing user information
        """
        params = {
            "query": query,
            "startAt": start_at,
            "maxResults": max_results,
            "showAvatar": show_avatar
        }
            
        return self.get("rest/api/3/user/picker", params=params)
    
    def find_users_assignable_to_issues(
        self, 
        query: str, 
        project_keys: List[str] = None, 
        issue_key: str = None,
        start_at: int = 0, 
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find users assignable to issues.
        
        Args:
            query: Search query
            project_keys: List of project keys
            issue_key: Issue key
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            
        Returns:
            List of dictionaries containing user information
        """
        params = {
            "query": query,
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if project_keys:
            params["projectKeys"] = ",".join(project_keys) if isinstance(project_keys, list) else project_keys
            
        if issue_key:
            params["issueKey"] = issue_key
            
        return self.get("rest/api/3/user/assignable/search", params=params)
    
    def find_users_assignable_to_projects(
        self, 
        query: str, 
        project_keys: List[str], 
        start_at: int = 0, 
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find users assignable to projects.
        
        Args:
            query: Search query
            project_keys: List of project keys
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            
        Returns:
            List of dictionaries containing user information
        """
        params = {
            "query": query,
            "projectKeys": ",".join(project_keys) if isinstance(project_keys, list) else project_keys,
            "startAt": start_at,
            "maxResults": max_results
        }
            
        return self.get("rest/api/3/user/assignable/multiProjectSearch", params=params)
    
    def get_user_property(
        self, 
        account_id: str, 
        property_key: str
    ) -> Dict[str, Any]:
        """
        Get user property.
        
        Args:
            account_id: User account ID
            property_key: Property key
            
        Returns:
            Dictionary containing property information
        """
        return self.get(f"rest/api/3/user/properties/{property_key}", params={"accountId": account_id})
    
    def set_user_property(
        self, 
        account_id: str, 
        property_key: str, 
        value: Any
    ) -> None:
        """
        Set user property.
        
        Args:
            account_id: User account ID
            property_key: Property key
            value: Property value (will be serialized to JSON)
        """
        return self.put(
            f"rest/api/3/user/properties/{property_key}", 
            params={"accountId": account_id}, 
            data=value
        )
    
    def delete_user_property(
        self, 
        account_id: str, 
        property_key: str
    ) -> None:
        """
        Delete user property.
        
        Args:
            account_id: User account ID
            property_key: Property key
        """
        return self.delete(f"rest/api/3/user/properties/{property_key}", params={"accountId": account_id})
    
    # Group operations
    
    def get_groups(
        self, 
        query: str = None, 
        exclude: List[str] = None,
        start_at: int = 0, 
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Get groups.
        
        Args:
            query: Group name query (optional, returns all groups if not provided)
            exclude: List of group names to exclude
            start_at: Index of the first group to return
            max_results: Maximum number of groups to return
            
        Returns:
            Dictionary containing group information
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if query:
            params["query"] = query
            
        if exclude:
            params["exclude"] = ",".join(exclude) if isinstance(exclude, list) else exclude
            
        return self.get("rest/api/3/groups/picker", params=params)
    
    def get_group(
        self, 
        group_name: str,
        expand: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get group details.
        
        Args:
            group_name: Group name
            expand: List of fields to expand
            
        Returns:
            Dictionary containing group details
        """
        params = {
            "groupname": group_name
        }
        
        if expand:
            params["expand"] = ",".join(expand) if isinstance(expand, list) else expand
            
        return self.get("rest/api/3/group", params=params)
    
    def create_group(
        self, 
        name: str
    ) -> Dict[str, Any]:
        """
        Create a group.
        
        Args:
            name: Group name
            
        Returns:
            Dictionary containing created group information
        """
        data = {
            "name": name
        }
            
        return self.post("rest/api/3/group", data=data)
    
    def delete_group(
        self, 
        group_name: str,
        swap_group: str = None
    ) -> None:
        """
        Delete a group.
        
        Args:
            group_name: Group name
            swap_group: Group to transfer restrictions to
        """
        params = {
            "groupname": group_name
        }
        
        if swap_group:
            params["swapGroup"] = swap_group
            
        return self.delete("rest/api/3/group", params=params)
    
    def get_group_members(
        self, 
        group_name: str,
        include_inactive_users: bool = False,
        start_at: int = 0, 
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Get group members.
        
        Args:
            group_name: Group name
            include_inactive_users: Whether to include inactive users
            start_at: Index of the first user to return
            max_results: Maximum number of users to return
            
        Returns:
            Dictionary containing group members information
        """
        params = {
            "groupname": group_name,
            "includeInactiveUsers": include_inactive_users,
            "startAt": start_at,
            "maxResults": max_results
        }
            
        return self.get("rest/api/3/group/member", params=params)
    
    def add_user_to_group(
        self, 
        group_name: str,
        account_id: str
    ) -> Dict[str, Any]:
        """
        Add user to group.
        
        Args:
            group_name: Group name
            account_id: User account ID
            
        Returns:
            Dictionary containing added user information
        """
        data = {
            "accountId": account_id
        }
            
        return self.post(f"rest/api/3/group/user", params={"groupname": group_name}, data=data)
    
    def remove_user_from_group(
        self, 
        group_name: str,
        account_id: str
    ) -> None:
        """
        Remove user from group.
        
        Args:
            group_name: Group name
            account_id: User account ID
        """
        params = {
            "groupname": group_name,
            "accountId": account_id
        }
            
        return self.delete("rest/api/3/group/user", params=params)
    
    # User bulk operations
    
    def bulk_get_users(
        self, 
        account_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Bulk get users.
        
        Args:
            account_ids: List of user account IDs
            
        Returns:
            List of dictionaries containing user information
        """
        params = {
            "accountId": account_ids
        }
            
        return self.get("rest/api/3/user/bulk", params=params)
    
    def bulk_get_user_properties(
        self, 
        account_ids: List[str],
        property_keys: List[str] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Bulk get user properties.
        
        Args:
            account_ids: List of user account IDs
            property_keys: List of property keys
            
        Returns:
            Dictionary mapping account IDs to user properties
        """
        params = {
            "accountId": account_ids
        }
        
        if property_keys:
            params["propertyKey"] = property_keys
            
        return self.get("rest/api/3/user/properties", params=params)
    
    # User column operations
    
    def get_user_default_columns(
        self, 
        account_id: str = None,
        username: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get user default columns.
        
        Args:
            account_id: User account ID
            username: Username (deprecated)
            
        Returns:
            List of dictionaries containing column information
        """
        params = {}
        
        if account_id:
            params["accountId"] = account_id
            
        if username:
            params["username"] = username
            
        return self.get("rest/api/3/user/columns", params=params)
    
    def set_user_default_columns(
        self, 
        columns: List[str],
        account_id: str = None,
        username: str = None
    ) -> None:
        """
        Set user default columns.
        
        Args:
            columns: List of column ids
            account_id: User account ID
            username: Username (deprecated)
        """
        params = {}
        
        if account_id:
            params["accountId"] = account_id
            
        if username:
            params["username"] = username
            
        return self.put("rest/api/3/user/columns", params=params, data=columns)
    
    def reset_user_default_columns(
        self, 
        account_id: str = None,
        username: str = None
    ) -> None:
        """
        Reset user default columns to the system default.
        
        Args:
            account_id: User account ID
            username: Username (deprecated)
        """
        params = {}
        
        if account_id:
            params["accountId"] = account_id
            
        if username:
            params["username"] = username
            
        return self.delete("rest/api/3/user/columns", params=params) 