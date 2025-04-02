"""
Confluence base module for shared functionality between API versions
"""
import logging
from typing import Dict, List, Optional, Union, Any, Tuple
from urllib.parse import urlparse

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
        
        # Whiteboard endpoints
        'whiteboard': 'api/v2/whiteboards',
        'whiteboard_by_id': 'api/v2/whiteboards/{id}',
        'whiteboard_children': 'api/v2/whiteboards/{id}/children',
        'whiteboard_ancestors': 'api/v2/whiteboards/{id}/ancestors',
        
        # Custom content endpoints
        'custom_content': 'api/v2/custom-content',
        'custom_content_by_id': 'api/v2/custom-content/{id}',
        'custom_content_children': 'api/v2/custom-content/{id}/children',
        'custom_content_ancestors': 'api/v2/custom-content/{id}/ancestors',
        'custom_content_labels': 'api/v2/custom-content/{id}/labels',
        'custom_content_properties': 'api/v2/custom-content/{id}/properties',
        'custom_content_property_by_key': 'api/v2/custom-content/{id}/properties/{key}',
        
        # More v2 endpoints will be added in Phase 2 and 3
    }


class ConfluenceBase(AtlassianRestAPI):
    """Base class for Confluence operations with version support"""

    @staticmethod
    def _is_cloud_url(url: str) -> bool:
        """
        Securely validate if a URL is a Confluence Cloud URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if the URL is a valid Confluence Cloud URL, False otherwise
            
        Security:
            This method implements strict URL validation:
            - Only allows http:// and https:// schemes
            - Properly validates domain names using full hostname matching
            - Prevents common URL parsing attacks
        """
        try:
            parsed = urlparse(url)
            
            # Validate scheme
            if parsed.scheme not in ('http', 'https'):
                return False
                
            # Ensure we have a valid hostname
            if not parsed.hostname:
                return False
                
            # Convert to lowercase for comparison
            hostname = parsed.hostname.lower()
            
            # Split hostname into parts and validate
            parts = hostname.split('.')
            
            # Must have at least 3 parts (e.g., site.atlassian.net)
            if len(parts) < 3:
                return False
                
            # Check exact matches for allowed domains
            # This prevents attacks like: evil.com?atlassian.net
            # or malicious-atlassian.net.evil.com
            if hostname.endswith('.atlassian.net'):
                return hostname == f"{parts[-3]}.atlassian.net"
            elif hostname.endswith('.jira.com'):
                return hostname == f"{parts[-3]}.jira.com"
                
            return False
            
        except Exception:
            # Any parsing error means invalid URL
            return False

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
        if self._is_cloud_url(url) and "/wiki" not in url:
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
                # Check if the response has a base URL provided (common in Confluence v2 API)
                base_url = response.get("_links", {}).get("base")
                if base_url and next_url.startswith('/'):
                    # Construct the full URL using the base URL from the response
                    url = f"{base_url}{next_url}"
                    absolute = True
                else:
                    url = next_url
                    # Check if the URL is absolute (has http:// or https://) or contains the server's domain
                    if next_url.startswith(('http://', 'https://')) or self.url.split('/')[2] in next_url:
                        absolute = True
                    else:
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