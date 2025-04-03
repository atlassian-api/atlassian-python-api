#!/usr/bin/env python3
"""
Mock responses for Jira v3 API endpoints.
This file contains predefined mock responses for testing the Jira v3 implementation.
"""

from copy import deepcopy

# User mocks
USER_MOCK = {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "Test User",
    "emailAddress": "test@example.com",
    "active": True,
    "timeZone": "America/New_York",
    "locale": "en_US",
    "self": "https://example.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede21g",
}

CURRENT_USER_MOCK = deepcopy(USER_MOCK)

USERS_RESULT = {
    "size": 2,
    "items": [
        deepcopy(USER_MOCK),
        {
            "accountId": "5b10a2844c20165700ede22h",
            "displayName": "Another User",
            "emailAddress": "another@example.com",
            "active": True,
            "self": "https://example.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede22h",
        },
    ],
}

# Group mocks
GROUP_MOCK = {
    "name": "test-group",
    "groupId": "abc123",
    "self": "https://example.atlassian.net/rest/api/3/group?groupId=abc123",
}

GROUPS_RESULT = {
    "total": 2,
    "groups": [
        deepcopy(GROUP_MOCK),
        {
            "name": "another-group",
            "groupId": "def456",
            "self": "https://example.atlassian.net/rest/api/3/group?groupId=def456",
        },
    ],
    "self": "https://example.atlassian.net/rest/api/3/groups",
}

GROUP_MEMBERS_RESULT = {
    "self": "https://example.atlassian.net/rest/api/3/group/member?groupId=abc123",
    "maxResults": 50,
    "total": 2,
    "isLast": True,
    "values": [
        deepcopy(USER_MOCK),
        {
            "accountId": "5b10a2844c20165700ede22h",
            "displayName": "Another User",
            "emailAddress": "another@example.com",
            "active": True,
            "self": "https://example.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede22h",
        },
    ],
}

# Issue mocks
ISSUE_MOCK = {
    "id": "10001",
    "key": "TEST-1",
    "self": "https://example.atlassian.net/rest/api/3/issue/10001",
    "fields": {
        "summary": "Test Issue",
        "description": {
            "version": 1,
            "type": "doc",
            "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "This is a test issue description."}]}
            ],
        },
        "project": {
            "id": "10000",
            "key": "TEST",
            "name": "Test Project",
            "self": "https://example.atlassian.net/rest/api/3/project/10000",
        },
        "issuetype": {
            "id": "10002",
            "name": "Task",
            "self": "https://example.atlassian.net/rest/api/3/issuetype/10002",
        },
        "status": {"id": "10003", "name": "To Do", "self": "https://example.atlassian.net/rest/api/3/status/10003"},
        "priority": {"id": "3", "name": "Medium", "self": "https://example.atlassian.net/rest/api/3/priority/3"},
        "created": "2023-08-01T12:00:00.000Z",
        "updated": "2023-08-01T12:00:00.000Z",
        "creator": deepcopy(USER_MOCK),
        "reporter": deepcopy(USER_MOCK),
        "assignee": deepcopy(USER_MOCK),
    },
}

ISSUES_SEARCH_RESULT = {
    "expand": "names,schema",
    "startAt": 0,
    "maxResults": 50,
    "total": 2,
    "issues": [
        deepcopy(ISSUE_MOCK),
        {
            "id": "10002",
            "key": "TEST-2",
            "self": "https://example.atlassian.net/rest/api/3/issue/10002",
            "fields": {
                "summary": "Another Test Issue",
                "issuetype": {
                    "id": "10002",
                    "name": "Task",
                    "self": "https://example.atlassian.net/rest/api/3/issuetype/10002",
                },
                "status": {
                    "id": "10004",
                    "name": "In Progress",
                    "self": "https://example.atlassian.net/rest/api/3/status/10004",
                },
            },
        },
    ],
}

# Comment mocks
COMMENT_MOCK = {
    "id": "10001",
    "self": "https://example.atlassian.net/rest/api/3/issue/TEST-1/comment/10001",
    "body": {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "This is a test comment."}]}],
    },
    "author": deepcopy(USER_MOCK),
    "created": "2023-08-01T12:00:00.000Z",
    "updated": "2023-08-01T12:00:00.000Z",
}

COMMENTS_RESULT = {
    "self": "https://example.atlassian.net/rest/api/3/issue/TEST-1/comment",
    "maxResults": 50,
    "total": 2,
    "comments": [
        deepcopy(COMMENT_MOCK),
        {
            "id": "10002",
            "self": "https://example.atlassian.net/rest/api/3/issue/TEST-1/comment/10002",
            "body": {
                "version": 1,
                "type": "doc",
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "This is another test comment."}]}
                ],
            },
            "author": deepcopy(USER_MOCK),
            "created": "2023-08-01T13:00:00.000Z",
            "updated": "2023-08-01T13:00:00.000Z",
        },
    ],
}

