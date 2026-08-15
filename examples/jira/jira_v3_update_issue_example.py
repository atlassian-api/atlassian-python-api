#!/usr/bin/env python3
"""
Example script showing how to update issues with ADF content using Jira v3 API
"""

import logging
import os
from pprint import pprint

from atlassian import JiraADF, JiraV3

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Jira V3 client
jira = JiraV3(
    url="https://your-domain.atlassian.net",
    # Option 1: Using API token
    token=os.environ.get("JIRA_API_TOKEN"),
    # Option 2: Using username/password
    # username=os.environ.get("JIRA_USERNAME"),
    # password=os.environ.get("JIRA_PASSWORD"),
    cloud=True,  # V3 API is only available on Jira Cloud
)

# Example 1: Update an issue's description with ADF content
print("\n=== Example 1: Update issue description ===")
update_response = jira.update_issue_field(
    key="EXAMPLE-123",
    fields={
        "description": "This is an updated *description* with _formatting_",
        "summary": "Updated issue title",  # Non-ADF field
    },
)
print("Issue updated successfully")

# Example 2: Update an issue using the edit_issue method with operations
print("\n=== Example 2: Edit issue with operations ===")
edit_response = jira.edit_issue(
    issue_id_or_key="EXAMPLE-123",
    fields={
        # Set operation for description (ADF field)
        "description": [{"set": "This is a *formatted* description set via operations"}],
        # Add and remove labels (non-ADF field)
        "labels": [{"add": "new-label"}, {"remove": "old-label"}],
    },
)
print("Issue edited successfully with operations")

# Example 3: Create a complex ADF document and update an issue field
print("\n=== Example 3: Update with complex ADF content ===")

# Create a complex ADF document
complex_doc = JiraADF.create_doc()
complex_doc["content"].extend(
    [
        JiraADF.heading("Issue Overview", 1),
        JiraADF.paragraph("This issue requires attention from the dev team."),
        JiraADF.bullet_list(["First action item", "Second action item", "Third action item with priority"]),
    ]
)

# Update the issue with the complex ADF content
complex_update = jira.update_issue_field(
    key="EXAMPLE-123", fields={"description": complex_doc}  # Pass the ADF document directly
)
print("Issue updated with complex ADF content")

# Example 4: Comprehensive issue update with multiple fields
print("\n=== Example 4: Comprehensive issue update ===")
issue_update = jira.issue_update(
    issue_key="EXAMPLE-123",
    fields={"summary": "Comprehensive update example", "description": "This will be converted to *ADF* automatically"},
    update={
        "labels": [{"add": "comprehensive"}, {"remove": "simple"}],
        "comment": [{"add": {"body": "Adding a comment with *formatting*"}}],
    },
    history_metadata={
        "type": "myplugin:type",
        "description": "Update through API example",
    },
)
print("Issue updated comprehensively")

# Example 5: Working with custom fields that may contain ADF content
print("\n=== Example 5: Update custom fields ===")

# First get custom fields to find the ones that support ADF
custom_fields = jira.get_custom_fields()
textarea_field = None

# Find a textarea custom field that supports ADF
for field in custom_fields:
    if (
        field.get("supportsADF", False)
        and "schema" in field
        and field["schema"].get("custom", "").endswith(":textarea")
    ):
        textarea_field = field["id"]
        print(f"Found textarea field: {field['name']} (ID: {textarea_field})")
        break

if textarea_field:
    # Update the textarea custom field
    custom_update = jira.update_issue_field(
        key="EXAMPLE-123", fields={textarea_field: "This custom field supports *ADF content* with _formatting_"}
    )
    print(f"Updated custom field {textarea_field} with ADF content")
else:
    print("No textarea custom field found that supports ADF")

print("\nAll examples completed")
