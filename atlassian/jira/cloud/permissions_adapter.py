"""
Jira Cloud API Adapter for permissions and security schemes
This module provides adapters to maintain backward compatibility with existing code
"""

import logging
import warnings
from typing import Any, Dict, List, Optional, Union

from atlassian.jira.cloud.permissions import PermissionsJira

log = logging.getLogger(__name__)


class PermissionsJiraAdapter(PermissionsJira):
    """
    Adapter class for Jira Permissions API to maintain backward compatibility with the original Jira client.
    This class wraps the new PermissionsJira implementation and provides methods with the same names and signatures
    as in the original client.
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Permissions Jira Adapter instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the PermissionsJira constructor
        """
        super(PermissionsJiraAdapter, self).__init__(url, username, password, **kwargs)
        
        # Dictionary mapping legacy method names to new method names
        self._legacy_method_map = {
            "get_permissions_schemes": "get_all_permission_schemes",
            "get_permissions_scheme": "get_permission_scheme",
            "create_permissions_scheme": "create_permission_scheme",
            "delete_permissions_scheme": "delete_permission_scheme",
            
            "get_permissions": "get_my_permissions",
            "get_project_permissions": "get_permitted_projects",
        }
    
    # Permission schemes - legacy methods
    
    def get_permissions_schemes(self, expand: str = None) -> Dict[str, Any]:
        """
        Get all permission schemes. (Legacy method)
        
        Args:
            expand: Expand properties
            
        Returns:
            Dictionary containing permission schemes
        """
        warnings.warn(
            "The 'get_permissions_schemes' method is deprecated. Use 'get_all_permission_schemes' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_all_permission_schemes(expand=expand)
    
    def get_permissions_scheme(self, scheme_id: int, expand: str = None) -> Dict[str, Any]:
        """
        Get a permission scheme. (Legacy method)
        
        Args:
            scheme_id: Permission scheme ID
            expand: Expand properties
            
        Returns:
            Dictionary containing permission scheme details
        """
        warnings.warn(
            "The 'get_permissions_scheme' method is deprecated. Use 'get_permission_scheme' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_permission_scheme(scheme_id=scheme_id, expand=expand)
    
    def create_permissions_scheme(self, name: str, description: str = None) -> Dict[str, Any]:
        """
        Create a permission scheme. (Legacy method)
        
        Args:
            name: Scheme name
            description: Scheme description
            
        Returns:
            Dictionary containing created permission scheme details
        """
        warnings.warn(
            "The 'create_permissions_scheme' method is deprecated. Use 'create_permission_scheme' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.create_permission_scheme(name=name, description=description)
    
    def delete_permissions_scheme(self, scheme_id: int) -> None:
        """
        Delete a permission scheme. (Legacy method)
        
        Args:
            scheme_id: Permission scheme ID
        """
        warnings.warn(
            "The 'delete_permissions_scheme' method is deprecated. Use 'delete_permission_scheme' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.delete_permission_scheme(scheme_id=scheme_id)
    
    # User permissions - legacy methods
    
    def get_permissions(
        self, 
        project_key: str = None, 
        issue_key: str = None, 
        permissions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get permissions for the current user. (Legacy method)
        
        Args:
            project_key: Project key to check permissions in
            issue_key: Issue key to check permissions for
            permissions: List of permission keys to check
            
        Returns:
            Dictionary containing permissions information
        """
        warnings.warn(
            "The 'get_permissions' method is deprecated. Use 'get_my_permissions' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_my_permissions(
            project_key=project_key,
            issue_key=issue_key,
            permissions=permissions
        )
    
    def get_project_permissions(self, permission_key: str) -> Dict[str, Any]:
        """
        Get projects where the user has the specified permission. (Legacy method)
        
        Args:
            permission_key: Permission key (e.g., "BROWSE")
            
        Returns:
            Dictionary containing projects information
        """
        warnings.warn(
            "The 'get_project_permissions' method is deprecated. Use 'get_permitted_projects' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_permitted_projects(permission_key=permission_key) 