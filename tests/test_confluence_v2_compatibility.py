#!/usr/bin/env python3
"""Tests for the Confluence V2 API compatibility layer."""

import unittest
import warnings
from unittest.mock import MagicMock, patch

from atlassian import ConfluenceV2


class TestConfluenceV2Compatibility(unittest.TestCase):
    """Test case for ConfluenceV2 compatibility layer."""

    def setUp(self):
        """Set up the test case."""
        self.confluence_v2 = ConfluenceV2(
            url="https://example.atlassian.net/wiki",
            username="username",
            password="password",
        )

    def test_method_mapping_exists(self):
        """Test that compatibility method mapping exists."""
        self.assertTrue(hasattr(self.confluence_v2, "_compatibility_method_mapping"))
        self.assertIsInstance(self.confluence_v2._compatibility_method_mapping, dict)
        self.assertGreater(len(self.confluence_v2._compatibility_method_mapping.keys()), 0)

    def test_getattr_for_missing_attribute(self):
        """Test that __getattr__ raises AttributeError for missing attributes."""
        with self.assertRaises(AttributeError):
            self.confluence_v2.nonexistent_method()

    @patch("atlassian.confluence_v2.ConfluenceV2.get_page_by_id")
    def test_get_content_by_id_compatibility(self, mock_get_page_by_id):
        """Test compatibility for get_content_by_id -> get_page_by_id."""
        # Set up the mock
        mock_page = {"id": "123", "title": "Test Page"}
        mock_get_page_by_id.return_value = mock_page

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.get_content_by_id("123")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("get_content_by_id", str(w[0].message))
            self.assertIn("get_page_by_id", str(w[0].message))

        # Verify results
        mock_get_page_by_id.assert_called_once_with("123")
        self.assertEqual(result, mock_page)

    @patch("atlassian.confluence_v2.ConfluenceV2.get_pages")
    def test_get_content_compatibility(self, mock_get_pages):
        """Test compatibility for get_content -> get_pages."""
        # Set up the mock
        mock_pages = [{"id": "123", "title": "Test Page"}]
        mock_get_pages.return_value = mock_pages

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.get_content(space_id="ABC")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("get_content", str(w[0].message))
            self.assertIn("get_pages", str(w[0].message))

        # Verify results
        mock_get_pages.assert_called_once_with(space_id="ABC")
        self.assertEqual(result, mock_pages)

    @patch("atlassian.confluence_v2.ConfluenceV2.get_child_pages")
    def test_get_content_children_compatibility(self, mock_get_child_pages):
        """Test compatibility for get_content_children -> get_child_pages."""
        # Set up the mock
        mock_children = [{"id": "456", "title": "Child Page"}]
        mock_get_child_pages.return_value = mock_children

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.get_content_children("123")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("get_content_children", str(w[0].message))
            self.assertIn("get_child_pages", str(w[0].message))

        # Verify results
        mock_get_child_pages.assert_called_once_with("123")
        self.assertEqual(result, mock_children)

    @patch("atlassian.confluence_v2.ConfluenceV2.create_page")
    def test_create_content_compatibility(self, mock_create_page):
        """Test compatibility for create_content -> create_page."""
        # Set up the mock
        mock_page = {"id": "123", "title": "New Page"}
        mock_create_page.return_value = mock_page

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.create_content(space_id="ABC", title="New Page", body="Content")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("create_content", str(w[0].message))
            self.assertIn("create_page", str(w[0].message))

        # Verify results
        mock_create_page.assert_called_once_with(space_id="ABC", title="New Page", body="Content")
        self.assertEqual(result, mock_page)

    @patch("atlassian.confluence_v2.ConfluenceV2.update_page")
    def test_update_content_compatibility(self, mock_update_page):
        """Test compatibility for update_content -> update_page."""
        # Set up the mock
        mock_page = {"id": "123", "title": "Updated Page"}
        mock_update_page.return_value = mock_page

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.update_content(page_id="123", title="Updated Page", body="Updated content")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("update_content", str(w[0].message))
            self.assertIn("update_page", str(w[0].message))

        # Verify results
        mock_update_page.assert_called_once_with(page_id="123", title="Updated Page", body="Updated content")
        self.assertEqual(result, mock_page)

    @patch("atlassian.confluence_v2.ConfluenceV2.delete_page")
    def test_delete_content_compatibility(self, mock_delete_page):
        """Test compatibility for delete_content -> delete_page."""
        # Set up the mock
        mock_delete_page.return_value = True

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.delete_content("123")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("delete_content", str(w[0].message))
            self.assertIn("delete_page", str(w[0].message))

        # Verify results
        mock_delete_page.assert_called_once_with("123")
        self.assertTrue(result)

    @patch("atlassian.confluence_v2.ConfluenceV2.get_spaces")
    def test_get_all_spaces_compatibility(self, mock_get_spaces):
        """Test compatibility for get_all_spaces -> get_spaces."""
        # Set up the mock
        mock_spaces = [{"id": "ABC", "key": "SPACE1"}]
        mock_get_spaces.return_value = mock_spaces

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.get_all_spaces()

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("get_all_spaces", str(w[0].message))
            self.assertIn("get_spaces", str(w[0].message))

        # Verify results
        mock_get_spaces.assert_called_once_with()
        self.assertEqual(result, mock_spaces)

    @patch("atlassian.confluence_v2.ConfluenceV2.get_space_by_key")
    def test_get_space_by_name_compatibility(self, mock_get_space_by_key):
        """Test compatibility for get_space_by_name -> get_space_by_key."""
        # Set up the mock
        mock_space = {"id": "ABC", "key": "SPACE1"}
        mock_get_space_by_key.return_value = mock_space

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.get_space_by_name("SPACE1")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("get_space_by_name", str(w[0].message))
            self.assertIn("get_space_by_key", str(w[0].message))

        # Verify results
        mock_get_space_by_key.assert_called_once_with("SPACE1")
        self.assertEqual(result, mock_space)

    @patch("atlassian.confluence_v2.ConfluenceV2.add_page_label")
    def test_add_content_label_compatibility(self, mock_add_page_label):
        """Test compatibility for add_content_label -> add_page_label."""
        # Set up the mock
        mock_label = {"id": "L1", "name": "label1"}
        mock_add_page_label.return_value = mock_label

        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Call deprecated method
            result = self.confluence_v2.add_content_label("123", "label1")

            # Verify warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("add_content_label", str(w[0].message))
            self.assertIn("add_page_label", str(w[0].message))

        # Verify results
        mock_add_page_label.assert_called_once_with("123", "label1")
        self.assertEqual(result, mock_label)


if __name__ == "__main__":
    unittest.main()
