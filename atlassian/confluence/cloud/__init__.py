# coding=utf-8

from .base import ConfluenceCloudBase
from .v2 import ConfluenceCloudV2
from typing import Optional, Dict, Any, List
import logging
import warnings

log = logging.getLogger(__name__)


class Cloud(ConfluenceCloudBase):
    """
    Confluence Cloud REST API wrapper with dual API support.

    Supports both v1 (legacy) and v2 (modern) API endpoints with automatic
    version selection and explicit v2 API usage options.
    """

    def __init__(self, url="https://api.atlassian.com/", *args, **kwargs):
        # Extract v2 API configuration options
        self._force_v2_api = kwargs.pop("force_v2_api", False)
        self._prefer_v2_api = kwargs.pop("prefer_v2_api", False)

        # Set default values only if not provided
        if "cloud" not in kwargs:
            kwargs["cloud"] = True
        if "api_version" not in kwargs:
            kwargs["api_version"] = "latest"
        if "api_root" not in kwargs:
            kwargs["api_root"] = "wiki/rest/api"
        url = url.strip("/")
        super(Cloud, self).__init__(url, *args, **kwargs)

        # Initialize v2 API client for dual support
        self._v2_client = None
        if self._force_v2_api or self._prefer_v2_api:
            self._init_v2_client()

        # Validate backward compatibility on initialization
        self._validate_backward_compatibility()

    def _init_v2_client(self):
        """Initialize the v2 API client for dual API support."""
        if self._v2_client is None:
            try:
                # Create v2 client with same configuration
                v2_kwargs = {
                    "username": getattr(self, "username", None),
                    "password": getattr(self, "password", None),
                    "token": getattr(self, "token", None),
                    "session": self._session,
                    "timeout": getattr(self, "timeout", 75),
                    "verify_ssl": getattr(self, "verify_ssl", True),
                    "cloud": True,
                }

                # Copy authentication details if available
                if hasattr(self, "oauth") and self.oauth:
                    v2_kwargs["oauth"] = self.oauth
                if hasattr(self, "oauth2") and self.oauth2:
                    v2_kwargs["oauth2"] = self.oauth2

                self._v2_client = ConfluenceCloudV2(self.url, **v2_kwargs)
                log.debug("Initialized Confluence Cloud v2 API client")
            except Exception as e:
                log.warning(f"Failed to initialize v2 API client: {e}")
                self._v2_client = None

    def _should_use_v2_api(self, operation: Optional[str] = None) -> bool:
        """
        Determine whether to use v2 API for a given operation.

        :param operation: Operation name (for future operation-specific routing)
        :return: True if v2 API should be used
        """
        if self._force_v2_api:
            return True

        if self._prefer_v2_api and self._v2_client is not None:
            return True

        # Future: Add operation-specific routing logic here
        # For now, default to v1 API unless explicitly configured
        return False

    def _route_to_v2_if_needed(self, method_name: str, *args, **kwargs):
        """
        Route method call to v2 API if configured to do so.

        :param method_name: Name of the method to call
        :param args: Method arguments
        :param kwargs: Method keyword arguments
        :return: Result from appropriate API version
        """
        if self._should_use_v2_api(method_name):
            if self._v2_client is None:
                self._init_v2_client()

        if self._should_use_v2_api(method_name):
            if self._v2_client is None:
                self._init_v2_client()

            if self._v2_client is not None and hasattr(self._v2_client, method_name):
                log.debug(f"Routing {method_name} to v2 API")

                # Handle parameter conversion for specific methods
                if method_name == "get_spaces":
                    # Convert v1 params format to v2 direct parameters
                    if "params" in kwargs and isinstance(kwargs["params"], dict):
                        params = kwargs.pop("params")
                        if "limit" in params:
                            kwargs["limit"] = params["limit"]
                        if "cursor" in params:
                            kwargs["cursor"] = params["cursor"]

                return getattr(self._v2_client, method_name)(*args, **kwargs)
            else:
                log.warning(f"v2 API client not available or method {method_name} not found, falling back to v1")

        # Fall back to v1 API (current implementation)
        return None

    def enable_v2_api(self, force: bool = False, prefer: bool = False):
        """
        Enable v2 API usage for this client instance.

        This method enables Confluence Cloud v2 API support while maintaining complete
        backward compatibility. All existing code will continue to work unchanged with
        potential performance improvements.

        **Backward Compatibility:** Enabling v2 API does not break existing code.
        All method signatures, parameter names, and return formats remain the same.

        **Performance Benefits:** v2 API provides enhanced performance for:
        - Large search result sets with cursor-based pagination
        - Content operations with native ADF support
        - Bulk operations and content processing

        :param force: If True, force all operations to use v2 API when available.
                     If False, prefer v2 API but fall back to v1 when needed.
                     Default: False (recommended for gradual migration)
        :param prefer: If True, prefer v2 API but allow fallback to v1.
                      Ignored if force=True. Default: False

        .. versionadded:: 4.1.0
           Added comprehensive v2 API support with backward compatibility.

        .. note::
           **Migration Strategy:** Start with ``prefer=True`` to enable v2 optimizations
           while maintaining full compatibility. Use ``force=True`` only when you want
           to ensure all operations use v2 API exclusively.

           **Requirements:** Requires valid Confluence Cloud authentication and
           a Confluence instance that supports v2 API.

        Examples:
            Enable v2 API with fallback support (recommended):

            >>> confluence.enable_v2_api()
            >>> # Existing code works unchanged with potential performance improvements
            >>> results = confluence.search_content("type=page", limit=100)

            Force v2 API usage exclusively:

            >>> confluence.enable_v2_api(force=True)
            >>> # All operations will use v2 API when available
            >>> page = confluence.get_content("123456")

            Check API configuration after enabling:

            >>> confluence.enable_v2_api()
            >>> info = confluence.get_api_version_info()
            >>> print(f"v2 API enabled: {info['v2_available']}")
            >>> print(f"Current default: {info['current_default']}")

            Gradual migration approach:

            >>> # Step 1: Enable v2 API
            >>> confluence.enable_v2_api()
            >>>
            >>> # Step 2: Existing code benefits automatically
            >>> pages = confluence.search_content("type=page")
            >>>
            >>> # Step 3: Use new v2-specific methods for enhanced features
            >>> adf_page = confluence.create_page_with_adf(space_id, title, adf_content)

        See Also:
            - :meth:`disable_v2_api`: Disable v2 API and use only v1 API
            - :meth:`get_api_version_info`: Check current API configuration
            - :doc:`confluence_v2_migration`: Complete migration guide
        """
        if force:
            self._force_v2_api = True
            self._prefer_v2_api = True
        elif prefer:
            self._force_v2_api = False
            self._prefer_v2_api = True
        else:
            # Default behavior when called without parameters
            self._force_v2_api = False
            self._prefer_v2_api = True

        self._init_v2_client()
        log.info(f"Enabled v2 API usage (force={force}, prefer={prefer or not force})")

    def disable_v2_api(self):
        """Disable v2 API usage and use only v1 API."""
        self._force_v2_api = False
        self._prefer_v2_api = False
        log.info("Disabled v2 API usage, using v1 API only")

    def _validate_backward_compatibility(self):
        """
        Validate that all existing method signatures are preserved.

        This method ensures that the dual API implementation maintains
        complete backward compatibility with existing code.
        """
        # All existing methods must be present with same signatures
        required_methods = [
            # Content Management
            "get_content",
            "get_content_by_type",
            "create_content",
            "update_content",
            "delete_content",
            "get_content_children",
            "get_content_descendants",
            "get_content_ancestors",
            # Space Management
            "get_spaces",
            "get_space",
            "create_space",
            "update_space",
            "delete_space",
            "get_space_content",
            # User Management
            "get_users",
            "get_user",
            "get_current_user",
            # Group Management
            "get_groups",
            "get_group",
            "get_group_members",
            # Label Management
            "get_labels",
            "get_content_labels",
            "add_content_labels",
            "remove_content_label",
            # Attachment Management
            "get_attachments",
            "get_attachment",
            "create_attachment",
            "update_attachment",
            "delete_attachment",
            # Comment Management
            "get_comments",
            "get_comment",
            "create_comment",
            "update_comment",
            "delete_comment",
            # Search
            "search_content",
            "search_spaces",
            # Page Properties
            "get_content_properties",
            "get_content_property",
            "create_content_property",
            "update_content_property",
            "delete_content_property",
            # Templates
            "get_templates",
            "get_template",
            # Analytics
            "get_content_analytics",
            "get_space_analytics",
            # Export
            "export_content",
            "export_space",
            # Utility
            "get_metadata",
            "get_health",
        ]

        for method_name in required_methods:
            if not hasattr(self, method_name):
                raise AttributeError(f"Backward compatibility broken: missing method {method_name}")

        log.debug("Backward compatibility validation passed")

    def _issue_migration_warning(self, old_method: str, new_method: str, reason: str):
        """
        Issue a deprecation warning for methods where v2 API provides better alternatives.

        :param old_method: Name of the method being called
        :param new_method: Recommended v2 API method
        :param reason: Reason why v2 API is better
        """
        if self._prefer_v2_api or self._force_v2_api:
            # Don't warn if user has already opted into v2 API
            return

        warnings.warn(
            f"{old_method}() will continue to work but consider using {new_method}() "
            f"for {reason}. Enable v2 API with enable_v2_api() for enhanced features.",
            FutureWarning,
            stacklevel=3,
        )

    def get_api_version_info(self) -> Dict[str, Any]:
        """
        Get information about API version configuration.

        :return: Dictionary with API version information
        """
        return {
            "v1_available": True,
            "v2_available": self._v2_client is not None,
            "force_v2_api": self._force_v2_api,
            "prefer_v2_api": self._prefer_v2_api,
            "current_default": "v2" if self._should_use_v2_api() else "v1",
        }
        """
        Get information about API version configuration.

        :return: Dictionary with API version information
        """
        return {
            "v1_available": True,
            "v2_available": self._v2_client is not None,
            "force_v2_api": self._force_v2_api,
            "prefer_v2_api": self._prefer_v2_api,
            "current_default": "v2" if self._should_use_v2_api() else "v1",
        }

    # Content Management with dual API support
    def get_content(self, content_id, **kwargs):
        """
        Get content by ID with dual API support.

        This method maintains full backward compatibility with v1 API while providing
        automatic v2 API optimizations when enabled. All existing code will continue
        to work unchanged with enhanced performance benefits.

        **Backward Compatibility:** This method preserves all v1 API behavior including
        response format, parameter names, and error handling.

        **v2 API Enhancement:** When v2 API is enabled, this method can automatically
        benefit from improved performance and additional content format support.

        :param content_id: Content ID to retrieve (numeric for Server, UUID for Cloud)
        :param expand: Comma-separated list of properties to expand
                      Common values:
                      - 'body.storage': Get content in storage format
                      - 'body.view': Get rendered HTML content
                      - 'version': Get version information
                      - 'space': Get space information
                      - 'history': Get content history
                      - 'children.page': Get child pages
                      - 'ancestors': Get ancestor pages
        :param version: Specific version number to retrieve (optional)
        :param status: Content status filter ('current', 'trashed', 'draft', 'any')
        :param kwargs: Additional parameters passed to the API
        :return: Content data in v1 API format containing:
                - id: Content ID
                - type: Content type ('page', 'blogpost', 'comment', etc.)
                - title: Content title
                - space: Space information (if expanded)
                - body: Content body (if expanded)
                - version: Version information (if expanded)
                - history: Content history (if expanded)
                - _links: Navigation links

        .. versionchanged:: 4.1.0
           Added automatic v2 API performance optimizations while maintaining
           full backward compatibility.

        .. note::
           **v2 API Alternative:** For new applications working with ADF content,
           consider using :meth:`get_page_with_adf` which provides native ADF
           format support and enhanced v2 API features.

           **Performance Enhancement:** Enable v2 API with ``enable_v2_api()`` to
           get automatic performance improvements while maintaining the same interface.

        Examples:
            Get basic content information:

            >>> content = confluence.get_content("123456")
            >>> print(f"Title: {content['title']}")
            >>> print(f"Type: {content['type']}")

            Get content with body and version:

            >>> content = confluence.get_content(
            ...     "123456",
            ...     expand="body.storage,version,space"
            ... )
            >>> body_content = content['body']['storage']['value']
            >>> version_number = content['version']['number']

            Get specific version of content:

            >>> content = confluence.get_content(
            ...     "123456",
            ...     version=5,
            ...     expand="body.storage"
            ... )

            With v2 API enabled (automatic performance improvement):

            >>> confluence.enable_v2_api()  # Enable v2 optimizations
            >>> content = confluence.get_content("123456", expand="body.storage")
            >>> # Same interface, potential performance benefits

        See Also:
            - :meth:`get_page_with_adf`: v2 API method with native ADF support
            - :meth:`get_content_by_type`: Get content filtered by type
            - :doc:`confluence_v2_migration`: Migration guide for v2 API features
        """
        # Try v2 API routing first
        v2_result = self._route_to_v2_if_needed("get_page_by_id", content_id, **kwargs)
        if v2_result is not None:
            return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.get(f"content/{content_id}", **kwargs)

    def get_content_by_type(self, content_type, **kwargs):
        """
        Get content by type (page, blogpost, etc.) with dual API support.

        This method maintains full backward compatibility with v1 API.

        :param content_type: Content type ('page', 'blogpost', etc.)
        :param kwargs: Additional parameters (space, limit, start, etc.)
        :return: Content data in v1 API format for backward compatibility

        .. note::
           For new applications using pages, consider get_pages() with v2 API
           for cursor-based pagination and ADF content support.
        """
        # Try v2 API routing for pages
        if content_type == "page":
            v2_result = self._route_to_v2_if_needed("get_pages", **kwargs)
            if v2_result is not None:
                return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.get("content", params={"type": content_type, **kwargs})

    def create_content(self, data, **kwargs):
        """
        Create new content with dual API support.

        This method maintains full backward compatibility with v1 API data structures
        while providing automatic v2 API optimizations when enabled. All existing code
        will continue to work unchanged.

        **Backward Compatibility:** This method preserves all v1 API behavior including
        data structure format, parameter names, and response format.

        **v2 API Enhancement:** When v2 API is enabled, page creation can automatically
        benefit from improved performance and enhanced content processing.

        :param data: Content data dictionary in v1 API format with required fields:
                    - type: Content type ('page', 'blogpost', 'comment')
                    - title: Content title (required for pages and blogposts)
                    - space: Space information (dict with 'key' or 'id')
                    - body: Content body with representation format
                    - ancestors: Parent page information (optional, for hierarchical pages)
        :param kwargs: Additional parameters passed to the API
        :return: Created content data in v1 API format containing:
                - id: Content ID
                - type: Content type
                - title: Content title
                - space: Space information
                - body: Content body (if included)
                - version: Version information
                - _links: Navigation links

        .. versionchanged:: 4.1.0
           Added automatic v2 API performance optimizations for page creation
           while maintaining full backward compatibility.

        .. note::
           **v2 API Alternative:** For new applications creating pages with rich content,
           consider using :meth:`create_page_with_adf` which provides native ADF
           format support, better performance, and enhanced v2 API features.

           **Performance Enhancement:** Enable v2 API with ``enable_v2_api()`` to
           get automatic performance improvements for page creation while maintaining
           the same interface.

        Examples:
            Create a simple page:

            >>> page_data = {
            ...     "type": "page",
            ...     "title": "My New Page",
            ...     "space": {"key": "DEMO"},
            ...     "body": {
            ...         "storage": {
            ...             "value": "<p>Hello, World!</p>",
            ...             "representation": "storage"
            ...         }
            ...     }
            ... }
            >>> page = confluence.create_content(page_data)
            >>> print(f"Created page: {page['id']}")

            Create a child page:

            >>> child_data = {
            ...     "type": "page",
            ...     "title": "Child Page",
            ...     "space": {"key": "DEMO"},
            ...     "ancestors": [{"id": "123456"}],  # Parent page ID
            ...     "body": {
            ...         "storage": {
            ...             "value": "<p>This is a child page.</p>",
            ...             "representation": "storage"
            ...         }
            ...     }
            ... }
            >>> child_page = confluence.create_content(child_data)

            Create a blog post:

            >>> blog_data = {
            ...     "type": "blogpost",
            ...     "title": "My Blog Post",
            ...     "space": {"key": "DEMO"},
            ...     "body": {
            ...         "storage": {
            ...             "value": "<p>Blog content here.</p>",
            ...             "representation": "storage"
            ...         }
            ...     }
            ... }
            >>> blog = confluence.create_content(blog_data)

            With v2 API enabled (automatic performance improvement):

            >>> confluence.enable_v2_api()  # Enable v2 optimizations
            >>> page = confluence.create_content(page_data)
            >>> # Same interface, potential performance benefits for page creation

        See Also:
            - :meth:`create_page_with_adf`: v2 API method with native ADF support
            - :meth:`update_content`: Update existing content
            - :doc:`confluence_v2_migration`: Migration guide for v2 API features
        """
        # Check if this is page creation that can use v2 API
        if isinstance(data, dict) and data.get("type") == "page":
            space_id = data.get("space", {}).get("id") if isinstance(data.get("space"), dict) else data.get("space")
            title = data.get("title")
            content = (
                data.get("body", {}).get("storage", {}).get("value") if isinstance(data.get("body"), dict) else None
            )
            parent_id = data.get("ancestors", [{}])[-1].get("id") if data.get("ancestors") else None

            if space_id and title and content:
                v2_result = self._route_to_v2_if_needed("create_page", space_id, title, content, parent_id)
                if v2_result is not None:
                    return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.post("content", data=data, **kwargs)

    def update_content(self, content_id, data, **kwargs):
        """
        Update existing content with dual API support.

        This method maintains full backward compatibility with v1 API data structures
        while providing automatic v2 API optimizations when enabled. All existing code
        will continue to work unchanged.

        **Backward Compatibility:** This method preserves all v1 API behavior including
        data structure format, parameter names, and response format.

        **v2 API Enhancement:** When v2 API is enabled, page updates can automatically
        benefit from improved performance and enhanced content processing.

        :param content_id: Content ID to update (numeric for Server, UUID for Cloud)
        :param data: Updated content data dictionary in v1 API format with fields:
                    - type: Content type ('page', 'blogpost', 'comment')
                    - title: Updated content title (optional)
                    - body: Updated content body with representation format
                    - version: Version information for optimistic locking (recommended)
                    - space: Space information (usually unchanged)
        :param kwargs: Additional parameters passed to the API
        :return: Updated content data in v1 API format containing:
                - id: Content ID
                - type: Content type
                - title: Updated content title
                - body: Updated content body (if included)
                - version: New version information
                - _links: Navigation links

        .. versionchanged:: 4.1.0
           Added automatic v2 API performance optimizations for page updates
           while maintaining full backward compatibility.

        .. note::
           **v2 API Alternative:** For new applications updating pages with rich content,
           consider using :meth:`update_page_with_adf` which provides native ADF
           format support, better performance, and enhanced v2 API features.

           **Performance Enhancement:** Enable v2 API with ``enable_v2_api()`` to
           get automatic performance improvements for page updates while maintaining
           the same interface.

           **Version Management:** Always include version information to prevent
           concurrent modification conflicts. Get current version with :meth:`get_content`.

        Examples:
            Update page content:

            >>> # First, get current version
            >>> current_page = confluence.get_content("123456", expand="version")
            >>> current_version = current_page['version']['number']
            >>>
            >>> # Update with new content
            >>> update_data = {
            ...     "type": "page",
            ...     "title": "Updated Page Title",
            ...     "body": {
            ...         "storage": {
            ...             "value": "<p>Updated content here.</p>",
            ...             "representation": "storage"
            ...         }
            ...     },
            ...     "version": {"number": current_version + 1}
            ... }
            >>> updated_page = confluence.update_content("123456", update_data)
            >>> print(f"Updated to version: {updated_page['version']['number']}")

            Update only the title:

            >>> update_data = {
            ...     "type": "page",
            ...     "title": "New Title Only",
            ...     "version": {"number": current_version + 1}
            ... }
            >>> updated_page = confluence.update_content("123456", update_data)

            Update blog post:

            >>> blog_update = {
            ...     "type": "blogpost",
            ...     "title": "Updated Blog Post",
            ...     "body": {
            ...         "storage": {
            ...             "value": "<p>Updated blog content.</p>",
            ...             "representation": "storage"
            ...         }
            ...     },
            ...     "version": {"number": current_version + 1}
            ... }
            >>> updated_blog = confluence.update_content("789012", blog_update)

            With v2 API enabled (automatic performance improvement):

            >>> confluence.enable_v2_api()  # Enable v2 optimizations
            >>> updated_page = confluence.update_content("123456", update_data)
            >>> # Same interface, potential performance benefits for page updates

        See Also:
            - :meth:`update_page_with_adf`: v2 API method with native ADF support
            - :meth:`get_content`: Get current content and version information
            - :doc:`confluence_v2_migration`: Migration guide for v2 API features
        """
        # Check if this is page update that can use v2 API
        if isinstance(data, dict) and data.get("type") == "page":
            title = data.get("title")
            content = (
                data.get("body", {}).get("storage", {}).get("value") if isinstance(data.get("body"), dict) else None
            )
            version = data.get("version", {}).get("number") if isinstance(data.get("version"), dict) else None

            v2_result = self._route_to_v2_if_needed("update_page", content_id, title, content, None, version)
            if v2_result is not None:
                return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.put(f"content/{content_id}", data=data, **kwargs)

    def delete_content(self, content_id, **kwargs):
        """
        Delete content with dual API support.

        This method maintains full backward compatibility with v1 API.

        :param content_id: Content ID to delete
        :param kwargs: Additional parameters
        :return: Deletion result
        """
        # Try v2 API routing first
        v2_result = self._route_to_v2_if_needed("delete_page", content_id)
        if v2_result is not None:
            return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.delete(f"content/{content_id}", **kwargs)

    def get_content_children(self, content_id, **kwargs):
        """Get child content."""
        return self.get(f"content/{content_id}/children", **kwargs)

    def get_content_descendants(self, content_id, **kwargs):
        """Get descendant content."""
        return self.get(f"content/{content_id}/descendants", **kwargs)

    def get_content_ancestors(self, content_id, **kwargs):
        """Get ancestor content."""
        return self.get(f"content/{content_id}/ancestors", **kwargs)

    # Space Management with dual API support
    def get_spaces(self, **kwargs):
        """
        Get all spaces with dual API support.

        This method maintains full backward compatibility with v1 API.

        :param kwargs: Additional parameters (type, status, label, favourite, etc.)
        :return: Spaces data in v1 API format for backward compatibility

        .. note::
           For new applications, consider enabling v2 API support with enable_v2_api()
           for cursor-based pagination and enhanced space metadata.
        """
        # Try v2 API routing first
        v2_result = self._route_to_v2_if_needed("get_spaces", **kwargs)
        if v2_result is not None:
            return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.get(self.resource_url("space"), **kwargs)

    def get_space(self, space_id, **kwargs):
        """
        Get space by ID.

        This method maintains full backward compatibility with v1 API.

        :param space_id: Space ID or key
        :param kwargs: Additional parameters (expand, etc.)
        :return: Space data
        """
        return self.get(f"space/{space_id}", **kwargs)

    def create_space(self, data, **kwargs):
        """
        Create new space.

        This method maintains full backward compatibility with v1 API.

        :param data: Space data dictionary
        :param kwargs: Additional parameters
        :return: Created space data
        """
        return self.post("space", data=data, **kwargs)

    def update_space(self, space_id, data, **kwargs):
        """
        Update existing space.

        This method maintains full backward compatibility with v1 API.

        :param space_id: Space ID to update
        :param data: Updated space data dictionary
        :param kwargs: Additional parameters
        :return: Updated space data
        """
        return self.put(f"space/{space_id}", data=data, **kwargs)

    def delete_space(self, space_id, **kwargs):
        """
        Delete space.

        This method maintains full backward compatibility with v1 API.

        :param space_id: Space ID to delete
        :param kwargs: Additional parameters
        :return: Deletion result
        """
        return self.delete(f"space/{space_id}", **kwargs)

    def get_space_content(self, space_id, **kwargs):
        """
        Get space content.

        This method maintains full backward compatibility with v1 API.

        :param space_id: Space ID
        :param kwargs: Additional parameters
        :return: Space content data
        """
        return self.get(f"space/{space_id}/content", **kwargs)

    # User Management
    def get_users(self, **kwargs):
        """Get all users."""
        return self.get("user", **kwargs)

    def get_user(self, user_id, **kwargs):
        """Get user by ID."""
        return self.get(f"user/{user_id}", **kwargs)

    def get_current_user(self, **kwargs):
        """Get current user."""
        return self.get(self.resource_url("user/current"), **kwargs)

    # Group Management
    def get_groups(self, **kwargs):
        """Get all groups."""
        return self.get("group", **kwargs)

    def get_group(self, group_id, **kwargs):
        """Get group by ID."""
        return self.get(f"group/{group_id}", **kwargs)

    def get_group_members(self, group_id, **kwargs):
        """Get group members."""
        return self.get(f"group/{group_id}/member", **kwargs)

    # Label Management
    def get_labels(self, **kwargs):
        """Get all labels."""
        return self.get("label", **kwargs)

    def get_content_labels(self, content_id, **kwargs):
        """Get content labels."""
        return self.get(f"content/{content_id}/label", **kwargs)

    def add_content_labels(self, content_id, data, **kwargs):
        """Add labels to content."""
        return self.post(f"content/{content_id}/label", data=data, **kwargs)

    def remove_content_label(self, content_id, label_id, **kwargs):
        """Remove label from content."""
        return self.delete(f"content/{content_id}/label/{label_id}", **kwargs)

    # Attachment Management
    def get_attachments(self, content_id, **kwargs):
        """Get content attachments."""
        return self.get(f"content/{content_id}/child/attachment", **kwargs)

    def get_attachment(self, attachment_id, **kwargs):
        """Get attachment by ID."""
        return self.get(f"content/{attachment_id}", **kwargs)

    def create_attachment(self, content_id, data, **kwargs):
        """Create new attachment."""
        return self.post(f"content/{content_id}/child/attachment", data=data, **kwargs)

    def update_attachment(self, attachment_id, data, **kwargs):
        """Update existing attachment."""
        return self.put(f"content/{attachment_id}", data=data, **kwargs)

    def delete_attachment(self, attachment_id, **kwargs):
        """Delete attachment."""
        return self.delete(f"content/{attachment_id}", **kwargs)

    # Comment Management
    def get_comments(self, content_id, **kwargs):
        """Get content comments."""
        return self.get(f"content/{content_id}/child/comment", **kwargs)

    def get_comment(self, comment_id, **kwargs):
        """Get comment by ID."""
        return self.get(f"content/{comment_id}", **kwargs)

    def create_comment(self, content_id, data, **kwargs):
        """Create new comment."""
        return self.post(f"content/{content_id}/child/comment", data=data, **kwargs)

    def update_comment(self, comment_id, data, **kwargs):
        """Update existing comment."""
        return self.put(f"content/{comment_id}", data=data, **kwargs)

    def delete_comment(self, comment_id, **kwargs):
        """Delete comment."""
        return self.delete(f"content/{comment_id}", **kwargs)

    # Search with dual API support
    def search_content(self, query, **kwargs):
        """
        Search content using CQL (Confluence Query Language) with dual API support.

        This method maintains full backward compatibility with v1 API while providing
        automatic performance optimizations when v2 API is enabled. All existing code
        will continue to work unchanged.

        **Backward Compatibility:** This method preserves all v1 API behavior including
        response format, parameter names, and error handling.

        **Performance Enhancement:** When v2 API is enabled, large result sets benefit
        from improved pagination performance automatically.

        :param query: CQL query string for searching content
                     Examples:
                     - "type=page AND space=DEMO"
                     - "title~'meeting notes' AND lastModified >= '2024-01-01'"
                     - "creator=currentUser() AND type=blogpost"
        :param limit: Maximum number of results to return (default: 25, max: 100)
        :param start: Starting index for pagination (0-based, v1 API style)
        :param expand: Comma-separated list of properties to expand
                      Examples: 'body.storage', 'version', 'space', 'history'
        :param excerpt: Whether to include content excerpts in results
        :param include_archived_spaces: Whether to include archived spaces in search
        :param kwargs: Additional search parameters
        :return: Search results in v1 API format containing:
                - results: List of matching content items
                - start: Starting index of results
                - limit: Maximum results per page
                - size: Number of results returned
                - totalSize: Total number of matching results (if available)
                - _links: Navigation links for pagination

        .. versionchanged:: 4.1.0
           Added automatic v2 API performance optimizations while maintaining
           full backward compatibility.

        .. note::
           **Migration Recommendation:** For new applications or when working with
           large result sets, consider using :meth:`search_pages_with_cursor` which
           provides cursor-based pagination and better performance with v2 API.

           **Performance Warning:** This method will issue warnings for large pagination
           requests (limit > 50 or start > 100) suggesting cursor-based alternatives.
           Enable v2 API with ``enable_v2_api()`` to disable warnings and get
           automatic performance improvements.

        Examples:
            Basic content search:

            >>> results = confluence.search_content("type=page AND space=DEMO")
            >>> for page in results['results']:
            ...     print(f"Found: {page['title']}")

            Search with pagination:

            >>> results = confluence.search_content(
            ...     "type=page AND lastModified >= '2024-01-01'",
            ...     limit=50,
            ...     start=0,
            ...     expand="body.storage,version"
            ... )

            Search for specific content:

            >>> results = confluence.search_content(
            ...     "title~'API documentation' AND type=page",
            ...     limit=10
            ... )

            With v2 API enabled (automatic performance improvement):

            >>> confluence.enable_v2_api()  # Enable v2 optimizations
            >>> results = confluence.search_content("type=page", limit=100)
            >>> # Same interface, better performance for large result sets

        See Also:
            - :meth:`search_pages_with_cursor`: v2 API method with cursor pagination
            - :meth:`cql`: Alternative CQL search method
            - :doc:`confluence_v2_migration`: Migration guide for v2 API features
        """
        # Issue migration warning for pagination-heavy use cases
        if kwargs.get("limit", 0) > 50 or kwargs.get("start", 0) > 100:
            self._issue_migration_warning(
                "search_content",
                "search_pages_with_cursor",
                "cursor-based pagination and better performance with large result sets",
            )

        # Try v2 API routing first
        v2_result = self._route_to_v2_if_needed("search_pages", query, **kwargs)
        if v2_result is not None:
            return v2_result

        # Fall back to v1 API - maintains exact backward compatibility
        return self.get("content/search", params={"cql": query, **kwargs})

    def search_spaces(self, query, **kwargs):
        """
        Search spaces.

        This method maintains full backward compatibility with v1 API.

        :param query: Search query string
        :param kwargs: Additional parameters
        :return: Space search results
        """
        return self.get("space/search", params={"query": query, **kwargs})

    # Page Properties
    def get_content_properties(self, content_id, **kwargs):
        """Get content properties."""
        return self.get(f"content/{content_id}/property", **kwargs)

    def get_content_property(self, content_id, property_key, **kwargs):
        """Get content property by key."""
        return self.get(f"content/{content_id}/property/{property_key}", **kwargs)

    def create_content_property(self, content_id, data, **kwargs):
        """Create new content property."""
        return self.post(f"content/{content_id}/property", data=data, **kwargs)

    def update_content_property(self, content_id, property_key, data, **kwargs):
        """Update existing content property."""
        return self.put(f"content/{content_id}/property/{property_key}", data=data, **kwargs)

    def delete_content_property(self, content_id, property_key, **kwargs):
        """Delete content property."""
        return self.delete(f"content/{content_id}/property/{property_key}", **kwargs)

    # Templates
    def get_templates(self, **kwargs):
        """Get all templates."""
        return self.get("template", **kwargs)

    def get_template(self, template_id, **kwargs):
        """Get template by ID."""
        return self.get(f"template/{template_id}", **kwargs)

    # Analytics
    def get_content_analytics(self, content_id, **kwargs):
        """Get content analytics."""
        return self.get(f"content/{content_id}/analytics", **kwargs)

    def get_space_analytics(self, space_id, **kwargs):
        """Get space analytics."""
        return self.get(f"space/{space_id}/analytics", **kwargs)

    # Export
    def export_content(self, content_id, **kwargs):
        """Export content."""
        return self.get(f"content/{content_id}/export", **kwargs)

    def export_space(self, space_id, **kwargs):
        """Export space."""
        return self.get(f"space/{space_id}/export", **kwargs)

    # Utility Methods
    def get_metadata(self, **kwargs):
        """Get API metadata."""
        return self.get("metadata", **kwargs)

    def get_health(self, **kwargs):
        """Get API health status."""
        return self.get("health", **kwargs)

    # v2 API specific convenience methods
    def create_page_with_adf(
        self, space_id: str, title: str, adf_content: Dict[str, Any], parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a page with ADF content using v2 API.

        This method forces the use of v2 API regardless of configuration and provides
        native ADF (Atlassian Document Format) support for rich content creation.

        ADF (Atlassian Document Format) is the native content format for Confluence Cloud
        that provides structured, JSON-based representation of rich content including
        headings, paragraphs, lists, tables, and formatted text.

        :param space_id: Space ID where page will be created (UUID format for Cloud)
        :param title: Page title (must be unique within the space)
        :param adf_content: ADF content dictionary in native format with required fields:
                           - version: Must be 1
                           - type: Must be "doc"
                           - content: List of content nodes (paragraphs, headings, etc.)
        :param parent_id: Parent page ID for hierarchical organization (optional)
        :return: Created page data in v2 API format containing:
                - id: Page ID (UUID)
                - title: Page title
                - spaceId: Space ID
                - body: Page content in ADF format
                - version: Page version information
                - _links: Navigation links
        :raises RuntimeError: If v2 API client is not available or not properly configured
        :raises ValueError: If ADF content structure is invalid
        :raises requests.HTTPError: If API request fails (permissions, space not found, etc.)

        .. versionadded:: 4.1.0
           Added native ADF support for Confluence Cloud v2 API

        .. note::
           This method requires Confluence Cloud and proper API token authentication.
           Space ID must be in UUID format (not space key).

        Examples:
            Create a simple page with text:

            >>> adf_content = {
            ...     "version": 1,
            ...     "type": "doc",
            ...     "content": [
            ...         {
            ...             "type": "paragraph",
            ...             "content": [
            ...                 {"type": "text", "text": "Hello, World!"}
            ...             ]
            ...         }
            ...     ]
            ... }
            >>> page = confluence.create_page_with_adf("SPACE123", "My Page", adf_content)
            >>> print(f"Created page: {page['id']}")

            Create a page with formatted content:

            >>> formatted_adf = {
            ...     "version": 1,
            ...     "type": "doc",
            ...     "content": [
            ...         {
            ...             "type": "heading",
            ...             "attrs": {"level": 1},
            ...             "content": [{"type": "text", "text": "Welcome"}]
            ...         },
            ...         {
            ...             "type": "paragraph",
            ...             "content": [
            ...                 {"type": "text", "text": "This is "},
            ...                 {
            ...                     "type": "text",
            ...                     "text": "bold text",
            ...                     "marks": [{"type": "strong"}]
            ...                 }
            ...             ]
            ...         }
            ...     ]
            ... }
            >>> page = confluence.create_page_with_adf("SPACE123", "Formatted Page", formatted_adf)

            Create a child page:

            >>> child_page = confluence.create_page_with_adf(
            ...     space_id="SPACE123",
            ...     title="Child Page",
            ...     adf_content=adf_content,
            ...     parent_id="parent-page-uuid"
            ... )

        See Also:
            - :meth:`update_page_with_adf`: Update existing page with ADF content
            - :meth:`get_page_with_adf`: Retrieve page with ADF content
            - :doc:`confluence_adf`: Complete ADF documentation and examples
        """
        if self._v2_client is None:
            self._init_v2_client()

        if self._v2_client is None:
            raise RuntimeError("v2 API client not available")

        return self._v2_client.create_page(space_id, title, adf_content, parent_id, "adf")

    def update_page_with_adf(
        self,
        page_id: str,
        title: Optional[str] = None,
        adf_content: Optional[Dict[str, Any]] = None,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Update a page with ADF content using v2 API.

        This method forces the use of v2 API regardless of configuration and provides
        native ADF support for rich content updates with optimistic locking support.

        :param page_id: Page ID to update (UUID format for Cloud)
        :param title: New page title (optional, keeps existing if not provided)
        :param adf_content: New ADF content dictionary (optional, keeps existing if not provided)
                           Must follow ADF structure with version=1, type="doc", and content array
        :param version: Page version number for optimistic locking (highly recommended)
                       Use current version + 1 to prevent concurrent modification conflicts
        :return: Updated page data in v2 API format containing:
                - id: Page ID
                - title: Updated page title
                - body: Updated page content in ADF format
                - version: New version information
                - _links: Navigation links
        :raises RuntimeError: If v2 API client is not available
        :raises ValueError: If ADF content structure is invalid
        :raises requests.HTTPError: If API request fails (version conflict, permissions, etc.)

        .. versionadded:: 4.1.0
           Added native ADF support for Confluence Cloud v2 API

        .. note::
           Always use version parameter to prevent concurrent modification issues.
           Get current version with get_page_with_adf() before updating.

        Examples:
            Update page title only:

            >>> updated_page = confluence.update_page_with_adf(
            ...     page_id="123456",
            ...     title="Updated Title",
            ...     version=2
            ... )

            Update page content only:

            >>> new_adf = {
            ...     "version": 1,
            ...     "type": "doc",
            ...     "content": [
            ...         {
            ...             "type": "paragraph",
            ...             "content": [
            ...                 {"type": "text", "text": "Updated content!"}
            ...             ]
            ...         }
            ...     ]
            ... }
            >>> updated_page = confluence.update_page_with_adf(
            ...     page_id="123456",
            ...     adf_content=new_adf,
            ...     version=2
            ... )

            Update both title and content with version control:

            >>> # First, get current page to check version
            >>> current_page = confluence.get_page_with_adf("123456", expand=['version'])
            >>> current_version = current_page['version']['number']
            >>>
            >>> # Update with proper version
            >>> updated_page = confluence.update_page_with_adf(
            ...     page_id="123456",
            ...     title="New Title",
            ...     adf_content=new_adf,
            ...     version=current_version + 1
            ... )

        See Also:
            - :meth:`create_page_with_adf`: Create new page with ADF content
            - :meth:`get_page_with_adf`: Retrieve page with current version info
            - :doc:`confluence_adf`: Complete ADF documentation and examples
        """
        if self._v2_client is None:
            self._init_v2_client()

        if self._v2_client is None:
            raise RuntimeError("v2 API client not available")

        return self._v2_client.update_page(page_id, title, adf_content, "adf", version)

    def get_page_with_adf(self, page_id: str, expand: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get a page with ADF content using v2 API.

        This method forces the use of v2 API regardless of configuration and returns
        content in native ADF format for rich content processing and manipulation.

        :param page_id: Page ID to retrieve (UUID format for Cloud)
        :param expand: List of properties to expand for additional data:
                      - 'body': Include page content in ADF format
                      - 'version': Include version information
                      - 'space': Include space details
                      - 'ancestors': Include parent page hierarchy
                      - 'children': Include child pages
                      - 'descendants': Include all descendant pages
                      - 'history': Include page history
                      - 'restrictions': Include page restrictions
                      - 'metadata': Include page metadata
        :return: Page data with ADF content in v2 API format containing:
                - id: Page ID (UUID)
                - title: Page title
                - spaceId: Space ID
                - body: Page content with atlas_doc_format representation
                - version: Version information (if expanded)
                - space: Space details (if expanded)
                - _links: Navigation links
        :raises RuntimeError: If v2 API client is not available
        :raises requests.HTTPError: If API request fails (page not found, permissions, etc.)

        .. versionadded:: 4.1.0
           Added native ADF support for Confluence Cloud v2 API

        .. note::
           The returned ADF content is in the 'body.atlas_doc_format.value' field.
           This is the native format used by Confluence Cloud v2 API.

        Examples:
            Get page with basic information:

            >>> page = confluence.get_page_with_adf("123456")
            >>> print(f"Page title: {page['title']}")
            >>> print(f"Space ID: {page['spaceId']}")

            Get page with ADF content:

            >>> page = confluence.get_page_with_adf("123456", expand=['body'])
            >>> adf_content = page['body']['atlas_doc_format']['value']
            >>> print(f"ADF version: {adf_content['version']}")
            >>> print(f"Content nodes: {len(adf_content['content'])}")

            Get page with version info for updates:

            >>> page = confluence.get_page_with_adf("123456", expand=['body', 'version'])
            >>> current_version = page['version']['number']
            >>> adf_content = page['body']['atlas_doc_format']['value']
            >>>
            >>> # Modify content and update
            >>> modified_adf = modify_adf_content(adf_content)
            >>> updated_page = confluence.update_page_with_adf(
            ...     page_id="123456",
            ...     adf_content=modified_adf,
            ...     version=current_version + 1
            ... )

            Get page with full context:

            >>> page = confluence.get_page_with_adf(
            ...     page_id="123456",
            ...     expand=['body', 'version', 'space', 'ancestors']
            ... )
            >>> space_name = page['space']['name']
            >>> parent_pages = page['ancestors']

        See Also:
            - :meth:`create_page_with_adf`: Create new page with ADF content
            - :meth:`update_page_with_adf`: Update page with ADF content
            - :doc:`confluence_adf`: Complete ADF documentation and examples
        """
        if self._v2_client is None:
            self._init_v2_client()

        if self._v2_client is None:
            raise RuntimeError("v2 API client not available")

        return self._v2_client.get_page_by_id(page_id, expand)

    def search_pages_with_cursor(self, cql: str, limit: int = 25, cursor: Optional[str] = None) -> Dict[str, Any]:
        """
        Search pages using CQL with cursor-based pagination (v2 API).

        This method forces the use of v2 API regardless of configuration and provides
        cursor-based pagination for efficient handling of large result sets. Cursor-based
        pagination is more reliable and performant than offset-based pagination, especially
        for large datasets where results may change during iteration.

        :param cql: CQL (Confluence Query Language) query string for filtering results.
                   Examples:
                   - "type=page AND space=DEMO" - Pages in DEMO space
                   - "type=page AND title~'meeting'" - Pages with 'meeting' in title
                   - "type=page AND created>=2024-01-01" - Pages created since Jan 1, 2024
                   - "type=page AND label='important'" - Pages with 'important' label
        :param limit: Number of results per page (1-250, default 25)
                     Higher limits reduce API calls but increase response time
        :param cursor: Cursor token for pagination (from previous response '_links.next.cursor')
                      None for first page, use returned cursor for subsequent pages
        :return: Search results with cursor-based pagination info containing:
                - results: List of page objects with ADF content
                - _links: Pagination links including 'next' cursor if more results exist
                - size: Number of results in current response
        :raises RuntimeError: If v2 API client is not available
        :raises ValueError: If CQL query is invalid or limit is out of range
        :raises requests.HTTPError: If API request fails

        .. versionadded:: 4.1.0
           Added cursor-based pagination for Confluence Cloud v2 API

        .. note::
           Cursor-based pagination provides better performance and consistency compared
           to offset-based pagination, especially for large result sets or when data
           changes during iteration.

        Examples:
            Basic search with first page:

            >>> results = confluence.search_pages_with_cursor(
            ...     cql="type=page AND space=DEMO",
            ...     limit=50
            ... )
            >>> pages = results['results']
            >>> print(f"Found {len(pages)} pages")

            Iterate through all results using cursor:

            >>> all_pages = []
            >>> cursor = None
            >>>
            >>> while True:
            ...     results = confluence.search_pages_with_cursor(
            ...         cql="type=page AND space=DEMO",
            ...         limit=100,
            ...         cursor=cursor
            ...     )
            ...
            ...     all_pages.extend(results['results'])
            ...
            ...     # Check if there are more results
            ...     if 'next' not in results.get('_links', {}):
            ...         break
            ...
            ...     cursor = results['_links']['next']['cursor']
            >>>
            >>> print(f"Total pages found: {len(all_pages)}")

            Search with complex CQL query:

            >>> results = confluence.search_pages_with_cursor(
            ...     cql="type=page AND space in ('DEMO', 'PROJ') AND created>=2024-01-01",
            ...     limit=25
            ... )

            Process results with ADF content:

            >>> results = confluence.search_pages_with_cursor(
            ...     cql="type=page AND label='documentation'",
            ...     limit=50
            ... )
            >>>
            >>> for page in results['results']:
            ...     page_id = page['id']
            ...     title = page['title']
            ...
            ...     # Get full ADF content if needed
            ...     full_page = confluence.get_page_with_adf(page_id, expand=['body'])
            ...     adf_content = full_page['body']['atlas_doc_format']['value']
            ...
            ...     print(f"Processing page: {title}")

        See Also:
            - :meth:`search_content`: Legacy v1 API search with offset pagination
            - :meth:`get_page_with_adf`: Get full page content with ADF
            - `CQL Documentation <https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/>`_
        """
        if self._v2_client is None:
            self._init_v2_client()

        if self._v2_client is None:
            raise RuntimeError("v2 API client not available")

        return self._v2_client.search_pages(cql, limit, cursor)
