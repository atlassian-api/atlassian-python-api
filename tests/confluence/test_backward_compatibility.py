# coding=utf-8
"""
Test cases for Confluence Cloud backward compatibility validation.

This test suite ensures that all existing method signatures and behaviors
are preserved when dual API support is enabled.
"""

import pytest
import warnings
from unittest.mock import patch

from atlassian.confluence import ConfluenceCloud


@pytest.fixture
def confluence_cloud():
    """Fixture for ConfluenceCloud client with default v1 API behavior."""
    return ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True)


@pytest.fixture
def confluence_cloud_v2_preferred():
    """Fixture for ConfluenceCloud client with v2 API preferred."""
    return ConfluenceCloud(url="https://test.atlassian.net", token="test-token", cloud=True, prefer_v2_api=True)


class TestBackwardCompatibility:
    """Test cases for backward compatibility validation."""

    def test_all_required_methods_exist(self, confluence_cloud):
        """Test that all required methods exist for backward compatibility."""
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
            assert hasattr(confluence_cloud, method_name), f"Missing method: {method_name}"
            assert callable(getattr(confluence_cloud, method_name)), f"Method not callable: {method_name}"

    def test_backward_compatibility_validation_on_init(self):
        """Test that backward compatibility validation runs on initialization."""
        # This should not raise any exceptions
        confluence = ConfluenceCloud(url="https://test.atlassian.net", token="test-token")
        assert confluence is not None

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_signature_preserved(self, mock_get, confluence_cloud):
        """Test that get_content method signature is preserved."""
        mock_get.return_value = {"id": "123", "title": "Test Page"}

        # Test with positional argument
        result = confluence_cloud.get_content("123")
        assert result == {"id": "123", "title": "Test Page"}
        mock_get.assert_called_with("content/123", **{})

        # Test with keyword arguments
        result = confluence_cloud.get_content("123", expand="body,version")
        mock_get.assert_called_with("content/123", expand="body,version")

    @patch.object(ConfluenceCloud, "get")
    def test_get_content_by_type_signature_preserved(self, mock_get, confluence_cloud):
        """Test that get_content_by_type method signature is preserved."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Test Page"}]}

        # Test with positional argument
        result = confluence_cloud.get_content_by_type("page")
        assert result == {"results": [{"id": "123", "title": "Test Page"}]}
        mock_get.assert_called_with("content", params={"type": "page", **{}})

        # Test with keyword arguments
        result = confluence_cloud.get_content_by_type("page", space="TEST", limit=10)
        mock_get.assert_called_with("content", params={"type": "page", "space": "TEST", "limit": 10})

    @patch.object(ConfluenceCloud, "post")
    def test_create_content_signature_preserved(self, mock_post, confluence_cloud):
        """Test that create_content method signature is preserved."""
        content_data = {"title": "New Page", "type": "page", "space": {"key": "TEST"}}
        mock_post.return_value = {"id": "456", "title": "New Page"}

        result = confluence_cloud.create_content(content_data)
        assert result == {"id": "456", "title": "New Page"}
        mock_post.assert_called_with("content", data=content_data, **{})

    @patch.object(ConfluenceCloud, "put")
    def test_update_content_signature_preserved(self, mock_put, confluence_cloud):
        """Test that update_content method signature is preserved."""
        content_data = {"title": "Updated Page", "version": {"number": 2}}
        mock_put.return_value = {"id": "123", "title": "Updated Page"}

        result = confluence_cloud.update_content("123", content_data)
        assert result == {"id": "123", "title": "Updated Page"}
        mock_put.assert_called_with("content/123", data=content_data, **{})

    @patch.object(ConfluenceCloud, "delete")
    def test_delete_content_signature_preserved(self, mock_delete, confluence_cloud):
        """Test that delete_content method signature is preserved."""
        mock_delete.return_value = {"success": True}

        result = confluence_cloud.delete_content("123")
        assert result == {"success": True}
        mock_delete.assert_called_with("content/123", **{})

    @patch.object(ConfluenceCloud, "get")
    def test_search_content_signature_preserved(self, mock_get, confluence_cloud):
        """Test that search_content method signature is preserved."""
        mock_get.return_value = {"results": [{"id": "123", "title": "Search Result"}]}

        # Test basic search
        result = confluence_cloud.search_content("type=page")
        assert result == {"results": [{"id": "123", "title": "Search Result"}]}
        mock_get.assert_called_with("content/search", params={"cql": "type=page", **{}})

        # Test with additional parameters
        result = confluence_cloud.search_content("type=page", limit=50, start=10)
        mock_get.assert_called_with("content/search", params={"cql": "type=page", "limit": 50, "start": 10})

    def test_deprecation_warning_for_large_pagination(self, confluence_cloud):
        """Test that deprecation warning is issued for large pagination requests."""
        with patch.object(confluence_cloud, "get") as mock_get:
            mock_get.return_value = {"results": []}

            # Should issue warning for large limit
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                confluence_cloud.search_content("type=page", limit=100)

                assert len(w) == 1
                assert issubclass(w[0].category, FutureWarning)
                assert "search_pages_with_cursor" in str(w[0].message)
                assert "cursor-based pagination" in str(w[0].message)

    def test_no_deprecation_warning_with_v2_enabled(self, confluence_cloud_v2_preferred):
        """Test that no deprecation warning is issued when v2 API is preferred."""
        # Mock the v2 client to avoid actual HTTP requests
        with patch.object(confluence_cloud_v2_preferred, "_v2_client") as mock_v2_client:
            mock_v2_client.search_pages.return_value = {"results": []}

            # Should NOT issue warning when v2 is preferred
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                confluence_cloud_v2_preferred.search_content("type=page", limit=100)

                # No warnings should be issued
                assert len(w) == 0

    def test_api_version_info_method_exists(self, confluence_cloud):
        """Test that get_api_version_info method exists and returns expected structure."""
        info = confluence_cloud.get_api_version_info()

        assert isinstance(info, dict)
        assert "v1_available" in info
        assert "v2_available" in info
        assert "force_v2_api" in info
        assert "prefer_v2_api" in info
        assert "current_default" in info

        # Default configuration should prefer v1
        assert info["v1_available"] is True
        assert info["force_v2_api"] is False
        assert info["prefer_v2_api"] is False
        assert info["current_default"] == "v1"

    def test_v2_convenience_methods_exist(self, confluence_cloud):
        """Test that v2 convenience methods exist for enhanced functionality."""
        v2_methods = ["create_page_with_adf", "update_page_with_adf", "get_page_with_adf", "search_pages_with_cursor"]

        for method_name in v2_methods:
            assert hasattr(confluence_cloud, method_name), f"Missing v2 method: {method_name}"
            assert callable(getattr(confluence_cloud, method_name)), f"v2 method not callable: {method_name}"

    def test_enable_disable_v2_api_methods(self, confluence_cloud):
        """Test that v2 API can be enabled and disabled."""
        # Initially should be v1
        info = confluence_cloud.get_api_version_info()
        assert info["current_default"] == "v1"

        # Enable v2 API
        confluence_cloud.enable_v2_api()
        info = confluence_cloud.get_api_version_info()
        assert info["prefer_v2_api"] is True

        # Force v2 API
        confluence_cloud.enable_v2_api(force=True)
        info = confluence_cloud.get_api_version_info()
        assert info["force_v2_api"] is True
        assert info["prefer_v2_api"] is True

        # Disable v2 API
        confluence_cloud.disable_v2_api()
        info = confluence_cloud.get_api_version_info()
        assert info["force_v2_api"] is False
        assert info["prefer_v2_api"] is False

    def test_method_return_types_unchanged(self, confluence_cloud):
        """Test that method return types remain unchanged for backward compatibility."""
        with patch.object(confluence_cloud, "get") as mock_get:
            # Test that methods return the same data structures
            expected_content = {"id": "123", "title": "Test Page", "type": "page"}
            mock_get.return_value = expected_content

            result = confluence_cloud.get_content("123")
            assert result == expected_content
            assert isinstance(result, dict)

            # Test list results
            expected_list = {"results": [{"id": "123", "title": "Test Page"}]}
            mock_get.return_value = expected_list

            result = confluence_cloud.get_content_by_type("page")
            assert result == expected_list
            assert isinstance(result, dict)
            assert "results" in result
            assert isinstance(result["results"], list)

    def test_error_handling_unchanged(self, confluence_cloud):
        """Test that error handling behavior remains unchanged."""
        with patch.object(confluence_cloud, "get") as mock_get:
            # Test that exceptions are still raised as expected
            mock_get.side_effect = Exception("Test error")

            with pytest.raises(Exception, match="Test error"):
                confluence_cloud.get_content("123")

    def test_parameter_passing_unchanged(self, confluence_cloud):
        """Test that parameter passing behavior remains unchanged."""
        with patch.object(confluence_cloud, "get") as mock_get:
            mock_get.return_value = {"results": []}

            # Test that all parameter types are handled correctly
            confluence_cloud.get_content("123", expand="body,version", status="current")
            mock_get.assert_called_with("content/123", expand="body,version", status="current")

            # Test with mixed parameter types
            confluence_cloud.search_content("type=page", limit=25, start=0, expand=["body"])
            mock_get.assert_called_with(
                "content/search", params={"cql": "type=page", "limit": 25, "start": 0, "expand": ["body"]}
            )
