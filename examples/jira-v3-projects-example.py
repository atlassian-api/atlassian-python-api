#!/usr/bin/env python3
"""
Example script showing how to use the enhanced Jira Projects and Project Configuration API
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
    # Example 1: Using the direct ProjectsJira class (non-legacy mode)
    print("\n=== Example 1: Using ProjectsJira directly ===")
    jira_projects = jira.get_projects_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=False
    )

    print("Connected to Jira API v3 for Projects and Project Configuration")

    # Example 2: Getting all projects with expansions
    print("\n=== Example 2: Getting all projects with expansions ===")
    try:
        projects = jira_projects.get_all_projects(
            expand=["description", "lead", "url"], recent=10  # Limit to 10 recent projects
        )

        print(f"Found {len(projects)} projects:")
        for project in projects[:5]:  # Show first 5 only
            print(f"  - {project.get('name', 'Unknown')} ({project.get('key', 'Unknown Key')})")
            print(f"    Lead: {project.get('lead', {}).get('displayName', 'Unknown')}")
            print(f"    Description: {project.get('description', 'No description')[:50]}...")

    except Exception as e:
        print(f"Error getting projects: {str(e)}")

    # Example 3: Get project details
    print(f"\n=== Example 3: Getting project details for {PROJECT_KEY} ===")
    try:
        project = jira_projects.get_project(PROJECT_KEY, expand=["description", "lead", "issueTypes", "url"])

        print(f"Project: {project.get('name')} ({project.get('key')})")
        print(f"  URL: {project.get('url', 'No URL')}")
        print(f"  Lead: {project.get('lead', {}).get('displayName', 'Unknown')}")
        print(f"  Description: {project.get('description', 'No description')[:100]}...")

        # Get issue types for this project
        issue_types = project.get("issueTypes", [])
        print(f"\n  Issue Types ({len(issue_types)}):")
        for issue_type in issue_types:
            print(f"    - {issue_type.get('name', 'Unknown')} ({issue_type.get('id', 'Unknown ID')})")

    except Exception as e:
        print(f"Error getting project details: {str(e)}")

    # Example 4: Project components
    print(f"\n=== Example 4: Project components for {PROJECT_KEY} ===")
    try:
        components = jira_projects.get_project_components(PROJECT_KEY)

        print(f"Found {len(components)} components:")
        for component in components:
            print(f"  - {component.get('name', 'Unknown')} (ID: {component.get('id', 'Unknown ID')})")
            assignee_info = component.get("assignee", {})
            print(f"    Lead: {component.get('lead', {}).get('displayName', 'None')}")
            print(f"    Assignee: {assignee_info.get('displayName', 'None')}")

    except Exception as e:
        print(f"Error getting components: {str(e)}")

    # Example 5: Project versions
    print(f"\n=== Example 5: Project versions for {PROJECT_KEY} ===")
    try:
        versions = jira_projects.get_project_versions(PROJECT_KEY)

        print(f"Found {len(versions)} versions:")
        for version in versions:
            status = []
            if version.get("released", False):
                status.append("Released")
            if version.get("archived", False):
                status.append("Archived")

            status_str = ", ".join(status) if status else "Active"
            release_date = version.get("releaseDate", "No date")

            print(
                f"  - {version.get('name', 'Unknown')} "
                f"(ID: {version.get('id', 'Unknown ID')}, Status: {status_str})"
            )
            print(f"    Release Date: {release_date}")

    except Exception as e:
        print(f"Error getting versions: {str(e)}")

    # Example 6: Project roles
    print(f"\n=== Example 6: Project roles for {PROJECT_KEY} ===")
    try:
        roles = jira_projects.get_project_roles(PROJECT_KEY)

        print(f"Project roles:")
        for role_name, role_url in roles.items():
            print(f"  - {role_name}")

        # Get details for the first role
        if roles:
            first_role_name = next(iter(roles))
            role_id = roles[first_role_name].split("/")[-1]  # Extract ID from URL

            try:
                role_details = jira_projects.get_project_role(PROJECT_KEY, role_id)
                print(f"\n  Details for role '{first_role_name}':")

                actors = role_details.get("actors", [])
                print(f"  {len(actors)} actors assigned to this role")

                for actor in actors[:3]:  # Show first 3 actors only
                    actor_type = actor.get("type", "Unknown")
                    display_name = actor.get("displayName", "Unknown")
                    print(f"    - {display_name} (Type: {actor_type})")
            except Exception as e:
                print(f"  Error getting role details: {str(e)}")

    except Exception as e:
        print(f"Error getting project roles: {str(e)}")

    # Example 7: Using the adapter with legacy methods
    print("\n=== Example 7: Using ProjectsJiraAdapter (legacy mode) ===")
    jira_adapter = jira.get_projects_jira_instance(
        url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN, legacy_mode=True
    )

    try:
        # Use legacy method names
        print("\nUsing legacy method to get projects:")
        projects = jira_adapter.projects()
        print(f"Found {len(projects)} projects")

        print(f"\nUsing legacy method to get project components for {PROJECT_KEY}:")
        components = jira_adapter.project_components(PROJECT_KEY)
        print(f"Found {len(components)} components")

    except Exception as e:
        print(f"Error using legacy methods: {str(e)}")

    # Example 8: Creating/updating projects and components (commented out for safety)
    print("\n=== Example 8: Creating/updating projects and components (examples only) ===")
    print("Note: The following operations are not actually executed in this example")

    # Example of creating a new project
    print("\nExample data for creating a new project:")
    new_project_data = {
        "key": "TEST",
        "name": "Test Project",
        "projectTypeKey": "software",
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
        "description": "A project created through the API",
        "leadAccountId": "your-account-id",
    }
    print(new_project_data)

    # Example of creating a project component
    print("\nExample data for creating a new component:")
    new_component_data = {
        "project_key": PROJECT_KEY,
        "name": "API Component",
        "description": "Component created through the API",
        "lead_account_id": "your-account-id",
    }
    print(new_component_data)


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main()
