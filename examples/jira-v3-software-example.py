#!/usr/bin/env python3
"""
Example script showing how to use the new Jira v3 Software API features
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

# For debugging
print(f"Connecting to Jira at {JIRA_URL}")


def main():
    # Example 1: Using the direct SoftwareJira class (no legacy compatibility)
    print("\n=== Example 1: Using SoftwareJira directly ===")
    jira_software = jira.get_software_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=False
    )

    # Get current user
    user = jira_software.get_current_user()
    print(f"Current user: {user.get('displayName', 'Unknown')}")

    # Get all boards
    print("\nFetching boards:")
    try:
        boards = jira_software.get_all_boards(max_results=5)
        for board in boards.get("values", []):
            print(f"  - {board.get('name', 'Unknown')} (ID: {board.get('id', 'Unknown')})")
    except Exception as e:
        print(f"Error fetching boards: {str(e)}")

    # Example 2: Using the backward-compatible SoftwareJiraAdapter
    print("\n=== Example 2: Using SoftwareJiraAdapter (legacy mode) ===")
    jira_adapter = jira.get_software_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=True
    )

    # Use a legacy method name
    print("\nFetching boards using legacy method:")
    try:
        boards = jira_adapter.boards(maxResults=5)
        for board in boards.get("values", []):
            print(f"  - {board.get('name', 'Unknown')} (ID: {board.get('id', 'Unknown')})")
    except Exception as e:
        print(f"Error fetching boards: {str(e)}")

    # Example 3: Advanced board operations
    if boards and boards.get("values"):
        board_id = boards["values"][0]["id"]

        print(f"\nFetching sprints for board ID {board_id}:")
        try:
            sprints = jira_software.get_all_sprints(board_id=board_id, max_results=5)
            for sprint in sprints.get("values", []):
                print(f"  - {sprint.get('name', 'Unknown')} (ID: {sprint.get('id', 'Unknown')})")
                print(f"    Status: {sprint.get('state', 'Unknown')}")
        except Exception as e:
            print(f"Error fetching sprints: {str(e)}")

        print(f"\nFetching backlog issues for board ID {board_id}:")
        try:
            backlog = jira_software.get_backlog_issues(board_id=board_id, max_results=5)
            for issue in backlog.get("issues", []):
                print(f"  - {issue.get('key', 'Unknown')}: {issue.get('fields', {}).get('summary', 'Unknown')}")
        except Exception as e:
            print(f"Error fetching backlog: {str(e)}")

    # Example 4: Advanced JQL capabilities
    print("\n=== Example 4: Advanced JQL capabilities ===")
    try:
        reference_data = jira_software.get_field_reference_data()
        print("\nAvailable JQL fields:")
        for field in list(reference_data.get("visibleFieldNames", {}).keys())[:5]:
            print(f"  - {field}")

        print("\nPerforming JQL query:")
        jql = "project = DEMO AND status = 'In Progress'"
        # Parse the JQL query
        parsed = jira_software.parse_jql(jql)
        print(f"JQL validation: {parsed.get('queries', [{}])[0].get('valid', False)}")
    except Exception as e:
        print(f"Error with JQL operations: {str(e)}")


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main()
