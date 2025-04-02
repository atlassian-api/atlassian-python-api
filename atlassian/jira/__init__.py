"""
Jira API module with version support
"""

from typing import Any, Optional, Union

from atlassian.jira.base import JiraBase
from atlassian.jira.cloud import Jira as CloudJira

# For backwards compatibility
from atlassian.jira.cloud.cloud import Jira

# Export everything from the v2/v3 API
__all__ = ["Jira", "JiraBase", "get_jira_instance"]


def get_jira_instance(
    url: str = None,
    username: str = None,
    password: str = None,
    api_version: Union[str, int] = 2,
    cloud: Optional[bool] = None,
    **kwargs: Any
) -> Jira:
    """
    Factory function to create a Jira instance based on the arguments.
    This is a convenience function for backwards compatibility.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version (2 or 3)
        cloud: Force cloud instance if True, server if False, auto-detect if None
        kwargs: Additional arguments to pass to the constructor

    Returns:
        A Jira instance
    """
    return JiraBase.factory(
        url=url,
        username=username,
        password=password,
        api_version=api_version,
        cloud=cloud,
        **kwargs
    ) 