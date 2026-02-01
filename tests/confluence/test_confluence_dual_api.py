# coding=utf-8
"""
Test cases for Confluence Cloud dual API support.

This test suite covers the dual API functionality that allows seamless
switching between v1 and v2 APIs while maintaining backward compatibility.
"""

import pytest
from unittest.mock import patch

from atlassian.confluence.cloud import Cloud as ConfluenceCloud
from atlassian.confluence.cloud.v2 import ConfluenceCloudV2


@pytest.fixture
def confluence_dual():
    """Fixture for ConfluenceCloud client with dual API support."""
    return ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True)


@pytest.fixture
def confluence_v2_enabled():
    """Fixture for ConfluenceCloud client with v2 API enabled."""
    client = ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True)
    client.enable_v2_api()
    return client


@pytest.fixture
def confluence_v2_forced():
    """Fixture for ConfluenceCloud client with v2 API forced."""
    client = ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True)
    client.enable_v2_api(force=True)
    return client


@pytest.fixture
def sample_adf_content():
    """Fixture providing sample ADF content."""
    return {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Test ADF content"}]}],
    }


class TestDualAPIInitialization:
    """Test cases for dual API initialization."""

    def test_init_default_configuration(self):
        """Test default initialization without v2 API."""
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token")

        assert confluence._force_v2_api is False
        assert confluence._prefer_v2_api is False
        assert confluence._v2_client is None
        assert confluence.cloud is True
        assert confluence.api_version == "latest"
        assert confluence.api_root == "wiki/rest/api"

    def test_init_with_v2_preference(self):
        """Test initialization with v2 API preference."""
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token", prefer_v2_api=True)

        assert confluence._force_v2_api is False
        assert confluence._prefer_v2_api is True
        # v2 client should be initialized when preferred
        assert confluence._v2_client is not None

    def test_init_with_v2_forced(self):
        """Test initialization with v2 API forced."""
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token", force_v2_api=True)

        assert confluence._force_v2_api is True
        # force_v2_api doesn't automatically set prefer_v2_api
        assert confluence._prefer_v2_api is False
        assert confluence._v2_client is not None

    def test_backward_compatibility_validation(self):
        """Test that backward compatibility validation passes."""
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token")

        # Should not raise any exceptions during initialization
        # All required methods should be present
        required_methods = [
            "get_content",
            "create_content",
            "update_content",
            "delete_content",
            "get_spaces",
            "create_space",
            "search_content",
        ]

        for method_name in required_methods:
            assert hasattr(confluence, method_name), f"Missing method: {method_name}"


class TestDualAPIConfiguration:
    """Test cases for dual API configuration methods."""

    def test_enable_v2_api_prefer(self, confluence_dual):
        """Test enabling v2 API with preference."""
        assert confluence_dual._prefer_v2_api is False
        assert confluence_dual._force_v2_api is False

        confluence_dual.enable_v2_api()

        assert confluence_dual._prefer_v2_api is True
        assert confluence_dual._force_v2_api is False
        assert confluence_dual._v2_client is not None

    def test_enable_v2_api_force(self, confluence_dual):
        """Test enabling v2 API with force."""
        confluence_dual.enable_v2_api(force=True)

        assert confluence_dual._prefer_v2_api is True
        assert confluence_dual._force_v2_api is True
        assert confluence_dual._v2_client is not None

    def test_disable_v2_api(self, confluence_v2_enabled):
        """Test disabling v2 API."""
        assert confluence_v2_enabled._prefer_v2_api is True

        confluence_v2_enabled.disable_v2_api()

        assert confluence_v2_enabled._prefer_v2_api is False
        assert confluence_v2_enabled._force_v2_api is False

    def test_get_api_version_info_default(self, confluence_dual):
        """Test getting API version info with default configuration."""
        info = confluence_dual.get_api_version_info()

        assert info["v1_available"] is True
        assert info["v2_available"] is False  # Not initialized by default
        assert info["force_v2_api"] is False
        assert info["prefer_v2_api"] is False
        assert info["current_default"] == "v1"

    def test_get_api_version_info_v2_enabled(self, confluence_v2_enabled):
        """Test getting API version info with v2 enabled."""
        info = confluence_v2_enabled.get_api_version_info()

        assert info["v1_available"] is True
        assert info["v2_available"] is True
        assert info["force_v2_api"] is False
        assert info["prefer_v2_api"] is True
        assert info["current_default"] == "v2"

    def test_get_api_version_info_v2_forced(self, confluence_v2_forced):
        """Test getting API version info with v2 forced."""
        info = confluence_v2_forced.get_api_version_info()

        assert info["v1_available"] is True
        assert info["v2_available"] is True
        assert info["force_v2_api"] is True
        assert info["prefer_v2_api"] is True
        assert info["current_default"] == "v2"


