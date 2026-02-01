#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud v1 to v2 API Migration

This example demonstrates how to migrate from Confluence Cloud v1 API to v2 API,
showing the differences in approach, data structures, and best practices for
transitioning existing code.

Key migration topics covered:
- API endpoint differences
- Authentication (same for both versions)
- Content format changes (Storage Format → ADF)
- Pagination changes (offset-based → cursor-based)
- Response structure differences
- Error handling improvements
- Performance optimizations

Prerequisites:
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_v1_to_v2_migration.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


def demonstrate_api_differences():
    """
    Demonstrate the key differences between v1 and v2 APIs.
    """
    print("=== API Differences Overview ===\n")

    differences = [
        {
            "aspect": "API Root",
            "v1": "wiki/rest/api",
            "v2": "wiki/api/v2",
            "impact": "Different base URLs for API calls",
        },
        {
            "aspect": "Content Format",
            "v1": "Storage Format (XHTML-like)",
            "v2": "ADF (Atlassian Document Format)",
            "impact": "Content structure completely different",
        },
        {
            "aspect": "Pagination",
            "v1": "start/limit parameters",
            "v2": "cursor-based pagination",
            "impact": "More efficient for large datasets",
        },
        {
            "aspect": "Content IDs",
            "v1": "Numeric IDs (e.g., 12345)",
            "v2": "UUID strings (e.g., abc123-def456)",
            "impact": "ID format changes in responses",
        },
        {
            "aspect": "Space References",
            "v1": "Space keys (e.g., 'DEMO')",
            "v2": "Space IDs (UUID strings)",
            "impact": "Need to resolve space keys to IDs",
        },
        {
            "aspect": "Response Structure",
            "v1": "Nested expansion model",
            "v2": "Flatter, more consistent structure",
            "impact": "Response parsing logic changes",
        },
    ]

    print("Key Differences:")
    for diff in differences:
        print(f"\n{diff['aspect']}:")
        print(f"  v1: {diff['v1']}")
        print(f"  v2: {diff['v2']}")
        print(f"  Impact: {diff['impact']}")

    print("\n" + "=" * 60 + "\n")


def demonstrate_dual_api_usage():
    """
    Demonstrate using both v1 and v2 APIs in the same application.
    """
    print("=== Dual API Usage Example ===\n")

    # Initialize Confluence Cloud client (defaults to v1)
    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    print("1. Client initialized (defaults to v1 API)")
    api_status = confluence.get_api_status()
    print(f"   Current API: {api_status.get('current_default')}")
    print(f"   v2 Available: {api_status.get('v2_available')}")

    try:
        # Get spaces using v1 API
        print("\n2. Getting spaces with v1 API...")
        v1_spaces = confluence.get_spaces(limit=5)
        print(f"   v1 API returned {len(v1_spaces.get('results', []))} spaces")

        if v1_spaces.get("results"):
            first_space = v1_spaces["results"][0]
            space_key = first_space.get("key")
            print(f"   Example space: {first_space.get('name')} (key: {space_key})")

        # Enable v2 API
        print("\n3. Enabling v2 API...")
        confluence.enable_v2_api()

        api_status = confluence.get_api_status()
        print(f"   Current API: {api_status.get('current_default')}")

        # Get spaces using v2 API
        print("\n4. Getting spaces with v2 API...")
        v2_spaces = confluence._v2_client.get_spaces(limit=5)
        print(f"   v2 API returned {len(v2_spaces.get('results', []))} spaces")

        if v2_spaces.get("results"):
            first_space_v2 = v2_spaces["results"][0]
            space_id = first_space_v2.get("id")
            print(f"   Example space: {first_space_v2.get('name')} (ID: {space_id})")

        # Compare response structures
        print("\n5. Comparing response structures...")
        if v1_spaces.get("results") and v2_spaces.get("results"):
            v1_space = v1_spaces["results"][0]
            v2_space = v2_spaces["results"][0]

            print("   v1 space structure:")
            for key in sorted(v1_space.keys())[:5]:  # Show first 5 keys
                print(f"     {key}: {type(v1_space[key]).__name__}")

            print("   v2 space structure:")
            for key in sorted(v2_space.keys())[:5]:  # Show first 5 keys
                print(f"     {key}: {type(v2_space[key]).__name__}")

        # Disable v2 API to return to v1
        print("\n6. Returning to v1 API...")
        confluence.disable_v2_api()

        api_status = confluence.get_api_status()
        print(f"   Current API: {api_status.get('current_default')}")

        print("\n✅ Dual API usage demonstrated successfully!")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")


