"""
Jira base module for shared functionality between API versions
"""

import logging
import os
import platform
import signal
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

from atlassian.rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class JiraEndpoints:
    """
    Class to define endpoint mappings for different Jira API versions.
    These endpoints can be accessed through the JiraBase get_endpoint method.
    """

    V2 = {
        # Core API endpoints
        "issue": "rest/api/2/issue",
        "issue_by_id": "rest/api/2/issue/{id}",
        "issue_createmeta": "rest/api/2/issue/createmeta",
        "issue_changelog": "rest/api/2/issue/{id}/changelog",
        "issue_watchers": "rest/api/2/issue/{id}/watchers",
        "issue_comment": "rest/api/2/issue/{id}/comment",
        "issue_comment_by_id": "rest/api/2/issue/{id}/comment/{comment_id}",
        "issue_worklog": "rest/api/2/issue/{id}/worklog",
        "issue_worklog_by_id": "rest/api/2/issue/{id}/worklog/{worklog_id}",
        "search": "rest/api/2/search",
        "project": "rest/api/2/project",
        "project_by_id": "rest/api/2/project/{id}",
        "user": "rest/api/2/user",
        "user_search": "rest/api/2/user/search",
        # Additional endpoints will be added during Phase 2
    }

    V3 = {
        # Core API endpoints
        "issue": "rest/api/3/issue",
        "issue_by_id": "rest/api/3/issue/{id}",
        "issue_createmeta": "rest/api/3/issue/createmeta",
        "issue_changelog": "rest/api/3/issue/{id}/changelog",
        "issue_watchers": "rest/api/3/issue/{id}/watchers",
        "issue_comment": "rest/api/3/issue/{id}/comment",
        "issue_comment_by_id": "rest/api/3/issue/{id}/comment/{comment_id}",
        "issue_worklog": "rest/api/3/issue/{id}/worklog",
        "issue_worklog_by_id": "rest/api/3/issue/{id}/worklog/{worklog_id}",
        "search": "rest/api/3/search",
        "project": "rest/api/3/project",
        "project_by_id": "rest/api/3/project/{id}",
        "user": "rest/api/3/user",
        "user_search": "rest/api/3/user/search",
        # Additional endpoints will be added during Phase 2
    }


