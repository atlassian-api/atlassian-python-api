"""
Confluence base module for shared functionality between API versions
"""
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

from atlassian.rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class ConfluenceEndpoints:
    """
    Class to define endpoint mappings for different Confluence API versions.
    These endpoints can be accessed through the ConfluenceBase get_endpoint method.
    """
    V1 = {
        "page": "rest/api/content",
        "page_by_id": "rest/api/content/{id}",
        "child_pages": "rest/api/content/{id}/child/page",
        "content_search": "rest/api/content/search",
        "space": "rest/api/space",
        "space_by_key": "rest/api/space/{key}",
    }

    V2 = {
        'page_by_id': 'api/v2/pages/{id}',
        'page': 'api/v2/pages',
        'child_pages': 'api/v2/pages/{id}/children/page',
        'search': 'api/v2/search',
        'spaces': 'api/v2/spaces',
        'space_by_id': 'api/v2/spaces/{id}',
        'page_properties': 'api/v2/pages/{id}/properties',
        'page_property_by_key': 'api/v2/pages/{id}/properties/{key}',
        'page_labels': 'api/v2/pages/{id}/labels',
        'space_labels': 'api/v2/spaces/{id}/labels',
        
        # Comment endpoints for V2 API
        'page_footer_comments': 'api/v2/pages/{id}/footer-comments',
        'page_inline_comments': 'api/v2/pages/{id}/inline-comments',
        'blogpost_footer_comments': 'api/v2/blogposts/{id}/footer-comments',
        'blogpost_inline_comments': 'api/v2/blogposts/{id}/inline-comments',
        'attachment_comments': 'api/v2/attachments/{id}/footer-comments',
        'custom_content_comments': 'api/v2/custom-content/{id}/footer-comments',
        'comment': 'api/v2/comments',
        'comment_by_id': 'api/v2/comments/{id}',
        'comment_children': 'api/v2/comments/{id}/children',
        
        # More v2 endpoints will be added in Phase 2 and 3
    }


class ConfluenceBase(AtlassianRestAPI):
    """Base class for Confluence operations with version support"""

    def __init__(
        self,
        url: str,
        *args,
        api_version: Union[str, int] = 1,
        **kwargs
    ):
        """
        Initialize the Confluence Base instance with version support.

        Args:
            url: The Confluence instance URL
            api_version: API version, 1 or 2, defaults to 1
            args: Arguments to pass to AtlassianRestAPI constructor
            kwargs: Keyword arguments to pass to AtlassianRestAPI constructor
        """
        if ("atlassian.net" in url or "jira.com" in url) and ("/wiki" not in url):
            url = AtlassianRestAPI.url_joiner(url, "/wiki")
            if "cloud" not in kwargs:
                kwargs["cloud"] = True

        super(ConfluenceBase, self).__init__(url, *args, **kwargs)
        self.api_version = int(api_version)
        if self.api_version not in [1, 2]:
            raise ValueError("API version must be 1 or 2")

    def get_endpoint(self, endpoint_key: str, **kwargs) -> str:
        """
        Get the appropriate endpoint based on the API version.

        Args:
            endpoint_key: The key for the endpoint in the endpoints dictionary
            kwargs: Format parameters for the endpoint

        Returns:
            The formatted endpoint URL
        """
        endpoints = ConfluenceEndpoints.V1 if self.api_version == 1 else ConfluenceEndpoints.V2
        
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
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        flags: Optional[List] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
    ):
        """
        Get paged results with version-appropriate pagination.

        Args:
            url: The URL to retrieve
            params: The query parameters
            data: The request data
            flags: Additional flags
            trailing: If True, a trailing slash is added to the URL
            absolute: If True, the URL is used absolute and not relative to the root

        Yields:
            The result elements
        """
        if params is None:
            params = {}

        if self.api_version == 1:
            # V1 API pagination (offset-based)
            while True:
                response = self.get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )
                if "results" not in response:
                    return

                for value in response.get("results", []):
                    yield value

                # According to Cloud and Server documentation the links are returned the same way:
                # https://developer.atlassian.com/cloud/confluence/rest/api-group-content/#api-wiki-rest-api-content-get
                # https://developer.atlassian.com/server/confluence/pagination-in-the-rest-api/
                url = response.get("_links", {}).get("next")
                if url is None:
                    break
                # From now on we have relative URLs with parameters
                absolute = False
                # Params are now provided by the url
                params = {}
                # Trailing should not be added as it is already part of the url
                trailing = False
                
        else:
            # V2 API pagination (cursor-based)
            while True:
                response = self.get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )
                
                if "results" not in response:
                    return

                for value in response.get("results", []):
                    yield value
                
                # Check for next cursor in _links or in response headers
                next_url = response.get("_links", {}).get("next")
                
                if not next_url:
                    # Check for Link header
                    if hasattr(self, "response") and self.response and "Link" in self.response.headers:
                        link_header = self.response.headers["Link"]
                        if 'rel="next"' in link_header:
                            import re
                            match = re.search(r'<([^>]*)>;', link_header)
                            if match:
                                next_url = match.group(1)
                
                if not next_url:
                    break
                
                # Use the next URL directly
                url = next_url
                absolute = False
                params = {}
                trailing = False

        return 

    @staticmethod
    def factory(url: str, api_version: int = 1, *args, **kwargs) -> 'ConfluenceBase':
        """
        Factory method to create a Confluence client with the specified API version
        
        Args:
            url: Confluence Cloud base URL
            api_version: API version to use (1 or 2)
            *args: Variable length argument list
            **kwargs: Keyword arguments
            
        Returns:
            Configured Confluence client for the specified API version
            
        Raises:
            ValueError: If api_version is not 1 or 2
        """
        if api_version == 1:
            from .confluence import Confluence
            return Confluence(url, *args, **kwargs)
        elif api_version == 2:
            from .confluence_v2 import ConfluenceV2
            return ConfluenceV2(url, *args, **kwargs)
        else:
            raise ValueError(f"Unsupported API version: {api_version}. Use 1 or 2.") 