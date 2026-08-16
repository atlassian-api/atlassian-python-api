#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example showing how to use both Confluence API v1 and v2 with the library
"""

import datetime
import logging
import os

from atlassian import Confluence, ConfluenceV2, create_confluence

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Confluence credentials from environment variables
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://example.atlassian.net")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME", "email@example.com")
CONFLUENCE_PASSWORD = os.environ.get("CONFLUENCE_PASSWORD", "api-token")

# Example 1: Using the Confluence class with explicit API version
# For backwards compatibility, api_version=1 is the default
confluence_v1 = Confluence(
    url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD, api_version=1
)

# Example 2: Using the Confluence class with API v2
confluence_v1_with_v2 = Confluence(
    url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD, api_version=2
)

# Example 3: Using the dedicated ConfluenceV2 class (recommended for v2 API)
confluence_v2 = ConfluenceV2(url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD)

# Example 4: Using the factory method
confluence_v1_factory = create_confluence(
    url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD, api_version=1
)

confluence_v2_factory = create_confluence(
    url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD, api_version=2
)

# Verify the types and versions
print(f"confluence_v1 type: {type(confluence_v1)}, API version: {confluence_v1.api_version}")
print(f"confluence_v1_with_v2 type: {type(confluence_v1_with_v2)}, API version: {confluence_v1_with_v2.api_version}")
print(f"confluence_v2 type: {type(confluence_v2)}, API version: {confluence_v2.api_version}")
print(f"confluence_v1_factory type: {type(confluence_v1_factory)}, API version: {confluence_v1_factory.api_version}")
print(f"confluence_v2_factory type: {type(confluence_v2_factory)}, API version: {confluence_v2_factory.api_version}")

# Note: Currently most v2-specific methods are not implemented yet
# They will be added in Phase 2 and Phase 3 of the implementation

# Demonstration of API V2 methods


def example_get_page_by_id():
    """Example showing how to get a page by ID using the v2 API"""
    print("\n=== Getting a page by ID (v2) ===")

    # You need a valid page ID
    page_id = "123456"  # Replace with a real page ID

    try:
        # Get the page without body content
        page = confluence_v2.get_page_by_id(page_id, get_body=False)
        print(f"Page title: {page.get('title', 'Unknown')}")

        # Get the page with storage format body and expanded version
        page_with_body = confluence_v2.get_page_by_id(page_id, body_format="storage", expand=["version"])
        print(f"Page version: {page_with_body.get('version', {}).get('number', 'Unknown')}")

        # Print the first 100 characters of the body content (if present)
        body = page_with_body.get("body", {}).get("storage", {}).get("value", "")
        print(f"Body preview: {body[:100]}...")

    except Exception as e:
        print(f"Error getting page: {e}")


def example_get_pages():
    """Example showing how to get a list of pages using the v2 API"""
    print("\n=== Getting pages (v2) ===")

    # Get pages from a specific space
    space_id = "123456"  # Replace with a real space ID

    try:
        # Get up to 10 pages from the space
        pages = confluence_v2.get_pages(
            space_id=space_id, limit=10, sort="-modified-date"  # Most recently modified first
        )

        print(f"Found {len(pages)} pages:")
        for page in pages:
            print(f"  - {page.get('title', 'Unknown')} (ID: {page.get('id', 'Unknown')})")

        # Search by title
        title_pages = confluence_v2.get_pages(
            space_id=space_id, title="Meeting Notes", limit=5  # Pages with this exact title
        )

        print(f"\nFound {len(title_pages)} pages with title 'Meeting Notes'")

    except Exception as e:
        print(f"Error getting pages: {e}")


def example_get_child_pages():
    """Example showing how to get child pages using the v2 API"""
    print("\n=== Getting child pages (v2) ===")

    # You need a valid parent page ID
    parent_id = "123456"  # Replace with a real page ID

    try:
        # Get child pages sorted by their position
        child_pages = confluence_v2.get_child_pages(parent_id=parent_id, sort="child-position")

        print(f"Found {len(child_pages)} child pages:")
        for page in child_pages:
            print(f"  - {page.get('title', 'Unknown')} (ID: {page.get('id', 'Unknown')})")

    except Exception as e:
        print(f"Error getting child pages: {e}")


def example_create_page():
    """Example showing how to create a page using the v2 API"""
    print("\n=== Creating a page (v2) ===")

    # You need a valid space ID
    space_id = "123456"  # Replace with a real space ID

    try:
        # Create a new page with storage format content
        new_page = confluence_v2.create_page(
            space_id=space_id,
            title="API Created Page",
            body="<p>This page was created using the Confluence API v2</p>",
            body_format="storage",
        )

        print(f"Created page: {new_page.get('title', 'Unknown')} (ID: {new_page.get('id', 'Unknown')})")

        # Create a child page under the page we just created
        child_page = confluence_v2.create_page(
            space_id=space_id,
            title="Child of API Created Page",
            body="<p>This is a child page created using the Confluence API v2</p>",
            parent_id=new_page.get("id"),
            body_format="storage",
        )

        print(f"Created child page: {child_page.get('title', 'Unknown')} (ID: {child_page.get('id', 'Unknown')})")

        # The created page IDs should be stored for later examples
        return new_page.get("id"), child_page.get("id")

    except Exception as e:
        print(f"Error creating pages: {e}")
        return None, None


def example_update_page(page_id):
    """Example showing how to update a page using the v2 API"""
    print("\n=== Updating a page (v2) ===")

    if not page_id:
        print("No page ID provided for update example")
        return

    try:
        # First, get the current page to see its title
        page = confluence_v2.get_page_by_id(page_id)
        print(f"Original page title: {page.get('title', 'Unknown')}")

        # Update the page title and content
        updated_page = confluence_v2.update_page(
            page_id=page_id,
            title=f"{page.get('title', 'Unknown')} - Updated",
            body="<p>This content has been updated using the Confluence API v2</p><p>Update time: "
            + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "</p>",
            body_format="storage",
        )

        print(f"Updated page: {updated_page.get('title', 'Unknown')}")
        print(f"New version: {updated_page.get('version', {}).get('number', 'Unknown')}")

    except Exception as e:
        print(f"Error updating page: {e}")


def example_delete_page(page_id):
    """Example showing how to delete a page using the v2 API"""
    print("\n=== Deleting a page (v2) ===")

    if not page_id:
        print("No page ID provided for delete example")
        return

    try:
        # Delete the page
        result = confluence_v2.delete_page(page_id)

        if result:
            print(f"Successfully deleted page with ID: {page_id}")
        else:
            print(f"Failed to delete page with ID: {page_id}")

    except Exception as e:
        print(f"Error deleting page: {e}")


def example_search():
    """Example showing how to search for content using the v2 API"""
    print("\n=== Searching content (v2) ===")

    try:
        # Simple text search
        print("Simple text search:")
        results = confluence_v2.search("meeting notes")

        # Print the first few results
        print(f"Found {len(results.get('results', []))} results")
        for i, result in enumerate(results.get("results", [])[:3]):
            content = result.get("content", {})
            print(f"{i+1}. {content.get('title', 'Unknown')} (ID: {content.get('id', 'Unknown')})")

        # Search with CQL (Confluence Query Language)
        print("\nSearch with CQL:")
        cql_results = confluence_v2.search(query="", cql="type = 'page' AND created > startOfMonth(-1)", limit=5)

        # Print the results
        print(f"Found {len(cql_results.get('results', []))} pages created in the last month")
        for i, result in enumerate(cql_results.get("results", [])[:3]):
            content = result.get("content", {})
            print(f"{i+1}. {content.get('title', 'Unknown')}")

    except Exception as e:
        print(f"Error searching content: {e}")


def example_search_content():
    """Example showing how to use the search_content convenience method"""
    print("\n=== Searching content with filters (v2) ===")

    try:
        # Search for pages containing "project" in a specific space
        space_id = "123456"  # Replace with a real space ID

        results = confluence_v2.search_content(
            query="project", type="page", space_id=space_id, status="current", limit=5
        )

        # Print the results
        print(f"Found {len(results)} pages containing 'project'")
        for i, result in enumerate(results[:3]):
            content = result.get("content", {})
            print(f"{i+1}. {content.get('title', 'Unknown')}")

        # Search for recent blog posts
        print("\nRecent blog posts:")
        blog_results = confluence_v2.search_content(
            query="", type="blogpost", status="current", limit=3  # Empty query to match any content
        )

        # Print the results
        print(f"Found {len(blog_results)} recent blog posts")
        for i, result in enumerate(blog_results):
            content = result.get("content", {})
            print(f"{i+1}. {content.get('title', 'Unknown')}")

    except Exception as e:
        print(f"Error searching content with filters: {e}")


def example_get_spaces():
    """Example showing how to get spaces using the v2 API"""
    print("\n=== Getting spaces (v2) ===")

    try:
        # Get all spaces
        spaces = confluence_v2.get_spaces(limit=10)

        print(f"Found {len(spaces)} spaces:")
        for i, space in enumerate(spaces[:5]):
            print(f"{i+1}. {space.get('name', 'Unknown')} (Key: {space.get('key', 'Unknown')})")

        # Filter spaces by type and status
        global_spaces = confluence_v2.get_spaces(type="global", status="current", limit=5)

        print(f"\nFound {len(global_spaces)} global spaces:")
        for i, space in enumerate(global_spaces[:3]):
            print(f"{i+1}. {space.get('name', 'Unknown')}")

        # Get spaces with specific labels
        labeled_spaces = confluence_v2.get_spaces(labels=["documentation", "team"], sort="name", limit=5)

        print(f"\nFound {len(labeled_spaces)} spaces with documentation or team labels:")
        for i, space in enumerate(labeled_spaces[:3]):
            print(f"{i+1}. {space.get('name', 'Unknown')}")

    except Exception as e:
        print(f"Error getting spaces: {e}")


def example_get_space_by_id():
    """Example showing how to get a specific space by ID"""
    print("\n=== Getting a space by ID (v2) ===")

    # You need a valid space ID
    space_id = "123456"  # Replace with a real space ID

    try:
        # Get the space details
        space = confluence_v2.get_space(space_id)

        print(f"Space details:")
        print(f"  Name: {space.get('name', 'Unknown')}")
        print(f"  Key: {space.get('key', 'Unknown')}")
        print(f"  Type: {space.get('type', 'Unknown')}")
        print(f"  Status: {space.get('status', 'Unknown')}")

        # Get space content (pages, blog posts, etc.)
        content = confluence_v2.get_space_content(space_id=space_id, sort="-modified", limit=5)

        print(f"\nRecent content in space ({len(content)} items):")
        for i, item in enumerate(content[:3]):
            content_item = item.get("content", {})
            print(f"{i+1}. {content_item.get('title', 'Unknown')} " f"(Type: {content_item.get('type', 'Unknown')})")

    except Exception as e:
        print(f"Error getting space: {e}")


def example_get_space_by_key():
    """Example showing how to get a specific space by key"""
    print("\n=== Getting a space by key (v2) ===")

    # You need a valid space key (usually uppercase, like "DEV" or "HR")
    space_key = "DOC"  # Replace with a real space key

    try:
        # Get the space details by key
        space = confluence_v2.get_space_by_key(space_key)

        print(f"Space details:")
        print(f"  ID: {space.get('id', 'Unknown')}")
        print(f"  Name: {space.get('name', 'Unknown')}")
        print(f"  Description: {space.get('description', {}).get('plain', {}).get('value', 'No description')}")

    except Exception as e:
        print(f"Error getting space by key: {e}")


if __name__ == "__main__":
    # This script will run the examples if executed directly
    # Replace the page IDs with real IDs before running

    # Uncomment to run the examples
    # example_get_page_by_id()
    # example_get_pages()
    # example_get_child_pages()

    # Examples for content creation - these should be run in sequence
    # parent_id, child_id = example_create_page()
    # if parent_id:
    #     example_update_page(parent_id)
    #     # Optionally delete pages - be careful with this!
    #     example_delete_page(child_id)  # Delete child first
    #     example_delete_page(parent_id)  # Then delete parent

    # Search examples
    # example_search()
    # example_search_content()

    # Space examples
    # example_get_spaces()
    # example_get_space_by_id()
    # example_get_space_by_key()

    print("This script contains examples for using the Confluence API v2.")
    print("Edit the page IDs and uncomment the example functions to run them.")
