"""
Jira module for Jira API v2 and v3.
This module supports versioning.
"""

from typing import Optional, Union

from atlassian.jira.base import JiraBase
from atlassian.jira.cloud.cloud_base import CloudJira
from atlassian.jira.cloud.adapter import JiraAdapter
from atlassian.jira.cloud.cloud import Jira
from atlassian.jira.cloud.endpoints import JiraEndpoints
from atlassian.jira.cloud.issues import IssuesJira
from atlassian.jira.cloud.issues_adapter import IssuesJiraAdapter
from atlassian.jira.cloud.permissions import PermissionsJira
from atlassian.jira.cloud.permissions_adapter import PermissionsJiraAdapter
from atlassian.jira.cloud.software import SoftwareJira
from atlassian.jira.cloud.software_adapter import SoftwareJiraAdapter
from atlassian.jira.cloud.users import UsersJira
from atlassian.jira.cloud.users_adapter import UsersJiraAdapter
from atlassian.jira.cloud.richtext import RichTextJira
from atlassian.jira.cloud.richtext_adapter import RichTextJiraAdapter
from atlassian.jira.cloud.jira_versions import JiraVersions
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
from atlassian.jira.cloud.issuetypes import IssueTypesJira
from atlassian.jira.cloud.issuetypes_adapter import IssueTypesJiraAdapter

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
    "get_users_jira_instance",
    "get_issues_jira_instance",
    "get_richtext_jira_instance",
    "get_issuetypes_jira_instance",
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
) -> Union[JiraAdapter, Jira, ServerJira]:
    """
    Get a Jira instance based on the provided parameters.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        cloud: Force cloud or server instance, if not provided, will be determined from the URL
        legacy_mode: If True, return a JiraAdapter instance, otherwise return a direct Jira instance
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
            return Jira(url, username, password, **kwargs)
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


def get_users_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[UsersJiraAdapter, UsersJira]:
    """
    Get a Jira Users instance with specialized user and group management features.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        legacy_mode: If True, return a UsersJiraAdapter instance, otherwise return a direct UsersJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira Users instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 3

    kwargs.setdefault("api_version", api_version)
    
    if legacy_mode:
        # Wrap in adapter for backward compatibility
        return UsersJiraAdapter(url, username, password, **kwargs)
    else:
        # Return direct users instance
        return UsersJira(url, username, password, **kwargs)


def get_issues_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[IssuesJiraAdapter, IssuesJira]:
    """
    Get a Jira Issues instance with specialized issue management features.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        legacy_mode: If True, return a IssuesJiraAdapter instance, otherwise return a direct IssuesJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira Issues instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 3

    kwargs.setdefault("api_version", api_version)
    
    if legacy_mode:
        # Wrap in adapter for backward compatibility
        return IssuesJiraAdapter(url, username, password, **kwargs)
    else:
        # Return direct issues instance
        return IssuesJira(url, username, password, **kwargs)


def get_richtext_jira_instance(url="", username="", password="", api_version=None, legacy_mode=False, **kwargs):
    """
    Creates a Jira Rich Text instance with specialized rich text Atlassian Document Format (ADF) features.

    :param url: URL to Jira instance
    :param username: Username for authentication
    :param password: Password (or access token) for authentication
    :param api_version: API version, '3' recommended for rich text features
    :param legacy_mode: Whether to use legacy mode, which activates the adapter class
                        for backward compatibility
    :param kwargs: Additional arguments to be passed to the Jira instance

    :return: RichTextJiraAdapter in legacy mode, RichTextJira instance in direct mode
    :rtype: Union[RichTextJiraAdapter, RichTextJira]
    """
    api_version = api_version or JiraVersions.JIRA_CLOUD_API_V3
    
    if legacy_mode:
        return RichTextJiraAdapter(url=url, username=username, password=password, api_version=api_version, **kwargs)
    else:
        return RichTextJira(url=url, username=username, password=password, api_version=api_version, **kwargs)


def get_issuetypes_jira_instance(
    url: str,
    username: str = None,
    password: str = None,
    api_version: Optional[int] = None,
    legacy_mode: bool = True,
    **kwargs,
) -> Union[IssueTypesJiraAdapter, IssueTypesJira]:
    """
    Get a Jira Issue Types instance with specialized issue type and field configuration features.

    Args:
        url: Jira URL
        username: Username for authentication
        password: Password or API token for authentication
        api_version: API version to use (2 or 3)
        legacy_mode: If True, return a IssueTypesJiraAdapter instance, otherwise return a direct IssueTypesJira instance
        **kwargs: Additional arguments to pass to the Jira constructor

    Returns:
        Jira Issue Types instance of the appropriate type
    """
    if api_version is None:
        api_version = kwargs.pop("version", None) or 3

    kwargs.setdefault("api_version", api_version)
    
    if legacy_mode:
        # Wrap in adapter for backward compatibility
        return IssueTypesJiraAdapter(url, username, password, **kwargs)
    else:
        # Return direct issue types instance
        return IssueTypesJira(url, username, password, **kwargs) 