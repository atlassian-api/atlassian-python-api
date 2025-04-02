#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import unittest
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv

from atlassian import ConfluenceV2

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class TestConfluenceV2Integration(unittest.TestCase):
    """
    Integration tests for ConfluenceV2 methods using real API calls
    """

    def setUp(self):
        # Get and process the URL from .env
        url = os.environ.get("CONFLUENCE_URL")

        # Debug information
        logger.debug(f"Original URL from env: {url}")

        # Properly parse the URL to avoid path issues
        parsed_url = urlparse(url)

        # Use hostname without any path to avoid duplicating /wiki
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        logger.debug(f"Using base URL: {base_url}")

        # Create the client
        self.confluence = ConfluenceV2(
            url=base_url,
            username=os.environ.get("CONFLUENCE_USERNAME"),
            password=os.environ.get("CONFLUENCE_API_TOKEN"),
        )

        # Print the actual URL being used after initialization
        logger.debug(f"Confluence URL after initialization: {self.confluence.url}")

        # For debugging API calls, log the spaces endpoint
        spaces_endpoint = self.confluence.get_endpoint("spaces")
        logger.debug(f"Spaces endpoint path: {spaces_endpoint}")
        logger.debug(f"Full spaces URL would be: {self.confluence.url_joiner(self.confluence.url, spaces_endpoint)}")

        # Get the space key from environment variable or use a default
        self.space_key = os.environ.get("CONFLUENCE_SPACE_KEY", "TS")
        logger.debug(f"Using space key from environment: {self.space_key}")

        # Try to get the space ID for this space key
        try:
            space = self.confluence.get_space_by_key(self.space_key)
            if space and "id" in space:
                self.space_id = space["id"]
                logger.debug(f"Found space ID: {self.space_id} for key: {self.space_key}")
            else:
                logger.warning(f"Space with key {self.space_key} found but no ID available")
                self.space_id = None
        except Exception as e:
            logger.warning(f"Could not get space ID for key {self.space_key}: {e}")
            self.space_id = None

    def test_get_spaces(self):
        """Test retrieving spaces from the Confluence instance"""
        try:
            spaces = self.confluence.get_spaces(limit=10)
            self.assertIsNotNone(spaces)
            self.assertIsInstance(spaces, list)
            # Verify we got some spaces back
            self.assertTrue(len(spaces) > 0)
        except Exception as e:
            logger.error(f"Error in test_get_spaces: {e}")
            raise

    def test_get_space_by_key(self):
        """Test retrieving a specific space by key"""
        try:
            space = self.confluence.get_space_by_key(self.space_key)
            self.assertIsNotNone(space)
            self.assertIsInstance(space, dict)
            self.assertIn("key", space)
            self.assertIn("id", space)
            self.assertIn("name", space)
            # Log what we got vs what we expected
            if space["key"] != self.space_key:
                logger.warning(f"Warning: Requested space key '{self.space_key}' but got '{space['key']}' instead.")
        except Exception as e:
            logger.error(f"Error in test_get_space_by_key: {e}")
            raise

    @pytest.mark.xfail(reason="API access limitations or permissions - not working in current environment")
    def test_get_space_content(self):
        """Test retrieving content from a space"""
        try:
            # First, get a valid space to use
            spaces = self.confluence.get_spaces(limit=1)
            self.assertIsNotNone(spaces)
            self.assertGreater(len(spaces), 0, "No spaces available to test with")

            # Use the ID of the first space we have access to
            space_id = spaces[0]["id"]
            space_key = spaces[0]["key"]
            logger.debug(f"Testing content retrieval for space: {space_key} (ID: {space_id})")

            # Get content using the space ID
            content = self.confluence.get_space_content(space_id, limit=10)
            self.assertIsNotNone(content)
            self.assertIsInstance(content, list)
            logger.debug(f"Found {len(content)} content items in space {space_key}")
        except Exception as e:
            logger.error(f"Error in test_get_space_content: {e}")
            raise

    @pytest.mark.xfail(reason="API access limitations or permissions - not working in current environment")
    def test_search_content(self):
        """Test searching for content in Confluence"""
        try:
            # First try a generic search term
            results = self.confluence.search_content("page", limit=5)

            # If that doesn't return results, try a few more common search terms
            if not results:
                logger.debug("First search term 'page' returned no results, trying alternatives")

                # Try additional common terms that might exist in the Confluence instance
                for term in ["meeting", "project", "test", "document", "welcome"]:
                    logger.debug(f"Trying search term: '{term}'")
                    results = self.confluence.search_content(term, limit=5)
                    if results:
                        logger.debug(f"Found {len(results)} results with search term '{term}'")
                        break

            # As long as the search API works, the test passes
            # We don't assert on results since the content might be empty in a test instance
            self.assertIsNotNone(results)
            self.assertIsInstance(results, list)

            # Log the number of results
            logger.debug(f"Content search returned {len(results)} results")

        except Exception as e:
            logger.error(f"Error in test_search_content: {e}")
            raise


if __name__ == "__main__":
    unittest.main()
