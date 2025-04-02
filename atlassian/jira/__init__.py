"""
Jira module for Jira API v2 and v3.
This module supports versioning.
"""

from typing import Union

from atlassian.jira.base import JiraBase
from atlassian.jira.cloud import CloudJira, JiraAdapter
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
    api_version: int = 3,
    cloud: bool = None,
    legacy_mode: bool = True,
    **kwargs
) -> Union[JiraAdapter, CloudJira, ServerJira]:
    """
    Factory function to create a Jira instance based on URL or explicit cloud parameter.
    
    Args:
        url: Jira instance URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        cloud: Explicitly set whether this is a cloud instance (True) or server instance (False)
        legacy_mode: Whether to return a JiraAdapter instance for backward compatibility
        **kwargs: Additional keyword arguments for the Jira client
        
    Returns:
        Jira instance configured for the right environment
    """
    # Determine if this is a cloud instance
    is_cloud = cloud if cloud is not None else JiraBase._is_cloud_url(url)
    
    # Create the appropriate instance
    if is_cloud:
        instance = CloudJira(url, username, password, api_version=api_version, **kwargs)
        if legacy_mode:
            # Wrap in adapter for backward compatibility
            return JiraAdapter(url, username, password, api_version=api_version, **kwargs)
        return instance
    else:
        # Fall back to server instance
        return ServerJira(url, username, password, api_version=api_version, **kwargs) 