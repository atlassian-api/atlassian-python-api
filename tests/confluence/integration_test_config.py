# coding=utf-8
"""
Configuration and utilities for Confluence Cloud v2 API integration tests.

This module provides configuration management and utilities for running
integration tests against real Confluence Cloud instances.
"""

import os
import pytest
from typing import Dict, Optional, Any
from atlassian.confluence.cloud.v2 import ConfluenceCloudV2


class IntegrationTestConfig:
    """Configuration manager for integration tests."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self.url = os.getenv("CONFLUENCE_URL")
        self.token = os.getenv("CONFLUENCE_TOKEN")
        self.username = os.getenv("CONFLUENCE_USERNAME")
        self.password = os.getenv("CONFLUENCE_PASSWORD")
        self.space_id = os.getenv("CONFLUENCE_SPACE_ID")
        self.space_key = os.getenv("CONFLUENCE_SPACE_KEY", "TEST")
        self.test_page_prefix = os.getenv("CONFLUENCE_TEST_PAGE_PREFIX", "V2_API_TEST")

    def is_configured(self) -> bool:
        """Check if integration tests are properly configured."""
        return bool(self.url and (self.token or (self.username and self.password)) and self.space_id)

    def get_client(self) -> ConfluenceCloudV2:
        """Get configured v2 API client."""
        if not self.is_configured():
            raise ValueError("Integration test configuration incomplete")

        if self.token:
            return ConfluenceCloudV2(url=self.url, token=self.token)
        else:
            return ConfluenceCloudV2(url=self.url, username=self.username, password=self.password)

    def get_test_page_title(self, test_name: str) -> str:
        """Generate unique test page title."""
        import time

        timestamp = int(time.time())
        return f"{self.test_page_prefix}_{test_name}_{timestamp}"


def skip_if_not_configured():
    """Decorator to skip tests if integration configuration is missing."""
    config = IntegrationTestConfig()
    return pytest.mark.skipif(
        not config.is_configured(),
        reason="Integration test configuration missing. Set CONFLUENCE_URL, CONFLUENCE_TOKEN, and CONFLUENCE_SPACE_ID",
    )


def create_test_adf_content(text: str = "Test content") -> Dict[str, Any]:
    """Create test ADF content for integration tests."""
    return {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
    }


def create_complex_adf_content() -> Dict[str, Any]:
    """Create complex ADF content for testing."""
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "Integration Test Page"}]},
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "This page was created by the Confluence Cloud v2 API integration test suite. ",
                    },
                    {"type": "text", "text": "Bold text", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": " and "},
                    {"type": "text", "text": "italic text", "marks": [{"type": "em"}]},
                    {"type": "text", "text": "."},
                ],
            },
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Test Features"}]},
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "ADF content creation"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Page management operations"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Cursor-based pagination"}]}
                        ],
                    },
                ],
            },
        ],
    }


class IntegrationTestHelper:
    """Helper class for integration tests."""

    def __init__(self, config: IntegrationTestConfig):
        """Initialize helper with configuration."""
        self.config = config
        self.client = config.get_client()
        self.created_pages = []  # Track created pages for cleanup

    def create_test_page(
        self, title: Optional[str] = None, content: Optional[Dict[str, Any]] = None, parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a test page and track it for cleanup."""
        if title is None:
            title = self.config.get_test_page_title("page")

        if content is None:
            content = create_test_adf_content(f"Test content for {title}")

        page = self.client.create_page(
            space_id=self.config.space_id, title=title, content=content, parent_id=parent_id, content_format="adf"
        )

        self.created_pages.append(page["id"])
        return page

    def cleanup_test_pages(self):
        """Clean up all created test pages."""
        for page_id in self.created_pages:
            try:
                self.client.delete_page(page_id)
            except Exception as e:
                # Log but don't fail cleanup
                print(f"Warning: Failed to cleanup page {page_id}: {e}")

        self.created_pages.clear()

    def search_test_pages(self, limit: int = 10) -> Dict[str, Any]:
        """Search for test pages in the configured space."""
        cql = f"type=page AND space={self.config.space_key} AND title~'{self.config.test_page_prefix}*'"
        return self.client.search_pages(cql, limit=limit)

    def get_space_pages(self, limit: int = 10) -> Dict[str, Any]:
        """Get pages from the configured test space."""
        return self.client.get_pages(space_id=self.config.space_id, limit=limit)


# Environment variable documentation
INTEGRATION_TEST_ENV_VARS = """
Integration Test Environment Variables:

Required:
- CONFLUENCE_URL: Confluence Cloud base URL (e.g., https://your-domain.atlassian.net)
- CONFLUENCE_SPACE_ID: Space ID for testing (e.g., 123456789)

Authentication (choose one):
- CONFLUENCE_TOKEN: API token for authentication
- CONFLUENCE_USERNAME + CONFLUENCE_PASSWORD: Basic auth credentials

Optional:
- CONFLUENCE_SPACE_KEY: Space key for testing (default: TEST)
- CONFLUENCE_TEST_PAGE_PREFIX: Prefix for test pages (default: V2_API_TEST)

Example setup:
export CONFLUENCE_URL="https://your-domain.atlassian.net"
export CONFLUENCE_TOKEN="your-api-token"
export CONFLUENCE_SPACE_ID="123456789"
export CONFLUENCE_SPACE_KEY="TESTSPACE"

To run integration tests:
pytest -m integration tests/confluence/test_confluence_cloud_v2.py

To skip integration tests:
pytest -m "not integration" tests/confluence/test_confluence_cloud_v2.py
"""


def print_integration_test_help():
    """Print help for setting up integration tests."""
    print(INTEGRATION_TEST_ENV_VARS)


if __name__ == "__main__":
    print_integration_test_help()
