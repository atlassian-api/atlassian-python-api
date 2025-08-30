#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud Content Management

This example demonstrates how to use the Confluence Cloud API client
for basic content management operations.
"""

from atlassian.confluence import ConfluenceCloud


def main():
    """Main function demonstrating Confluence Cloud content management."""

    # Initialize Confluence Cloud client
    # Replace with your actual Confluence Cloud URL and credentials
    confluence = ConfluenceCloud(
        url="https://your-domain.atlassian.net", token="your-api-token"  # Use API token for Cloud
    )

    print("=== Confluence Cloud Content Management Example ===\n")

    try:
        # Get all spaces
        print("1. Getting all spaces...")
        spaces = confluence.get_spaces()
        print(f"   Found {len(spaces.get('results', []))} spaces")

        if spaces.get("results"):
            first_space = spaces["results"][0]
            space_id = first_space["id"]
            print(f"   Using space: {first_space['name']} (ID: {space_id})")

            # Get space content
            print("\n2. Getting space content...")
            content = confluence.get_space_content(space_id)
            print(f"   Found {len(content.get('results', []))} content items")

            # Get content by type (pages)
            print("\n3. Getting pages from space...")
            pages = confluence.get_content_by_type("page")
            print(f"   Found {len(pages.get('results', []))} pages")

            if pages.get("results"):
                first_page = pages["results"][0]
                page_id = first_page["id"]
                print(f"   Using page: {first_page['title']} (ID: {page_id})")

                # Get page details
                print("\n4. Getting page details...")
                page_details = confluence.get_content(page_id)
                print(f"   Page title: {page_details.get('title')}")
                print(f"   Page type: {page_details.get('type')}")
                print(f"   Created: {page_details.get('createdAt')}")

                # Get page children
                print("\n5. Getting page children...")
                children = confluence.get_content_children(page_id)
                print(f"   Found {len(children.get('results', []))} child items")

                # Get page labels
                print("\n6. Getting page labels...")
                labels = confluence.get_content_labels(page_id)
                print(f"   Found {len(labels.get('results', []))} labels")

                # Get page comments
                print("\n7. Getting page comments...")
                comments = confluence.get_comments(page_id)
                print(f"   Found {len(comments.get('results', []))} comments")

                # Get page attachments
                print("\n8. Getting page attachments...")
                attachments = confluence.get_attachments(page_id)
                print(f"   Found {len(attachments.get('results', []))} attachments")

        # Search for content
        print("\n9. Searching for content...")
        search_results = confluence.search_content("type=page")
        print(f"   Found {len(search_results.get('results', []))} pages in search")

        # Get current user
        print("\n10. Getting current user...")
        current_user = confluence.get_current_user()
        print(f"   Current user: {current_user.get('displayName')} ({current_user.get('accountId')})")

        print("\n=== Example completed successfully! ===")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")


if __name__ == "__main__":
    main()
