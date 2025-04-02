#!/usr/bin/env python3
"""
Example demonstrating the usage of Whiteboard and Custom Content methods
with the Confluence API v2.
"""

import os
import logging
from pprint import pprint

from atlassian.confluence_base import ConfluenceBase

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Confluence client with API v2
# Use your Confluence Cloud URL, username, and API token
url = os.environ.get("CONFLUENCE_URL")
username = os.environ.get("CONFLUENCE_USERNAME")
api_token = os.environ.get("CONFLUENCE_API_TOKEN")

# Initialize the client with API version 2
confluence = ConfluenceBase.factory(url=url, username=username, password=api_token, api_version=2)


def whiteboard_examples(space_id):
    """
    Examples of using whiteboard methods with Confluence API v2.

    Args:
        space_id: ID of the space where whiteboards will be created
    """
    print("\n=== WHITEBOARD EXAMPLES ===\n")

    # Create a whiteboard
    print("Creating whiteboard...")
    whiteboard = confluence.create_whiteboard(
        space_id=space_id, title="API Created Whiteboard", template_key="timeline"  # Optional: use a template
    )

    whiteboard_id = whiteboard["id"]
    print(f"Created whiteboard with ID: {whiteboard_id}")
    print("Whiteboard details:")
    pprint(whiteboard)

    # Get whiteboard by ID
    print("\nRetrieving whiteboard...")
    retrieved_whiteboard = confluence.get_whiteboard_by_id(whiteboard_id)
    print(f"Retrieved whiteboard title: {retrieved_whiteboard['title']}")

    # Create a nested whiteboard
    print("\nCreating nested whiteboard...")
    nested_whiteboard = confluence.create_whiteboard(
        space_id=space_id, title="Nested Whiteboard", parent_id=whiteboard_id
    )

    nested_whiteboard_id = nested_whiteboard["id"]
    print(f"Created nested whiteboard with ID: {nested_whiteboard_id}")

    # Get whiteboard children
    print("\nRetrieving whiteboard children...")
    children = confluence.get_whiteboard_children(whiteboard_id)
    print(f"Whiteboard has {len(children)} children:")
    for child in children:
        print(f"- {child['title']} (ID: {child['id']})")

    # Get whiteboard ancestors
    print("\nRetrieving whiteboard ancestors...")
    ancestors = confluence.get_whiteboard_ancestors(nested_whiteboard_id)
    print(f"Nested whiteboard has {len(ancestors)} ancestors:")
    for ancestor in ancestors:
        print(f"- {ancestor.get('id')}")

    # Delete whiteboards
    print("\nDeleting nested whiteboard...")
    confluence.delete_whiteboard(nested_whiteboard_id)
    print("Nested whiteboard deleted")

    print("\nDeleting parent whiteboard...")
    confluence.delete_whiteboard(whiteboard_id)
    print("Parent whiteboard deleted")

    return whiteboard_id


