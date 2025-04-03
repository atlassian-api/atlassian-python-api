#!/usr/bin/env python3
"""
Example script showing how to use the Jira Advanced Search API capabilities
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
    # Example 1: Using the direct SearchJira class (non-legacy mode)
    print("\n=== Example 1: Using SearchJira directly ===")
    jira_search = jira.get_search_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=False
    )

    print("Connected to Jira API v3 for Advanced Search")

    # Example 2: Advanced issue search with JQL
    print("\n=== Example 2: Advanced issue search with JQL ===")
    try:
        # Search for issues in the specified project
        jql = f"project = {PROJECT_KEY} ORDER BY created DESC"

        issues = jira_search.search_issues(
            jql=jql,
            max_results=5,
            fields=["summary", "status", "assignee", "created", "updated"],
            expand=["names"],  # Include field names for easier interpretation
            validate_query=True,
        )

        total = issues.get("total", 0)
        results = issues.get("issues", [])
        field_names = issues.get("names", {})

        print(f"Found {total} issues matching query: '{jql}'")
        print(f"Showing first {len(results)} results:")

        for issue in results:
            issue_key = issue.get("key", "Unknown")
            fields = issue.get("fields", {})
            summary = fields.get("summary", "No summary")
            status = fields.get("status", {}).get("name", "Unknown")
            assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
            created = fields.get("created", "Unknown")

            print(f"  - {issue_key}: {summary}")
            print(f"    Status: {status} | Assignee: {assignee} | Created: {created}")

    except Exception as e:
        print(f"Error searching for issues: {str(e)}")

    # Example 3: JQL field reference data and autocomplete
    print("\n=== Example 3: JQL field reference data and autocomplete ===")
    try:
        # Get field reference data for JQL queries
        field_reference = jira_search.get_field_reference_data()

        # Extract visible field names
        visible_fields = field_reference.get("visibleFieldNames", {})
        reserved_words = field_reference.get("jqlReservedWords", [])
        functions = field_reference.get("visibleFunctionNames", {})

        print(f"Available fields for JQL queries: {len(visible_fields)} fields")
        # Print first 5 fields as examples
        field_count = 0
        for field_id, field_name in visible_fields.items():
            if field_count < 5:
                print(f"  - {field_name} (ID: {field_id})")
                field_count += 1

        print(f"\nAvailable JQL functions: {len(functions)} functions")
        # Print first 3 functions as examples
        function_count = 0
        for function_id, function_name in functions.items():
            if function_count < 3:
                print(f"  - {function_name}")
                function_count += 1

        print(f"\nJQL reserved words: {len(reserved_words)} words")
        # Print first 5 reserved words as examples
        print(f"  Example reserved words: {', '.join(reserved_words[:5])}")

        # Get autocomplete suggestions for a specific field
        print("\nGetting autocomplete suggestions for 'status' field:")
        status_suggestions = jira_search.get_field_auto_complete_suggestions(field_name="status")

        suggestions = status_suggestions.get("results", [])
        print(f"Found {len(suggestions)} suggestions:")
        for suggestion in suggestions[:5]:  # Show first 5 suggestions
            value = suggestion.get("value", "Unknown")
            display_name = suggestion.get("displayName", value)
            print(f"  - {display_name}")

    except Exception as e:
        print(f"Error getting JQL reference data: {str(e)}")

    # Example 4: JQL validation and parsing
    print("\n=== Example 4: JQL validation and parsing ===")
    try:
        # Validate some JQL queries
        jql_queries = [
            f"project = {PROJECT_KEY}",  # Valid query
            "created > something",  # Invalid query
            f'project = {PROJECT_KEY} AND status = "In Progress"',  # Valid query with quotes
        ]

        validation_results = jira_search.validate_jql(jql_queries=jql_queries, validation_level="strict")

        print("JQL validation results:")
        query_results = validation_results.get("queries", [])

        for i, result in enumerate(query_results):
            query = jql_queries[i]
            is_valid = "errors" not in result or not result["errors"]
            status = "Valid" if is_valid else "Invalid"

            print(f"  Query: '{query}'")
            print(f"    Status: {status}")

            if not is_valid:
                errors = result.get("errors", [])
                for error in errors:
                    print(f"    Error: {error.get('message', 'Unknown error')}")

            print()

    except Exception as e:
        print(f"Error validating JQL: {str(e)}")

    # Example 5: User search capabilities
    print("\n=== Example 5: User search capabilities ===")
    try:
        # Search for users by query
        query = "admin"  # Example query; replace with appropriate query for your Jira instance
        users = jira_search.search_users(query=query, max_results=5)

        print(f"Found {len(users)} users matching '{query}':")
        for user in users:
            name = user.get("displayName", "Unknown")
            email = user.get("emailAddress", "No email")
            active = "Active" if user.get("active", False) else "Inactive"
            account_id = user.get("accountId", "No ID")

            print(f"  - {name} ({email}) - {active}")
            print(f"    Account ID: {account_id}")

        # Find users with specific permissions
        print("\nFinding users with specific permissions:")
        users_with_permissions = jira_search.find_users_with_permissions(
            permissions=["BROWSE_PROJECTS", "EDIT_ISSUES"], project_key=PROJECT_KEY, max_results=5
        )

        print(f"Users with BROWSE_PROJECTS and EDIT_ISSUES permissions in {PROJECT_KEY}:")
        for user in users_with_permissions:
            name = user.get("displayName", "Unknown")
            account_id = user.get("accountId", "No ID")
            print(f"  - {name} (Account ID: {account_id})")

    except Exception as e:
        print(f"Error with user search: {str(e)}")

    # Example 6: Using the adapter with legacy methods
    print("\n=== Example 6: Using SearchJiraAdapter (legacy mode) ===")
    jira_adapter = jira.get_search_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=True
    )

    try:
        # Use legacy method names
        jql = f"project = {PROJECT_KEY} ORDER BY created DESC"

        print(f"\nUsing legacy 'jql' method for query: '{jql}':")
        search_results = jira_adapter.jql(jql=jql, fields=["summary", "status"], limit=3)

        total = search_results.get("total", 0)
        results = search_results.get("issues", [])

        print(f"Found {total} issues, showing first {len(results)} results:")
        for issue in results:
            issue_key = issue.get("key", "Unknown")
            fields = issue.get("fields", {})
            summary = fields.get("summary", "No summary")
            status = fields.get("status", {}).get("name", "Unknown")

            print(f"  - {issue_key}: {summary} (Status: {status})")

        # Use legacy user search method
        print("\nUsing legacy 'user_find' method:")
        query = "admin"  # Example query
        users = jira_adapter.user_find(query=query, limit=3)

        print(f"Found {len(users)} users matching '{query}'")

    except Exception as e:
        print(f"Error using legacy methods: {str(e)}")


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main()
