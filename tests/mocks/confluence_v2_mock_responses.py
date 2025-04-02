#!/usr/bin/env python3
"""
Mock responses for Confluence v2 API endpoints.
This file contains predefined mock responses for testing the Confluence v2 implementation.
"""

from copy import deepcopy


# Page mocks
PAGE_MOCK = {
    "id": "123456",
    "title": "Test Page",
    "status": "current",
    "body": {
        "storage": {
            "value": "<p>This is a test page content.</p>",
            "representation": "storage"
        }
    },
    "spaceId": "789012",
    "parentId": "654321",
    "authorId": "112233",
    "createdAt": "2023-08-01T12:00:00Z",
    "version": {
        "number": 1,
        "message": "",
        "createdAt": "2023-08-01T12:00:00Z",
        "authorId": "112233"
    },
    "_links": {
        "webui": "/spaces/TESTSPACE/pages/123456/Test+Page",
        "tinyui": "/x/AbCdEf",
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456"
    }
}

CHILD_PAGE_MOCK = {
    "id": "234567",
    "title": "Child Page",
    "status": "current",
    "parentId": "123456",
    "spaceId": "789012",
    "authorId": "112233",
    "_links": {
        "webui": "/spaces/TESTSPACE/pages/234567/Child+Page",
        "self": "https://example.atlassian.net/wiki/api/v2/pages/234567"
    }
}