def custom_content_examples(space_id, page_id=None):
    """
    Examples of using custom content methods with Confluence API v2.

    Args:
        space_id: ID of the space where custom content will be created
        page_id: (optional) ID of a page to associate custom content with
    """
    print("\n=== CUSTOM CONTENT EXAMPLES ===\n")

    # Create custom content
    print("Creating custom content...")
    custom_content = confluence.create_custom_content(
        type="my.custom.type",  # Define your custom content type
        title="API Created Custom Content",
        body="<p>This is a test custom content created via API</p>",
        space_id=space_id,
        page_id=page_id,  # Optional: associate with a page
        body_format="storage",  # Can be storage, atlas_doc_format, or raw
    )

    custom_content_id = custom_content["id"]
    print(f"Created custom content with ID: {custom_content_id}")
    print("Custom content details:")
    pprint(custom_content)

    # Get custom content by ID
    print("\nRetrieving custom content...")
    retrieved_content = confluence.get_custom_content_by_id(custom_content_id, body_format="storage")
    print(f"Retrieved custom content title: {retrieved_content['title']}")

    # Update custom content
    print("\nUpdating custom content...")
    current_version = retrieved_content["version"]["number"]
    updated_content = confluence.update_custom_content(
        custom_content_id=custom_content_id,
        type="my.custom.type",
        title="Updated Custom Content",
        body="<p>This content has been updated via API</p>",
        status="current",
        version_number=current_version + 1,
        space_id=space_id,
        page_id=page_id,
        body_format="storage",
        version_message="Updated via API example",
    )

    print(f"Updated custom content to version: {updated_content['version']['number']}")

    # Work with custom content properties
    print("\nAdding a property to custom content...")
    property_data = {"color": "blue", "priority": "high", "tags": ["example", "api", "v2"]}

    property_key = "my-example-property"

    # Create property
    created_property = confluence.create_custom_content_property(
        custom_content_id=custom_content_id, key=property_key, value=property_data
    )

    print(f"Created property with key: {created_property['key']}")

    # Get properties
    print("\nRetrieving custom content properties...")
    properties = confluence.get_custom_content_properties(custom_content_id)
    print(f"Custom content has {len(properties)} properties:")
    for prop in properties:
        print(f"- {prop['key']}")

    # Get specific property
    print(f"\nRetrieving specific property '{property_key}'...")
    property_details = confluence.get_custom_content_property_by_key(
        custom_content_id=custom_content_id, property_key=property_key
    )
    print("Property value:")
    pprint(property_details["value"])

    # Update property
    print("\nUpdating property...")
    property_data["color"] = "red"
    property_data["status"] = "active"

    updated_property = confluence.update_custom_content_property(
        custom_content_id=custom_content_id,
        key=property_key,
        value=property_data,
        version_number=property_details["version"]["number"] + 1,
    )

    print(f"Updated property to version: {updated_property['version']['number']}")

    # Add labels to custom content
    print("\nAdding labels to custom content...")
    label1 = confluence.add_custom_content_label(custom_content_id=custom_content_id, label="api-example")

    label2 = confluence.add_custom_content_label(
        custom_content_id=custom_content_id, label="documentation", prefix="global"
    )

    print(f"Added labels: {label1['name']}, {label2['prefix']}:{label2['name']}")

    # Get labels
    print("\nRetrieving custom content labels...")
    labels = confluence.get_custom_content_labels(custom_content_id)
    print(f"Custom content has {len(labels)} labels:")
    for label in labels:
        prefix = f"{label['prefix']}:" if label.get("prefix") else ""
        print(f"- {prefix}{label['name']}")

    # Create nested custom content
    print("\nCreating nested custom content...")
    nested_content = confluence.create_custom_content(
        type="my.custom.child.type",
        title="Nested Custom Content",
        body="<p>This is a nested custom content</p>",
        custom_content_id=custom_content_id,  # Set parent ID
        body_format="storage",
    )

    nested_content_id = nested_content["id"]
    print(f"Created nested custom content with ID: {nested_content_id}")

    # Get children
    print("\nRetrieving custom content children...")
    children = confluence.get_custom_content_children(custom_content_id)
    print(f"Custom content has {len(children)} children:")
    for child in children:
        print(f"- {child['title']} (ID: {child['id']})")

    # Get ancestors
    print("\nRetrieving custom content ancestors...")
    ancestors = confluence.get_custom_content_ancestors(nested_content_id)
    print(f"Nested custom content has {len(ancestors)} ancestors:")
    for ancestor in ancestors:
        print(f"- {ancestor.get('id')}")

    # Clean up - delete custom content
    # Delete property first
    print("\nDeleting property...")
    confluence.delete_custom_content_property(custom_content_id=custom_content_id, key=property_key)
    print(f"Deleted property {property_key}")

    # Delete label
    print("\nDeleting label...")
    confluence.delete_custom_content_label(custom_content_id=custom_content_id, label="api-example")
    print("Deleted label 'api-example'")

    # Delete nested custom content
    print("\nDeleting nested custom content...")
    confluence.delete_custom_content(nested_content_id)
    print(f"Deleted nested custom content {nested_content_id}")

    # Delete parent custom content
    print("\nDeleting parent custom content...")
    confluence.delete_custom_content(custom_content_id)
    print(f"Deleted parent custom content {custom_content_id}")

    return custom_content_id


def main():
    """
    Main function to run the examples.
    """
    # Replace these with actual IDs from your Confluence instance
    space_id = "123456"  # Replace with a real space ID
    page_id = "789012"  # Replace with a real page ID (optional)

    try:
        # Run whiteboard examples
        whiteboard_examples(space_id)

        # Run custom content examples (page_id is optional)
        custom_content_examples(space_id, page_id)
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    logging.info("Running Confluence V2 Content Types Examples")

    if not url or not username or not api_token:
        logging.error(
            "Please set the environment variables: " "CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN"
        )
    else:
        main()
