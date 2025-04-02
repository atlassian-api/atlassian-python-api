#!/usr/bin/env python3
"""
Example script showing how to use the Jira Issue Types and Field Configurations API
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
    # Example 1: Using the direct IssueTypesJira class (non-legacy mode)
    print("\n=== Example 1: Using IssueTypesJira directly ===")
    jira_types = jira.get_issuetypes_jira_instance(
        url=JIRA_URL,
        username=JIRA_USERNAME,
        password=JIRA_API_TOKEN,
        legacy_mode=False
    )
    
    print("Connected to Jira API v3 for Issue Types and Field Configurations")
    
    # Example 2: Get all issue types
    print("\n=== Example 2: Getting all issue types ===")
    try:
        issue_types = jira_types.get_all_issue_types()
        print(f"Found {len(issue_types)} issue types:")
        for issue_type in issue_types:
            print(f"  - {issue_type.get('name', 'Unknown')} ({issue_type.get('id', 'Unknown ID')})")
            
        # If we have at least one issue type, get its details
        if issue_types:
            first_issue_type_id = issue_types[0]["id"]
            print(f"\nGetting details for issue type {issue_types[0].get('name')}:")
            issue_type_details = jira_types.get_issue_type(first_issue_type_id)
            print(f"  - Name: {issue_type_details.get('name')}")
            print(f"  - Description: {issue_type_details.get('description', 'No description')}")
            print(f"  - Type: {issue_type_details.get('type')}")
            
    except Exception as e:
        print(f"Error getting issue types: {str(e)}")
    
    # Example 3: Get issue type schemes
    print("\n=== Example 3: Getting issue type schemes ===")
    try:
        schemes = jira_types.get_issue_type_schemes(max_results=5)
        print(f"Found {len(schemes.get('values', []))} issue type schemes:")
        for scheme in schemes.get("values", []):
            print(f"  - {scheme.get('name', 'Unknown')} (ID: {scheme.get('id', 'Unknown ID')})")
            
        # If we have at least one scheme, get its mapping
        if schemes.get("values"):
            first_scheme_id = schemes["values"][0]["id"]
            print(f"\nGetting mapping for scheme {schemes['values'][0].get('name')}:")
            try:
                mapping = jira_types.get_issue_type_scheme_mapping(first_scheme_id)
                print(f"  Issue types in scheme: {len(mapping.get('issueTypeIds', []))}")
                for issue_type_id in mapping.get("issueTypeIds", []):
                    print(f"  - Issue Type ID: {issue_type_id}")
            except Exception as e:
                print(f"  Error getting mapping: {str(e)}")
            
    except Exception as e:
        print(f"Error getting issue type schemes: {str(e)}")
    
    # Example 4: Field configurations and custom fields
    print("\n=== Example 4: Field configurations and custom fields ===")
    try:
        # Get field configurations
        field_configs = jira_types.get_field_configurations(max_results=5)
        print(f"Found {len(field_configs.get('values', []))} field configurations:")
        for config in field_configs.get("values", []):
            print(f"  - {config.get('name', 'Unknown')} (ID: {config.get('id', 'Unknown ID')})")
            
        # Get all fields (both system and custom)
        fields = jira_types.get_all_fields()
        system_fields = [f for f in fields if f.get('schema', {}).get('type') != 'custom']
        custom_fields = [f for f in fields if f.get('schema', {}).get('type') == 'custom']
        
        print(f"\nFound {len(fields)} fields in total:")
        print(f"  - {len(system_fields)} system fields")
        print(f"  - {len(custom_fields)} custom fields")
        
        print("\nSample of system fields:")
        for field in system_fields[:5]:  # Show first 5 system fields
            print(f"  - {field.get('name', 'Unknown')} (Key: {field.get('key', 'Unknown Key')})")
            
        print("\nSample of custom fields:")
        for field in custom_fields[:5]:  # Show first 5 custom fields
            print(f"  - {field.get('name', 'Unknown')} (Key: {field.get('key', 'Unknown Key')})")
            
    except Exception as e:
        print(f"Error with field configurations or fields: {str(e)}")
    
    # Example 5: Using the adapter (legacy mode)
    print("\n=== Example 5: Using IssueTypesJiraAdapter (legacy mode) ===")
    jira_adapter = jira.get_issuetypes_jira_instance(
        url=JIRA_URL,
        username=JIRA_USERNAME,
        password=JIRA_API_TOKEN,
        legacy_mode=True
    )
    
    try:
        # Use legacy method names
        print("\nUsing legacy method to get issue types:")
        issue_types = jira_adapter.issue_types()
        print(f"Found {len(issue_types)} issue types")
        
        print("\nUsing legacy method to get custom fields:")
        custom_fields = jira_adapter.get_all_custom_fields()
        print(f"Found {len(custom_fields)} custom fields")
        
    except Exception as e:
        print(f"Error using legacy methods: {str(e)}")
        
    # Example 6: Creating and updating issue types (commented out for safety)
    print("\n=== Example 6: Creating and updating issue types (examples only) ===")
    print("Note: The following operations are not actually executed in this example")
    
    # Example of creating a new issue type
    print("\nExample data for creating a new issue type:")
    new_issue_type_data = {
        "name": "API Test Issue Type",
        "description": "Issue type created through the API",
        "type": "standard"
    }
    print(new_issue_type_data)
    
    # Example of updating an issue type
    print("\nExample data for updating an issue type:")
    update_issue_type_data = {
        "name": "Updated Name",
        "description": "Updated description via API"
    }
    print(update_issue_type_data)


if __name__ == "__main__":
    if not all([JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN]):
        print("Error: Environment variables JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN must be set")
    else:
        main() 