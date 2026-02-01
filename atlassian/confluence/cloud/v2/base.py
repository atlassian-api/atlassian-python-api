# coding=utf-8
"""
Confluence Cloud v2 API base implementation.

This module provides the base class for Confluence Cloud v2 API operations,
including support for ADF content and cursor-based pagination.
"""

import logging
from typing import Dict, Any, Optional, Union, List
from ...base import ConfluenceBase
from ....adf import validate_adf_document, convert_text_to_adf
from ....request_utils import detect_content_format

log = logging.getLogger(__name__)


class ConfluenceCloudV2(ConfluenceBase):
    """
    Confluence Cloud v2 API client.

    Provides access to Confluence Cloud REST API v2 endpoints with support for:

    - **ADF (Atlassian Document Format) content**: Native support for rich content
      creation and manipulation using Confluence's modern content format
    - **Cursor-based pagination**: Efficient handling of large result sets with
      better performance than offset-based pagination
    - **Modern Cloud API features**: Access to latest Confluence Cloud capabilities
      and enhanced API endpoints
    - **Enhanced performance**: Optimized API calls with reduced response times

    This client is designed for use with Confluence Cloud instances and requires
    proper API token authentication. It provides the foundation for v2 API
    operations while maintaining compatibility with the existing library structure.

    .. versionadded:: 4.1.0
       Added Confluence Cloud v2 API support

    .. note::
       This class is typically used internally by the main ConfluenceCloud class
       for dual API support. Direct usage is possible but not recommended for
       most use cases.

    Examples:
        Direct v2 API client usage:

        >>> v2_client = ConfluenceCloudV2(
        ...     url="https://your-domain.atlassian.net",
        ...     token="your-api-token"
        ... )
        >>>
        >>> # Create page with ADF content
        >>> adf_content = {
        ...     "version": 1,
        ...     "type": "doc",
        ...     "content": [
        ...         {
        ...             "type": "paragraph",
        ...             "content": [{"type": "text", "text": "Hello, v2 API!"}]
        ...         }
        ...     ]
        ... }
        >>> page = v2_client.create_page("SPACE123", "My Page", adf_content)

        Recommended usage through main client:

        >>> confluence = ConfluenceCloud(
        ...     url="https://your-domain.atlassian.net",
        ...     token="your-api-token"
        ... )
        >>> confluence.enable_v2_api()
        >>> page = confluence.create_page_with_adf("SPACE123", "My Page", adf_content)

    See Also:
        - :class:`atlassian.confluence.ConfluenceCloud`: Main Confluence Cloud client
        - :doc:`confluence_adf`: Complete ADF documentation
    """

    def __init__(self, url: str, *args, **kwargs):
        """
        Initialize Confluence Cloud v2 API client.

        :param url: Confluence Cloud base URL
        :param args: Additional arguments for AtlassianRestAPI
        :param kwargs: Additional keyword arguments for AtlassianRestAPI
        """
        # Force cloud mode and set v2 API defaults
        kwargs["cloud"] = True
        kwargs["api_root"] = kwargs.get("api_root", "wiki/api/v2")
        kwargs["api_version"] = kwargs.get("api_version", "")  # v2 doesn't use version in path

        super().__init__(url, *args, **kwargs)

        # v2 API specific headers
        self.v2_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _prepare_content_for_v2(
        self, content: Union[str, Dict[str, Any]], content_format: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Prepare content for v2 API submission.

        :param content: Content to prepare (string or ADF dict)
        :param content_format: Explicit content format ('adf', 'storage', 'wiki')
        :return: Prepared content dictionary for v2 API
        """
        if content_format is None:
            content_format = detect_content_format(content)

        if content_format == "adf":
            if isinstance(content, dict) and validate_adf_document(content):
                return {"representation": "atlas_doc_format", "value": content}
            else:
                raise ValueError("Invalid ADF content structure")

        elif content_format in ["storage", "wiki"]:
            # Convert to ADF for v2 API
            if isinstance(content, str):
                adf_content = convert_text_to_adf(content)
                return {"representation": "atlas_doc_format", "value": adf_content}
            else:
                raise ValueError(f"Expected string content for {content_format} format")

        else:
            # Default: treat as plain text and convert to ADF
            if isinstance(content, str):
                adf_content = convert_text_to_adf(content)
                return {"representation": "atlas_doc_format", "value": adf_content}
            else:
                raise ValueError("Unsupported content format")

    def _get_v2_endpoint(self, resource: str) -> str:
        """
        Get v2 API endpoint URL.

        :param resource: Resource path (e.g., 'pages', 'spaces')
        :return: Full endpoint URL
        """
        return self.resource_url(resource, api_root=self.api_root, api_version=self.api_version)

    def _v2_request(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a v2 API request with appropriate headers.

        :param method: HTTP method
        :param endpoint: API endpoint
        :param kwargs: Additional request parameters
        :return: Response data
        """
        # Use v2 headers by default
        headers = kwargs.get("headers", {})
        headers.update(self.v2_headers)
        kwargs["headers"] = headers

        # Make request using parent class method
        if method.upper() == "GET":
            return self.get(endpoint, **kwargs)
        elif method.upper() == "POST":
            return self.post(endpoint, **kwargs)
        elif method.upper() == "PUT":
            return self.put(endpoint, **kwargs)
        elif method.upper() == "DELETE":
            return self.delete(endpoint, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    def get_page_by_id(
        self, page_id: str, expand: Optional[List[str]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get a page by ID using v2 API.

        :param page_id: Page ID
        :param expand: List of properties to expand
        :return: Page data
        """
        endpoint = self._get_v2_endpoint(f"pages/{page_id}")
        params = {}

        if expand:
            params["body-format"] = "atlas_doc_format"  # Request ADF format
            if isinstance(expand, list):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = expand

        return self._v2_request("GET", endpoint, params=params)

    def get_pages(
        self, space_id: Optional[str] = None, limit: int = 25, cursor: Optional[str] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get pages using v2 API with cursor-based pagination.

        :param space_id: Space ID to filter by
        :param limit: Number of results per page
        :param cursor: Cursor for pagination
        :return: Pages response with results and pagination info
        """
        endpoint = self._get_v2_endpoint("pages")
        params = {"limit": limit, "body-format": "atlas_doc_format"}  # Request ADF format

        if space_id:
            params["space-id"] = space_id

        if cursor:
            params["cursor"] = cursor

        return self._v2_request("GET", endpoint, params=params)

    def create_page(
        self,
        space_id: str,
        title: str,
        content: Union[str, Dict[str, Any]],
        parent_id: Optional[str] = None,
        content_format: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Create a page using v2 API.

        :param space_id: Space ID where page will be created
        :param title: Page title
        :param content: Page content (string or ADF dict)
        :param parent_id: Parent page ID (optional)
        :param content_format: Content format ('adf', 'storage', 'wiki')
        :return: Created page data
        """
        endpoint = self._get_v2_endpoint("pages")

        # Prepare content for v2 API
        prepared_content = self._prepare_content_for_v2(content, content_format)

        data = {"spaceId": space_id, "title": title, "body": prepared_content}

        if parent_id:
            data["parentId"] = parent_id

        return self._v2_request("POST", endpoint, json=data)

    def update_page(
        self,
        page_id: str,
        title: Optional[str] = None,
        content: Optional[Union[str, Dict[str, Any]]] = None,
        content_format: Optional[str] = None,
        version: Optional[int] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Update a page using v2 API.

        :param page_id: Page ID to update
        :param title: New page title (optional)
        :param content: New page content (optional)
        :param content_format: Content format ('adf', 'storage', 'wiki')
        :param version: Page version for optimistic locking
        :return: Updated page data
        """
        endpoint = self._get_v2_endpoint(f"pages/{page_id}")

        data = {}

        if title:
            data["title"] = title

        if content is not None:
            prepared_content = self._prepare_content_for_v2(content, content_format)
            data["body"] = prepared_content  # type: ignore[assignment]

        if version:
            data["version"] = {"number": version}  # type: ignore[assignment]

        return self._v2_request("PUT", endpoint, json=data)

    def delete_page(self, page_id: str) -> None:
        """
        Delete a page using v2 API.

        :param page_id: Page ID to delete
        """
        endpoint = self._get_v2_endpoint(f"pages/{page_id}")
        self._v2_request("DELETE", endpoint)

    def get_spaces(self, limit: int = 25, cursor: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get spaces using v2 API with cursor-based pagination.

        :param limit: Number of results per page
        :param cursor: Cursor for pagination
        :return: Spaces response with results and pagination info
        """
        endpoint = self._get_v2_endpoint("spaces")
        params: Dict[str, Any] = {"limit": limit}

        if cursor:
            params["cursor"] = cursor

        return self._v2_request("GET", endpoint, params=params)

    def search_pages(
        self, cql: str, limit: int = 25, cursor: Optional[str] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Search pages using CQL with v2 API.

        :param cql: CQL (Confluence Query Language) query
        :param limit: Number of results per page
        :param cursor: Cursor for pagination
        :return: Search results with pagination info
        """
        endpoint = self._get_v2_endpoint("pages")
        params = {"cql": cql, "limit": limit, "body-format": "atlas_doc_format"}  # Request ADF format

        if cursor:
            params["cursor"] = cursor

        return self._v2_request("GET", endpoint, params=params)
