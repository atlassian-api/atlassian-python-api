#!/usr/bin/env python3
"""
Example script showing how to use the new Jira v3 Rich Text API features with Atlassian Document Format (ADF)
"""

import os
from dotenv import load_dotenv
from atlassian import jira

# Load environment variables
load_dotenv()

# Get credentials from environment variables
JIRA_URL = os.environ.get("JIRA_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
PROJECT_KEY = os.environ.get("JIRA_PROJECT_KEY", "DEMO")

# For debugging
print(f"Connecting to Jira at {JIRA_URL}")


def main():
    # Example 1: Using the direct RichTextJira class (no legacy compatibility)
    print("\n=== Example 1: Using RichTextJira directly ===")
    jira_richtext = jira.get_richtext_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=False
    )

    print("Connected to Jira API v3 with ADF support")

    # Example 2: Converting plain text to ADF
    print("\n=== Example 2: Converting text to ADF ===")
    simple_text = "This is a simple text that will be converted to ADF"
    adf_document = jira_richtext.convert_text_to_adf(simple_text)

    print("Plain text converted to ADF:")
    print(adf_document)

    # Example 3: Create different ADF nodes
    print("\n=== Example 3: Creating rich ADF content ===")

    # Create a heading
    heading = jira_richtext.create_adf_heading("This is a heading", level=1)

    # Create a paragraph with bold and italic text
    paragraph = jira_richtext.create_adf_paragraph("This is a paragraph with formatting", marks=["strong", "em"])

    # Create a bullet list
    bullet_list = jira_richtext.create_adf_bullet_list(["First bullet item", "Second bullet item", "Third bullet item"])

    # Create a numbered list
    numbered_list = jira_richtext.create_adf_numbered_list(
        ["First numbered item", "Second numbered item", "Third numbered item"]
    )

    # Create a code block
    code_block = jira_richtext.create_adf_code_block(
        "def hello_world():\n    print('Hello, World!')", language="python"
    )

    # Create a blockquote
    blockquote = jira_richtext.create_adf_quote("This is a quote from someone important")

    # Create a link
    link = jira_richtext.create_adf_link("Atlassian", "https://atlassian.com")

    # Combine all nodes into a complete ADF document
    content = [heading, paragraph, bullet_list, numbered_list, code_block, blockquote, link]

    rich_adf_document = jira_richtext.create_adf_document(content)

    print("Rich ADF document created with multiple node types")

    # Example 4: Using ADF to create comments or issues
    print("\n=== Example 4: Using ADF with issues and comments ===")
    try:
        # This is just a demonstration - to actually create an issue or add a comment,
        # you would need a valid project key and issue key
        print("\nExample data for creating an issue with ADF description:")
        issue_data = {
            "project": {"key": PROJECT_KEY},
            "summary": "Issue created with ADF description",
            "description": rich_adf_document,
            "issuetype": {"name": "Task"},
        }
        print(issue_data)

        # Uncomment to actually create the issue:
        # new_issue = jira_richtext.create_issue_with_adf(issue_data)
        # print(f"Created issue: {new_issue.get('key')}")

        # Example comment ADF - for adding to an issue
        print("\nExample data for adding a comment with ADF:")
        comment_adf = jira_richtext.create_adf_document(
            [
                jira_richtext.create_adf_paragraph("This is a comment with *formatting*"),
                jira_richtext.create_adf_bullet_list(["Point 1", "Point 2"]),
            ]
        )

        # Uncomment to add comment to an actual issue:
        # issue_key = "DEMO-123"  # Replace with actual issue key
        # new_comment = jira_richtext.add_comment_with_adf(issue_key, comment_adf)
        # print(f"Added comment ID: {new_comment.get('id')}")

    except Exception as e:
        print(f"Error with ADF operations: {str(e)}")

    # Example 5: Using the adapter for backward compatibility
    print("\n=== Example 5: Using the adapter (legacy mode) ===")
    jira_adapter = jira.get_richtext_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=True
    )

    try:
        # Use a legacy method name with automatic conversion to ADF
        simple_text = "This is text that will be automatically converted to ADF"
        print("\nAdding a comment with legacy method (text auto-converted to ADF):")

        # Uncomment to add comment to an actual issue:
        # issue_key = "DEMO-123"  # Replace with actual issue key
        # new_comment = jira_adapter.add_comment(issue_key, simple_text)
        # print(f"Added comment ID: {new_comment.get('id')}")

    except Exception as e:
        print(f"Error using legacy method: {str(e)}")


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main()