# Project mocks
PROJECT_MOCK = {
    "id": "10000",
    "key": "TEST",
    "name": "Test Project",
    "description": "This is a test project",
    "lead": deepcopy(USER_MOCK),
    "url": "https://example.atlassian.net/browse/TEST",
    "projectTypeKey": "software",
    "self": "https://example.atlassian.net/rest/api/3/project/10000",
}

PROJECTS_RESULT = {
    "self": "https://example.atlassian.net/rest/api/3/project",
    "nextPage": "https://example.atlassian.net/rest/api/3/project?startAt=50",
    "maxResults": 50,
    "startAt": 0,
    "total": 2,
    "isLast": True,
    "values": [
        deepcopy(PROJECT_MOCK),
        {
            "id": "10001",
            "key": "DEMO",
            "name": "Demo Project",
            "description": "This is a demo project",
            "lead": deepcopy(USER_MOCK),
            "projectTypeKey": "business",
            "self": "https://example.atlassian.net/rest/api/3/project/10001",
        },
    ],
}

# Component mocks
COMPONENT_MOCK = {
    "id": "10000",
    "name": "Test Component",
    "description": "This is a test component",
    "lead": deepcopy(USER_MOCK),
    "assigneeType": "PROJECT_LEAD",
    "assignee": deepcopy(USER_MOCK),
    "realAssigneeType": "PROJECT_LEAD",
    "realAssignee": deepcopy(USER_MOCK),
    "isAssigneeTypeValid": True,
    "project": "TEST",
    "projectId": 10000,
    "self": "https://example.atlassian.net/rest/api/3/component/10000",
}

COMPONENTS_RESULT = [
    deepcopy(COMPONENT_MOCK),
    {
        "id": "10001",
        "name": "Another Component",
        "description": "This is another test component",
        "project": "TEST",
        "projectId": 10000,
        "self": "https://example.atlassian.net/rest/api/3/component/10001",
    },
]

# Version mocks
VERSION_MOCK = {
    "id": "10000",
    "name": "v1.0",
    "description": "Version 1.0",
    "released": False,
    "archived": False,
    "releaseDate": "2023-12-31",
    "userReleaseDate": "31/Dec/23",
    "projectId": 10000,
    "self": "https://example.atlassian.net/rest/api/3/version/10000",
}

VERSIONS_RESULT = [
    deepcopy(VERSION_MOCK),
    {
        "id": "10001",
        "name": "v1.1",
        "description": "Version 1.1",
        "released": True,
        "archived": False,
        "releaseDate": "2023-06-30",
        "userReleaseDate": "30/Jun/23",
        "projectId": 10000,
        "self": "https://example.atlassian.net/rest/api/3/version/10001",
    },
]

# Issue type mocks
ISSUE_TYPE_MOCK = {
    "id": "10002",
    "name": "Task",
    "description": "A task that needs to be done.",
    "iconUrl": "https://example.atlassian.net/secure/viewavatar?size=xsmall&avatarId=10318&avatarType=issuetype",
    "self": "https://example.atlassian.net/rest/api/3/issuetype/10002",
}

ISSUE_TYPES_RESULT = [
    deepcopy(ISSUE_TYPE_MOCK),
    {
        "id": "10003",
        "name": "Bug",
        "description": "A problem which impairs or prevents the functions of the product.",
        "iconUrl": "https://example.atlassian.net/secure/viewavatar?size=xsmall&avatarId=10303&avatarType=issuetype",
        "self": "https://example.atlassian.net/rest/api/3/issuetype/10003",
    },
]

# Permission mocks
PERMISSIONS_RESULT = {
    "permissions": {
        "BROWSE_PROJECTS": {
            "id": "10",
            "key": "BROWSE_PROJECTS",
            "name": "Browse Projects",
            "type": "PROJECT",
            "description": "Ability to browse projects and the issues within them.",
        },
        "CREATE_ISSUES": {
            "id": "11",
            "key": "CREATE_ISSUES",
            "name": "Create Issues",
            "type": "PROJECT",
            "description": "Ability to create issues.",
        },
    }
}

# Field mocks
FIELD_MOCK = {
    "id": "summary",
    "key": "summary",
    "name": "Summary",
    "custom": False,
    "orderable": True,
    "navigable": True,
    "searchable": True,
    "clauseNames": ["summary"],
    "schema": {"type": "string", "system": "summary"},
}