class TestDualAPIRouting:
    """Test cases for API routing logic."""

    def test_should_use_v2_api_default(self, confluence_dual):
        """Test v2 API usage decision with default configuration."""
        assert confluence_dual._should_use_v2_api() is False
        assert confluence_dual._should_use_v2_api("get_content") is False

    def test_should_use_v2_api_preferred(self, confluence_v2_enabled):
        """Test v2 API usage decision with v2 preferred."""
        assert confluence_v2_enabled._should_use_v2_api() is True
        assert confluence_v2_enabled._should_use_v2_api("get_content") is True

    def test_should_use_v2_api_forced(self, confluence_v2_forced):
        """Test v2 API usage decision with v2 forced."""
        assert confluence_v2_forced._should_use_v2_api() is True
        assert confluence_v2_forced._should_use_v2_api("get_content") is True

    @patch.object(ConfluenceCloudV2, "get_page_by_id")
    def test_route_to_v2_if_needed_success(self, mock_v2_method, confluence_v2_enabled):
        """Test successful routing to v2 API."""
        mock_v2_method.return_value = {"id": "123", "title": "Test Page"}

        result = confluence_v2_enabled._route_to_v2_if_needed("get_page_by_id", "123")

        assert result == {"id": "123", "title": "Test Page"}
        mock_v2_method.assert_called_once_with("123")

    def test_route_to_v2_if_needed_no_routing(self, confluence_dual):
        """Test no routing when v2 API is not enabled."""
        result = confluence_dual._route_to_v2_if_needed("get_page_by_id", "123")

        assert result is None

    @patch.object(ConfluenceCloudV2, "__init__", side_effect=Exception("Init failed"))
    def test_route_to_v2_if_needed_init_failure(self, mock_init, confluence_dual):
        """Test routing when v2 client initialization fails."""
        confluence_dual.enable_v2_api()

        result = confluence_dual._route_to_v2_if_needed("get_page_by_id", "123")

        assert result is None


class TestDualAPIContentOperations:
    """Test cases for content operations with dual API support."""

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_v1_fallback(self, mock_get, confluence_dual):
        """Test get_content falls back to v1 API by default."""
        mock_get.return_value = {"id": "123", "title": "Test Page"}

        result = confluence_dual.get_content("123")

        mock_get.assert_called_once_with("content/123")
        assert result == {"id": "123", "title": "Test Page"}

    @patch.object(ConfluenceCloudV2, "get_page_by_id")
    def test_get_content_v2_routing(self, mock_v2_method, confluence_v2_enabled):
        """Test get_content routes to v2 API when enabled."""
        mock_v2_method.return_value = {"id": "123", "title": "Test Page"}

        result = confluence_v2_enabled.get_content("123", expand=["body"])

        mock_v2_method.assert_called_once_with("123", expand=["body"])
        assert result == {"id": "123", "title": "Test Page"}

    @patch.object(ConfluenceCloud, "get")
    @patch.object(ConfluenceCloudV2, "get_pages")
    def test_get_content_by_type_v2_routing_pages(self, mock_v2_method, mock_v1_get, confluence_v2_enabled):
        """Test get_content_by_type routes to v2 API for pages."""
        mock_v2_method.return_value = {"results": [{"id": "123", "title": "Test Page"}]}

        result = confluence_v2_enabled.get_content_by_type("page", space="TEST")

        mock_v2_method.assert_called_once_with(space="TEST")
        mock_v1_get.assert_not_called()
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_by_type_v1_fallback_blogpost(self, mock_get, confluence_v2_enabled):
        """Test get_content_by_type falls back to v1 API for non-page types."""
        mock_get.return_value = {"results": [{"id": "456", "title": "Test Blog"}]}

        result = confluence_v2_enabled.get_content_by_type("blogpost", space="TEST")

        mock_get.assert_called_once_with("content", params={"type": "blogpost", "space": "TEST"})
        assert result == {"results": [{"id": "456", "title": "Test Blog"}]}

    @patch.object(ConfluenceCloud, "post")
    @patch.object(ConfluenceCloudV2, "create_page")
    def test_create_content_v2_routing_page(self, mock_v2_method, mock_v1_post, confluence_v2_enabled):
        """Test create_content routes to v2 API for page creation."""
        mock_v2_method.return_value = {"id": "123", "title": "New Page"}

        page_data = {
            "type": "page",
            "title": "New Page",
            "space": {"id": "SPACE123"},
            "body": {"storage": {"value": "<p>Content</p>"}},
        }

        result = confluence_v2_enabled.create_content(page_data)

        mock_v2_method.assert_called_once_with("SPACE123", "New Page", "<p>Content</p>", None)
        mock_v1_post.assert_not_called()
        assert result == {"id": "123", "title": "New Page"}

    @patch.object(ConfluenceCloud, "post")
    def test_create_content_v1_fallback_non_page(self, mock_post, confluence_v2_enabled):
        """Test create_content falls back to v1 API for non-page content."""
        mock_post.return_value = {"id": "456", "title": "New Blog"}

        blog_data = {"type": "blogpost", "title": "New Blog", "space": {"key": "TEST"}}

        result = confluence_v2_enabled.create_content(blog_data)

        mock_post.assert_called_once_with("content", data=blog_data)
        assert result == {"id": "456", "title": "New Blog"}


