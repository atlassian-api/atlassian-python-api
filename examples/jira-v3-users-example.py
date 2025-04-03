#!/usr/bin/env python3
"""
Example script showing how to use the new Jira v3 User and Group Management API features
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
    # Example 1: Using the direct UsersJira class (no legacy compatibility)
    print("\n=== Example 1: Using UsersJira directly ===")
    jira_users = jira.get_users_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=False
    )

    # Get current user
    user = jira_users.get_current_user()
    print(f"Current user: {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")

    # Example 2: Search for users
    print("\n=== Example 2: Searching for users ===")
    try:
        # Find users by query
        search_query = "admin"  # Replace with a relevant search term for your Jira instance
        print(f"\nSearching for users with query '{search_query}':")
        users = jira_users.find_users(query=search_query, max_results=5)

        for user in users:
            print(f"  - {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")

        # Find users assignable to a project
        print(f"\nFinding users assignable to project {PROJECT_KEY}:")
        assignable_users = jira_users.find_users_assignable_to_issues(
            query="", project_keys=[PROJECT_KEY], max_results=5
        )

        for user in assignable_users:
            print(f"  - {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")
    except Exception as e:
        print(f"Error searching for users: {str(e)}")

    # Example 3: Get all users
    print("\n=== Example 3: Getting all users ===")
    try:
        users = jira_users.get_all_users(max_results=5)
        print("\nAll users (limited to 5):")
        for user in users:
            print(f"  - {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")
    except Exception as e:
        print(f"Error getting all users: {str(e)}")

    # Example 4: Group operations
    print("\n=== Example 4: Group operations ===")
    try:
        # Get all groups
        print("\nAll groups (limited to 5):")
        groups = jira_users.get_groups(max_results=5)

        for group in groups.get("groups", []):
            print(f"  - {group.get('name', 'Unknown')}")

        # If we have at least one group, get its members
        if groups.get("groups"):
            group_name = groups["groups"][0]["name"]
            print(f"\nMembers of group '{group_name}' (limited to 5):")

            members = jira_users.get_group_members(group_name=group_name, max_results=5)

            for user in members.get("values", []):
                print(f"  - {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")
    except Exception as e:
        print(f"Error with group operations: {str(e)}")

    # Example 5: User columns
    print("\n=== Example 5: User columns ===")
    try:
        # Get current user's columns
        columns = jira_users.get_user_default_columns(account_id=user.get("accountId"))

        print("\nUser's default columns:")
        for column in columns:
            print(f"  - {column.get('name', 'Unknown')}")
    except Exception as e:
        print(f"Error getting user columns: {str(e)}")

    # Example 6: Using the adapter for backward compatibility
    print("\n=== Example 6: Using the adapter (legacy mode) ===")
    jira_adapter = jira.get_users_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=True
    )

    try:
        # Use a legacy method name
        search_query = "admin"  # Replace with a relevant search term for your Jira instance
        print(f"\nSearching for users with legacy method and query '{search_query}':")
        users = jira_adapter.search_users(query=search_query, max_results=5)

        for user in users:
            print(f"  - {user.get('displayName', 'Unknown')} ({user.get('accountId', 'Unknown')})")
    except Exception as e:
        print(f"Error using legacy method: {str(e)}")


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main()
