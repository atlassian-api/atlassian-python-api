#!/usr/bin/env python3
# coding=utf-8
"""
Example script demonstrating the Jira v3 API's comment and worklog methods with ADF support.

This example shows how to:
1. Add a comment with ADF content
2. Retrieve comments in ADF format
3. Edit a comment with ADF content
4. Add a worklog with ADF comments
5. Retrieve worklog entries with ADF content
"""

from pprint import pprint

from atlassian import Jira
from atlassian.jira_adf import JiraADF
from atlassian.jira_v3 import JiraV3


def main():
    """
    Main function demonstrating Jira v3 API comment and worklog operations.

    To use this example, replace the placeholder values with your actual Jira instance details.
    """

    # Initialize the Jira v3 client
    jira = JiraV3(
        url="https://your-instance.atlassian.net",
        username="your-email@example.com",
        password="your-api-token",  # Use an API token for Jira Cloud
        cloud=True,  # Set to True for Jira Cloud, False for Jira Server/Data Center
    )

    # Alternatively, use the factory method from the base Jira class
    # jira = Jira.create(
    #     url="https://your-instance.atlassian.net",
    #     username="your-email@example.com",
    #     password="your-api-token",
    #     api_version="3",
    #     cloud=True
    # )

    # The issue to work with
    issue_key = "PROJ-123"

    # --------------------------------------------------
    # Example 1: Creating a comment with ADF content
    # --------------------------------------------------
    print("\n=== Example 1: Creating a comment with ADF content ===")

    # Create a simple text comment (automatically converted to ADF)
    simple_comment = "This is a simple comment that will be automatically converted to ADF format."
    comment_result = jira.issue_add_comment(issue_key, simple_comment)
    print("Created comment ID:", comment_result.get("id"))

    # Create a more complex ADF comment with formatting
    # First, create an empty ADF document
    complex_adf = JiraADF.create_doc()

    # Add a heading
    complex_adf["content"].append(JiraADF.heading("ADF Formatted Comment", 2))

    # Add paragraphs with text
    complex_adf["content"].append(JiraADF.paragraph("This is a paragraph in ADF format."))

    # Add a bullet list
    bullet_items = ["First item", "Second item", "Third item with emphasis"]
    complex_adf["content"].append(JiraADF.bullet_list(bullet_items))

    # Add the comment to the issue
    formatted_comment_result = jira.issue_add_comment(issue_key, complex_adf)
    formatted_comment_id = formatted_comment_result.get("id")
    print("Created formatted comment ID:", formatted_comment_id)

    # --------------------------------------------------
    # Example 2: Retrieving comments in ADF format
    # --------------------------------------------------
    print("\n=== Example 2: Retrieving comments in ADF format ===")

    # Get all comments for the issue
    comments = jira.issue_get_comments(issue_key)
    print(f"Total comments: {comments.get('total', 0)}")

    # Get a specific comment by ID (from the one we just created)
    if formatted_comment_id:
        comment = jira.issue_get_comment(issue_key, formatted_comment_id)
        print("\nRetrieved comment:")
        print(f"Comment ID: {comment.get('id')}")
        print(f"Created: {comment.get('created')}")
        print(f"Author: {comment.get('author', {}).get('displayName')}")

        # Extract plain text from the ADF content
        comment_body = comment.get("body", {})
        plain_text = jira.extract_text_from_adf(comment_body)
        print(f"\nComment as plain text:\n{plain_text}")

    # --------------------------------------------------
    # Example 3: Editing a comment with ADF content
    # --------------------------------------------------
    print("\n=== Example 3: Editing a comment with ADF content ===")

    if formatted_comment_id:
        # Create updated ADF content
        updated_adf = JiraADF.create_doc()
        updated_adf["content"].append(JiraADF.heading("Updated ADF Comment", 2))
        updated_adf["content"].append(JiraADF.paragraph("This comment has been updated with new ADF content."))

        # Update the comment
        updated_comment = jira.issue_edit_comment(issue_key, formatted_comment_id, updated_adf)
        print("Comment updated successfully!")

        # Extract plain text from the updated ADF content
        updated_body = updated_comment.get("body", {})
        updated_text = jira.extract_text_from_adf(updated_body)
        print(f"\nUpdated comment as plain text:\n{updated_text}")

    # --------------------------------------------------
    # Example 4: Adding a worklog with ADF comments
    # --------------------------------------------------
    print("\n=== Example 4: Adding a worklog with ADF comments ===")

    # Create a worklog with a simple text comment (automatically converted to ADF)
    worklog_comment = "Time spent on implementing the new feature."
    worklog_result = jira.issue_add_worklog(
        issue_id_or_key=issue_key,
        comment=worklog_comment,
        time_spent="1h 30m",  # Or use time_spent_seconds=5400
        # ISO 8601 format for started time
        started="2023-04-25T09:00:00.000+0000",
    )

    worklog_id = worklog_result.get("id")
    print(f"Created worklog ID: {worklog_id}")

    # --------------------------------------------------
    # Example 5: Retrieving worklog entries with ADF content
    # --------------------------------------------------
    print("\n=== Example 5: Retrieving worklog entries with ADF content ===")

    # Get all worklogs for the issue
    worklogs = jira.issue_get_worklog(issue_key)
    print(f"Total worklogs: {worklogs.get('total', 0)}")

    # Get the specific worklog we just created
    if worklog_id:
        worklog = jira.issue_get_worklog_by_id(issue_key, worklog_id)
        print("\nRetrieved worklog:")
        print(f"Worklog ID: {worklog.get('id')}")
        print(f"Author: {worklog.get('author', {}).get('displayName')}")
        print(f"Time spent: {worklog.get('timeSpent')} ({worklog.get('timeSpentSeconds')} seconds)")
        print(f"Started: {worklog.get('started')}")

        # Extract plain text from the ADF comment
        if "comment" in worklog:
            worklog_comment_text = jira.extract_text_from_adf(worklog.get("comment", {}))
            print(f"\nWorklog comment as plain text:\n{worklog_comment_text}")


if __name__ == "__main__":
    main()
