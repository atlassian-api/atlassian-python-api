#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud v2 API Basics

This example demonstrates the fundamental operations using the Confluence Cloud v2 API,
including page creation, retrieval, and management with ADF content support.

Key features demonstrated:
- v2 API client initialization and configuration
- Basic page operations (create, read, update, delete)
- ADF (Atlassian Document Format) content handling
- Cursor-based pagination
- Error handling and best practices

Prerequisites:
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_v2_api_basics.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
from typing import Dict, Any, Optional

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


def create_sample_adf_content() -> Dict[str, Any]:
    """
    Create a sample ADF (Atlassian Document Format) document.

    This demonstrates the structure of ADF content that can be used
    with the v2 API for rich content creation.

    Returns:
        Dict containing a valid ADF document
    """
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": "Welcome to Confluence v2 API"}],
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This page was created using the Confluence Cloud v2 API with "},
                    {"type": "text", "text": "ADF (Atlassian Document Format)", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": " content."},
                ],
            },
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Key Features"}]},
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Native ADF content support"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Cursor-based pagination"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Enhanced performance"}]}
                        ],
                    },
                ],
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "For more information, visit the "},
                    {
                        "type": "text",
                        "text": "Confluence Cloud REST API documentation",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": "https://developer.atlassian.com/cloud/confluence/rest/v2/intro/"},
                            }
                        ],
                    },
                    {"type": "text", "text": "."},
                ],
            },
        ],
    }


def demonstrate_v2_api_basics():
    """
    Demonstrate basic v2 API operations.
    """
    print("=== Confluence Cloud v2 API Basics Example ===\n")

    # Initialize Confluence Cloud client
    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    # Enable v2 API usage
    print("1. Enabling v2 API...")
    confluence.enable_v2_api()

    # Check API configuration
    api_status = confluence.get_api_status()
    print(f"   API Status: {api_status}")
    print(f"   Using v2 API: {api_status.get('current_default') == 'v2'}")

    try:
        # Get spaces using v2 API
        print("\n2. Getting spaces with v2 API...")
        spaces_response = confluence._v2_client.get_spaces(limit=10)
        spaces = spaces_response.get("results", [])
        print(f"   Found {len(spaces)} spaces")

        if not spaces:
            print("   No spaces found. Please create a space first.")
            return

        # Find test space or use first available
        test_space = None
        for space in spaces:
            if space.get("key") == TEST_SPACE_KEY:
                test_space = space
                break

        if not test_space:
            test_space = spaces[0]
            print(f"   Test space '{TEST_SPACE_KEY}' not found, using '{test_space.get('name')}'")

        space_id = test_space["id"]
        print(f"   Using space: {test_space.get('name')} (ID: {space_id})")

        # Create a page with ADF content
        print("\n3. Creating page with ADF content...")
        adf_content = create_sample_adf_content()

        page_data = confluence._v2_client.create_page(
            space_id=space_id, title="v2 API Example Page", content=adf_content, content_format="adf"
        )

        page_id = page_data["id"]
        print(f"   Created page: {page_data.get('title')} (ID: {page_id})")
        print(f"   Page URL: {CONFLUENCE_URL}/wiki/spaces/{test_space.get('key')}/pages/{page_id}")

        # Retrieve the page
        print("\n4. Retrieving page with v2 API...")
        retrieved_page = confluence._v2_client.get_page_by_id(
            page_id, expand=["body.atlas_doc_format", "version", "space"]
        )

        print(f"   Page title: {retrieved_page.get('title')}")
        print(f"   Page version: {retrieved_page.get('version', {}).get('number')}")
        print(f"   Content format: {retrieved_page.get('body', {}).get('representation')}")

        # Update the page
        print("\n5. Updating page content...")
        updated_adf = create_sample_adf_content()
        # Add an update notice
        updated_adf["content"].insert(
            1,
            {
                "type": "panel",
                "attrs": {"panelType": "info"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "This page was updated using the v2 API!",
                                "marks": [{"type": "strong"}],
                            }
                        ],
                    }
                ],
            },
        )

        current_version = retrieved_page.get("version", {}).get("number", 1)
        updated_page = confluence._v2_client.update_page(
            page_id=page_id,
            title="v2 API Example Page (Updated)",
            content=updated_adf,
            content_format="adf",
            version=current_version + 1,
        )

        print(f"   Updated page version: {updated_page.get('version', {}).get('number')}")

        # Get pages with cursor pagination
        print("\n6. Demonstrating cursor-based pagination...")
        pages_response = confluence._v2_client.get_pages(space_id=space_id, limit=5)
        pages = pages_response.get("results", [])
        print(f"   Retrieved {len(pages)} pages from space")

        # Check for next page cursor
        next_cursor = pages_response.get("_links", {}).get("next")
        if next_cursor:
            print("   More pages available (cursor pagination working)")
        else:
            print("   No more pages (end of results)")

        # Search pages using CQL
        print("\n7. Searching pages with CQL...")
        search_results = confluence._v2_client.search_pages(cql=f"space.id = {space_id} AND type = page", limit=10)

        found_pages = search_results.get("results", [])
        print(f"   Found {len(found_pages)} pages matching search criteria")

        # Clean up - delete the test page
        print("\n8. Cleaning up test page...")
        confluence._v2_client.delete_page(page_id)
        print("   Test page deleted successfully")

        print("\n=== v2 API Basics Example completed successfully! ===")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")
        print("Make sure you have appropriate permissions in the test space.")


def main():
    """Main function."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    demonstrate_v2_api_basics()


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
