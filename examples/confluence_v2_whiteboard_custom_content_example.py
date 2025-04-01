#!/usr/bin/env python3
"""
Example for working with Confluence API V2 whiteboards and custom content.
"""

import logging
import os
import json
from atlassian import ConfluenceV2

logging.basicConfig(level=logging.INFO)

# Get credentials from environment variables
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://your-domain.atlassian.net")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME", "email@example.com")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN", "api-token")

# Initialize the ConfluenceV2 client
confluence = ConfluenceV2(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_USERNAME,
    password=CONFLUENCE_API_TOKEN,
    cloud=True
)


def pretty_print(data):
    """Print data in a readable format"""
    if isinstance(data, (list, dict)):
        print(json.dumps(data, indent=4))
    else:
        print(data)


# Whiteboard Examples

def create_whiteboard_example(space_id, title, parent_id=None):
    """
    Example demonstrating how to create a new whiteboard.
    
    Args:
        space_id: ID of the space where the whiteboard will be created
        title: Title of the new whiteboard
        parent_id: Optional parent ID (can be a page or another whiteboard)
    """
    print(f"\n=== Creating a new whiteboard '{title}' ===")
    
    try:
        # Create a whiteboard with default template
        whiteboard = confluence.create_whiteboard(
            space_id=space_id,
            title=title,
            parent_id=parent_id,
            template_key="timeline",  # Other options: blank, grid, mindmap, timeline
            locale="en-US"
        )
        
        print(f"Created whiteboard: {whiteboard['title']} (ID: {whiteboard['id']})")
        return whiteboard["id"]
    
    except Exception as e:
        print(f"Error creating whiteboard: {e}")
        return None


def get_whiteboard_example(whiteboard_id):
    """
    Example demonstrating how to retrieve a whiteboard by its ID.
    
    Args:
        whiteboard_id: ID of the whiteboard to retrieve
    """
    print(f"\n=== Getting whiteboard (ID: {whiteboard_id}) ===")
    
    try:
        whiteboard = confluence.get_whiteboard_by_id(whiteboard_id)
        print(f"Retrieved whiteboard: {whiteboard['title']}")
        pretty_print(whiteboard)
        return whiteboard
    
    except Exception as e:
        print(f"Error retrieving whiteboard: {e}")
        return None


def get_whiteboard_children_example(whiteboard_id):
    """
    Example demonstrating how to retrieve children of a whiteboard.
    
    Args:
        whiteboard_id: ID of the whiteboard to retrieve children for
    """
    print(f"\n=== Getting children of whiteboard (ID: {whiteboard_id}) ===")
    
    try:
        children = confluence.get_whiteboard_children(whiteboard_id, limit=10)
        
        if children:
            print(f"Found {len(children)} children for whiteboard")
            for child in children:
                print(f"- {child.get('title', 'No title')} (ID: {child.get('id', 'No ID')})")
        else:
            print("No children found for this whiteboard")
        
        return children
    
    except Exception as e:
        print(f"Error retrieving whiteboard children: {e}")
        return None


def get_whiteboard_ancestors_example(whiteboard_id):
    """
    Example demonstrating how to retrieve ancestors of a whiteboard.
    
    Args:
        whiteboard_id: ID of the whiteboard to retrieve ancestors for
    """
    print(f"\n=== Getting ancestors of whiteboard (ID: {whiteboard_id}) ===")
    
    try:
        ancestors = confluence.get_whiteboard_ancestors(whiteboard_id)
        
        if ancestors:
            print(f"Found {len(ancestors)} ancestors for whiteboard")
            for ancestor in ancestors:
                print(f"- {ancestor.get('title', 'No title')} (Type: {ancestor.get('type', 'Unknown')})")
        else:
            print("No ancestors found for this whiteboard")
        
        return ancestors
    
    except Exception as e:
        print(f"Error retrieving whiteboard ancestors: {e}")
        return None


def delete_whiteboard_example(whiteboard_id):
    """
    Example demonstrating how to delete a whiteboard.
    
    Args:
        whiteboard_id: ID of the whiteboard to delete
    """
    print(f"\n=== Deleting whiteboard (ID: {whiteboard_id}) ===")
    
    try:
        result = confluence.delete_whiteboard(whiteboard_id)
        print(f"Whiteboard deleted successfully")
        return True
    
    except Exception as e:
        print(f"Error deleting whiteboard: {e}")
        return False


# Custom Content Examples

def create_custom_content_example(space_id, title, body, content_type, page_id=None):
    """
    Example demonstrating how to create custom content.
    
    Args:
        space_id: ID of the space where the custom content will be created
        title: Title of the custom content
        body: HTML body content
        content_type: Custom content type identifier
        page_id: Optional page ID to associate with the custom content
    """
    print(f"\n=== Creating custom content '{title}' ===")
    
    try:
        custom_content = confluence.create_custom_content(
            type=content_type,
            title=title,
            body=body,
            space_id=space_id,
            page_id=page_id,
        )
        
        print(f"Created custom content: {custom_content['title']} (ID: {custom_content['id']})")
        return custom_content["id"]
    
    except Exception as e:
        print(f"Error creating custom content: {e}")
        return None


