#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
from atlassian import ConfluenceV2

"""
This example shows how to work with Confluence page properties using the API v2
"""

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Confluence credentials from environment variables
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://example.atlassian.net")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME", "email@example.com")
CONFLUENCE_PASSWORD = os.environ.get("CONFLUENCE_PASSWORD", "api-token")

# Create the ConfluenceV2 client
confluence = ConfluenceV2(url=CONFLUENCE_URL, username=CONFLUENCE_USERNAME, password=CONFLUENCE_PASSWORD)


def print_property(prop):
    """Helper function to print a property in a readable format"""
    print(f"\nProperty: {prop.get('key', 'unknown')}")
    print(f"  ID: {prop.get('id', 'unknown')}")

    # Format the property value
    value = prop.get("value")
    if isinstance(value, (dict, list)):
        value_str = json.dumps(value, indent=2)
        print(f"  Value: {value_str}")
    else:
        print(f"  Value: {value}")

    # Print version info if available
    if "version" in prop:
        print(f"  Version: {prop.get('version', {}).get('number', 'unknown')}")

    print(f"  Created by: {prop.get('createdBy', {}).get('displayName', 'unknown')}")
    print(f"  Created at: {prop.get('createdAt', 'unknown')}")


def get_properties_example(page_id):
    """Example showing how to get page properties"""
    print("\n=== Getting Page Properties ===")

    try:
        # Get all properties for the page
        properties = confluence.get_page_properties(page_id)

        print(f"Found {len(properties)} properties for page {page_id}:")
        for prop in properties:
            print(f"  - {prop.get('key', 'unknown')}: {type(prop.get('value')).__name__}")

        # If there are properties, get details for the first one
        if properties:
            first_property_key = properties[0].get("key")
            print(f"\nGetting details for property '{first_property_key}'")

            property_details = confluence.get_page_property_by_key(page_id, first_property_key)
            print_property(property_details)

    except Exception as e:
        print(f"Error getting properties: {e}")


def create_property_example(page_id):
    """Example showing how to create a page property"""
    print("\n=== Creating Page Properties ===")

    try:
        # Create a simple string property
        string_prop = confluence.create_page_property(
            page_id=page_id, property_key="example.string", property_value="This is a string value"
        )

        print("Created string property:")
        print_property(string_prop)

        # Create a numeric property
        number_prop = confluence.create_page_property(page_id=page_id, property_key="example.number", property_value=42)

        print("Created numeric property:")
        print_property(number_prop)

        # Create a complex JSON property
        json_prop = confluence.create_page_property(
            page_id=page_id,
            property_key="example.complex",
            property_value={
                "name": "Complex Object",
                "attributes": ["attr1", "attr2"],
                "nested": {"key": "value", "number": 123},
            },
        )

        print("Created complex JSON property:")
        print_property(json_prop)

        return string_prop.get("key"), json_prop.get("key")

    except Exception as e:
        print(f"Error creating properties: {e}")
        return None, None


def update_property_example(page_id, property_key):
    """Example showing how to update a page property"""
    print("\n=== Updating Page Properties ===")

    if not property_key:
        print("No property key provided for update example")
        return

    try:
        # First, get the current property to see its value
        current_prop = confluence.get_page_property_by_key(page_id, property_key)
        print(f"Current property '{property_key}':")
        print_property(current_prop)

        # Update the property with a new value
        if isinstance(current_prop.get("value"), dict):
            # If it's a dictionary, add a new field
            new_value = current_prop.get("value", {}).copy()
            new_value["updated"] = True
            new_value["timestamp"] = "2023-01-01T00:00:00Z"
        else:
            # For simple values, append text
            new_value = f"{current_prop.get('value', '')} (Updated)"

        # Perform the update
        updated_prop = confluence.update_page_property(
            page_id=page_id, property_key=property_key, property_value=new_value
        )

        print(f"\nUpdated property '{property_key}':")
        print_property(updated_prop)

    except Exception as e:
        print(f"Error updating property: {e}")


def delete_property_example(page_id, property_key):
    """Example showing how to delete a page property"""
    print("\n=== Deleting Page Properties ===")

    if not property_key:
        print("No property key provided for delete example")
        return

    try:
        # Delete the property
        result = confluence.delete_page_property(page_id, property_key)

        if result:
            print(f"Successfully deleted property '{property_key}' from page {page_id}")
        else:
            print(f"Failed to delete property '{property_key}' from page {page_id}")

    except Exception as e:
        print(f"Error deleting property: {e}")


if __name__ == "__main__":
    # You need a valid page ID for these examples
    page_id = "123456"  # Replace with a real page ID

    # Get existing properties for the page
    get_properties_example(page_id)

    # Create example properties
    string_key, json_key = create_property_example(page_id)

    # Update a property
    if json_key:
        update_property_example(page_id, json_key)

    # Clean up by deleting the properties we created
    if string_key:
        delete_property_example(page_id, string_key)
    if json_key:
        delete_property_example(page_id, json_key)

    # Verify the properties were deleted
    print("\n=== Verifying Properties Were Deleted ===")
    get_properties_example(page_id)
