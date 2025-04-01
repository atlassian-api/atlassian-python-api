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

from atlassian import ConfluenceV2
from tests.mocks.confluence_v2_mock_responses import (
    PAGE_MOCK, PAGE_RESULT_LIST, CHILD_PAGES_RESULT, SPACE_MOCK, SPACES_RESULT,
    SEARCH_RESULT, PROPERTY_MOCK, PROPERTIES_RESULT, LABEL_MOCK, LABELS_RESULT,
    COMMENT_MOCK, COMMENTS_RESULT, WHITEBOARD_MOCK, CUSTOM_CONTENT_MOCK,
    ERROR_NOT_FOUND, ERROR_PERMISSION_DENIED, ERROR_VALIDATION,
    get_mock_for_endpoint
)


class TestConfluenceV2WithMocks(unittest.TestCase):
    """Test case for ConfluenceV2 using mock responses."""

    def setUp(self):
        """Set up the test case."""
        self.confluence = ConfluenceV2(
            url="https://example.atlassian.net/wiki",
            username="username",
            password="password",
        )
        
        # Create a mock for the underlying rest client methods
        self.mock_response = MagicMock(spec=Response)
        self.mock_response.headers = {}
        self.mock_response.reason = "OK"  # Add reason attribute
        self.confluence._session = MagicMock()
        self.confluence._session.request.return_value = self.mock_response
    
    def mock_response_for_endpoint(self, endpoint, params=None, status_code=200, mock_data=None):
        """Configure the mock to return a response for a specific endpoint."""
        if mock_data is None:
            mock_data = get_mock_for_endpoint(endpoint, params)
        
        self.mock_response.status_code = status_code
        self.mock_response.text = json.dumps(mock_data)
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
        if "_links" in mock_data and "next" in mock_data["_links"]:
            self.mock_response.headers = {
                "Link": f'<{mock_data["_links"]["next"]}>; rel="next"'
            }
        else:
            self.mock_response.headers = {}
        
        # Configure raise_for_status to raise HTTPError when status_code >= 400
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once_with(
            "GET", 
            f"https://example.atlassian.net/wiki/{endpoint}",
            params={"body-format": None},
            headers=self.confluence.form_token_headers,
            data=None,
            files=None,
            timeout=None
        )
        
        # Verify the result
        self.assertEqual(result, expected_data)
        self.assertEqual(result["id"], page_id)
    
    def test_get_pages_with_pagination(self):
        """Test retrieving pages with pagination."""
        endpoint = "api/v2/pages"
        
        # Set up a sequence of mock responses for pagination
        page1_data = self.mock_response_for_endpoint(endpoint)
        page2_data = {
            "results": [
                {
                    "id": "567890",
                    "title": "Third Page",
                    "status": "current",
                    "spaceId": "789012"
                }
            ],
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/pages?cursor=page2"
            }
        }
        
        # Configure the mock to return different responses for each call
        mock_resp_1 = self.mock_response
        mock_resp_2 = MagicMock(spec=Response)
        mock_resp_2.status_code = 200
        mock_resp_2.reason = "OK"  # Add reason attribute
        mock_resp_2.text = json.dumps(page2_data)
        mock_resp_2.json.return_value = page2_data
        mock_resp_2.headers = {}
        mock_resp_2.raise_for_status.side_effect = None
        
        self.confluence._session.request.side_effect = [mock_resp_1, mock_resp_2]
        
        # Call the method with pagination
        result = self.confluence.get_pages(limit=3)  # Should fetch all pages (3 total)
        
        # Verify the requests were made correctly
        self.assertEqual(self.confluence._session.request.call_count, 2)
        
        # Verify the combined result
        self.assertEqual(len(result), 3)  # 2 from first page, 1 from second page
        self.assertEqual(result[0]["id"], "123456")
        self.assertEqual(result[1]["id"], "345678")
        self.assertEqual(result[2]["id"], "567890")
    
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
        endpoint = f"api/v2/pages/{page_id}/properties"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_page_properties(page_id)
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["key"], "test-property")
        self.assertEqual(result[1]["key"], "another-property")
    
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
        
        # Verify the request was made correctly with the right data
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertEqual(call_args[0][1], f"https://example.atlassian.net/wiki/{endpoint}")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["key"], property_key)
        self.assertEqual(request_data["value"], property_value)
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_get_page_labels(self):
        """Test retrieving labels for a page."""
        page_id = "123456"
        endpoint = f"api/v2/pages/{page_id}/labels"
        
        # Mock the response
        expected_data = self.mock_response_for_endpoint(endpoint)
        
        # Call the method
        result = self.confluence.get_page_labels(page_id)
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        
        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "test-label")
        self.assertEqual(result[1]["name"], "another-label")
    
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["name"], label)
        
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["pageId"], page_id)
        self.assertEqual(request_data["body"]["storage"]["value"], body)
        
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["pageId"], page_id)
        self.assertEqual(request_data["body"]["storage"]["value"], body)
        self.assertEqual(request_data["inlineCommentProperties"], inline_comment_properties)
        
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["spaceId"], space_id)
        self.assertEqual(request_data["title"], title)
        self.assertEqual(request_data["templateKey"], template_key)
        
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
        
        # Verify the request was made correctly
        self.confluence._session.request.assert_called_once()
        call_args = self.confluence._session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        
        # Check the request data
        request_data = json.loads(call_args[1]["data"])
        self.assertEqual(request_data["type"], content_type)
        self.assertEqual(request_data["title"], title)
        self.assertEqual(request_data["spaceId"], space_id)
        self.assertEqual(request_data["body"]["storage"]["value"], body)
        
        # Verify the result
        self.assertEqual(result, expected_data)
    
    def test_search_with_pagination(self):
        """Test search with pagination."""
        query = "test"
        endpoint = "api/v2/search"
        
        # Set up a sequence of mock responses for pagination
        page1_data = self.mock_response_for_endpoint(endpoint)
        page2_data = {
            "results": [
                {
                    "content": {
                        "id": "987654",
                        "title": "Additional Page",
                        "type": "page",
                        "status": "current",
                        "spaceId": "789012"
                    },
                    "excerpt": "This is an <b>additional</b> test page.",
                    "lastModified": "2023-08-01T14:00:00Z"
                }
            ],
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/search?cursor=page2"
            }
        }
        
        # Configure the mock to return different responses for each call
        mock_resp_1 = self.mock_response
        mock_resp_2 = MagicMock(spec=Response)
        mock_resp_2.status_code = 200
        mock_resp_2.reason = "OK"  # Add reason attribute
        mock_resp_2.text = json.dumps(page2_data)
        mock_resp_2.json.return_value = page2_data
        mock_resp_2.headers = {}
        mock_resp_2.raise_for_status.side_effect = None
        
        self.confluence._session.request.side_effect = [mock_resp_1, mock_resp_2]
        
        # Call the method with pagination
        result = self.confluence.search(query=query, limit=3)
        
        # Verify the requests were made correctly
        self.assertEqual(self.confluence._session.request.call_count, 2)
        
        # Verify the result contains results from both pages
        self.assertEqual(len(result["results"]), 3)  # 2 from first page, 1 from second page
        self.assertEqual(result["results"][0]["content"]["id"], "123456")
        self.assertEqual(result["results"][1]["content"]["id"], "345678")
        self.assertEqual(result["results"][2]["content"]["id"], "987654")


if __name__ == "__main__":
    unittest.main() 