def get_custom_content_example(custom_content_id):
    """
    Example demonstrating how to retrieve custom content by its ID.
    
    Args:
        custom_content_id: ID of the custom content to retrieve
    """
    print(f"\n=== Getting custom content (ID: {custom_content_id}) ===")
    
    try:
        custom_content = confluence.get_custom_content_by_id(
            custom_content_id=custom_content_id,
            body_format="storage"
        )
        
        print(f"Retrieved custom content: {custom_content['title']}")
        pretty_print(custom_content)
        return custom_content
    
    except Exception as e:
        print(f"Error retrieving custom content: {e}")
        return None


def list_custom_content_example(space_id, content_type):
    """
    Example demonstrating how to list custom content with filters.
    
    Args:
        space_id: ID of the space to filter custom content by
        content_type: Custom content type identifier
    """
    print(f"\n=== Listing custom content in space (ID: {space_id}) ===")
    
    try:
        custom_contents = confluence.get_custom_content(
            type=content_type,
            space_id=space_id,
            status="current",
            sort="-created-date",
            limit=10
        )
        
        if custom_contents:
            print(f"Found {len(custom_contents)} custom content items")
            for item in custom_contents:
                print(f"- {item.get('title', 'No title')} (ID: {item.get('id', 'No ID')})")
        else:
            print(f"No custom content found of type '{content_type}' in this space")
        
        return custom_contents
    
    except Exception as e:
        print(f"Error listing custom content: {e}")
        return None


def update_custom_content_example(custom_content_id, title, body, content_type, version_number):
    """
    Example demonstrating how to update custom content.
    
    Args:
        custom_content_id: ID of the custom content to update
        title: Updated title
        body: Updated HTML body content
        content_type: Custom content type identifier
        version_number: Current version number of the custom content
    """
    print(f"\n=== Updating custom content (ID: {custom_content_id}) ===")
    
    try:
        # First, get the current content to check its version
        current = confluence.get_custom_content_by_id(custom_content_id)
        current_version = current.get("version", {}).get("number", 1)
        
        # Update the custom content
        updated = confluence.update_custom_content(
            custom_content_id=custom_content_id,
            type=content_type,
            title=title,
            body=body,
            version_number=version_number,
            status="current",
            version_message="Updated via API example"
        )
        
        print(f"Updated custom content: {updated['title']} (Version: {updated['version']['number']})")
        return updated
    
    except Exception as e:
        print(f"Error updating custom content: {e}")
        return None


def custom_content_labels_example(custom_content_id):
    """
    Example demonstrating how to work with custom content labels.
    
    Args:
        custom_content_id: ID of the custom content to manage labels for
    """
    print(f"\n=== Working with labels for custom content (ID: {custom_content_id}) ===")
    
    try:
        # Add a label to the custom content
        label = "example-label"
        print(f"Adding label '{label}' to custom content")
        added_label = confluence.add_custom_content_label(
            custom_content_id=custom_content_id,
            label=label
        )
        
        # Get all labels for the custom content
        print("Retrieving all labels for the custom content")
        labels = confluence.get_custom_content_labels(custom_content_id)
        
        if labels:
            print(f"Found {len(labels)} labels:")
            for l in labels:
                print(f"- {l.get('prefix', 'global')}:{l.get('name', 'unknown')}")
        else:
            print("No labels found")
        
        # Delete the label
        print(f"Deleting label '{label}' from custom content")
        confluence.delete_custom_content_label(
            custom_content_id=custom_content_id,
            label=label
        )
        
        return labels
    
    except Exception as e:
        print(f"Error working with custom content labels: {e}")
        return None


def custom_content_properties_example(custom_content_id):
    """
    Example demonstrating how to work with custom content properties.
    
    Args:
        custom_content_id: ID of the custom content to manage properties for
    """
    print(f"\n=== Working with properties for custom content (ID: {custom_content_id}) ===")
    
    try:
        # Create a property for the custom content
        property_key = "example-property"
        property_value = {
            "items": [
                {"name": "item1", "value": 42},
                {"name": "item2", "value": "string value"}
            ],
            "description": "This is an example property"
        }
        
        print(f"Creating property '{property_key}' for custom content")
        created_prop = confluence.create_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key,
            value=property_value
        )
        
        # Get the property by key
        print(f"Retrieving property '{property_key}'")
        prop = confluence.get_custom_content_property_by_key(
            custom_content_id=custom_content_id,
            property_key=property_key
        )
        
        # Update the property
        updated_value = property_value.copy()
        updated_value["description"] = "This is an updated description"
        
        print(f"Updating property '{property_key}'")
        updated_prop = confluence.update_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key,
            value=updated_value,
            version_number=prop["version"]["number"]
        )
        
        # Get all properties
        print("Retrieving all properties for the custom content")
        properties = confluence.get_custom_content_properties(custom_content_id)
        
        if properties:
            print(f"Found {len(properties)} properties:")
            for p in properties:
                print(f"- {p.get('key', 'unknown')}")
        else:
            print("No properties found")
        
        # Delete the property
        print(f"Deleting property '{property_key}'")
        confluence.delete_custom_content_property(
            custom_content_id=custom_content_id,
            key=property_key
        )
        
        return properties
    
    except Exception as e:
        print(f"Error working with custom content properties: {e}")
        return None


