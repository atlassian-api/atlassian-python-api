#!/usr/bin/env python3
"""
Example demonstrating the compatibility layer of Confluence API v2.
Shows how to use both v2 methods and v1 method names via the compatibility layer.
"""

import os
import logging
import warnings

from atlassian import ConfluenceV2

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get credentials from environment variables
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://your-domain.atlassian.net")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME", "email@example.com")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN", "api-token")

# Initialize the ConfluenceV2 client
confluence = ConfluenceV2(url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_API_TOKEN, cloud=True)


def demonstrate_v1_v2_method_equivalence():
    """
    Demonstrate equivalence between v1 and v2 method names.
    Shows how to use both naming conventions with ConfluenceV2.
    """
    print("=== Confluence V2 API Method Name Compatibility ===\n")

    # Show available method mappings
    print("Available method mappings from v1 to v2:")
    for v1_method, v2_method in sorted(confluence._compatibility_method_mapping.items()):
        print(f"  {v1_method} -> {v2_method}")
    print()

    # Example 1: Get page by ID
    # -------------------------------------
    print("Example 1: Get page by ID")
    print("v1 method name: get_content_by_id(page_id)")
    print("v2 method name: get_page_by_id(page_id)")

    page_id = "12345"  # Replace with a real page ID to test

    # Enable warning capture
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Using v1 method name (will show deprecation warning)
        try:
            print("\nAttempting to use v1 method name:")
            # page = confluence.get_content_by_id(page_id)
            print(f"Would call: confluence.get_content_by_id('{page_id}')")
            print("This would show a deprecation warning")
        except Exception as e:
            print(f"Error: {e}")

        # Using v2 method name (preferred)
        try:
            print("\nUsing v2 method name (preferred):")
            # page = confluence.get_page_by_id(page_id)
            print(f"Would call: confluence.get_page_by_id('{page_id}')")
            print("No deprecation warning")
        except Exception as e:
            print(f"Error: {e}")

    # Example 2: Create content/page
    # -------------------------------------
    print("\nExample 2: Create content/page")
    print("v1 method name: create_content(space_id, title, body, ...)")
    print("v2 method name: create_page(space_id, title, body, ...)")

    space_id = "67890"  # Replace with a real space ID to test
    title = "Test Page"
    body = "<p>This is a test page.</p>"

    # Using v1 method name (will show deprecation warning)
    try:
        print("\nAttempting to use v1 method name:")
        # page = confluence.create_content(space_id=space_id, title=title, body=body)
        print(f"Would call: confluence.create_content(space_id='{space_id}', title='{title}', body='...')")
        print("This would show a deprecation warning")
    except Exception as e:
        print(f"Error: {e}")

    # Using v2 method name (preferred)
    try:
        print("\nUsing v2 method name (preferred):")
        # page = confluence.create_page(space_id=space_id, title=title, body=body)
        print(f"Would call: confluence.create_page(space_id='{space_id}', title='{title}', body='...')")
        print("No deprecation warning")
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Get spaces
    # -------------------------------------
    print("\nExample 3: Get spaces")
    print("v1 method name: get_all_spaces()")
    print("v2 method name: get_spaces()")

    # Using v1 method name (will show deprecation warning)
    try:
        print("\nAttempting to use v1 method name:")
        # spaces = confluence.get_all_spaces()
        print("Would call: confluence.get_all_spaces()")
        print("This would show a deprecation warning")
    except Exception as e:
        print(f"Error: {e}")

    # Using v2 method name (preferred)
    try:
        print("\nUsing v2 method name (preferred):")
        # spaces = confluence.get_spaces()
        print("Would call: confluence.get_spaces()")
        print("No deprecation warning")
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Working with properties
    # -------------------------------------
    print("\nExample 4: Working with properties")
    print("v1 method names: add_property(), get_property(), get_properties()")
    print("v2 method names: create_page_property(), get_page_property_by_key(), get_page_properties()")

    # Using v1 method names (will show deprecation warnings)
    try:
        print("\nAttempting to use v1 method names:")
        # prop = confluence.add_property(page_id, "example-key", {"value": "example"})
        # prop_value = confluence.get_property(page_id, "example-key")
        # all_props = confluence.get_properties(page_id)
        print(f"Would call: confluence.add_property('{page_id}', 'example-key', ...)")
        print(f"Would call: confluence.get_property('{page_id}', 'example-key')")
        print(f"Would call: confluence.get_properties('{page_id}')")
        print("These would show deprecation warnings")
    except Exception as e:
        print(f"Error: {e}")

    # Using v2 method names (preferred)
    try:
        print("\nUsing v2 method names (preferred):")
        # prop = confluence.create_page_property(page_id, "example-key", {"value": "example"})
        # prop_value = confluence.get_page_property_by_key(page_id, "example-key")
        # all_props = confluence.get_page_properties(page_id)
        print(f"Would call: confluence.create_page_property('{page_id}', 'example-key', ...)")
        print(f"Would call: confluence.get_page_property_by_key('{page_id}', 'example-key')")
        print(f"Would call: confluence.get_page_properties('{page_id}')")
        print("No deprecation warnings")
    except Exception as e:
        print(f"Error: {e}")


def show_migration_recommendations():
    """Show recommendations for migrating from v1 to v2 API."""
    print("\n=== Migration Recommendations ===\n")
    print("1. Use ConfluenceV2 class for all new code")
    print("2. Prefer v2 method names over v1 method names")
    print("3. When upgrading existing code:")
    print("   a. Search for v1 method names and replace with v2 equivalents")
    print("   b. Pay attention to parameter differences")
    print("   c. Update response handling as v2 API may return different structures")
    print("4. Temporarily enable deprecation warnings to find usage of deprecated methods:")
    print("   import warnings")
    print("   warnings.filterwarnings('always', category=DeprecationWarning)")
    print("5. Consult the method mapping dictionary for v1->v2 equivalents:")
    print("   confluence._compatibility_method_mapping")


if __name__ == "__main__":
    print("Running Confluence V2 API Compatibility Example\n")

    # Temporarily enable warnings to show deprecation messages
    warnings.filterwarnings("always", category=DeprecationWarning)

    if not CONFLUENCE_URL or not CONFLUENCE_USERNAME or not CONFLUENCE_API_TOKEN:
        print(
            "NOTE: This example shows code snippets but doesn't execute real API calls.\n"
            "To run with real API calls, set these environment variables:\n"
            "- CONFLUENCE_URL\n"
            "- CONFLUENCE_USERNAME\n"
            "- CONFLUENCE_API_TOKEN\n"
        )

    demonstrate_v1_v2_method_equivalence()
    show_migration_recommendations()
