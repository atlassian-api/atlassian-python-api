#!/usr/bin/env python3
"""
Integration tests for the Confluence v2 API implementation.
These tests are designed to be run against a real Confluence instance.

NOTE: To run these tests, you need to set the following environment variables:
    - CONFLUENCE_URL: The URL of the Confluence instance
    - CONFLUENCE_USERNAME: The username to use for authentication
    - CONFLUENCE_API_TOKEN: The API token to use for authentication
    - CONFLUENCE_SPACE_KEY: A space key to use for testing
"""

import os
import unittest
import warnings
from typing import Dict, Any, List, Union

from atlassian import ConfluenceV2


@unittest.skipIf(
    not (
        os.environ.get("CONFLUENCE_URL")
        and os.environ.get("CONFLUENCE_USERNAME")
        and os.environ.get("CONFLUENCE_API_TOKEN")
        and os.environ.get("CONFLUENCE_SPACE_KEY")
    ),
    "Confluence credentials not found in environment variables",
)
class TestConfluenceV2Integration(unittest.TestCase):
    """Integration tests for the Confluence v2 API implementation."""

    @classmethod
    def setUpClass(cls):
        """Set up the test case with a real Confluence instance."""
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        cls.confluence = ConfluenceV2(
            url=os.environ.get("CONFLUENCE_URL"),
            username=os.environ.get("CONFLUENCE_USERNAME"),
            password=os.environ.get("CONFLUENCE_API_TOKEN"),
            cloud=True,
        )
        cls.space_key = os.environ.get("CONFLUENCE_SPACE_KEY")
        
        # Create test data for cleanup
        cls.test_resources = []

    @classmethod
    def tearDownClass(cls):
        """Clean up any resources created during testing."""
        # Clean up any test pages, comments, etc. that were created
        for resource in cls.test_resources:
            resource_type = resource.get("type")
            resource_id = resource.get("id")
            
            try:
                if resource_type == "page":
                    cls.confluence.delete_page(resource_id)
                elif resource_type == "whiteboard":
                    cls.confluence.delete_whiteboard(resource_id)
                elif resource_type == "custom_content":
                    cls.confluence.delete_custom_content(resource_id)
            except Exception as e:
                print(f"Error cleaning up {resource_type} {resource_id}: {e}")

    def test_01_authentication(self):
        """Test that authentication works."""
        # Simply getting spaces will verify that authentication works
        spaces = self.confluence.get_spaces(limit=1)
        self.assertIsInstance(spaces, dict)
        self.assertIn("results", spaces)
        
    def test_02_get_spaces(self):
        """Test getting spaces."""
        spaces = self.confluence.get_spaces(limit=3)
        self.assertIsInstance(spaces, dict)
        self.assertIn("results", spaces)
        self.assertLessEqual(len(spaces["results"]), 3)
        
        if spaces["results"]:
            space = spaces["results"][0]
            self.assertIn("id", space)
            self.assertIn("key", space)
            self.assertIn("name", space)
            
    def test_03_get_space_by_key(self):
        """Test getting a space by key."""
        space = self.confluence.get_space(self.space_key)
        self.assertIsInstance(space, dict)
        self.assertIn("id", space)
        self.assertIn("key", space)
        self.assertEqual(space["key"], self.space_key)
    
    def test_04_page_operations(self):
        """Test creating, updating, and deleting a page."""
        # Create a page
        title = "Test Page - ConfluenceV2 Integration Test"
        body = "<p>This is a test page created by the integration test.</p>"
        
        page = self.confluence.create_page(
            space_id=self.space_key,
            title=title,
            body=body,
        )
        
        self.assertIsInstance(page, dict)
        self.assertIn("id", page)
        page_id = page["id"]
        
        # Add to test resources for cleanup
        self.test_resources.append({"type": "page", "id": page_id})
        
        # Get the page
        retrieved_page = self.confluence.get_page_by_id(page_id)
        self.assertEqual(retrieved_page["id"], page_id)
        self.assertEqual(retrieved_page["title"], title)
        
        # Update the page
        updated_title = f"{title} - Updated"
        updated_body = f"{body} <p>This page has been updated.</p>"
        
        updated_page = self.confluence.update_page(
            page_id=page_id,
            title=updated_title,
            body=updated_body,
            version=retrieved_page["version"]["number"],
        )
        
        self.assertEqual(updated_page["id"], page_id)
        self.assertEqual(updated_page["title"], updated_title)
        
        # Get the updated page
        retrieved_updated_page = self.confluence.get_page_by_id(page_id)
        self.assertEqual(retrieved_updated_page["title"], updated_title)
        
        # Delete the page
        response = self.confluence.delete_page(page_id)
        self.assertEqual(response.get("status", 204), 204)
        
        # Remove from test resources since we deleted it
        self.test_resources = [r for r in self.test_resources if r["id"] != page_id]
        
        # Verify it's deleted by trying to get it (should raise an exception)
        with self.assertRaises(Exception):
            self.confluence.get_page_by_id(page_id)

    def test_05_search(self):
        """Test searching content."""
        # Search for content
        query = "test"
        results = self.confluence.search(cql=f'space="{self.space_key}" AND text~"{query}"', limit=5)
        
        self.assertIsInstance(results, dict)
        self.assertIn("results", results)
    
    def test_06_pagination(self):
        """Test pagination of results."""
        # Get pages with pagination
        page1 = self.confluence.get_pages(limit=5)
        self.assertIsInstance(page1, dict)
        self.assertIn("results", page1)
        
        # If there are more pages
        if "next" in page1.get("_links", {}):
            next_page_url = page1["_links"]["next"]
            # Extract the query parameters from the next page URL
            query_params = {}
            if "?" in next_page_url:
                query_string = next_page_url.split("?")[1]
                for param in query_string.split("&"):
                    key, value = param.split("=")
                    query_params[key] = value
            
            # Get next page using cursor
            if "cursor" in query_params:
                page2 = self.confluence.get_pages(limit=5, cursor=query_params["cursor"])
                self.assertIsInstance(page2, dict)
                self.assertIn("results", page2)
                
                # Verify we got different results
                if page1["results"] and page2["results"]:
                    self.assertNotEqual(
                        page1["results"][0]["id"] if page1["results"] else None,
                        page2["results"][0]["id"] if page2["results"] else None
                    )
    
    def test_07_error_handling(self):
        """Test error handling."""
        # Test with an invalid page ID
        with self.assertRaises(Exception):
            self.confluence.get_page_by_id("invalid-id")
        
        # Test with an invalid space key
        with self.assertRaises(Exception):
            self.confluence.get_space("invalid-space-key-that-does-not-exist")


if __name__ == "__main__":
    unittest.main() 