def get_custom_content_children_example(custom_content_id):
    """
    Example demonstrating how to retrieve children of custom content.
    
    Args:
        custom_content_id: ID of the custom content to retrieve children for
    """
    print(f"\n=== Getting children of custom content (ID: {custom_content_id}) ===")
    
    try:
        children = confluence.get_custom_content_children(custom_content_id, limit=10)
        
        if children:
            print(f"Found {len(children)} children for custom content")
            for child in children:
                print(f"- {child.get('title', 'No title')} (ID: {child.get('id', 'No ID')})")
        else:
            print("No children found for this custom content")
        
        return children
    
    except Exception as e:
        print(f"Error retrieving custom content children: {e}")
        return None


def get_custom_content_ancestors_example(custom_content_id):
    """
    Example demonstrating how to retrieve ancestors of custom content.
    
    Args:
        custom_content_id: ID of the custom content to retrieve ancestors for
    """
    print(f"\n=== Getting ancestors of custom content (ID: {custom_content_id}) ===")
    
    try:
        ancestors = confluence.get_custom_content_ancestors(custom_content_id)
        
        if ancestors:
            print(f"Found {len(ancestors)} ancestors for custom content")
            for ancestor in ancestors:
                print(f"- {ancestor.get('title', 'No title')} (Type: {ancestor.get('type', 'Unknown')})")
        else:
            print("No ancestors found for this custom content")
        
        return ancestors
    
    except Exception as e:
        print(f"Error retrieving custom content ancestors: {e}")
        return None


def delete_custom_content_example(custom_content_id):
    """
    Example demonstrating how to delete custom content.
    
    Args:
        custom_content_id: ID of the custom content to delete
    """
    print(f"\n=== Deleting custom content (ID: {custom_content_id}) ===")
    
    try:
        result = confluence.delete_custom_content(custom_content_id)
        print(f"Custom content deleted successfully")
        return True
    
    except Exception as e:
        print(f"Error deleting custom content: {e}")
        return False


# Main example execution
if __name__ == "__main__":
    print("Working with Confluence API V2 whiteboard and custom content features")
    
    # Replace with your actual space ID
    SPACE_ID = "123456"
    
    # Uncomment the sections you want to run
    
    # === Whiteboard Examples ===
    
    # Create a new whiteboard
    # whiteboard_id = create_whiteboard_example(SPACE_ID, "Example Whiteboard")
    
    # Get a whiteboard by ID
    # whiteboard = get_whiteboard_example(whiteboard_id)
    
    # Get whiteboard children
    # children = get_whiteboard_children_example(whiteboard_id)
    
    # Get whiteboard ancestors
    # ancestors = get_whiteboard_ancestors_example(whiteboard_id)
    
    # Delete a whiteboard
    # delete_whiteboard_example(whiteboard_id)
    
    # === Custom Content Examples ===
    
    # Define a custom content type (must be registered in your Confluence instance)
    # CUSTOM_TYPE = "example.custom.type"
    
    # Create custom content
    # custom_content_body = "<p>This is an example custom content.</p><ul><li>Feature 1</li><li>Feature 2</li></ul>"
    # custom_content_id = create_custom_content_example(SPACE_ID, "Example Custom Content", custom_content_body, CUSTOM_TYPE)
    
    # Get custom content by ID
    # custom_content = get_custom_content_example(custom_content_id)
    
    # List custom content with filters
    # custom_contents = list_custom_content_example(SPACE_ID, CUSTOM_TYPE)
    
    # If you retrieved a custom content, you can update it
    # if custom_content:
    #     version_number = custom_content.get("version", {}).get("number", 1)
    #     updated_body = "<p>This is updated custom content.</p><ul><li>Feature 1</li><li>Feature 2</li><li>New Feature</li></ul>"
    #     updated = update_custom_content_example(custom_content_id, "Updated Custom Content", updated_body, CUSTOM_TYPE, version_number)
    
    # Work with labels for custom content
    # labels = custom_content_labels_example(custom_content_id)
    
    # Work with properties for custom content
    # properties = custom_content_properties_example(custom_content_id)
    
    # Get custom content children
    # children = get_custom_content_children_example(custom_content_id)
    
    # Get custom content ancestors
    # ancestors = get_custom_content_ancestors_example(custom_content_id)
    
    # Delete custom content
    # delete_custom_content_example(custom_content_id) 