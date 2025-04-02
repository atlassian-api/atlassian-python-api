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
        "issue_editmeta": "rest/api/2/issue/{id}/editmeta",
        "issue_remotelinks": "rest/api/2/issue/{id}/remotelink",
        "issue_transitions": "rest/api/2/issue/{id}/transitions",
        "issue_watchers": "rest/api/2/issue/{id}/watchers",
        "issue_voters": "rest/api/2/issue/{id}/votes",
        "issue_comment": "rest/api/2/issue/{id}/comment",
        "issue_comment_by_id": "rest/api/2/issue/{id}/comment/{comment_id}",
        "issue_link": "rest/api/2/issueLink",
        "issue_link_types": "rest/api/2/issueLinkType",
        "issue_properties": "rest/api/2/issue/{id}/properties",
        "issue_property": "rest/api/2/issue/{id}/properties/{key}",
        "issue_worklog": "rest/api/2/issue/{id}/worklog",
        "issue_worklog_by_id": "rest/api/2/issue/{id}/worklog/{worklog_id}",
        "issue_attachments": "rest/api/2/issue/{id}/attachments",
        
        # Search API
        "search": "rest/api/2/search",
        
        # Project API
        "project": "rest/api/2/project",
        "project_by_id": "rest/api/2/project/{id}",
        "project_components": "rest/api/2/project/{id}/components",
        "project_versions": "rest/api/2/project/{id}/versions",
        "project_roles": "rest/api/2/project/{id}/role",
        "project_role": "rest/api/2/project/{id}/role/{role_id}",
        "project_properties": "rest/api/2/project/{id}/properties",
        "project_property": "rest/api/2/project/{id}/properties/{key}",
        
        # User API
        "user": "rest/api/2/user",
        "user_search": "rest/api/2/user/search",
        "user_assignable_search": "rest/api/2/user/assignable/search",
        "user_viewissue_search": "rest/api/2/user/viewissue/search",
        "user_avatar": "rest/api/2/user/avatar",
        "user_avatar_temporary": "rest/api/2/user/avatar/temporary",
        "user_properties": "rest/api/2/user/properties",
        "user_property": "rest/api/2/user/properties/{key}",
        "user_current": "rest/api/2/myself",
        
        # Group API
        "group": "rest/api/2/group",
        "group_member": "rest/api/2/group/member",
        
        # Field API
        "field": "rest/api/2/field",
        "field_by_id": "rest/api/2/field/{id}",
        
        # Filter API
        "filter": "rest/api/2/filter",
        "filter_by_id": "rest/api/2/filter/{id}",
        
        # Component API
        "component": "rest/api/2/component",
        "component_by_id": "rest/api/2/component/{id}",
        
        # Workflow API
        "workflow": "rest/api/2/workflow",
        "workflow_scheme": "rest/api/2/workflowscheme",
        
        # Attachment API
        "attachment": "rest/api/2/attachment",
        "attachment_by_id": "rest/api/2/attachment/{id}",
        "attachment_meta": "rest/api/2/attachment/meta",
        
        # Custom field API
        "custom_field_option": "rest/api/2/customFieldOption/{id}",
        
        # Issue type API
        "issue_type": "rest/api/2/issuetype",
        "issue_type_by_id": "rest/api/2/issuetype/{id}",
        
        # Status API
        "status": "rest/api/2/status",
        "status_by_id": "rest/api/2/status/{id}",
        "status_category": "rest/api/2/statuscategory",
        
        # Priority API
        "priority": "rest/api/2/priority",
        "priority_by_id": "rest/api/2/priority/{id}",
        
        # Resolution API
        "resolution": "rest/api/2/resolution",
        "resolution_by_id": "rest/api/2/resolution/{id}",
    }

    V3 = {
        # Core API endpoints
        "issue": "rest/api/3/issue",
        "issue_by_id": "rest/api/3/issue/{id}",
        "issue_createmeta": "rest/api/3/issue/createmeta",
        "issue_changelog": "rest/api/3/issue/{id}/changelog",
        "issue_editmeta": "rest/api/3/issue/{id}/editmeta",
        "issue_remotelinks": "rest/api/3/issue/{id}/remotelink",
        "issue_transitions": "rest/api/3/issue/{id}/transitions",
        "issue_watchers": "rest/api/3/issue/{id}/watchers",
        "issue_voters": "rest/api/3/issue/{id}/votes",
        "issue_comment": "rest/api/3/issue/{id}/comment",
        "issue_comment_by_id": "rest/api/3/issue/{id}/comment/{comment_id}",
        "issue_link": "rest/api/3/issueLink",
        "issue_link_types": "rest/api/3/issueLinkType",
        "issue_properties": "rest/api/3/issue/{id}/properties",
        "issue_property": "rest/api/3/issue/{id}/properties/{key}",
        "issue_worklog": "rest/api/3/issue/{id}/worklog",
        "issue_worklog_by_id": "rest/api/3/issue/{id}/worklog/{worklog_id}",
        "issue_attachments": "rest/api/3/issue/{id}/attachments",
        
        # Search API
        "search": "rest/api/3/search",
        
        # Project API
        "project": "rest/api/3/project",
        "project_by_id": "rest/api/3/project/{id}",
        "project_components": "rest/api/3/project/{id}/components",
        "project_versions": "rest/api/3/project/{id}/versions",
        "project_roles": "rest/api/3/project/{id}/role",
        "project_role": "rest/api/3/project/{id}/role/{role_id}",
        "project_properties": "rest/api/3/project/{id}/properties",
        "project_property": "rest/api/3/project/{id}/properties/{key}",
        
        # User API
        "user": "rest/api/3/user",
        "user_search": "rest/api/3/user/search",
        "user_assignable_search": "rest/api/3/user/assignable/search",
        "user_viewissue_search": "rest/api/3/user/viewissue/search",
        "user_avatar": "rest/api/3/user/avatar",
        "user_avatar_temporary": "rest/api/3/user/avatar/temporary",
        "user_properties": "rest/api/3/user/properties",
        "user_property": "rest/api/3/user/properties/{key}",
        "user_current": "rest/api/3/myself",
        
        # Group API
        "group": "rest/api/3/group",
        "group_member": "rest/api/3/group/member",
        
        # Field API
        "field": "rest/api/3/field",
        "field_by_id": "rest/api/3/field/{id}",
        
        # Filter API
        "filter": "rest/api/3/filter",
        "filter_by_id": "rest/api/3/filter/{id}",
        
        # Component API
        "component": "rest/api/3/component",
        "component_by_id": "rest/api/3/component/{id}",
        
        # Workflow API
        "workflow": "rest/api/3/workflow",
        "workflow_scheme": "rest/api/3/workflowscheme",
        
        # Attachment API
        "attachment": "rest/api/3/attachment",
        "attachment_by_id": "rest/api/3/attachment/{id}",
        "attachment_meta": "rest/api/3/attachment/meta",
        
        # Custom field API
        "custom_field_option": "rest/api/3/customFieldOption/{id}",
        
        # Issue type API
        "issue_type": "rest/api/3/issuetype",
        "issue_type_by_id": "rest/api/3/issuetype/{id}",
        
        # Status API
        "status": "rest/api/3/status",
        "status_by_id": "rest/api/3/status/{id}",
        "status_category": "rest/api/3/statuscategory",
        
        # Priority API
        "priority": "rest/api/3/priority",
        "priority_by_id": "rest/api/3/priority/{id}",
        
        # Resolution API
        "resolution": "rest/api/3/resolution",
        "resolution_by_id": "rest/api/3/resolution/{id}",
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
            # For server implementations, different pagination approach
            if params is None:
                params = {}
                
            start_at = params.get("startAt", 0)
            max_results = params.get("maxResults", 50)
            
            while True:
                response = super(JiraBase, self).get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )
                
                # Handle standard Jira server pagination
                if isinstance(response, dict):
                    # Different endpoints might use different keys for the actual data
                    values = []
                    if "values" in response:
                        values = response.get("values", [])
                    elif "issues" in response:
                        values = response.get("issues", [])
                    elif "comments" in response:
                        values = response.get("comments", [])
                    # Add more cases as needed for different endpoints
                    
                    # If we found values, yield them
                    for value in values:
                        yield value
                        
                    # Check if we need to get the next page
                    total = response.get("total", 0)
                    if total <= 0 or start_at + len(values) >= total or not values:
                        break
                        
                    # Update pagination parameters for the next page
                    start_at += max_results
                    params["startAt"] = start_at
                else:
                    # For non-paginated responses
                    if isinstance(response, list):
                        for item in response:
                            yield item
                    else:
                        yield response
                    break

        return

    @staticmethod
    def factory(
        url: str = None, 
        username: str = None, 
        password: str = None, 
        api_version: Union[str, int] = 2, 
        cloud: bool = None, 
        legacy_mode: bool = True,
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
            legacy_mode: Whether to return a JiraAdapter instance for backward compatibility
            kwargs: Additional arguments to pass to the constructor
            
        Returns:
            An instance of the appropriate Jira class
        """
        # Import here to avoid circular imports
        from atlassian.jira.cloud import Jira as CloudJira, JiraAdapter
        from atlassian.jira.server import Jira as ServerJira
        
        # Determine if this is a cloud instance
        is_cloud = cloud
        if is_cloud is None and url:
            is_cloud = JiraBase._is_cloud_url(url)
            
        # Create appropriate instance
        if is_cloud:
            if legacy_mode:
                return JiraAdapter(
                    url=url, 
                    username=username, 
                    password=password, 
                    api_version=api_version, 
                    **kwargs
                )
            else:
                return CloudJira(
                    url=url, 
                    username=username, 
                    password=password, 
                    api_version=api_version, 
                    **kwargs
                )
        else:
            # For server, always return the Server implementation
            # There's no adapter for server yet since it's still using API v2
            return ServerJira(
                url=url, 
                username=username, 
                password=password, 
                api_version=api_version, 
                **kwargs
            ) 