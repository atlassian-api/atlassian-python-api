# coding=utf-8
import unittest
from unittest.mock import patch, MagicMock, mock_open

from atlassian import Confluence, ConfluenceBase, ConfluenceCloud, create_confluence
from atlassian.confluence.cloud import ConfluenceCloud as ConcreteConfluenceCloud
from atlassian.confluence.server import ConfluenceServer


# Use ConfluenceCloud as it is the actual implementation (ConfluenceV2 is just an alias)
class TestConfluenceBase(unittest.TestCase):
    """Test cases for ConfluenceBase implementation"""

    def test_is_cloud_url(self):
        """Test the _is_cloud_url method"""
        # Valid URLs
        self.assertTrue(ConfluenceBase._is_cloud_url("https://example.atlassian.net"))
        self.assertTrue(ConfluenceBase._is_cloud_url("https://example.atlassian.net/wiki"))
        self.assertTrue(ConfluenceBase._is_cloud_url("https://example.jira.com"))

        # Invalid URLs
        self.assertFalse(ConfluenceBase._is_cloud_url("https://example.com"))
        self.assertFalse(ConfluenceBase._is_cloud_url("https://evil.com?atlassian.net"))
        self.assertFalse(ConfluenceBase._is_cloud_url("https://atlassian.net.evil.com"))
        self.assertFalse(ConfluenceBase._is_cloud_url("ftp://example.atlassian.net"))
        self.assertFalse(ConfluenceBase._is_cloud_url("not a url"))

    def test_init_with_api_version_1(self):
        """Test initialization with API version 1"""
        client = Confluence("https://example.atlassian.net", api_version=1)
        self.assertEqual(client.api_version, 1)
        self.assertEqual(client.url, "https://example.atlassian.net/wiki")

    def test_init_with_api_version_2(self):
        """Test initialization with API version 2"""
        client = Confluence("https://example.atlassian.net", api_version=2)
        self.assertEqual(client.api_version, 2)
        self.assertEqual(client.url, "https://example.atlassian.net/wiki")

    def test_get_endpoint_v1(self):
        """Test retrieving v1 endpoint"""
        client = Confluence("https://example.atlassian.net", api_version=1)
        endpoint = client.get_endpoint("content")
        self.assertEqual(endpoint, "rest/api/content")

    def test_get_endpoint_v2(self):
        """Test retrieving v2 endpoint"""
        client = Confluence("https://example.atlassian.net", api_version=2)
        endpoint = client.get_endpoint("content")
        self.assertEqual(endpoint, "api/v2/pages")

    def test_invalid_api_version(self):
        """Test raising error with invalid API version"""
        with self.assertRaises(ValueError):
            ConfluenceBase("https://example.atlassian.net", api_version=3)

    @patch("atlassian.confluence.base.ConfluenceBase._is_cloud_url")
    def test_factory_v1(self, mock_is_cloud):
        """Test factory method creating v1 client"""
        # Force to use cloud URL to make testing consistent
        mock_is_cloud.return_value = True

        client = ConfluenceBase.factory("https://example.atlassian.net", api_version=1)
        # Since this returns ConfluenceCloud which always uses api_version=2
        self.assertIsInstance(client, ConcreteConfluenceCloud)
        # Note: For cloud URLs, this will always be 2 in the current implementation
        self.assertEqual(client.api_version, 2)

    def test_factory_v2(self):
        """Test factory method creating v2 client"""
        client = ConfluenceBase.factory("https://example.atlassian.net", api_version=2)
        # Direct checking against the concrete class
        self.assertIsInstance(client, ConcreteConfluenceCloud)
        self.assertEqual(client.api_version, 2)

    @patch("atlassian.confluence.base.ConfluenceBase._is_cloud_url")
    def test_factory_default(self, mock_is_cloud):
        """Test factory method with default version"""
        # Force to use cloud URL to make testing consistent
        mock_is_cloud.return_value = True

        client = ConfluenceBase.factory("https://example.atlassian.net")
        # Since this returns ConfluenceCloud which always uses api_version=2
        self.assertIsInstance(client, ConcreteConfluenceCloud)
        # Note: For cloud URLs, this will always be 2 in the current implementation
        self.assertEqual(client.api_version, 2)

    @patch("atlassian.confluence.base.ConfluenceBase._is_cloud_url")
    def test_create_confluence_function_v1(self, mock_is_cloud):
        """Test create_confluence function with v1"""
        # Force to use cloud URL to make testing consistent
        mock_is_cloud.return_value = True

        client = create_confluence("https://example.atlassian.net", api_version=1)
        # Since this returns ConfluenceCloud which always uses api_version=2
        self.assertIsInstance(client, ConcreteConfluenceCloud)
        # Note: For cloud URLs, this will always be 2 in the current implementation
        self.assertEqual(client.api_version, 2)

    def test_create_confluence_function_v2(self):
        """Test create_confluence function with v2"""
        client = create_confluence("https://example.atlassian.net", api_version=2)
        # Direct checking against the concrete class
        self.assertIsInstance(client, ConcreteConfluenceCloud)
        self.assertEqual(client.api_version, 2)

    @patch("atlassian.rest_client.AtlassianRestAPI.get")
    def test_get_paged_v1(self, mock_get):
        """Test pagination with v1 API"""
        # Mock response for first page
        first_response = {
            "results": [{"id": "1", "title": "Page 1"}],
            "start": 0,
            "limit": 1,
            "size": 1,
            "_links": {"next": "/rest/api/content?start=1&limit=1"},
        }

        # Mock response for second page
        second_response = {"results": [{"id": "2", "title": "Page 2"}], "start": 1, "limit": 1, "size": 1, "_links": {}}

        # Set up mock to return responses in sequence
        mock_get.side_effect = [first_response, second_response]

        # Create client
        client = ConfluenceBase("https://example.atlassian.net", api_version=1)
        endpoint = "/rest/api/content"
        params = {"limit": 1}

        # Call _get_paged and collect results
        results = list(client._get_paged(endpoint, params=params))

        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "1")
        self.assertEqual(results[1]["id"], "2")

        # Verify the API was called correctly
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(
            "/rest/api/content", params={"limit": 1}, data=None, flags=None, trailing=None, absolute=False
        )

    @patch("atlassian.rest_client.AtlassianRestAPI.get")
    def test_get_paged_v2(self, mock_get):
        """Test pagination with v2 API"""
        # Mock response for first page
        first_response = {
            "results": [{"id": "1", "title": "Page 1"}],
            "_links": {"next": "/api/v2/pages?cursor=next_cursor"},
        }

        # Mock response for second page
        second_response = {"results": [{"id": "2", "title": "Page 2"}], "_links": {}}

        # Set up mock to return responses in sequence
        mock_get.side_effect = [first_response, second_response]

        # Create client
        client = ConfluenceBase("https://example.atlassian.net", api_version=2)
        endpoint = "/api/v2/pages"
        params = {"limit": 1}

        # Call _get_paged and collect results
        results = list(client._get_paged(endpoint, params=params))

        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "1")
        self.assertEqual(results[1]["id"], "2")

        # Verify the API was called correctly
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(
            "/api/v2/pages", params={"limit": 1}, data=None, flags=None, trailing=None, absolute=False
        )


class TestConfluenceV2(unittest.TestCase):
    """Test cases for ConfluenceV2 implementation (using ConfluenceCloud)"""

    def test_init(self):
        """Test ConfluenceV2 initialization sets correct API version"""
        client = ConfluenceCloud("https://example.atlassian.net")
        self.assertEqual(client.api_version, 2)
        self.assertEqual(client.url, "https://example.atlassian.net/wiki")

    def test_init_with_explicit_version(self):
        """Test ConfluenceV2 initialization with explicit API version"""
        # This actually is just calling ConfluenceCloud directly so always uses v2
        client = ConfluenceCloud("https://example.atlassian.net", api_version=2)
        self.assertEqual(client.api_version, 2)

        # The v2 client actually uses the version provided when called directly
        # (even though when used as ConfluenceV2 alias, it would force v2)
        client = ConfluenceCloud("https://example.atlassian.net", api_version=1)
        self.assertEqual(client.api_version, 1)  # This actually matches behavior


if __name__ == "__main__":
    unittest.main()