def demonstrate_content_migration():
    """
    Demonstrate migrating content between v1 and v2 formats.
    """
    print("=== Content Format Migration ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    try:
        # Find test space
        spaces = confluence.get_spaces(limit=10)
        if not spaces.get("results"):
            print("No spaces found. Please create a space first.")
            return

        test_space = None
        for space in spaces["results"]:
            if space.get("key") == TEST_SPACE_KEY:
                test_space = space
                break

        if not test_space:
            test_space = spaces["results"][0]

        space_key = test_space["key"]
        print(f"Using space: {test_space.get('name')} (key: {space_key})")

        # Create page with v1 API (Storage Format)
        print("\n1. Creating page with v1 API (Storage Format)...")

        v1_content = """
        <h1>Migration Example</h1>
        <p>This page was created using the <strong>v1 API</strong> with Storage Format.</p>
        <p>Storage Format uses XHTML-like markup:</p>
        <ul>
            <li>HTML-like tags</li>
            <li>Confluence-specific macros</li>
            <li>Inline styling</li>
        </ul>
        <ac:structured-macro ac:name="info">
            <ac:rich-text-body>
                <p>This is an info panel created with Storage Format.</p>
            </ac:rich-text-body>
        </ac:structured-macro>
        """

        v1_page = confluence.create_page(space=space_key, title="v1 API Migration Example", body=v1_content)

        print(f"   Created v1 page: {v1_page.get('title')} (ID: {v1_page.get('id')})")

        # Enable v2 API
        confluence.enable_v2_api()

        # Get space ID for v2 API
        v2_spaces = confluence._v2_client.get_spaces(limit=10)
        space_id = None
        for space in v2_spaces.get("results", []):
            if space.get("key") == space_key:
                space_id = space.get("id")
                break

        if not space_id:
            print("   Could not find space ID for v2 API")
            return

        # Create equivalent page with v2 API (ADF)
        print("\n2. Creating equivalent page with v2 API (ADF)...")

        v2_content = {
            "version": 1,
            "type": "doc",
            "content": [
                {"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "Migration Example"}]},
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "This page was created using the "},
                        {"type": "text", "text": "v2 API", "marks": [{"type": "strong"}]},
                        {"type": "text", "text": " with ADF (Atlassian Document Format)."},
                    ],
                },
                {"type": "paragraph", "content": [{"type": "text", "text": "ADF uses structured JSON:"}]},
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {"type": "paragraph", "content": [{"type": "text", "text": "JSON-based structure"}]}
                            ],
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Semantic content representation"}],
                                }
                            ],
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": "Better programmatic control"}],
                                }
                            ],
                        },
                    ],
                },
                {
                    "type": "panel",
                    "attrs": {"panelType": "info"},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "This is an info panel created with ADF."}],
                        }
                    ],
                },
            ],
        }

        v2_page = confluence._v2_client.create_page(
            space_id=space_id, title="v2 API Migration Example", content=v2_content, content_format="adf"
        )

        print(f"   Created v2 page: {v2_page.get('title')} (ID: {v2_page.get('id')})")

        # Compare the pages
        print("\n3. Comparing created pages...")

        # Get v1 page details
        confluence.disable_v2_api()
        v1_details = confluence.get_page_by_id(v1_page["id"], expand="body.storage,version")

        # Get v2 page details
        confluence.enable_v2_api()
        v2_details = confluence._v2_client.get_page_by_id(v2_page["id"], expand=["body.atlas_doc_format", "version"])

        print("   v1 page details:")
        print(f"     Content format: {v1_details.get('body', {}).get('storage', {}).get('representation', 'N/A')}")
        print(f"     Content length: {len(str(v1_details.get('body', {}).get('storage', {}).get('value', '')))}")
        print(f"     Version: {v1_details.get('version', {}).get('number', 'N/A')}")

        print("   v2 page details:")
        print(f"     Content format: {v2_details.get('body', {}).get('representation', 'N/A')}")
        print(f"     Content structure: {type(v2_details.get('body', {}).get('value', {}))}")
        print(f"     Version: {v2_details.get('version', {}).get('number', 'N/A')}")

        # Show URLs
        print(f"\n   v1 page URL: {CONFLUENCE_URL}/wiki/spaces/{space_key}/pages/{v1_page['id']}")
        print(f"   v2 page URL: {CONFLUENCE_URL}/wiki/spaces/{space_key}/pages/{v2_page['id']}")

        print("\n✅ Content migration demonstrated successfully!")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")