PAGE_RESULT_LIST = {
    "results": [
        deepcopy(PAGE_MOCK),
        {
            "id": "345678",
            "title": "Another Page",
            "status": "current",
            "spaceId": "789012",
            "_links": {
                "webui": "/spaces/TESTSPACE/pages/345678/Another+Page",
                "self": "https://example.atlassian.net/wiki/api/v2/pages/345678"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/pages?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/pages"
    }
}

CHILD_PAGES_RESULT = {
    "results": [
        deepcopy(CHILD_PAGE_MOCK),
        {
            "id": "456789",
            "title": "Another Child Page",
            "status": "current",
            "parentId": "123456",
            "spaceId": "789012",
            "_links": {
                "webui": "/spaces/TESTSPACE/pages/456789/Another+Child+Page",
                "self": "https://example.atlassian.net/wiki/api/v2/pages/456789"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/children"
    }
}

# Space mocks
SPACE_MOCK = {
    "id": "789012",
    "key": "TESTSPACE",
    "name": "Test Space",
    "type": "global",
    "status": "current",
    "description": {
        "plain": {
            "value": "This is a test space",
            "representation": "plain"
        }
    },
    "_links": {
        "webui": "/spaces/TESTSPACE",
        "self": "https://example.atlassian.net/wiki/api/v2/spaces/789012"
    }
}

SPACES_RESULT = {
    "results": [
        deepcopy(SPACE_MOCK),
        {
            "id": "987654",
            "key": "ANOTHERSPACE",
            "name": "Another Space",
            "type": "global",
            "status": "current",
            "_links": {
                "webui": "/spaces/ANOTHERSPACE",
                "self": "https://example.atlassian.net/wiki/api/v2/spaces/987654"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/spaces?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/spaces"
    }
}

SPACE_CONTENT_RESULT = {
    "results": [
        {
            "id": "123456",
            "title": "Test Page",
            "status": "current",
            "type": "page",
            "spaceId": "789012",
            "_links": {
                "webui": "/spaces/TESTSPACE/pages/123456/Test+Page",
                "self": "https://example.atlassian.net/wiki/api/v2/pages/123456"
            }
        },
        {
            "id": "567890",
            "title": "Test Blog Post",
            "status": "current",
            "type": "blogpost",
            "spaceId": "789012",
            "_links": {
                "webui": "/spaces/TESTSPACE/blog/567890/Test+Blog+Post",
                "self": "https://example.atlassian.net/wiki/api/v2/blogposts/567890"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/spaces/789012/content"
    }
}

# Search mocks
SEARCH_RESULT = {
    "results": [
        {
            "content": {
                "id": "123456",
                "title": "Test Page",
                "type": "page",
                "status": "current",
                "spaceId": "789012",
                "_links": {
                    "webui": "/spaces/TESTSPACE/pages/123456/Test+Page",
                    "self": "https://example.atlassian.net/wiki/api/v2/pages/123456"
                }
            },
            "excerpt": "This is a <b>test</b> page content.",
            "lastModified": "2023-08-01T12:00:00Z"
        },
        {
            "content": {
                "id": "345678",
                "title": "Another Page",
                "type": "page",
                "status": "current",
                "spaceId": "789012",
                "_links": {
                    "webui": "/spaces/TESTSPACE/pages/345678/Another+Page",
                    "self": "https://example.atlassian.net/wiki/api/v2/pages/345678"
                }
            },
            "excerpt": "This is <b>another</b> test page.",
            "lastModified": "2023-08-01T13:00:00Z"
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/search?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/search"
    }
}

# Property mocks
PROPERTY_MOCK = {
    "id": "prop123",
    "key": "test-property",
    "value": {
        "testKey": "testValue",
        "nested": {
            "nestedKey": "nestedValue"
        }
    },
    "version": {
        "number": 1,
        "message": "",
        "createdAt": "2023-08-01T12:00:00Z",
        "authorId": "112233"
    },
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/properties/test-property"
    }
}

PROPERTIES_RESULT = {
    "results": [
        deepcopy(PROPERTY_MOCK),
        {
            "id": "prop456",
            "key": "another-property",
            "value": {
                "key1": "value1",
                "key2": 42
            },
            "version": {
                "number": 1
            },
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/properties/another-property"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/pages/123456/properties?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/properties"
    }
}

# Label mocks
LABEL_MOCK = {
    "id": "label123",
    "name": "test-label",
    "prefix": "global",
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/labels/label123"
    }
}

LABELS_RESULT = {
    "results": [
        deepcopy(LABEL_MOCK),
        {
            "id": "label456",
            "name": "another-label",
            "prefix": "global",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/labels/label456"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/pages/123456/labels?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/labels"
    }
}

# Comment mocks
COMMENT_MOCK = {
    "id": "comment123",
    "status": "current",
    "title": "",
    "body": {
        "storage": {
            "value": "<p>This is a test comment.</p>",
            "representation": "storage"
        }
    },
    "authorId": "112233",
    "createdAt": "2023-08-01T12:00:00Z",
    "version": {
        "number": 1,
        "createdAt": "2023-08-01T12:00:00Z",
        "authorId": "112233"
    },
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/comments/comment123"
    }
}

COMMENTS_RESULT = {
    "results": [
        deepcopy(COMMENT_MOCK),
        {
            "id": "comment456",
            "status": "current",
            "title": "",
            "body": {
                "storage": {
                    "value": "<p>This is another test comment.</p>",
                    "representation": "storage"
                }
            },
            "authorId": "112233",
            "createdAt": "2023-08-01T13:00:00Z",
            "version": {
                "number": 1
            },
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/comments/comment456"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/pages/123456/footer-comments?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/pages/123456/footer-comments"
    }
}

# Whiteboard mocks
WHITEBOARD_MOCK = {
    "id": "wb123",
    "title": "Test Whiteboard",
    "spaceId": "789012",
    "templateKey": "timeline",
    "authorId": "112233",
    "createdAt": "2023-08-01T12:00:00Z",
    "_links": {
        "webui": "/spaces/TESTSPACE/whiteboards/wb123/Test+Whiteboard",
        "self": "https://example.atlassian.net/wiki/api/v2/whiteboards/wb123"
    }
}

WHITEBOARD_CHILDREN_RESULT = {
    "results": [
        {
            "id": "wb456",
            "title": "Child Whiteboard",
            "parentId": "wb123",
            "spaceId": "789012",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/whiteboards/wb456"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/whiteboards/wb123/children"
    }
}

WHITEBOARD_ANCESTORS_RESULT = {
    "results": [
        {
            "id": "789012",
            "title": "Test Space",
            "type": "space",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/spaces/789012"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/whiteboards/wb123/ancestors"
    }
}

# Custom content mocks
CUSTOM_CONTENT_MOCK = {
    "id": "cc123",
    "type": "example.custom.type",
    "title": "Test Custom Content",
    "status": "current",
    "body": {
        "storage": {
            "value": "<p>This is custom content.</p>",
            "representation": "storage"
        }
    },
    "spaceId": "789012",
    "authorId": "112233",
    "createdAt": "2023-08-01T12:00:00Z",
    "version": {
        "number": 1,
        "createdAt": "2023-08-01T12:00:00Z",
        "authorId": "112233"
    },
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/custom-content/cc123"
    }
}

CUSTOM_CONTENT_RESULT = {
    "results": [
        deepcopy(CUSTOM_CONTENT_MOCK),
        {
            "id": "cc456",
            "type": "example.custom.type",
            "title": "Another Custom Content",
            "status": "current",
            "spaceId": "789012",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/custom-content/cc456"
            }
        }
    ],
    "_links": {
        "next": "/wiki/api/v2/custom-content?cursor=next-page-token",
        "self": "https://example.atlassian.net/wiki/api/v2/custom-content"
    }
}

CUSTOM_CONTENT_CHILDREN_RESULT = {
    "results": [
        {
            "id": "cc789",
            "type": "example.custom.type",
            "title": "Child Custom Content",
            "status": "current",
            "parentId": "cc123",
            "spaceId": "789012",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/custom-content/cc789"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/custom-content/cc123/children"
    }
}

CUSTOM_CONTENT_ANCESTORS_RESULT = {
    "results": [
        {
            "id": "123456",
            "title": "Test Page",
            "type": "page",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/pages/123456"
            }
        },
        {
            "id": "789012",
            "title": "Test Space",
            "type": "space",
            "_links": {
                "self": "https://example.atlassian.net/wiki/api/v2/spaces/789012"
            }
        }
    ],
    "_links": {
        "self": "https://example.atlassian.net/wiki/api/v2/custom-content/cc123/ancestors"
    }
}

# Error response mocks
ERROR_NOT_FOUND = {
    "statusCode": 404,
    "data": {
        "authorized": True,
        "valid": False,
        "errors": [
            {
                "message": "The requested resource could not be found",
                "exceptionName": "ResourceNotFoundException"
            }
        ],
        "successful": False
    }
}

ERROR_PERMISSION_DENIED = {
    "statusCode": 403,
    "data": {
        "authorized": False,
        "valid": True,
        "errors": [
            {
                "message": "Permission denied",
                "exceptionName": "PermissionDeniedException"
            }
        ],
        "successful": False
    }
}

ERROR_VALIDATION = {
    "statusCode": 400,
    "data": {
        "authorized": True,
        "valid": False,
        "errors": [
            {
                "message": "Invalid request",
                "exceptionName": "ValidationException",
                "validationErrors": [
                    {
                        "field": "title",
                        "message": "Title cannot be empty"
                    }
                ]
            }
        ],
        "successful": False
    }
}

# Define a function to get mock responses for specific endpoints
def get_mock_for_endpoint(endpoint, params=None):
    """
    Get the appropriate mock response for a given endpoint.
    
    Args:
        endpoint: The API endpoint path
        params: Optional parameters for the request
        
    Returns:
        A mock response object
    """
    if endpoint.startswith("api/v2/pages/") and endpoint.endswith("/children"):
        return deepcopy(CHILD_PAGES_RESULT)
    elif endpoint.startswith("api/v2/pages/") and endpoint.endswith("/properties"):
        return deepcopy(PROPERTIES_RESULT)
    elif endpoint.startswith("api/v2/pages/") and "/properties/" in endpoint:
        return deepcopy(PROPERTY_MOCK)
    elif endpoint.startswith("api/v2/pages/") and endpoint.endswith("/labels"):
        return deepcopy(LABELS_RESULT)
    elif endpoint.startswith("api/v2/pages/") and endpoint.endswith("/footer-comments"):
        return deepcopy(COMMENTS_RESULT)
    elif endpoint.startswith("api/v2/pages/") and endpoint.endswith("/inline-comments"):
        return deepcopy(COMMENTS_RESULT)
    elif endpoint.startswith("api/v2/pages/"):
        # Single page endpoint
        return deepcopy(PAGE_MOCK)
    elif endpoint == "api/v2/pages":
        return deepcopy(PAGE_RESULT_LIST)
    elif endpoint.startswith("api/v2/spaces/") and endpoint.endswith("/content"):
        return deepcopy(SPACE_CONTENT_RESULT)
    elif endpoint.startswith("api/v2/spaces/") and endpoint.endswith("/labels"):
        return deepcopy(LABELS_RESULT)
    elif endpoint.startswith("api/v2/spaces/"):
        # Single space endpoint
        return deepcopy(SPACE_MOCK)
    elif endpoint == "api/v2/spaces":
        return deepcopy(SPACES_RESULT)
    elif endpoint.startswith("api/v2/search"):
        return deepcopy(SEARCH_RESULT)
    elif endpoint.startswith("api/v2/comments/") and endpoint.endswith("/children"):
        return deepcopy(COMMENTS_RESULT)
    elif endpoint.startswith("api/v2/comments/"):
        return deepcopy(COMMENT_MOCK)
    elif endpoint == "api/v2/comments":
        return deepcopy(COMMENT_MOCK)
    elif endpoint.startswith("api/v2/whiteboards/") and endpoint.endswith("/children"):
        return deepcopy(WHITEBOARD_CHILDREN_RESULT)
    elif endpoint.startswith("api/v2/whiteboards/") and endpoint.endswith("/ancestors"):
        return deepcopy(WHITEBOARD_ANCESTORS_RESULT)
    elif endpoint.startswith("api/v2/whiteboards/"):
        return deepcopy(WHITEBOARD_MOCK)
    elif endpoint == "api/v2/whiteboards":
        return deepcopy(WHITEBOARD_MOCK)
    elif endpoint.startswith("api/v2/custom-content/") and endpoint.endswith("/children"):
        return deepcopy(CUSTOM_CONTENT_CHILDREN_RESULT)
    elif endpoint.startswith("api/v2/custom-content/") and endpoint.endswith("/ancestors"):
        return deepcopy(CUSTOM_CONTENT_ANCESTORS_RESULT)
    elif endpoint.startswith("api/v2/custom-content/") and endpoint.endswith("/labels"):
        return deepcopy(LABELS_RESULT)
    elif endpoint.startswith("api/v2/custom-content/") and endpoint.endswith("/properties"):
        return deepcopy(PROPERTIES_RESULT)
    elif endpoint.startswith("api/v2/custom-content/") and "/properties/" in endpoint:
        return deepcopy(PROPERTY_MOCK)
    elif endpoint.startswith("api/v2/custom-content/"):
        return deepcopy(CUSTOM_CONTENT_MOCK)
    elif endpoint == "api/v2/custom-content":
        return deepcopy(CUSTOM_CONTENT_RESULT)
    
    # Default to page mock
    return deepcopy(PAGE_MOCK) 