class TestDualAPISpaceOperations:
    """Test cases for space operations with dual API support."""

    @patch.object(ConfluenceCloud, "get")
    def test_get_spaces_v1_fallback(self, mock_get, confluence_dual):
        """Test get_spaces falls back to v1 API by default."""
        mock_get.return_value = {"results": [{"key": "TEST", "name": "Test Space"}]}

        result = confluence_dual.get_spaces()

        mock_get.assert_called_once_with("wiki/rest/api/latest/space")
        assert result == {"results": [{"key": "TEST", "name": "Test Space"}]}

    @patch.object(ConfluenceCloudV2, "get_spaces")
    def test_get_spaces_v2_routing(self, mock_v2_method, confluence_v2_enabled):
        """Test get_spaces routes to v2 API when enabled."""
        mock_v2_method.return_value = {"results": [{"id": "SPACE123", "key": "TEST"}]}

        result = confluence_v2_enabled.get_spaces(limit=50)

        mock_v2_method.assert_called_once_with(limit=50)
        assert result == {"results": [{"id": "SPACE123", "key": "TEST"}]}


class TestDualAPISearchOperations:
    """Test cases for search operations with dual API support."""

    @patch.object(ConfluenceCloud, "get")
    def test_search_content_v1_fallback(self, mock_get, confluence_dual):
        """Test search_content falls back to v1 API by default."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Search Result"}]}

        result = confluence_dual.search_content("type=page")

        mock_get.assert_called_once_with("content/search", params={"cql": "type=page"})
        assert result == {"results": [{"id": "123", "title": "Search Result"}]}

    @patch.object(ConfluenceCloudV2, "search_pages")
    def test_search_content_v2_routing(self, mock_v2_method, confluence_v2_enabled):
        """Test search_content routes to v2 API when enabled."""
        mock_v2_method.return_value = {"results": [{"id": "123", "title": "Search Result"}]}

        result = confluence_v2_enabled.search_content("type=page", limit=50)

        mock_v2_method.assert_called_once_with("type=page", limit=50)
        assert result == {"results": [{"id": "123", "title": "Search Result"}]}

    @patch("warnings.warn")
    def test_search_content_migration_warning(self, mock_warn, confluence_dual):
        """Test search_content issues migration warning for large result sets."""
        with patch.object(confluence_dual, "get") as mock_get:
            mock_get.return_value = {"results": []}

            # Should trigger warning for large limit
            confluence_dual.search_content("type=page", limit=100)

            mock_warn.assert_called_once()
            warning_message = mock_warn.call_args[0][0]
            assert "search_pages_with_cursor" in warning_message
            assert "cursor-based pagination" in warning_message


class TestDualAPIConvenienceMethods:
    """Test cases for v2 API convenience methods."""

    @patch.object(ConfluenceCloudV2, "create_page")
    def test_create_page_with_adf(self, mock_create, confluence_dual, sample_adf_content):
        """Test create_page_with_adf convenience method."""
        mock_create.return_value = {"id": "123", "title": "ADF Page"}

        result = confluence_dual.create_page_with_adf("SPACE123", "ADF Page", sample_adf_content, "parent123")

        mock_create.assert_called_once_with("SPACE123", "ADF Page", sample_adf_content, "parent123", "adf")
        assert result == {"id": "123", "title": "ADF Page"}

    def test_create_page_with_adf_no_v2_client(self, confluence_dual):
        """Test create_page_with_adf raises error when v2 client unavailable."""
        # Mock v2 client initialization to fail
        with patch.object(confluence_dual, "_init_v2_client") as mock_init:
            mock_init.return_value = None
            confluence_dual._v2_client = None

            with pytest.raises(RuntimeError, match="v2 API client not available"):
                confluence_dual.create_page_with_adf("SPACE123", "Title", {})

    @patch.object(ConfluenceCloudV2, "update_page")
    def test_update_page_with_adf(self, mock_update, confluence_dual, sample_adf_content):
        """Test update_page_with_adf convenience method."""
        mock_update.return_value = {"id": "123", "title": "Updated ADF Page"}

        result = confluence_dual.update_page_with_adf("123", "Updated ADF Page", sample_adf_content, version=2)

        mock_update.assert_called_once_with("123", "Updated ADF Page", sample_adf_content, "adf", 2)
        assert result == {"id": "123", "title": "Updated ADF Page"}

    @patch.object(ConfluenceCloudV2, "get_page_by_id")
    def test_get_page_with_adf(self, mock_get, confluence_dual):
        """Test get_page_with_adf convenience method."""
        mock_get.return_value = {"id": "123", "title": "ADF Page", "body": {"value": {}}}

        result = confluence_dual.get_page_with_adf("123", expand=["body", "version"])

        mock_get.assert_called_once_with("123", ["body", "version"])
        assert result == {"id": "123", "title": "ADF Page", "body": {"value": {}}}

    @patch.object(ConfluenceCloudV2, "search_pages")
    def test_search_pages_with_cursor(self, mock_search, confluence_dual):
        """Test search_pages_with_cursor convenience method."""
        mock_search.return_value = {"results": [{"id": "123"}], "_links": {"next": {"cursor": "next_cursor"}}}

        result = confluence_dual.search_pages_with_cursor("type=page AND space=TEST", limit=50, cursor="test_cursor")

        mock_search.assert_called_once_with("type=page AND space=TEST", 50, "test_cursor")
        assert result["results"] == [{"id": "123"}]
        assert result["_links"]["next"]["cursor"] == "next_cursor"


class TestDualAPIErrorHandling:
    """Test cases for error handling in dual API operations."""

    @patch.object(ConfluenceCloudV2, "get_page_by_id", side_effect=Exception("v2 API error"))
    @patch.object(ConfluenceCloud, "get")
    def test_v2_error_fallback_to_v1(self, mock_v1_get, mock_v2_get, confluence_v2_enabled):
        """Test that v2 API errors are properly raised (no automatic fallback)."""
        mock_v1_get.return_value = {"id": "123", "title": "Fallback Result"}

        # The current implementation raises v2 API errors rather than falling back
        # This documents the current behavior - fallback logic could be added later

        with pytest.raises(Exception, match="v2 API error"):
            confluence_v2_enabled.get_content("123")

    def test_v2_client_initialization_failure(self, confluence_dual):
        """Test handling of v2 client initialization failure."""
        with patch.object(ConfluenceCloudV2, "__init__", side_effect=Exception("Init failed")):
            confluence_dual.enable_v2_api()

            # Should handle initialization failure gracefully
            assert confluence_dual._v2_client is None
            assert confluence_dual._prefer_v2_api is True  # Preference should still be set


class TestDualAPIBackwardCompatibility:
    """Test cases for backward compatibility with dual API support."""

    def test_all_v1_methods_present(self, confluence_dual):
        """Test that all v1 API methods are still present and callable."""
        v1_methods = [
            "get_content",
            "get_content_by_type",
            "create_content",
            "update_content",
            "delete_content",
            "get_content_children",
            "get_content_descendants",
            "get_content_ancestors",
            "get_spaces",
            "get_space",
            "create_space",
            "update_space",
            "delete_space",
            "get_users",
            "get_user",
            "get_current_user",
            "get_groups",
            "get_group",
            "get_group_members",
            "search_content",
            "search_spaces",
        ]

        for method_name in v1_methods:
            assert hasattr(confluence_dual, method_name), f"Missing method: {method_name}"
            method = getattr(confluence_dual, method_name)
            assert callable(method), f"Method not callable: {method_name}"

    def test_method_signatures_unchanged(self, confluence_dual):
        """Test that method signatures remain unchanged for backward compatibility."""
        import inspect

        # Test a few key methods to ensure signatures are preserved
        get_content_sig = inspect.signature(confluence_dual.get_content)
        assert "content_id" in get_content_sig.parameters

        create_content_sig = inspect.signature(confluence_dual.create_content)
        assert "data" in create_content_sig.parameters

        search_content_sig = inspect.signature(confluence_dual.search_content)
        assert "query" in search_content_sig.parameters

    @patch.object(ConfluenceCloud, "get")
    def test_existing_code_compatibility(self, mock_get, confluence_dual):
        """Test that existing code patterns continue to work."""
        mock_get.return_value = {"id": "123", "title": "Test Page"}

        # Simulate existing code patterns
        page = confluence_dual.get_content("123", expand="body,version")
        assert page["id"] == "123"

        pages = confluence_dual.get_content_by_type("page", space="TEST", limit=10)  # noqa: F841
        # Should work without modification

        search_results = confluence_dual.search_content("type=page AND space=TEST")  # noqa: F841
        # Should work without modification
