#!/usr/bin/env python3
"""
Example script showing how to use the new Jira v3 Permissions API features
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
    # Example 1: Using the direct PermissionsJira class (no legacy compatibility)
    print("\n=== Example 1: Using PermissionsJira directly ===")
    jira_permissions = jira.get_permissions_jira_instance(
        url=JIRA_URL,
        username=JIRA_USERNAME,
        password=JIRA_API_TOKEN,
        legacy_mode=False
    )
    
    # Get current user
    user = jira_permissions.get_current_user()
    print(f"Current user: {user.get('displayName', 'Unknown')}")
    
    # Example 2: Get my permissions
    print("\n=== Example 2: My Permissions ===")
    try:
        # Get global permissions
        my_global_permissions = jira_permissions.get_my_permissions()
        print("\nGlobal permissions:")
        count = 0
        for perm_key, perm_data in my_global_permissions.get("permissions", {}).items():
            if count < 5 and perm_data.get("havePermission", False):
                print(f"  - {perm_key}")
                count += 1
        if count >= 5:
            print("  - ...")
        
        # Get project-specific permissions
        my_project_permissions = jira_permissions.get_my_permissions(project_key=PROJECT_KEY)
        print(f"\nPermissions for project {PROJECT_KEY}:")
        count = 0
        for perm_key, perm_data in my_project_permissions.get("permissions", {}).items():
            if count < 5 and perm_data.get("havePermission", False):
                print(f"  - {perm_key}")
                count += 1
        if count >= 5:
            print("  - ...")
    except Exception as e:
        print(f"Error getting permissions: {str(e)}")
    
    # Example 3: Permission schemes
    print("\n=== Example 3: Permission Schemes ===")
    try:
        # Get all permission schemes
        permission_schemes = jira_permissions.get_all_permission_schemes()
        print("\nPermission schemes:")
        for scheme in permission_schemes.get("permissionSchemes", []):
            print(f"  - {scheme.get('name', 'Unknown')} (ID: {scheme.get('id', 'Unknown')})")
            
        # If we have at least one scheme, look at its permissions
        if permission_schemes.get("permissionSchemes"):
            scheme_id = permission_schemes["permissionSchemes"][0]["id"]
            print(f"\nPermission grants for scheme ID {scheme_id}:")
            
            grants = jira_permissions.get_permission_scheme_grants(scheme_id)
            count = 0
            for grant in grants.get("permissions", []):
                if count < 5:
                    permission = grant.get("permission", "Unknown")
                    holder = grant.get("holder", {})
                    holder_type = holder.get("type", "Unknown")
                    holder_param = holder.get("parameter", "")
                    print(f"  - {permission}: {holder_type} {holder_param}")
                    count += 1
            if count >= 5:
                print("  - ...")
    except Exception as e:
        print(f"Error getting permission schemes: {str(e)}")
    
    # Example 4: Issue security schemes
    print("\n=== Example 4: Issue Security Schemes ===")
    try:
        security_schemes = jira_permissions.get_issue_security_schemes()
        print("\nIssue security schemes:")
        for scheme in security_schemes.get("issueSecuritySchemes", []):
            print(f"  - {scheme.get('name', 'Unknown')} (ID: {scheme.get('id', 'Unknown')})")
            print(f"    Description: {scheme.get('description', 'None')}")
    except Exception as e:
        print(f"Error getting security schemes: {str(e)}")
    
    # Example 5: Using the adapter for backward compatibility
    print("\n=== Example 5: Using the adapter (legacy mode) ===")
    jira_adapter = jira.get_permissions_jira_instance(
        url=JIRA_URL,
        username=JIRA_USERNAME,
        password=JIRA_API_TOKEN,
        legacy_mode=True
    )
    
    try:
        # Use a legacy method name
        permissions = jira_adapter.get_permissions(project_key=PROJECT_KEY)
        print(f"\nPermissions for project {PROJECT_KEY} using legacy method:")
        count = 0
        for perm_key, perm_data in permissions.get("permissions", {}).items():
            if count < 5 and perm_data.get("havePermission", False):
                print(f"  - {perm_key}")
                count += 1
        if count >= 5:
            print("  - ...")
    except Exception as e:
        print(f"Error using legacy method: {str(e)}")


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main() 