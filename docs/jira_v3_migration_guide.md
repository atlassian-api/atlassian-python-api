# Jira v3 API Migration Guide

This document provides guidelines and instructions for migrating from the Jira v2 API to the newer v3 API in the atlassian-python-api library.

## Introduction

The Jira v3 API is the latest REST API version for Jira Cloud that offers several advantages over the v2 API:

- Support for Atlassian Document Format (ADF) for rich text fields
- Improved pagination mechanisms
- Enhanced error handling with specialized exceptions
- Specialized clients for different Jira features
- Better typing and documentation
- Support for both Cloud and Server environments

While the v2 API is still supported, we recommend migrating to the v3 API for new development and gradually updating existing code.

## Getting Started with v3 API

### Instantiating a v3 API Client

The simplest way to use the v3 API is to specify the API version when creating your Jira instance:

```python
from atlassian import Jira

# Create a v3 API client for Jira Cloud
jira = Jira(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token",
    api_version=3,  # Specify API version 3
    cloud=True      # Auto-detected for cloud URLs but can be explicitly set
)

# Or for Jira Server
jira_server = Jira(
    url="https://jira.your-company.com",
    username="your-username",
    password="your-password",
    api_version=3,
    cloud=False
)
```

### Using the Factory Method

We recommend using the factory method for creating Jira instances as it provides better instance selection:

```python
from atlassian.jira import get_jira_instance

# Get a Jira instance with the appropriate client type
jira = get_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token", 
    api_version=3
)
```

### Specialized Clients

The v3 API introduces specialized clients for different Jira features:

```python
from atlassian.jira import (
    get_jira_instance,
    get_software_jira_instance,
    get_permissions_jira_instance,
    get_users_jira_instance,
    get_richtext_jira_instance,
    get_issuetypes_jira_instance,
    get_projects_jira_instance,
    get_search_jira_instance
)

# Get a Jira Software instance for board and sprint operations
jira_software = get_software_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

# Get a Jira Permissions instance for permission management
jira_permissions = get_permissions_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)
```

## Key Differences and Improvements

### 1. Atlassian Document Format (ADF) Support

The v3 API supports ADF for rich text fields, which allows for more complex formatting:

```python
from atlassian.jira import get_jira_instance, get_richtext_jira_instance

# Get a Jira instance
jira = get_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token",
    api_version=3
)

# Create an issue with ADF content in the description
jira.create_issue(
    fields={
        "project": {"key": "PROJ"},
        "summary": "Issue with ADF description",
        "issuetype": {"name": "Task"},
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "This is a description with "
                        },
                        {
                            "type": "text",
                            "text": "bold",
                            "marks": [
                                {
                                    "type": "strong"
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": " text."
                        }
                    ]
                }
            ]
        }
    }
)

# Or use the rich text helper client
richtext_jira = get_richtext_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

# Create a simple ADF document
adf_doc = richtext_jira.create_doc()
adf_doc.add_paragraph().add_text("Hello").add_text(" world!", mark="strong")

# Use it in an issue
jira.create_issue(
    fields={
        "project": {"key": "PROJ"},
        "summary": "Issue with helper-created ADF",
        "issuetype": {"name": "Task"},
        "description": adf_doc.to_dict()
    }
)
```

### 2. Improved Pagination

The v3 API provides better pagination support with helper methods:

#### v2 Style Pagination:
```python
# v2 style pagination
start_at = 0
max_results = 50
all_issues = []

while True:
    response = jira.jql(
        "project = PROJ ORDER BY created DESC",
        start=start_at,
        limit=max_results
    )
    
    if not response.get("issues"):
        break
    
    all_issues.extend(response["issues"])
    
    if len(all_issues) >= response["total"]:
        break
    
    start_at += max_results
```

#### v3 Style Pagination:
```python
# v3 style pagination using helper method
issues = jira.jql_get_all_issues(
    "project = PROJ ORDER BY created DESC"
)

# Or using specialized search client
search_jira = get_search_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

issues = search_jira.jql_get_all_issues(
    "project = PROJ ORDER BY created DESC"
)
```

