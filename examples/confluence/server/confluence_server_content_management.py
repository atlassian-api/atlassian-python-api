#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Server Content Management

This example demonstrates how to use the Confluence Server API client
for basic content management operations.
"""

from atlassian.confluence import ConfluenceServer


def main():
    """Main function demonstrating Confluence Server content management."""

    # Initialize Confluence Server client
    # Replace with your actual Confluence Server URL and credentials
    confluence = ConfluenceServer(
        url="https://your-confluence-server.com", username="your-username", password="your-password"
    )

    print("=== Confluence Server Content Management Example ===\n")

    try:
        # Get all spaces
        print("1. Getting all spaces...")
        spaces = confluence.get_spaces()
        print(f"   Found {len(spaces.get('results', []))} spaces")

        if spaces.get("results"):
            first_space = spaces["results"][0]
            space_key = first_space["key"]
            print(f"   Using space: {first_space['name']} (Key: {space_key})")

            # Get space content
            print("\n2. Getting space content...")
            content = confluence.get_space_content(space_key)
            print(f"   Found {len(content.get('results', []))} content items")

            # Get all pages from space
            print("\n3. Getting all pages from space...")
            pages = confluence.get_all_pages_from_space(space_key)
            print(f"   Found {len(pages.get('results', []))} pages")

            if pages.get("results"):
                first_page = pages["results"][0]
                page_id = first_page["id"]
                page_title = first_page["title"]
                print(f"   Using page: {page_title} (ID: {page_id})")

                # Check if page exists
                print("\n4. Checking if page exists...")
                page_exists = confluence.page_exists(space_key, page_title)
                print(f"   Page exists: {page_exists}")

                # Get page details
                print("\n5. Getting page details...")
                page_details = confluence.get_content_by_id(page_id, expand="space,version")
                print(f"   Page title: {page_details.get('title')}")
                print(f"   Page type: {page_details.get('type')}")
                print(f"   Version: {page_details.get('version', {}).get('number')}")
                print(f"   Space: {page_details.get('space', {}).get('name')}")

                # Get page children
                print("\n6. Getting page children...")
                children = confluence.get_content_children(page_id)
                print(f"   Found {len(children.get('results', []))} child items")

                # Get page labels
                print("\n7. Getting page labels...")
                labels = confluence.get_content_labels(page_id)
                print(f"   Found {len(labels.get('results', []))} labels")

                # Get page comments
                print("\n8. Getting page comments...")
                comments = confluence.get_comments(page_id)
                print(f"   Found {len(comments.get('results', []))} comments")

                # Get page attachments
                print("\n9. Getting page attachments...")
                attachments = confluence.get_attachments(page_id)
                print(f"   Found {len(attachments.get('results', []))} attachments")

                # Get page properties
                print("\n10. Getting page properties...")
                properties = confluence.get_content_properties(page_id)
                print(f"   Found {len(properties.get('results', []))} properties")

                # Get page space
                print("\n11. Getting page space...")
                page_space = confluence.get_page_space(page_id)
                print(f"   Page space key: {page_space}")

        # Get all blog posts from space
        print("\n12. Getting all blog posts from space...")
        blog_posts = confluence.get_all_blog_posts_from_space(space_key)
        print(f"   Found {len(blog_posts.get('results', []))} blog posts")

        # Get draft pages
        print("\n13. Getting draft pages from space...")
        draft_pages = confluence.get_all_draft_pages_from_space(space_key)
        print(f"   Found {len(draft_pages.get('results', []))} draft pages")

        # Get trash content
        print("\n14. Getting trash content from space...")
        trash_content = confluence.get_trash_content(space_key)
        print(f"   Found {len(trash_content.get('results', []))} trashed items")

        # Search for content using CQL
        print("\n15. Searching for content using CQL...")
        search_results = confluence.search_content("type=page")
        print(f"   Found {len(search_results.get('results', []))} pages in search")

        # Get current user
        print("\n16. Getting current user...")
        current_user = confluence.get_current_user()
        print(f"   Current user: {current_user.get('displayName')} ({current_user.get('username')})")

        # Get users
        print("\n17. Getting users...")
        users = confluence.get_users()
        print(f"   Found {len(users.get('results', []))} users")

        # Get groups
        print("\n18. Getting groups...")
        groups = confluence.get_groups()
        print(f"   Found {len(groups.get('results', []))} groups")

        # Get labels
        print("\n19. Getting all labels...")
        all_labels = confluence.get_labels()
        print(f"   Found {len(all_labels.get('results', []))} labels")

        # Get templates
        print("\n20. Getting templates...")
        templates = confluence.get_templates()
        print(f"   Found {len(templates.get('results', []))} templates")

        print("\n=== Example completed successfully! ===")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Server URL.")


if __name__ == "__main__":
    main()