FIELDS_RESULT = [
    deepcopy(FIELD_MOCK),
    {
        "id": "description",
        "key": "description",
        "name": "Description",
        "custom": False,
        "orderable": True,
        "navigable": True,
        "searchable": True,
        "clauseNames": ["description"],
        "schema": {"type": "string", "system": "description"},
    },
    {
        "id": "customfield_10000",
        "key": "customfield_10000",
        "name": "Custom Field",
        "custom": True,
        "orderable": True,
        "navigable": True,
        "searchable": True,
        "clauseNames": ["cf[10000]"],
        "schema": {
            "type": "string",
            "custom": "com.atlassian.jira.plugin.system.customfieldtypes:textfield",
            "customId": 10000,
        },
    },
]

# Error responses
ERROR_NOT_FOUND = {"errorMessages": ["The requested resource could not be found."], "errors": {}}

ERROR_PERMISSION_DENIED = {"errorMessages": ["You do not have permission to perform this operation."], "errors": {}}

ERROR_VALIDATION = {"errorMessages": [], "errors": {"summary": "Summary is required"}}

# Board mocks (Jira Software)
BOARD_MOCK = {
    "id": 1,
    "name": "Test Board",
    "type": "scrum",
    "self": "https://example.atlassian.net/rest/agile/1.0/board/1",
}

BOARDS_RESULT = {
    "maxResults": 50,
    "startAt": 0,
    "total": 2,
    "isLast": True,
    "values": [
        deepcopy(BOARD_MOCK),
        {
            "id": 2,
            "name": "Another Board",
            "type": "kanban",
            "self": "https://example.atlassian.net/rest/agile/1.0/board/2",
        },
    ],
}

# Sprint mocks (Jira Software)
SPRINT_MOCK = {
    "id": 1,
    "name": "Sprint 1",
    "state": "active",
    "startDate": "2023-08-01T00:00:00.000Z",
    "endDate": "2023-08-15T00:00:00.000Z",
    "originBoardId": 1,
    "goal": "Complete all priority tasks",
    "self": "https://example.atlassian.net/rest/agile/1.0/sprint/1",
}

SPRINTS_RESULT = {
    "maxResults": 50,
    "startAt": 0,
    "total": 2,
    "isLast": True,
    "values": [
        deepcopy(SPRINT_MOCK),
        {
            "id": 2,
            "name": "Sprint 2",
            "state": "future",
            "originBoardId": 1,
            "self": "https://example.atlassian.net/rest/agile/1.0/sprint/2",
        },
    ],
}


# Helper function to get mock data for specific endpoints
def get_mock_for_endpoint(endpoint, params=None):
    """
    Return appropriate mock data for a given endpoint.

    :param endpoint: API endpoint path
    :param params: Optional query parameters
    :return: Mock data dictionary
    """
    # Default to empty dict if endpoint not found
    endpoint = endpoint.lower()

    # User endpoints
    if endpoint == "rest/api/3/myself":
        return CURRENT_USER_MOCK
    elif endpoint == "rest/api/3/user" or endpoint == "rest/api/3/user/search":
        return USERS_RESULT

    # Group endpoints
    elif endpoint == "rest/api/3/group":
        return GROUP_MOCK
    elif endpoint == "rest/api/3/groups":
        return GROUPS_RESULT
    elif "rest/api/3/group/member" in endpoint:
        return GROUP_MEMBERS_RESULT

    # Issue endpoints
    elif "rest/api/3/issue/" in endpoint and "/comment" in endpoint:
        if endpoint.endswith("/comment"):
            return COMMENTS_RESULT
        else:
            return COMMENT_MOCK
    elif "rest/api/3/issue/" in endpoint:
        return ISSUE_MOCK
    elif endpoint == "rest/api/3/search":
        return ISSUES_SEARCH_RESULT

    # Project endpoints
    elif endpoint == "rest/api/3/project":
        return PROJECTS_RESULT
    elif "rest/api/3/project/" in endpoint:
        if "/component" in endpoint:
            return COMPONENTS_RESULT
        elif "/version" in endpoint:
            return VERSIONS_RESULT
        else:
            return PROJECT_MOCK

    # Issue type endpoints
    elif endpoint == "rest/api/3/issuetype":
        return ISSUE_TYPES_RESULT
    elif "rest/api/3/issuetype/" in endpoint:
        return ISSUE_TYPE_MOCK

    # Permission endpoints
    elif "rest/api/3/mypermissions" in endpoint:
        return PERMISSIONS_RESULT

    # Field endpoints
    elif endpoint == "rest/api/3/field":
        return FIELDS_RESULT

    # Jira Software endpoints
    elif "rest/agile/1.0/board" in endpoint:
        if endpoint.endswith("/board"):
            return BOARDS_RESULT
        elif "/sprint" in endpoint:
            return SPRINTS_RESULT
        else:
            return BOARD_MOCK
    elif "rest/agile/1.0/sprint" in endpoint:
        return SPRINT_MOCK

    # Default empty response
    return {}
