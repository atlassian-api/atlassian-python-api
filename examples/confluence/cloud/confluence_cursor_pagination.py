#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud Cursor-Based Pagination

This example demonstrates how to use cursor-based pagination with the Confluence Cloud v2 API.
Cursor-based pagination is more efficient than offset-based pagination, especially for large
datasets, and provides better performance and consistency.

Key features demonstrated:
- Basic cursor pagination for pages and spaces
- Handling pagination state and continuation
- Performance comparison with offset-based pagination
- Best practices for large dataset processing
- Error handling and edge cases
- Memory-efficient iteration patterns

Prerequisites:
- Confluence Cloud instance with multiple pages/spaces
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_cursor_pagination.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
import time
from typing import Dict, Any, List, Optional, Iterator, Tuple
from datetime import datetime

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


class CursorPaginationHelper:
    """
    Helper class for cursor-based pagination with the Confluence v2 API.

    This class provides utilities for efficiently iterating through large
    datasets using cursor-based pagination.
    """

    def __init__(self, confluence_client: ConfluenceCloud):
        """
        Initialize the pagination helper.

        Args:
            confluence_client: ConfluenceCloud client with v2 API enabled
        """
        self.confluence = confluence_client
        if not hasattr(confluence_client, "_v2_client") or confluence_client._v2_client is None:
            raise ValueError("Confluence client must have v2 API enabled")

    def iterate_pages(
        self, space_id: Optional[str] = None, limit: int = 25, max_pages: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Iterate through pages using cursor-based pagination.

        Args:
            space_id: Optional space ID to filter by
            limit: Number of results per API call
            max_pages: Maximum number of pages to retrieve (None for all)

        Yields:
            Individual page dictionaries
        """
        cursor = None
        pages_retrieved = 0

        while True:
            # Make API call
            response = self.confluence._v2_client.get_pages(space_id=space_id, limit=limit, cursor=cursor)

            # Yield individual pages
            pages = response.get("results", [])
            for page in pages:
                if max_pages and pages_retrieved >= max_pages:
                    return
                yield page
                pages_retrieved += 1

            # Check for next page
            next_link = response.get("_links", {}).get("next")
            if not next_link:
                break

            # Extract cursor from next link
            cursor = self._extract_cursor_from_url(next_link.get("href", ""))
            if not cursor:
                break

    def iterate_spaces(self, limit: int = 25, max_spaces: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """
        Iterate through spaces using cursor-based pagination.

        Args:
            limit: Number of results per API call
            max_spaces: Maximum number of spaces to retrieve (None for all)

        Yields:
            Individual space dictionaries
        """
        cursor = None
        spaces_retrieved = 0

        while True:
            # Make API call
            response = self.confluence._v2_client.get_spaces(limit=limit, cursor=cursor)

            # Yield individual spaces
            spaces = response.get("results", [])
            for space in spaces:
                if max_spaces and spaces_retrieved >= max_spaces:
                    return
                yield space
                spaces_retrieved += 1

            # Check for next page
            next_link = response.get("_links", {}).get("next")
            if not next_link:
                break

            # Extract cursor from next link
            cursor = self._extract_cursor_from_url(next_link.get("href", ""))
            if not cursor:
                break

    def get_page_batch(
        self, space_id: Optional[str] = None, limit: int = 25, cursor: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Get a batch of pages and return the next cursor.

        Args:
            space_id: Optional space ID to filter by
            limit: Number of results per API call
            cursor: Current cursor position

        Returns:
            Tuple of (pages_list, next_cursor)
        """
        response = self.confluence._v2_client.get_pages(space_id=space_id, limit=limit, cursor=cursor)

        pages = response.get("results", [])
        next_link = response.get("_links", {}).get("next")
        next_cursor = None

        if next_link:
            next_cursor = self._extract_cursor_from_url(next_link.get("href", ""))

        return pages, next_cursor

    def _extract_cursor_from_url(self, url: str) -> Optional[str]:
        """
        Extract cursor parameter from a pagination URL.

        Args:
            url: URL containing cursor parameter

        Returns:
            Cursor string or None if not found
        """
        if not url or "cursor=" not in url:
            return None

        # Simple extraction - in production, use proper URL parsing
        try:
            cursor_start = url.find("cursor=") + 7
            cursor_end = url.find("&", cursor_start)
            if cursor_end == -1:
                cursor_end = len(url)
            return url[cursor_start:cursor_end]
        except Exception:
            return None


def demonstrate_basic_cursor_pagination():
    """
    Demonstrate basic cursor-based pagination.
    """
    print("=== Basic Cursor Pagination ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()

    try:
        # Get first batch of spaces
        print("1. Getting first batch of spaces...")
        spaces_response = confluence._v2_client.get_spaces(limit=3)
        spaces = spaces_response.get("results", [])

        print(f"   Retrieved {len(spaces)} spaces")
        for i, space in enumerate(spaces, 1):
            print(f"   {i}. {space.get('name')} (ID: {space.get('id')})")

        # Check for next page
        next_link = spaces_response.get("_links", {}).get("next")
        if next_link:
            print(f"\n   Next page available: {next_link.get('href')}")

            # Extract cursor from URL (simplified)
            cursor = None
            href = next_link.get("href", "")
            if "cursor=" in href:
                cursor_start = href.find("cursor=") + 7
                cursor_end = href.find("&", cursor_start)
                if cursor_end == -1:
                    cursor_end = len(href)
                cursor = href[cursor_start:cursor_end]

            if cursor:
                print(f"   Cursor: {cursor[:20]}..." if len(cursor) > 20 else f"   Cursor: {cursor}")

                # Get next batch using cursor
                print("\n2. Getting next batch using cursor...")
                next_response = confluence._v2_client.get_spaces(limit=3, cursor=cursor)
                next_spaces = next_response.get("results", [])

                print(f"   Retrieved {len(next_spaces)} more spaces")
                for i, space in enumerate(next_spaces, len(spaces) + 1):
                    print(f"   {i}. {space.get('name')} (ID: {space.get('id')})")
        else:
            print("\n   No more spaces available")

        print("\n✅ Basic cursor pagination demonstrated!")

    except Exception as e:
        print(f"\nError occurred: {e}")


def demonstrate_iterator_pattern():
    """
    Demonstrate using iterator pattern for efficient pagination.
    """
    print("=== Iterator Pattern for Pagination ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()

    try:
        # Create pagination helper
        paginator = CursorPaginationHelper(confluence)

        print("1. Iterating through all spaces...")
        space_count = 0
        for space in paginator.iterate_spaces(limit=5, max_spaces=10):
            space_count += 1
            print(f"   {space_count}. {space.get('name')} (ID: {space.get('id')})")

        print(f"\n   Total spaces processed: {space_count}")

        # Find a space with pages
        print("\n2. Finding space with pages...")
        target_space_id = None
        for space in paginator.iterate_spaces(limit=10):
            # Check if space has pages
            pages_response = confluence._v2_client.get_pages(space_id=space["id"], limit=1)
            if pages_response.get("results"):
                target_space_id = space["id"]
                print(f"   Using space: {space.get('name')} (ID: {target_space_id})")
                break

        if target_space_id:
            print("\n3. Iterating through pages in space...")
            page_count = 0
            for page in paginator.iterate_pages(space_id=target_space_id, limit=5, max_pages=10):
                page_count += 1
                print(f"   {page_count}. {page.get('title')} (ID: {page.get('id')})")

            print(f"\n   Total pages processed: {page_count}")
        else:
            print("\n   No spaces with pages found")

        print("\n✅ Iterator pattern demonstrated!")

    except Exception as e:
        print(f"\nError occurred: {e}")


def demonstrate_batch_processing():
    """
    Demonstrate batch processing with cursor pagination.
    """
    print("=== Batch Processing with Cursors ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()

    try:
        paginator = CursorPaginationHelper(confluence)

        print("1. Processing pages in batches...")

        # Find a space to work with
        spaces_response = confluence._v2_client.get_spaces(limit=5)
        spaces = spaces_response.get("results", [])

        if not spaces:
            print("   No spaces found")
            return

        target_space = spaces[0]
        space_id = target_space["id"]
        print(f"   Using space: {target_space.get('name')} (ID: {space_id})")

        # Process pages in batches
        cursor = None
        batch_number = 0
        total_pages = 0

        while True:
            batch_number += 1
            print(f"\n   Processing batch {batch_number}...")

            # Get batch of pages
            pages, next_cursor = paginator.get_page_batch(space_id=space_id, limit=3, cursor=cursor)

            if not pages:
                print("     No more pages")
                break

            # Process batch
            print(f"     Batch size: {len(pages)}")
            for i, page in enumerate(pages, 1):
                print(f"     {i}. {page.get('title')} (Version: {page.get('version', {}).get('number', 'N/A')})")

            total_pages += len(pages)

            # Check for next batch
            if not next_cursor:
                print("     No more batches")
                break

            cursor = next_cursor

            # Simulate processing time
            time.sleep(0.1)

        print(f"\n   Processed {batch_number} batches with {total_pages} total pages")
        print("\n✅ Batch processing demonstrated!")

    except Exception as e:
        print(f"\nError occurred: {e}")


def demonstrate_performance_comparison():
    """
    Demonstrate performance comparison between cursor and offset pagination.
    """
    print("=== Performance Comparison ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)

    try:
        # Test v1 offset-based pagination
        print("1. Testing v1 offset-based pagination...")
        confluence.disable_v2_api()

        start_time = time.time()
        v1_pages = []

        try:
            # Get pages using v1 API (offset-based)
            response = confluence.get_all_pages_from_space(space=TEST_SPACE_KEY, start=0, limit=10, expand="version")
            v1_pages = response if isinstance(response, list) else []
        except Exception as e:
            print(f"   v1 API error (expected if space doesn't exist): {e}")

        v1_time = time.time() - start_time
        print(f"   v1 API: Retrieved {len(v1_pages)} pages in {v1_time:.3f} seconds")

        # Test v2 cursor-based pagination
        print("\n2. Testing v2 cursor-based pagination...")
        confluence.enable_v2_api()

        start_time = time.time()
        v2_pages = []

        # Find space ID
        spaces_response = confluence._v2_client.get_spaces(limit=10)
        space_id = None
        for space in spaces_response.get("results", []):
            if space.get("key") == TEST_SPACE_KEY:
                space_id = space.get("id")
                break

        if not space_id and spaces_response.get("results"):
            space_id = spaces_response["results"][0]["id"]

        if space_id:
            # Get pages using v2 API (cursor-based)
            response = confluence._v2_client.get_pages(space_id=space_id, limit=10)
            v2_pages = response.get("results", [])

        v2_time = time.time() - start_time
        print(f"   v2 API: Retrieved {len(v2_pages)} pages in {v2_time:.3f} seconds")

        # Compare results
        print("\n3. Performance comparison:")
        if v1_time > 0 and v2_time > 0:
            improvement = ((v1_time - v2_time) / v1_time) * 100
            print(f"   Time improvement: {improvement:.1f}%")

        print(f"   v1 pages retrieved: {len(v1_pages)}")
        print(f"   v2 pages retrieved: {len(v2_pages)}")

        # Advantages of cursor pagination
        print("\n4. Cursor pagination advantages:")
        advantages = [
            "Consistent performance regardless of offset",
            "No duplicate results during concurrent modifications",
            "Better memory usage for large datasets",
            "More efficient database queries on the server",
            "Handles real-time data changes gracefully",
        ]

        for advantage in advantages:
            print(f"   • {advantage}")

        print("\n✅ Performance comparison completed!")

    except Exception as e:
        print(f"\nError occurred: {e}")


def demonstrate_error_handling():
    """
    Demonstrate error handling with cursor pagination.
    """
    print("=== Error Handling with Cursor Pagination ===\n")

    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()

    try:
        print("1. Testing invalid cursor handling...")

        # Test with invalid cursor
        try:
            response = confluence._v2_client.get_pages(limit=5, cursor="invalid-cursor-value")
            print("   Unexpected: Invalid cursor was accepted")
        except Exception as e:
            print(f"   ✅ Invalid cursor properly rejected: {type(e).__name__}")

        print("\n2. Testing empty results handling...")

        # Test with non-existent space
        try:
            response = confluence._v2_client.get_pages(space_id="non-existent-space-id", limit=5)
            results = response.get("results", [])
            print(f"   Empty results handled gracefully: {len(results)} results")
        except Exception as e:
            print(f"   Error with non-existent space: {type(e).__name__}")

        print("\n3. Best practices for error handling:")
        best_practices = [
            "Always check for 'results' key in response",
            "Validate cursor format before using",
            "Handle network timeouts gracefully",
            "Implement retry logic for transient errors",
            "Log pagination state for debugging",
            "Set reasonable limits to avoid memory issues",
        ]

        for practice in best_practices:
            print(f"   • {practice}")

        print("\n4. Example error-safe pagination code:")
        print("""
   ```python
   def safe_paginate_pages(confluence, space_id, limit=25):
       cursor = None
       all_pages = []
       
       while True:
           try:
               response = confluence._v2_client.get_pages(
                   space_id=space_id,
                   limit=limit,
                   cursor=cursor
               )
               
               pages = response.get('results', [])
               if not pages:
                   break
               
               all_pages.extend(pages)
               
               # Get next cursor
               next_link = response.get('_links', {}).get('next')
               if not next_link:
                   break
               
               cursor = extract_cursor(next_link.get('href'))
               if not cursor:
                   break
                   
           except Exception as e:
               print(f"Pagination error: {e}")
               break
       
       return all_pages
   ```
        """)

        print("\n✅ Error handling demonstrated!")

    except Exception as e:
        print(f"\nError occurred: {e}")


def provide_pagination_best_practices():
    """
    Provide best practices for cursor-based pagination.
    """
    print("=== Cursor Pagination Best Practices ===\n")

    practices = [
        {
            "category": "Performance",
            "items": [
                "Use appropriate page sizes (25-100 items per request)",
                "Don't request more data than you need",
                "Consider parallel processing for independent operations",
                "Cache cursors for resumable operations",
                "Monitor API rate limits and adjust accordingly",
            ],
        },
        {
            "category": "Reliability",
            "items": [
                "Always validate cursor values before use",
                "Implement exponential backoff for retries",
                "Handle network timeouts gracefully",
                "Store pagination state for long-running operations",
                "Test with empty result sets",
            ],
        },
        {
            "category": "Memory Management",
            "items": [
                "Process items as you receive them (streaming)",
                "Don't accumulate all results in memory",
                "Use generators/iterators for large datasets",
                "Clean up processed items promptly",
                "Set maximum limits to prevent runaway operations",
            ],
        },
        {
            "category": "User Experience",
            "items": [
                "Show progress indicators for long operations",
                "Allow users to cancel long-running operations",
                "Provide estimated completion times when possible",
                "Handle partial failures gracefully",
                "Log operations for troubleshooting",
            ],
        },
    ]

    for section in practices:
        print(f"{section['category']}:")
        for item in section["items"]:
            print(f"  • {item}")
        print()

    print("Common Pitfalls to Avoid:")
    pitfalls = [
        "Storing all results in memory for large datasets",
        "Not handling cursor expiration",
        "Ignoring rate limits",
        "Not validating cursor format",
        "Assuming cursors are reusable across sessions",
        "Not implementing proper error recovery",
    ]

    for pitfall in pitfalls:
        print(f"  ❌ {pitfall}")

    print("\nRecommended Libraries:")
    print("  • requests-ratelimiter: For rate limit handling")
    print("  • tenacity: For retry logic")
    print("  • tqdm: For progress bars")
    print("  • asyncio: For concurrent operations")


def main():
    """Main function demonstrating cursor-based pagination."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    print("Confluence Cloud Cursor-Based Pagination Examples")
    print("=" * 55)
    print()

    # Run all demonstrations
    demonstrate_basic_cursor_pagination()
    print("\n" + "-" * 55 + "\n")

    demonstrate_iterator_pattern()
    print("\n" + "-" * 55 + "\n")

    demonstrate_batch_processing()
    print("\n" + "-" * 55 + "\n")

    demonstrate_performance_comparison()
    print("\n" + "-" * 55 + "\n")

    demonstrate_error_handling()
    print("\n" + "-" * 55 + "\n")

    provide_pagination_best_practices()

    print("\n" + "=" * 55)
    print("Cursor pagination demonstration completed!")
    print("\nKey takeaways:")
    print("1. Cursor pagination is more efficient than offset pagination")
    print("2. Use iterators for memory-efficient processing")
    print("3. Always handle errors and edge cases")
    print("4. Monitor performance and adjust page sizes accordingly")
    print("5. Consider user experience for long-running operations")


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
