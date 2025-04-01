#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from atlassian import ConfluenceV2

"""
This example shows how to work with labels in Confluence using the API v2
"""

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Confluence credentials from environment variables
CONFLUENCE_URL = os.environ.get('CONFLUENCE_URL', 'https://example.atlassian.net')
CONFLUENCE_USERNAME = os.environ.get('CONFLUENCE_USERNAME', 'email@example.com')
CONFLUENCE_PASSWORD = os.environ.get('CONFLUENCE_PASSWORD', 'api-token')

# Create the ConfluenceV2 client
confluence = ConfluenceV2(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_USERNAME,
    password=CONFLUENCE_PASSWORD
)

def get_page_labels_example(page_id):
    """Example showing how to get labels from a page"""
    print("\n=== Getting Page Labels ===")
    
    try:
        # Get all labels for the page
        labels = confluence.get_page_labels(page_id)
        
        print(f"Found {len(labels)} labels for page {page_id}:")
        for label in labels:
            print(f"  - {label.get('name', 'unknown')} (ID: {label.get('id', 'unknown')})")
            
        # Get labels with a specific prefix
        team_labels = confluence.get_page_labels(page_id, prefix="team-")
        
        print(f"\nFound {len(team_labels)} team labels:")
        for label in team_labels:
            print(f"  - {label.get('name', 'unknown')}")
            
    except Exception as e:
        print(f"Error getting page labels: {e}")

def add_page_labels_example(page_id):
    """Example showing how to add labels to a page"""
    print("\n=== Adding Page Labels ===")
    
    try:
        # Add a single label
        single_label = confluence.add_page_label(
            page_id=page_id,
            label="example-label"
        )
        
        print(f"Added label: {single_label.get('name', 'unknown')}")
        
        # Add multiple labels at once
        multiple_labels = confluence.add_page_labels(
            page_id=page_id,
            labels=["test-label-1", "test-label-2", "example-api"]
        )
        
        print(f"Added {len(multiple_labels)} labels:")
        for label in multiple_labels:
            print(f"  - {label.get('name', 'unknown')}")
            
        # Return the labels we added for cleanup
        return ["example-label", "test-label-1", "test-label-2", "example-api"]
            
    except Exception as e:
        print(f"Error adding page labels: {e}")
        return []

def delete_page_labels_example(page_id, labels_to_delete):
    """Example showing how to delete labels from a page"""
    print("\n=== Deleting Page Labels ===")
    
    if not labels_to_delete:
        print("No labels provided for deletion")
        return
    
    try:
        # Delete each label
        for label in labels_to_delete:
            result = confluence.delete_page_label(page_id, label)
            
            if result:
                print(f"Successfully deleted label '{label}' from page {page_id}")
            else:
                print(f"Failed to delete label '{label}' from page {page_id}")
            
    except Exception as e:
        print(f"Error deleting page labels: {e}")

def get_space_labels_example(space_id):
    """Example showing how to get labels from a space"""
    print("\n=== Getting Space Labels ===")
    
    try:
        # Get all labels for the space
        labels = confluence.get_space_labels(space_id)
        
        print(f"Found {len(labels)} labels for space {space_id}:")
        for label in labels:
            print(f"  - {label.get('name', 'unknown')}")
            
    except Exception as e:
        print(f"Error getting space labels: {e}")

def manage_space_labels_example(space_id):
    """Example showing how to add and delete labels on a space"""
    print("\n=== Managing Space Labels ===")
    
    try:
        # Add a single label
        single_label = confluence.add_space_label(
            space_id=space_id,
            label="space-example"
        )
        
        print(f"Added label: {single_label.get('name', 'unknown')}")
        
        # Add multiple labels at once
        multiple_labels = confluence.add_space_labels(
            space_id=space_id,
            labels=["space-test-1", "space-test-2"]
        )
        
        print(f"Added {len(multiple_labels)} labels:")
        for label in multiple_labels:
            print(f"  - {label.get('name', 'unknown')}")
            
        # Now delete the labels we just added
        labels_to_delete = ["space-example", "space-test-1", "space-test-2"]
        
        for label in labels_to_delete:
            result = confluence.delete_space_label(space_id, label)
            
            if result:
                print(f"Successfully deleted label '{label}' from space {space_id}")
            else:
                print(f"Failed to delete label '{label}' from space {space_id}")
            
    except Exception as e:
        print(f"Error managing space labels: {e}")

if __name__ == "__main__":
    # You need valid IDs for these examples
    page_id = "123456"   # Replace with a real page ID
    space_id = "654321"  # Replace with a real space ID
    
    # Page label examples
    get_page_labels_example(page_id)
    added_labels = add_page_labels_example(page_id)
    
    # Verify the labels were added
    get_page_labels_example(page_id)
    
    # Clean up by deleting the labels we added
    delete_page_labels_example(page_id, added_labels)
    
    # Space label examples
    get_space_labels_example(space_id)
    manage_space_labels_example(space_id)
    
    # Verify the space labels were cleaned up
    get_space_labels_example(space_id) 