class JiraBase(AtlassianRestAPI):
    """Base class for Jira operations with version support"""

    @staticmethod
    def _is_cloud_url(url: str) -> bool:
        """
        Securely validate if a URL is a Jira Cloud URL.

        Args:
            url: The URL to validate

        Returns:
            bool: True if the URL is a valid Jira Cloud URL, False otherwise

        Security:
            This method implements strict URL validation:
            - Only allows http:// and https:// schemes
            - Properly validates domain names using full hostname matching
            - Prevents common URL parsing attacks
        """
        try:
            # For Unix/Linux/Mac
            if platform.system() != "Windows" and hasattr(signal, "SIGALRM"):
                # Define a timeout handler
                def timeout_handler(signum, frame):
                    raise TimeoutError("URL validation timed out")

                # Set a timeout of 5 seconds
                original_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(5)

                try:
                    parsed = urlparse(url)

                    # Validate scheme
                    if parsed.scheme not in ("http", "https"):
                        return False

                    # Ensure we have a valid hostname
                    if not parsed.hostname:
                        return False

                    # Convert to lowercase for comparison
                    hostname = parsed.hostname.lower()

                    # Check if the hostname ends with .atlassian.net or .jira.com
                    return hostname.endswith(".atlassian.net") or hostname.endswith(".jira.com")
                finally:
                    # Reset the alarm and restore the original handler
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, original_handler)
            else:
                # For Windows or systems without SIGALRM
                parsed = urlparse(url)

                # Validate scheme
                if parsed.scheme not in ("http", "https"):
                    return False

                # Ensure we have a valid hostname
                if not parsed.hostname:
                    return False

                # Convert to lowercase for comparison
                hostname = parsed.hostname.lower()

                # Simple check for valid cloud URLs
                return hostname.endswith(".atlassian.net") or hostname.endswith(".jira.com")

        except Exception:
            # Any parsing error means invalid URL
            return False

    def __init__(self, url: str, *args, api_version: Union[str, int] = 2, **kwargs):
        """
        Initialize the Jira Base instance with version support.

        Args:
            url: The Jira instance URL
            api_version: API version, 2 or 3, defaults to 2
            args: Arguments to pass to AtlassianRestAPI constructor
            kwargs: Keyword arguments to pass to AtlassianRestAPI constructor
        """
        # Set cloud flag based on URL
        if self._is_cloud_url(url):
            if "cloud" not in kwargs:
                kwargs["cloud"] = True

        super(JiraBase, self).__init__(url, *args, **kwargs)
        self.api_version = int(api_version)
        if self.api_version not in [2, 3]:
            raise ValueError("API version must be 2 or 3")

    def get_endpoint(self, endpoint_key: str, **kwargs) -> str:
        """
        Get the appropriate endpoint based on the API version.

        Args:
            endpoint_key: The key for the endpoint in the endpoints dictionary
            kwargs: Format parameters for the endpoint

        Returns:
            The formatted endpoint URL
        """
        endpoints = JiraEndpoints.V2 if self.api_version == 2 else JiraEndpoints.V3

        if endpoint_key not in endpoints:
            raise ValueError(f"Endpoint key '{endpoint_key}' not found for API version {self.api_version}")

        endpoint = endpoints[endpoint_key]

        # Format the endpoint if kwargs are provided
        if kwargs:
            endpoint = endpoint.format(**kwargs)

        return endpoint

    def _get_paged(
        self,
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        flags: Optional[list] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
    ):
        """
        Used to get the paged data

        :param url: string:                        The url to retrieve
        :param params: dict (default is None):     The parameter's
        :param data: dict (default is None):       The data
        :param flags: string[] (default is None):  The flags
        :param trailing: bool (default is None):   If True, a trailing slash is added to the url
        :param absolute: bool (default is False):  If True, the url is used absolute and not relative to the root

        :return: A generator object for the data elements
        """

        if self.cloud:
            if params is None:
                params = {}

            while True:
                response = super(JiraBase, self).get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )
                
                # Handle differences in pagination format between Cloud API versions
                if isinstance(response, dict):
                    values = response.get("values", [])
                    for value in values:
                        yield value

                    if response.get("isLast", False) or len(values) == 0:
                        break

                    # The nextPage URL might be provided directly or in a different format
                    next_page = response.get("nextPage")
                    if next_page is None:
                        break
                        
                    # From now on we have absolute URLs with parameters
                    url = next_page
                    absolute = True
                    # Params are now provided by the url
                    params = {}
                    # Trailing should not be added as it is already part of the url
                    trailing = False
                else:
                    # Handle case where response is not a dict
                    yield response
                    break
        else:
            # For server implementations, different pagination approach may be needed
            # Will be implemented in Phase 2
            raise ValueError("``_get_paged`` method is not fully implemented for Jira Server yet")

        return

    @staticmethod
    def factory(
        url: str = None, 
        username: str = None, 
        password: str = None, 
        api_version: Union[str, int] = 2, 
        cloud: bool = None, 
        **kwargs
    ):
        """
        Factory method to create appropriate Jira instance.
        
        Args:
            url: Jira URL
            username: Username for authentication
            password: Password or API token for authentication
            api_version: API version (2 or 3)
            cloud: Force cloud instance if True, server if False, auto-detect if None
            kwargs: Additional arguments to pass to the constructor
            
        Returns:
            An instance of the appropriate Jira class
        """
        # Import here to avoid circular imports
        from atlassian.jira.cloud import Jira as CloudJira
        
        # Determine if this is a cloud instance
        is_cloud = cloud
        if is_cloud is None and url:
            is_cloud = JiraBase._is_cloud_url(url)
            
        # Create cloud instance
        if is_cloud:
            return CloudJira(url=url, username=username, password=password, api_version=api_version, **kwargs)
        else:
            # Server instance will be implemented in Phase 2
            # For now, return cloud instance as fallback
            return CloudJira(url=url, username=username, password=password, api_version=api_version, **kwargs) 