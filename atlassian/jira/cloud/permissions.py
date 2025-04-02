"""
Jira Cloud API implementation for permissions and security schemes in Jira API v3
"""

import logging
from typing import Any, Dict, List, Optional, Union

from atlassian.jira.cloud.cloud import Jira as CloudJira

log = logging.getLogger(__name__)


class PermissionsJira(CloudJira):
    """
    Jira Cloud API implementation with permissions and security features
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Permissions Jira Cloud instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the CloudJira constructor
        """
        super(PermissionsJira, self).__init__(url, username, password, **kwargs)
        
    # Permission schemes
    
    def get_all_permission_schemes(
        self, 
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get all permission schemes.
        
        Args:
            expand: Expand properties
            
        Returns:
            Dictionary containing permission schemes
        """
        params = {}
        if expand:
            params["expand"] = expand
            
        return self.get("rest/api/3/permissionscheme", params=params)
    
    def get_permission_scheme(
        self, 
        scheme_id: int, 
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get a permission scheme.
        
        Args:
            scheme_id: Permission scheme ID
            expand: Expand properties
            
        Returns:
            Dictionary containing permission scheme details
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        params = {}
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/api/3/permissionscheme/{scheme_id}", params=params)
    
    def create_permission_scheme(
        self, 
        name: str, 
        description: str = None
    ) -> Dict[str, Any]:
        """
        Create a permission scheme.
        
        Args:
            name: Scheme name
            description: Scheme description
            
        Returns:
            Dictionary containing created permission scheme details
        """
        data = {
            "name": name
        }
        
        if description:
            data["description"] = description
            
        return self.post("rest/api/3/permissionscheme", data=data)
    
    def delete_permission_scheme(
        self, 
        scheme_id: int
    ) -> None:
        """
        Delete a permission scheme.
        
        Args:
            scheme_id: Permission scheme ID
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        return self.delete(f"rest/api/3/permissionscheme/{scheme_id}")
    
    def get_permission_scheme_grants(
        self, 
        scheme_id: int, 
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get all permission grants for a scheme.
        
        Args:
            scheme_id: Permission scheme ID
            expand: Expand properties
            
        Returns:
            Dictionary containing permission grants
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        params = {}
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/api/3/permissionscheme/{scheme_id}/permission", params=params)
    
    def create_permission_grant(
        self, 
        scheme_id: int, 
        permission: str, 
        holder_type: str, 
        holder_parameter: str = None
    ) -> Dict[str, Any]:
        """
        Create a permission grant in a permission scheme.
        
        Args:
            scheme_id: Permission scheme ID
            permission: Permission key (e.g., "ADMINISTER", "CREATE_ISSUE")
            holder_type: Type of permission holder (e.g., "user", "group", "role")
            holder_parameter: Identifier for the permission holder (e.g., username, group name, role ID)
            
        Returns:
            Dictionary containing created permission grant
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        
        data = {
            "permission": permission,
            "holder": {
                "type": holder_type
            }
        }
        
        if holder_parameter:
            data["holder"]["parameter"] = holder_parameter
            
        return self.post(f"rest/api/3/permissionscheme/{scheme_id}/permission", data=data)
    
    def delete_permission_grant(
        self, 
        scheme_id: int, 
        permission_id: int
    ) -> None:
        """
        Delete a permission grant from a permission scheme.
        
        Args:
            scheme_id: Permission scheme ID
            permission_id: Permission grant ID
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        permission_id = self.validate_id_or_key(str(permission_id), "permission_id")
        
        return self.delete(f"rest/api/3/permissionscheme/{scheme_id}/permission/{permission_id}")
    
    # Security schemes
    
    def get_issue_security_schemes(self) -> Dict[str, Any]:
        """
        Get all issue security schemes.
        
        Returns:
            Dictionary containing issue security schemes
        """
        return self.get("rest/api/3/issuesecurityschemes")
    
    def get_issue_security_scheme(
        self, 
        scheme_id: int
    ) -> Dict[str, Any]:
        """
        Get an issue security scheme.
        
        Args:
            scheme_id: Issue security scheme ID
            
        Returns:
            Dictionary containing issue security scheme details
        """
        scheme_id = self.validate_id_or_key(str(scheme_id), "scheme_id")
        return self.get(f"rest/api/3/issuesecurityschemes/{scheme_id}")
    
    # Project security levels
    
    def get_project_security_levels(
        self, 
        project_key_or_id: str
    ) -> Dict[str, Any]:
        """
        Get security levels for a project.
        
        Args:
            project_key_or_id: Project key or ID
            
        Returns:
            Dictionary containing project security levels
        """
        project_key_or_id = self.validate_id_or_key(project_key_or_id, "project_key_or_id")
        return self.get(f"rest/api/3/project/{project_key_or_id}/securitylevel")
    
    # My permissions
    
    def get_my_permissions(
        self, 
        project_key: str = None, 
        issue_key: str = None, 
        permissions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get permissions for the current user.
        
        Args:
            project_key: Project key to check permissions in
            issue_key: Issue key to check permissions for
            permissions: List of permission keys to check
            
        Returns:
            Dictionary containing permissions information
        """
        params = {}
        
        if project_key:
            params["projectKey"] = project_key
            
        if issue_key:
            params["issueKey"] = issue_key
            
        if permissions:
            params["permissions"] = ",".join(permissions)
            
        return self.get("rest/api/3/mypermissions", params=params)
    
    # User permissions
    
    def get_permitted_projects(
        self, 
        permission_key: str
    ) -> Dict[str, Any]:
        """
        Get projects where the user has the specified permission.
        
        Args:
            permission_key: Permission key (e.g., "BROWSE")
            
        Returns:
            Dictionary containing projects information
        """
        data = {
            "permissions": [permission_key]
        }
        
        return self.post("rest/api/3/permissions/project", data=data)
    
    def get_bulk_permissions(
        self, 
        project_ids: List[int] = None,
        project_keys: List[str] = None,
        issue_ids: List[int] = None,
        issue_keys: List[str] = None,
        permissions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get permissions for the current user for multiple projects or issues.
        
        Args:
            project_ids: List of project IDs
            project_keys: List of project keys
            issue_ids: List of issue IDs
            issue_keys: List of issue keys
            permissions: List of permission keys to check
            
        Returns:
            Dictionary containing permissions information
        """
        data = {}
        
        if project_ids:
            data["projectIds"] = project_ids
            
        if project_keys:
            data["projectKeys"] = project_keys
            
        if issue_ids:
            data["issueIds"] = issue_ids
            
        if issue_keys:
            data["issueKeys"] = issue_keys
            
        if permissions:
            data["permissions"] = permissions
            
        return self.post("rest/api/3/permissions/check", data=data) 