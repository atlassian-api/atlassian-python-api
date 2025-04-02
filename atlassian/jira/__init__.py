"""
Jira module for Jira API v2 and v3.
This module supports versioning.
"""

from typing import Optional, Union

from atlassian.jira.base import JiraBase
from atlassian.jira.cloud import CloudJira, JiraAdapter
from atlassian.jira.cloud.permissions import PermissionsJira
from atlassian.jira.cloud.permissions_adapter import PermissionsJiraAdapter
from atlassian.jira.cloud.software import SoftwareJira
from atlassian.jira.cloud.software_adapter import SoftwareJiraAdapter
from atlassian.jira.errors import (
    JiraApiError,
    JiraAuthenticationError,
    JiraConflictError,
    JiraNotFoundError,
    JiraPermissionError, 
    JiraRateLimitError,
    JiraServerError,
    JiraValueError
)
from atlassian.jira.server import ServerJira

# For backward compatibility
Jira = JiraAdapter

__all__ = [
    "Jira",
    "CloudJira",
    "ServerJira",
    "JiraBase",
    "get_jira_instance",
    "get_software_jira_instance",
    "get_permissions_jira_instance",
    "JiraApiError",
    "JiraAuthenticationError",
    "JiraConflictError",
    "JiraNotFoundError",
    "JiraPermissionError",
    "JiraRateLimitError",
    "JiraServerError",
    "JiraValueError"
]


def get_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    cloud: Optional[bool] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[JiraAdapter, CloudJira, ServerJira]:
    """
    Get a Jira instance based on the provided parameters.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        cloud: Force cloud or server instance, if not provided, will be determined from the URL
        legacy_mode: If True, return a JiraAdapter instance, otherwise return a direct CloudJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 2

    # Auto-detect cloud, if not specified
    if cloud is None:
        cloud = ".atlassian.net" in url

    if cloud:
        # Return a cloud instance
        kwargs.setdefault("api_version", api_version)
        
        if legacy_mode:
            # Wrap in adapter for backward compatibility
            return JiraAdapter(url, username, password, **kwargs)
        else:
            # Return direct cloud instance
            return CloudJira(url, username, password, **kwargs)
    else:
        # Return a server instance
        return ServerJira(url, username, password, **kwargs)


def get_software_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[SoftwareJiraAdapter, SoftwareJira]:
    """
    Get a Jira Software instance with specialized Jira Software features like boards, sprints, and backlog.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        legacy_mode: If True, return a SoftwareJiraAdapter instance, otherwise return a direct SoftwareJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira Software instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 3

    kwargs.setdefault("api_version", api_version)
    
    if legacy_mode:
        # Wrap in adapter for backward compatibility
        return SoftwareJiraAdapter(url, username, password, **kwargs)
    else:
        # Return direct software instance
        return SoftwareJira(url, username, password, **kwargs)


def get_permissions_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[PermissionsJiraAdapter, PermissionsJira]:
    """
    Get a Jira Permissions instance with specialized permissions and security features.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        legacy_mode: If True, return a PermissionsJiraAdapter instance, otherwise return a direct PermissionsJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira Permissions instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 3

    kwargs.setdefault("api_version", api_version)
    
    if legacy_mode:
        # Wrap in adapter for backward compatibility
        return PermissionsJiraAdapter(url, username, password, **kwargs)
    else:
        # Return direct permissions instance
        return PermissionsJira(url, username, password, **kwargs) 