def demonstrate_pagination_migration():
    """
    Demonstrate migrating from offset-based to cursor-based pagination.
    """
    print("=== Pagination Migration ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    try:
        # v1 pagination example
        print("1. v1 API pagination (offset-based)...")

        # Get first page of results
        v1_pages = confluence.get_all_pages_from_space(space=TEST_SPACE_KEY, start=0, limit=3, expand="version")

        print(f"   Retrieved {len(v1_pages)} pages with v1 pagination")
        print("   v1 pagination uses 'start' and 'limit' parameters")
        print("   Example: GET /rest/api/content?start=0&limit=25")

        # v2 pagination example
        print("\n2. v2 API pagination (cursor-based)...")
        confluence.enable_v2_api()

        # Find space ID
        spaces = confluence._v2_client.get_spaces(limit=10)
        space_id = None
        for space in spaces.get("results", []):
            if space.get("key") == TEST_SPACE_KEY:
                space_id = space.get("id")
                break

        if space_id:
            # Get first page of results
            v2_pages = confluence._v2_client.get_pages(space_id=space_id, limit=3)

            pages_list = v2_pages.get("results", [])
            print(f"   Retrieved {len(pages_list)} pages with v2 pagination")
            print("   v2 pagination uses 'cursor' parameter")
            print("   Example: GET /api/v2/pages?limit=25&cursor=abc123")

            # Check for next page
            next_link = v2_pages.get("_links", {}).get("next")
            if next_link:
                print("   Next page available via cursor")
                print(f"   Next URL: {next_link.get('href', 'N/A')}")
            else:
                print("   No more pages available")

        # Migration code example
        print("\n3. Migration code patterns...")

        print("""
   v1 Pagination Pattern:
   ```python
   start = 0
   limit = 25
   while True:
       response = confluence.get_all_pages_from_space(
           space='DEMO', start=start, limit=limit
       )
       if not response or len(response) < limit:
           break
       start += limit
   ```
   
   v2 Pagination Pattern:
   ```python
   cursor = None
   limit = 25
   while True:
       response = confluence._v2_client.get_pages(
           space_id='space123', limit=limit, cursor=cursor
       )
       results = response.get('results', [])
       if not results:
           break
       cursor = response.get('_links', {}).get('next', {}).get('href')
       if not cursor:
           break
   ```
        """)

        print("✅ Pagination migration demonstrated successfully!")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")


def provide_migration_checklist():
    """
    Provide a comprehensive migration checklist.
    """
    print("=== Migration Checklist ===\n")

    checklist = [
        {
            "category": "Planning",
            "items": [
                "Audit existing v1 API usage in your codebase",
                "Identify which operations need v2 equivalents",
                "Plan for content format conversion (Storage → ADF)",
                "Test v2 API with your Confluence instance",
                "Plan rollback strategy if needed",
            ],
        },
        {
            "category": "Authentication",
            "items": [
                "✅ No changes needed - same API tokens work for both versions",
                "✅ Same authentication headers and methods",
                "✅ Same rate limiting applies to both APIs",
            ],
        },
        {
            "category": "Code Changes",
            "items": [
                "Update API endpoint URLs (rest/api → api/v2)",
                "Convert content from Storage Format to ADF",
                "Update pagination logic (offset → cursor)",
                "Handle new response structures",
                "Update error handling for v2 error formats",
                "Test with both small and large datasets",
            ],
        },
        {
            "category": "Content Migration",
            "items": [
                "Understand ADF structure and validation",
                "Create utilities for Storage Format → ADF conversion",
                "Test content rendering in Confluence",
                "Validate complex content (tables, macros, etc.)",
                "Plan for unsupported Storage Format elements",
            ],
        },
        {
            "category": "Testing",
            "items": [
                "Unit tests for new v2 API calls",
                "Integration tests with real Confluence instance",
                "Performance testing (v2 should be faster)",
                "Error handling and edge case testing",
                "Backward compatibility testing if supporting both APIs",
            ],
        },
        {
            "category": "Deployment",
            "items": [
                "Feature flags for gradual v2 rollout",
                "Monitoring and logging for v2 API calls",
                "Performance metrics comparison",
                "User acceptance testing",
                "Documentation updates for API changes",
            ],
        },
    ]

    for section in checklist:
        print(f"{section['category']}:")
        for item in section["items"]:
            status = "✅" if item.startswith("✅") else "☐"
            clean_item = item.replace("✅ ", "")
            print(f"  {status} {clean_item}")
        print()

    print("Migration Resources:")
    print("  • Confluence Cloud REST API v2: https://developer.atlassian.com/cloud/confluence/rest/v2/")
    print("  • ADF Documentation: https://developer.atlassian.com/cloud/confluence/adf/")
    print("  • Migration Guide: https://developer.atlassian.com/cloud/confluence/migration-guide/")
    print("  • Community Support: Atlassian Developer Community")


def main():
    """Main function demonstrating v1 to v2 migration."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    print("Confluence Cloud v1 to v2 API Migration Guide")
    print("=" * 50)
    print()

    # Run all demonstrations
    demonstrate_api_differences()
    demonstrate_dual_api_usage()
    demonstrate_content_migration()
    demonstrate_pagination_migration()
    provide_migration_checklist()

    print("\n" + "=" * 50)
    print("Migration demonstration completed!")
    print("\nNext steps:")
    print("1. Review the created pages in your Confluence instance")
    print("2. Compare the v1 and v2 page structures")
    print("3. Use the migration checklist to plan your transition")
    print("4. Start with low-risk operations for initial v2 testing")
    print("5. Gradually migrate more complex operations")


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
