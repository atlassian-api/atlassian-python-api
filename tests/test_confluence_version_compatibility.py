#!/usr/bin/env python3
"""
Tests for compatibility between Confluence v1 and v2 APIs.
This tests backward compatibility and consistent method behavior between both API versions.
"""

import json
import unittest
from unittest.mock import patch, Mock, MagicMock

from atlassian import Confluence
from atlassian import ConfluenceV2


class TestConfluenceVersionCompatibility(unittest.TestCase):
    """Test case for checking compatibility between Confluence API versions."""

    def setUp(self):
        """Set up the test case."""
        # Initialize both API versions
        self.confluence_v1 = Confluence(
            url="https://example.atlassian.net/wiki", username="username", password="password", api_version=1
        )

        self.confluence_v2 = ConfluenceV2(
            url="https://example.atlassian.net/wiki", username="username", password="password"
        )

        # Create mocks for the underlying rest client methods
        self.mock_response_v1 = MagicMock()
        self.mock_response_v1.headers = {}
        self.mock_response_v1.reason = "OK"
        self.confluence_v1._session = MagicMock()
        self.confluence_v1._session.request.return_value = self.mock_response_v1

        self.mock_response_v2 = MagicMock()
        self.mock_response_v2.headers = {}
        self.mock_response_v2.reason = "OK"
        self.confluence_v2._session = MagicMock()
        self.confluence_v2._session.request.return_value = self.mock_response_v2

    def test_v1_and_v2_method_availability(self):
        """Test that v1 methods are available in both API versions."""
        # List of key methods that should be available in both API versions
        # Only include methods that are definitely in v1 API
        key_methods = [
            "get_page_by_id",
            "create_page",
            "update_page",
            "get_page_space",
            "get_page_properties",
            "add_label",
            "get_all_spaces",
            "create_space",
            "get_space",
        ]

        for method_name in key_methods:
            # Check that both v1 and v2 instances have the method
            self.assertTrue(hasattr(self.confluence_v1, method_name), f"Method {method_name} not found in v1 API")
            self.assertTrue(hasattr(self.confluence_v2, method_name), f"Method {method_name} not found in v2 API")

        # Test that v2 has compatibility methods
        compat_methods = ["get_content_by_id", "get_content", "get_content_property"]

        for method_name in compat_methods:
            self.assertTrue(
                hasattr(self.confluence_v2, method_name), f"Compatibility method {method_name} not found in v2 API"
            )

    def test_get_page_by_id_compatibility(self):
        """Test that get_page_by_id works similarly in both API versions."""
        page_id = "123456"

        # Configure v1 mock response
        v1_response = {
            "id": page_id,
            "type": "page",
            "title": "Test Page",
            "version": {"number": 1},
            "body": {"storage": {"value": "<p>Test content</p>", "representation": "storage"}},
            "space": {"key": "TEST", "id": "789012"},
        }
        self.mock_response_v1.status_code = 200
        self.mock_response_v1.text = json.dumps(v1_response)
        self.mock_response_v1.json.return_value = v1_response

        # Configure v2 mock response
        v2_response = {
            "id": page_id,
            "title": "Test Page",
            "version": {"number": 1},
            "body": {"storage": {"value": "<p>Test content</p>", "representation": "storage"}},
            "spaceId": "789012",
            "status": "current",
        }
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Call methods on both API versions
        v1_result = self.confluence_v1.get_page_by_id(page_id)
        v2_result = self.confluence_v2.get_page_by_id(page_id)

        # Verify the results have expected common properties
        self.assertEqual(v1_result["id"], v2_result["id"])
        self.assertEqual(v1_result["title"], v2_result["title"])
        self.assertEqual(v1_result["version"]["number"], v2_result["version"]["number"])
        self.assertEqual(v1_result["body"]["storage"]["value"], v2_result["body"]["storage"]["value"])

    def test_create_page_compatibility(self):
        """Test that create_page works similarly in both API versions."""
        space_key = "TEST"
        space_id = "789012"
        title = "New Test Page"
        body = "<p>Test content</p>"

        # Configure v1 mock response
        v1_response = {
            "id": "123456",
            "type": "page",
            "title": title,
            "version": {"number": 1},
            "body": {"storage": {"value": body, "representation": "storage"}},
            "space": {"key": space_key, "id": space_id},
        }
        self.mock_response_v1.status_code = 200
        self.mock_response_v1.text = json.dumps(v1_response)
        self.mock_response_v1.json.return_value = v1_response

        # Configure v2 mock response
        v2_response = {
            "id": "123456",
            "title": title,
            "version": {"number": 1},
            "body": {"storage": {"value": body, "representation": "storage"}},
            "spaceId": space_id,
            "status": "current",
        }
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Call methods on both API versions
        v1_result = self.confluence_v1.create_page(space=space_key, title=title, body=body)

        v2_result = self.confluence_v2.create_page(
            space_id=space_id, title=title, body=body  # v2 uses space_id instead of space_key
        )

        # Verify the results have expected common properties
        self.assertEqual(v1_result["id"], v2_result["id"])
        self.assertEqual(v1_result["title"], v2_result["title"])
        self.assertEqual(v1_result["version"]["number"], v2_result["version"]["number"])
        self.assertEqual(v1_result["body"]["storage"]["value"], v2_result["body"]["storage"]["value"])

    def test_get_all_spaces_compatibility(self):
        """Test that get_all_spaces works similarly in both API versions."""
        # Configure v1 mock response
        v1_response = {
            "results": [
                {"id": "123456", "key": "TEST", "name": "Test Space", "type": "global"},
                {"id": "789012", "key": "DEV", "name": "Development Space", "type": "global"},
            ],
            "start": 0,
            "limit": 25,
            "size": 2,
            "_links": {"self": "https://example.atlassian.net/wiki/rest/api/space"},
        }
        self.mock_response_v1.status_code = 200
        self.mock_response_v1.text = json.dumps(v1_response)
        self.mock_response_v1.json.return_value = v1_response

        # Configure v2 mock response - v2 returns list directly, not in "results" key
        v2_response = [
            {"id": "123456", "key": "TEST", "name": "Test Space"},
            {"id": "789012", "key": "DEV", "name": "Development Space"},
        ]
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Call methods on both API versions
        v1_result = self.confluence_v1.get_all_spaces()
        v2_result = self.confluence_v2.get_all_spaces()

        # Verify the results have expected number of spaces
        self.assertEqual(len(v1_result["results"]), len(v2_result))

        # Verify spaces have common properties
        for i in range(len(v1_result["results"])):
            self.assertEqual(v1_result["results"][i]["id"], v2_result[i]["id"])
            self.assertEqual(v1_result["results"][i]["key"], v2_result[i]["key"])
            self.assertEqual(v1_result["results"][i]["name"], v2_result[i]["name"])

    def test_properties_compatibility(self):
        """Test that content properties methods work similarly in both versions."""
        content_id = "123456"

        # Configure v1 mock response - using the correct v1 method
        v1_response = {
            "results": [
                {"id": "1", "key": "test-property", "value": {"key": "value"}, "version": {"number": 1}},
                {"id": "2", "key": "another-property", "value": {"another": "value"}, "version": {"number": 1}},
            ],
            "start": 0,
            "limit": 25,
            "size": 2,
            "_links": {"self": f"https://example.atlassian.net/wiki/rest/api/content/{content_id}/property"},
        }
        self.mock_response_v1.status_code = 200
        self.mock_response_v1.text = json.dumps(v1_response)
        self.mock_response_v1.json.return_value = v1_response

        # Configure v2 mock response
        v2_response = [
            {"id": "1", "key": "test-property", "value": {"key": "value"}, "version": {"number": 1}},
            {"id": "2", "key": "another-property", "value": {"another": "value"}, "version": {"number": 1}},
        ]
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Call methods on both API versions
        # For v1, we have to use the property API endpoint
        v1_result = self.confluence_v1.get_page_properties(content_id)
        v2_result = self.confluence_v2.get_page_properties(content_id)

        # For v1, results is a key in the response, for v2 the response is the list directly
        if "results" in v1_result:
            v1_properties = v1_result["results"]
        else:
            v1_properties = v1_result

        # Verify the results have expected properties
        self.assertEqual(len(v1_properties), len(v2_result))
        for i in range(len(v1_properties)):
            self.assertEqual(v1_properties[i]["key"], v2_result[i]["key"])
            self.assertEqual(v1_properties[i]["value"], v2_result[i]["value"])

    def test_labels_compatibility(self):
        """Test that label methods work similarly in both API versions."""
        content_id = "123456"

        # Configure v1 mock response
        v1_response = {
            "results": [
                {"prefix": "global", "name": "test-label", "id": "1"},
                {"prefix": "global", "name": "another-label", "id": "2"},
            ],
            "start": 0,
            "limit": 25,
            "size": 2,
            "_links": {"self": f"https://example.atlassian.net/wiki/rest/api/content/{content_id}/label"},
        }
        self.mock_response_v1.status_code = 200
        self.mock_response_v1.text = json.dumps(v1_response)
        self.mock_response_v1.json.return_value = v1_response

        # Configure v2 mock response - v2 returns list directly
        v2_response = [
            {"id": "1", "name": "test-label", "prefix": "global"},
            {"id": "2", "name": "another-label", "prefix": "global"},
        ]
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Call methods on both API versions
        v1_result = self.confluence_v1.get_page_labels(content_id)
        v2_result = self.confluence_v2.get_page_labels(content_id)

        # Verify the results have expected properties
        self.assertEqual(len(v1_result["results"]), len(v2_result))
        for i in range(len(v1_result["results"])):
            self.assertEqual(v1_result["results"][i]["id"], v2_result[i]["id"])
            self.assertEqual(v1_result["results"][i]["name"], v2_result[i]["name"])
            self.assertEqual(v1_result["results"][i]["prefix"], v2_result[i]["prefix"])

    def test_v2_used_via_v1_interface(self):
        """
        Test that ConfluenceV2 instance can be used with v1 method names
        through the compatibility layer.
        """
        page_id = "123456"

        # Configure v2 mock response
        v2_response = {
            "id": page_id,
            "title": "Test Page",
            "version": {"number": 1},
            "body": {"storage": {"value": "<p>Test content</p>", "representation": "storage"}},
            "spaceId": "789012",
            "status": "current",
        }
        self.mock_response_v2.status_code = 200
        self.mock_response_v2.text = json.dumps(v2_response)
        self.mock_response_v2.json.return_value = v2_response

        # Use v1 method name on v2 instance
        result = self.confluence_v2.get_content_by_id(page_id)

        # Verify the result is as expected
        self.assertEqual(result["id"], page_id)

        # Verify that a request was made
        self.confluence_v2._session.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
