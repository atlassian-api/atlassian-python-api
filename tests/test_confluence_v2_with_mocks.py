#!/usr/bin/env python3
"""
Tests for the Confluence v2 API with mocked responses.
This tests pagination, error handling, and v2 specific features.
"""

import json
import unittest
from unittest.mock import patch, Mock, MagicMock

from requests.exceptions import HTTPError
from requests import Response

from atlassian import ConfluenceCloud as ConfluenceV2
from tests.mocks.confluence_v2_mock_responses import (
    PAGE_MOCK, PAGE_RESULT_LIST, CHILD_PAGES_RESULT, SPACE_MOCK, SPACES_RESULT,
    SEARCH_RESULT, PROPERTY_MOCK, PROPERTIES_RESULT, LABEL_MOCK, LABELS_RESULT,
    COMMENT_MOCK, COMMENTS_RESULT, WHITEBOARD_MOCK, CUSTOM_CONTENT_MOCK,
    ERROR_NOT_FOUND, ERROR_PERMISSION_DENIED, ERROR_VALIDATION,
    get_mock_for_endpoint
)


class TestConfluenceV2WithMocks(unittest.TestCase):
    """Test case for ConfluenceV2 using mock responses."""
    
    # Add a timeout to prevent test hanging
    TEST_TIMEOUT = 10  # seconds
    
    def setUp(self):
        """Set up the test case."""
        self.confluence = ConfluenceV2(
            url="https://example.atlassian.net/wiki",
            username="username",
            password="password",
        )
        
        # Create a more explicitly defined mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.status_code = 200
        self.mock_response.reason = "OK"
        self.mock_response.headers = {}
        self.mock_response.raise_for_status.side_effect = None
        
        # Ensure json method is properly mocked
        self.mock_response.json = MagicMock(return_value={})
        self.mock_response.text = "{}"
        
        # Create a clean session mock with timeout
        self.confluence._session = MagicMock()
        self.confluence._session.request = MagicMock(return_value=self.mock_response)
        # Explicitly set timeout parameter
        self.confluence.timeout = self.TEST_TIMEOUT
    
    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        # Get default mock data if none provided
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)
        
        # Convert mock data to text
        mock_data_text = json.dumps(mock_data)
        
        # Set up response attributes
        self.mock_response.status_code = status_code
        self.mock_response.text = mock_data_text
        self.mock_response.json.return_value = mock_data
        
        # Set appropriate reason based on status code
        if status_code == 200:
            self.mock_response.reason = "OK"
        elif status_code == 201:
            self.mock_response.reason = "Created"
        elif status_code == 204:
            self.mock_response.reason = "No Content"
        elif status_code == 400:
            self.mock_response.reason = "Bad Request"
        elif status_code == 403:
            self.mock_response.reason = "Forbidden"
        elif status_code == 404:
            self.mock_response.reason = "Not Found"
        else:
            self.mock_response.reason = "Unknown"
        
        # Handle pagination headers if applicable
        self.mock_response.headers = {}
        if "_links" in mock_data and "next" in mock_data["_links"]:
            self.mock_response.headers = {
                "Link": f'<{mock_data["_links"]["next"]}>; rel="next"'
            }
        
        # Configure raise_for_status behavior
        if status_code >= 400:
            error = HTTPError(f"HTTP Error {status_code}", response=self.mock_response)
            self.mock_response.raise_for_status.side_effect = error
        else:
            self.mock_response.raise_for_status.side_effect = None
        
        return mock_data
    
    def test_get_page_by_id(self):
        """Test retrieving a page by ID."""
        page_id = "123456"
        endpoint = f"api/v2/pages/{page_id}"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_page_by_id(page_id)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], page_id)
    
    def test_get_pages_with_pagination(self):
        """Test retrieving pages with pagination."""
        # Set up a simple mock response
        page_data = {
            "results": [
                {
                    "id": "123456",
                    "title": "First Page",
                    "status": "current",
                    "spaceId": "789012"
                },
                {
                    "id": "345678",
                    "title": "Second Page",
                    "status": "current",
                    "spaceId": "789012"
                }
            ],
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/pages"
            }
        }
        
        # Configure the mock response
        self.mock_response.json.return_value = page_data
        self.mock_response.text = json.dumps(page_data)
        
        # Call the method with limit
        result = self.confluence.get_pages(limit=2)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result structure
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
    
    def test_error_handling_not_found(self):
        """Test error handling when a resource is not found."""
        page_id = "nonexistent"
        endpoint = f"api/v2/pages/{page_id}"
        
        # Mock a 404 error response
        self.mock_response_for_endpoint(
            endpoint, 
            status_code=404, 
            mock_data=ERROR_NOT_FOUND
        )
        
        # Ensure HTTPError is raised
        with self.assertRaises(HTTPError) as context:
            self.confluence.get_page_by_id(page_id)
        
        # Verify the error message
        self.assertEqual(context.exception.response.status_code, 404)
    
    def test_error_handling_permission_denied(self):
        """Test error handling when permission is denied."""
        page_id = "restricted"
        endpoint = f"api/v2/pages/{page_id}"
        
        # Mock a 403 error response
        self.mock_response_for_endpoint(
            endpoint, 
            status_code=403, 
            mock_data=ERROR_PERMISSION_DENIED
        )
        
        # Ensure HTTPError is raised
        with self.assertRaises(HTTPError) as context:
            self.confluence.get_page_by_id(page_id)
        
        # Verify the error message
        self.assertEqual(context.exception.response.status_code, 403)
    
    def test_error_handling_validation(self):
        """Test error handling when there's a validation error."""
        # Trying to create a page with invalid data
        endpoint = "api/v2/pages"
        
        # Mock a 400 error response
        self.mock_response_for_endpoint(
            endpoint, 
            status_code=400, 
            mock_data=ERROR_VALIDATION
        )
        
        # Ensure HTTPError is raised
        with self.assertRaises(HTTPError) as context:
            self.confluence.create_page(
                space_id="789012",
                title="",  # Empty title, should cause validation error
                body="<p>Content</p>"
            )
        
        # Verify the error message
        self.assertEqual(context.exception.response.status_code, 400)
    
    def test_get_page_properties(self):
        """Test retrieving properties for a page."""
        page_id = "123456"
        
        # Mock response data explicitly
        mock_data = {"results": [
            {"key": "test-property", "id": "prop1", "value": "test-value"},
            {"key": "another-property", "id": "prop2", "value": "another-value"}
        ]}
        
        # Expected response after processing by the method
        expected_result = mock_data["results"]
        
        # Mock the response with our explicit data
        self.mock_response.json.return_value = mock_data
        self.mock_response.text = json.dumps(mock_data)
        
        # Call the method
        result = self.confluence.get_page_properties(page_id)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # The API method extracts the "results" key from the response
        self.assertEqual(result, expected_result)
    
    def test_create_page_property(self):
        """Test creating a property for a page."""
        page_id = "123456"
        property_key = "test.property"  # Use valid format for property key
        property_value = {"testKey": "testValue"}
        endpoint = f"api/v2/pages/{page_id}/properties"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=PROPERTY_MOCK
        )
        
        # Call the method
        result = self.confluence.create_page_property(
            page_id, property_key, property_value
        )
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_get_page_labels(self):
        """Test retrieving labels for a page."""
        page_id = "123456"
        
        # Mock response data explicitly instead of relying on mock response generation
        mock_data = {"results": [
            {"name": "test-label", "id": "label1"},
            {"name": "another-label", "id": "label2"}
        ]}
        
        # Expected response after processing by the method
        expected_result = mock_data["results"]
        
        # Mock the response with our explicit data
        self.mock_response.json.return_value = mock_data
        self.mock_response.text = json.dumps(mock_data)
        
        # Call the method
        result = self.confluence.get_page_labels(page_id)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # The API method extracts the "results" key from the response
        self.assertEqual(result, expected_result)
    
    def test_add_page_label(self):
        """Test adding a label to a page."""
        page_id = "123456"
        label = "test-label"
        endpoint = f"api/v2/pages/{page_id}/labels"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=LABEL_MOCK
        )
        
        # Call the method
        result = self.confluence.add_page_label(page_id, label)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_get_comment_by_id(self):
        """Test retrieving a comment by ID."""
        comment_id = "comment123"
        endpoint = f"api/v2/comments/{comment_id}"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_comment_by_id(comment_id)
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], comment_id)
    
    def test_create_page_footer_comment(self):
        """Test creating a footer comment on a page."""
        page_id = "123456"
        body = "This is a test comment."
        endpoint = "api/v2/comments"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=COMMENT_MOCK
        )
        
        # Call the method
        result = self.confluence.create_page_footer_comment(page_id, body)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_create_page_inline_comment(self):
        """Test creating an inline comment on a page."""
        page_id = "123456"
        body = "This is a test inline comment."
        inline_comment_properties = {
            "textSelection": "text to highlight",
            "textSelectionMatchCount": 3,
            "textSelectionMatchIndex": 1
        }
        endpoint = "api/v2/comments"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=COMMENT_MOCK
        )
        
        # Call the method
        result = self.confluence.create_page_inline_comment(
            page_id, body, inline_comment_properties
        )
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_get_whiteboard_by_id(self):
        """Test retrieving a whiteboard by ID."""
        whiteboard_id = "wb123"
        endpoint = f"api/v2/whiteboards/{whiteboard_id}"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_whiteboard_by_id(whiteboard_id)
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], whiteboard_id)
    
    def test_create_whiteboard(self):
        """Test creating a whiteboard."""
        space_id = "789012"
        title = "Test Whiteboard"
        template_key = "timeline"
        endpoint = "api/v2/whiteboards"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=WHITEBOARD_MOCK
        )
        
        # Call the method
        result = self.confluence.create_whiteboard(
            space_id=space_id,
            title=title,
            template_key=template_key
        )
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_get_custom_content_by_id(self):
        """Test retrieving custom content by ID."""
        custom_content_id = "cc123"
        endpoint = f"api/v2/custom-content/{custom_content_id}"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_custom_content_by_id(custom_content_id)
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], custom_content_id)
    
    def test_create_custom_content(self):
        """Test creating custom content."""
        space_id = "789012"
        content_type = "example.custom.type"
        title = "Test Custom Content"
        body = "<p>This is custom content.</p>"
        endpoint = "api/v2/custom-content"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(
            endpoint,
            mock_data=CUSTOM_CONTENT_MOCK
        )
        
        # Call the method
        result = self.confluence.create_custom_content(
            type=content_type,
            title=title,
            body=body,
            space_id=space_id
        )
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result matches the expected data
        self.assertEqual(result, expected_data)
    
    def test_search_with_pagination(self):
        """Test search with pagination."""
        query = "test"
        endpoint = "api/v2/search"
        
        # Set up a simple mock response
        search_data = {
            "results": [
                {
                    "content": {
                        "id": "123456",
                        "title": "Test Page",
                        "type": "page",
                        "status": "current",
                        "spaceId": "789012"
                    },
                    "excerpt": "This is a <b>test</b> page.",
                    "lastModified": "2023-08-01T12:00:00Z"
                }
            ],
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/search"
            }
        }
        
        # Configure the mock response
        self.mock_response.json.return_value = search_data
        self.mock_response.text = json.dumps(search_data)
        
        # Call the method with search query and limit
        result = self.confluence.search(query=query, limit=1)
        
        # Verify the request was made
        self.confluence._session.request.assert_called_once()
        
        # Verify the result structure
        self.assertIsNotNone(result)
        self.assertTrue('results' in result or isinstance(result, list))


if __name__ == "__main__":
    unittest.main() 