### 3. Enhanced Error Handling

The v3 API introduces specialized exceptions for better error handling:

```python
from atlassian.jira import get_jira_instance
from atlassian.jira.errors import (
    JiraApiError,
    JiraAuthenticationError,
    JiraPermissionError,
    JiraNotFoundError
)

jira = get_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token",
    api_version=3
)

try:
    issue = jira.get_issue("NONEXISTENT-123")
except JiraNotFoundError:
    print("Issue doesn't exist")
except JiraPermissionError:
    print("No permission to view this issue")
except JiraAuthenticationError:
    print("Authentication failed")
except JiraApiError as e:
    print(f"API error: {e}")
```

## Method Changes and Examples

### Issue Operations

```python
# Get an issue
issue = jira.get_issue("PROJ-123")

# Create an issue
new_issue = jira.create_issue(
    fields={
        "project": {"key": "PROJ"},
        "summary": "New issue summary",
        "issuetype": {"name": "Task"},
        "description": "Description text"
    }
)

# Update an issue
jira.update_issue(
    "PROJ-123",
    fields={
        "summary": "Updated summary"
    }
)

# Add a comment
jira.add_comment(
    "PROJ-123",
    "This is a comment"
)

# Add a comment with ADF
jira.add_comment(
    "PROJ-123",
    {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "This is a comment with ADF formatting"
                    }
                ]
            }
        ]
    }
)
```

### Search Operations

```python
# Using the core Jira client
issues = jira.jql_search("project = PROJ ORDER BY created DESC")

# Get all issues with helper method
all_issues = jira.jql_get_all_issues("project = PROJ")

# Using specialized search client
search_jira = get_search_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

# Advanced search with field selection
issues = search_jira.jql_search(
    "project = PROJ AND status = 'In Progress'",
    fields=["key", "summary", "status", "assignee"],
    start_at=0,
    max_results=100
)
```

### Project Operations

```python
# Using the core Jira client
projects = jira.get_all_projects()

# Using specialized projects client
projects_jira = get_projects_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

# Get project with expanded details
project = projects_jira.get_project(
    "PROJ",
    expand="description,lead,url,projectKeys"
)

# Get project versions
versions = projects_jira.get_project_versions("PROJ")

# Create a new version
new_version = projects_jira.create_version(
    "PROJ",
    name="1.0.0",
    description="Initial release",
    released=False,
    start_date="2023-01-01"
)
```

### Boards and Sprints (Jira Software)

```python
software_jira = get_software_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)

# Get all boards
boards = software_jira.get_all_boards()

# Get sprints for a board
sprints = software_jira.get_all_sprints(board_id=123)

# Get issues in a sprint
sprint_issues = software_jira.get_sprint_issues(sprint_id=456)

# Move issues to sprint
software_jira.add_issues_to_sprint(
    sprint_id=456,
    issues=["PROJ-123", "PROJ-124"]
)
```

## Response Structure

The response structure in v3 API is generally similar to v2, but with some differences:

- ADF format is used for text fields when appropriate
- More consistent field naming
- Better handling of pagination metadata
- Additional metadata fields for certain endpoints

## Tips for Migration

1. **Update one endpoint at a time**: Start by migrating your most critical endpoints to v3.
2. **Use specialized clients**: Take advantage of the specialized clients for cleaner, more focused code.
3. **Leverage type hints**: The v3 API includes comprehensive type hints that work well with modern IDEs.
4. **Update your error handling**: Use the specialized exceptions for better error handling.
5. **Test thoroughly**: The v3 API behaves slightly differently from v2, so test your code thoroughly.

## Conclusion

The Jira v3 API implementation in atlassian-python-api offers significant improvements in functionality, error handling, and developer experience. By migrating to the v3 API, you can take advantage of the latest Jira features and ensure your code is future-proof.

If you encounter any issues during migration or have questions, please refer to the documentation or raise an issue on the GitHub repository. 