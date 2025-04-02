"""
Jira module supporting versioning.

This module provides access to the Jira API with support for both v2 and v3 APIs.
"""

from typing import Optional, Union

from atlassian.jira.base import JiraBase
from atlassian.jira.cloud import JiraAdapter, Jira as CloudJira
from atlassian.jira.server import Jira as ServerJira

# For backward compatibility
Jira = JiraAdapter

__all__ = ["Jira", "CloudJira", "ServerJira", "get_jira_instance"]


def get_jira_instance(
    url: str = None,
    username: str = None,
    password: str = None,
    api_version: Union[str, int] = 2,
    cloud: Optional[bool] = None,
    legacy_mode: bool = True,
    **kwargs
) -> Union[JiraAdapter, CloudJira, ServerJira]:
    """
    Factory function to create the appropriate Jira instance.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version (2 or 3)
        cloud: Force cloud instance if True, server if False, auto-detect if None
        legacy_mode: Whether to return a legacy adapter (for backward compatibility)
        kwargs: Additional arguments to pass to the constructor

    Returns:
        An instance of the appropriate Jira class

    Examples:
        # Create a Jira instance with auto-detection of cloud/server
        jira = get_jira_instance(url="https://jira.example.com", username="user", password="pass")

        # Create a Jira Cloud instance with v3 API
        jira = get_jira_instance(
            url="https://example.atlassian.net", 
            username="user@example.com", 
            password="token",
            api_version=3,
            cloud=True
        )

        # Create a Jira Server instance with v2 API
        jira = get_jira_instance(
            url="https://jira.example.com", 
            username="user", 
            password="pass",
            api_version=2,
            cloud=False
        )

        # Create a non-legacy Cloud instance (direct CloudJira)
        jira = get_jira_instance(
            url="https://example.atlassian.net", 
            username="user@example.com", 
            password="token",
            legacy_mode=False
        )
    """
    return JiraBase.factory(
        url=url,
        username=username,
        password=password,
        api_version=api_version,
        cloud=cloud,
        legacy_mode=legacy_mode,
        **kwargs
    ) 