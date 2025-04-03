"""
Jira base module for shared functionality between API versions
"""

import logging
import os
import platform
import signal
import sys
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

from requests import Response
from requests.utils import default_user_agent

from atlassian.jira.errors import raise_error_from_response
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
        "projects": "rest/api/3/project",  # Alias for project
        "project_by_id": "rest/api/3/project/{id}",
        "project_by_key": "rest/api/3/project/{key}",  # For accessing project by key instead of ID
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

    def __init__(self, url: str, *args, **kwargs):
        """
        Initialize the Jira base object.

        Args:
            url: Jira URL
            *args: Any arguments to pass to the AtlassianRestAPI constructor
            **kwargs: Any keyword arguments to pass to the AtlassianRestAPI constructor
        """
        self.api_version = kwargs.pop("api_version", 2)

        if "session" in kwargs:
            # session = kwargs["session"]
            pass

        # Auto-detect if this is a cloud install
        if self._is_cloud_url(url):
            if "cloud" not in kwargs:
                kwargs["cloud"] = True

        # Add user agent and version information
        client_info = f"atlassian-python-api/jira-v{self.api_version}"
        python_version = f"Python/{sys.version.split()[0]}"
        os_info = f"{platform.system()}/{platform.release()}"
        user_agent = f"{client_info} ({default_user_agent()}) {python_version} {os_info}"

        # Extract headers before passing to parent constructor
        headers = kwargs.pop("headers", {}) if "headers" in kwargs else {}

        if "User-Agent" not in headers:
            headers["User-Agent"] = user_agent

        # Enable debug logging if requested via environment variable
        self.debug = os.environ.get("JIRA_API_DEBUG", "").lower() in ("1", "true", "yes", "on")
        if self.debug:
            logging.getLogger("atlassian").setLevel(logging.DEBUG)
            logging.getLogger("requests").setLevel(logging.DEBUG)
            logging.getLogger("urllib3").setLevel(logging.DEBUG)

        # Pass on to parent class
        super(JiraBase, self).__init__(url, *args, **kwargs)

        # Set headers after initialization
        if headers:
            for key, value in headers.items():
                self._update_header(key, value)

    def get_endpoint(self, endpoint_key: str, **kwargs) -> str:
        """
        Get API endpoint for the specified key with parameter substitution.

        Args:
            endpoint_key: Key to lookup in the endpoints mapping
            **kwargs: Parameters to substitute in the endpoint URL

        Returns:
            Endpoint URL with parameters substituted

        Raises:
            ValueError: If endpoint_key is not found in the endpoints mapping
        """
        endpoints = JiraEndpoints.V2 if self.api_version == 2 else JiraEndpoints.V3

        if endpoint_key not in endpoints:
            raise ValueError(f"Endpoint key '{endpoint_key}' not found for API version {self.api_version}")

        endpoint = endpoints[endpoint_key]

        # Format the endpoint if kwargs are provided
        if kwargs:
            endpoint = endpoint.format(**kwargs)

        return endpoint

    def raise_for_status(self, response: Response) -> None:
        """
        Override raise_for_status to use specialized Jira error handling.

        Args:
            response: HTTP response object

        Raises:
            JiraApiError: If the response indicates an error
        """
        # Use our specialized error handler
        raise_error_from_response(response)

    def request(self, *args, **kwargs) -> Response:
        """
        Override request method to add additional debug logging

        Args:
            *args: Arguments to pass to parent request method
            **kwargs: Keyword arguments to pass to parent request method

        Returns:
            Response object
        """
        # Call the parent method
        response = super(JiraBase, self).request(*args, **kwargs)

        # Add additional debug logging if enabled
        if self.debug and response:
            method = kwargs.get("method", args[0] if args else "GET")
            path = kwargs.get("path", args[1] if len(args) > 1 else "/")

            log.debug("----- REQUEST -----")
            log.debug(f"REQUEST: {method} {path}")

            if "headers" in kwargs:
                log.debug(f"HEADERS: {kwargs['headers']}")

            if "data" in kwargs and kwargs["data"]:
                log.debug(f"DATA: {kwargs['data']}")

            if "params" in kwargs and kwargs["params"]:
                log.debug(f"PARAMS: {kwargs['params']}")

            log.debug("----- RESPONSE -----")
            log.debug(f"STATUS: {response.status_code} {response.reason}")
            log.debug(f"HEADERS: {response.headers}")

            # For security, don't log the full response body if it's very large
            if len(response.text) < 10000:  # Only log if less than 10KB
                log.debug(f"BODY: {response.text}")
            else:
                log.debug(f"BODY: (truncated, {len(response.text)} bytes)")

            log.debug("-------------------")

        return response

    def validate_params(self, **kwargs) -> Dict[str, Any]:
        """
        Validate and prepare parameters for API calls.

        Args:
            **kwargs: Parameters to validate

        Returns:
            Dict of validated parameters

        Raises:
            ValueError: If a parameter fails validation
        """
        result = {}
        for key, value in kwargs.items():
            if value is not None:  # Skip None values
                # Special handling for certain parameter types
                if key == "expand" and isinstance(value, list):
                    result[key] = ",".join(value)
                elif key in ("fields", "field") and isinstance(value, list):
                    result[key] = ",".join(value)
                else:
                    result[key] = value
        return result

    def validate_jql(self, jql: str) -> str:
        """
        Validate JQL query string

        Args:
            jql: JQL query string

        Returns:
            Validated JQL string

        Raises:
            ValueError: If JQL is empty or invalid
        """
        if not jql or not jql.strip():
            raise ValueError("JQL query cannot be empty")

        # Could add more validation here in the future
        return jql.strip()

    def validate_id_or_key(self, id_or_key: str, param_name: str = "id") -> str:
        """
        Validate an ID or key parameter

        Args:
            id_or_key: ID or key to validate
            param_name: Name of the parameter for error messages

        Returns:
            Validated ID or key

        Raises:
            ValueError: If ID or key is empty
        """
        if not id_or_key or not str(id_or_key).strip():
            raise ValueError(f"{param_name} cannot be empty")

        return str(id_or_key).strip()

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
        api_version: Union[str, int] = 3,
        cloud: bool = None,
        legacy_mode: bool = True,
        **kwargs,
    ):
        """
        Factory method to create a Jira instance based on URL or explicit cloud parameter.

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

        Raises:
            ValueError: If required arguments are missing or invalid
        """
        if not url:
            raise ValueError("URL is required")

        # Import here to avoid circular imports
        from atlassian.jira.cloud import CloudJira, JiraAdapter
        from atlassian.jira.server import ServerJira

        # Validate API version
        api_version = int(api_version)
        if api_version not in [2, 3]:
            raise ValueError(f"API version {api_version} is not supported. Use 2 or 3.")

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
