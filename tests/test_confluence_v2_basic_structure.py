#!/usr/bin/env python3
"""
Basic structure tests for the Confluence v2 API implementation.
Tests the class structure, inheritance, and endpoint handling.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock

from atlassian import ConfluenceV2
from atlassian.confluence_base import ConfluenceBase


class TestConfluenceV2BasicStructure(unittest.TestCase):
    """Test case for the basic structure of the ConfluenceV2 class."""

    def setUp(self):
        """Set up the test case."""
        self.confluence = ConfluenceV2(
            url="https://example.atlassian.net/wiki",
            username="username",
            password="password",
        )

    def test_inheritance(self):
        """Test that ConfluenceV2 inherits from ConfluenceBase."""
        self.assertIsInstance(self.confluence, ConfluenceBase)

    def test_api_version(self):
        """Test that the API version is set to 2."""
        self.assertEqual(self.confluence.api_version, 2)

    def test_core_method_presence(self):
        """Test that core methods are present."""
        core_methods = [
            "get_page_by_id",
            "get_pages",
            "get_child_pages",
            "create_page",
            "update_page",
            "delete_page",
            "get_spaces",
            "get_space",
            "search",
        ]

        for method_name in core_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_property_method_presence(self):
        """Test that property methods are present."""
        property_methods = [
            "get_page_properties",
            "get_page_property_by_key",
            "create_page_property",
            "update_page_property",
            "delete_page_property",
        ]

        for method_name in property_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_label_method_presence(self):
        """Test that label methods are present."""
        label_methods = [
            "get_page_labels",
            "add_page_label",
            "delete_page_label",
            "get_space_labels",
            "add_space_label",
            "delete_space_label",
        ]

        for method_name in label_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_comment_method_presence(self):
        """Test that comment methods are present."""
        comment_methods = [
            "get_comment_by_id",
            "get_page_footer_comments",
            "get_page_inline_comments",
            "create_page_footer_comment",
            "create_page_inline_comment",
            "update_comment",
            "delete_comment",
        ]

        for method_name in comment_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_whiteboard_method_presence(self):
        """Test that whiteboard methods are present."""
        whiteboard_methods = [
            "get_whiteboard_by_id",
            "get_whiteboard_ancestors",
            "get_whiteboard_children",
            "create_whiteboard",
            "delete_whiteboard",
        ]

        for method_name in whiteboard_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_custom_content_method_presence(self):
        """Test that custom content methods are present."""
        custom_content_methods = [
            "get_custom_content_by_id",
            "get_custom_content",
            "create_custom_content",
            "update_custom_content",
            "delete_custom_content",
            "get_custom_content_properties",
            "get_custom_content_property_by_key",
            "create_custom_content_property",
            "update_custom_content_property",
            "delete_custom_content_property",
        ]

        for method_name in custom_content_methods:
            self.assertTrue(hasattr(self.confluence, method_name), f"Method {method_name} not found in ConfluenceV2")

    def test_compatibility_layer_presence(self):
        """Test that compatibility layer methods are present."""
        compat_methods = ["get_content_by_id", "get_content", "create_content", "update_content", "delete_content"]

        for method_name in compat_methods:
            self.assertTrue(
                hasattr(self.confluence, method_name), f"Compatibility method {method_name} not found in ConfluenceV2"
            )

    @patch.object(ConfluenceV2, "get")
    def test_endpoint_handling(self, mock_get):
        """Test that endpoints are constructed correctly for v2 API."""
        # Configure the mock
        mock_get.return_value = {"id": "123456"}

        # Test method that uses v2 endpoint
        self.confluence.get_page_by_id("123456")

        # Verify the correct endpoint was used
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        self.assertEqual(args[0], "api/v2/pages/123456")


if __name__ == "__main__":
    unittest.main()
