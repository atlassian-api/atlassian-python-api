# Confluence API v1 to v2 Migration Guide

This guide explains how to migrate from Confluence API v1 to v2 in the `atlassian-python-api` library.

## Table of Contents

1. [Introduction](#introduction)
2. [Major Changes](#major-changes)
3. [Method Name Changes](#method-name-changes)
4. [Parameter Changes](#parameter-changes)
5. [Response Structure Changes](#response-structure-changes)
6. [Using the Compatibility Layer](#using-the-compatibility-layer)
7. [Migration Checklist](#migration-checklist)
8. [New v2-Only Features](#new-v2-only-features)

## Introduction

Atlassian has been transitioning from the older v1 REST API to the newer v2 REST API for Confluence Cloud. The v2 API provides several improvements:

- More consistent and intuitive endpoint paths
- Better performance for many operations
- New features like whiteboards and custom content
- More robust pagination with cursor-based results
- Improved content type handling
- Better error messages and validation

Our library supports both v1 and v2 APIs. The v2 implementation is accessible via the `ConfluenceV2` class, whereas the original `Confluence` class uses v1.

## Major Changes

The main differences between the v1 and v2 APIs include:

1. **Endpoint Structure**: v2 uses `api/v2/...` instead of `rest/api/...`
2. **Method Names**: Many method names have changed to be more descriptive
3. **Parameter Names**: Some parameter names have changed
4. **Response Structure**: Response JSON structures have changed
5. **Pagination**: v2 uses cursor-based pagination instead of offset-based
6. **New Features**: v2 adds support for whiteboards, custom content, etc.

## Method Name Changes

Here are the main method name changes between v1 and v2:

| v1 Method Name | v2 Method Name |
|----------------|---------------|
| `get_content` | `get_pages` |
| `get_content_by_id` | `get_page_by_id` |
| `get_content_children` | `get_child_pages` |
| `create_content` | `create_page` |
| `update_content` | `update_page` |
| `delete_content` | `delete_page` |
| `get_space_by_name` | `get_space_by_key` |
| `get_all_spaces` | `get_spaces` |
| `add_content_label` | `add_page_label` |
| `add_content_labels` | `add_page_labels` |
| `remove_content_label` | `delete_page_label` |
| `add_property` | `create_page_property` |
| `update_property` | `update_page_property` |
| `get_property` | `get_page_property_by_key` |
| `get_properties` | `get_page_properties` |
| `delete_property` | `delete_page_property` |

## Parameter Changes

When migrating to v2, be aware of these parameter changes:

1. `content_type` is no longer needed for page operations
2. `space_key` is replaced with `space_id` in most methods 
3. `expand` parameters now accept arrays of strings instead of comma-separated values
4. `body` format now uses a simpler structure in most cases
5. `status` parameter now accepts `current` instead of `current` or `draft`

Example of parameter changes:

```python
# v1 API
confluence.create_content(
    space="SPACE",
    title="Page Title",
    body="<p>Content</p>",
    type="page"
)

# v2 API
confluence_v2.create_page(
    space_id="123456",  # Note: space ID, not key
    title="Page Title",
    body="<p>Content</p>"
)
```

## Response Structure Changes

The structure of responses has changed in v2. Key differences include:

1. Pages now have a simpler top-level structure
2. Page content is directly accessible in the `body` field
3. Most IDs are now numeric strings instead of complex keys
4. Metadata is more consistently organized
5. Links to related resources are provided in the `_links` field

Example response structure changes:

```python
# v1 API response
{
    "id": "123456",
    "type": "page",
    "status": "current",
    "title": "Page Title",
    "body": {
        "storage": {
            "value": "<p>Content</p>",
            "representation": "storage"
        }
    },
    "space": {
        "key": "SPACE",
        "name": "Space Name"
    },
    "version": {
        "number": 1
    }
}

# v2 API response
{
    "id": "123456",
    "title": "Page Title",
    "status": "current",
    "body": {
        "storage": {
            "value": "<p>Content</p>",
            "representation": "storage"
        }
    },
    "spaceId": "789012",
    "version": {
        "number": 1,
        "message": "",
        "createdAt": "2023-08-01T12:00:00Z",
        "authorId": "112233"
    },
    "_links": {
        "webui": "/spaces/SPACE/pages/123456/Page+Title",
        "tinyui": "/x/AbCdEf",
        "self": "https://your-domain.atlassian.net/wiki/api/v2/pages/123456"
    }
}
```

## Using the Compatibility Layer

The `ConfluenceV2` class includes a compatibility layer that allows you to use v1 method names with the v2 implementation:

```python
from atlassian import ConfluenceV2

# Initialize with v2 API
confluence = ConfluenceV2(
    url="https://your-domain.atlassian.net/wiki",
    username="your-username",
    password="your-api-token"
)

# Using v1 method name - will work but show deprecation warning
page = confluence.get_content_by_id("123456")

# Using v2 method name - preferred approach
page = confluence.get_page_by_id("123456")
```

When using v1 method names with the v2 implementation:

1. The methods will work as expected
2. Deprecation warnings will be shown
3. Parameters are passed to the equivalent v2 method
4. The response format will be the v2 format (not the v1 format)

To suppress deprecation warnings:

```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

To make deprecation warnings more visible:

```python
import warnings
warnings.filterwarnings("always", category=DeprecationWarning)
```

## Migration Checklist

Follow these steps to migrate your code from v1 to v2:

1. Change your client initialization:
   ```python
   # Before
   from atlassian import Confluence
   confluence = Confluence(url="...", username="...", password="...")
   
   # After
   from atlassian import ConfluenceV2
   confluence = ConfluenceV2(url="...", username="...", password="...")
   ```

2. Update method names to use v2 equivalents (see [Method Name Changes](#method-name-changes))

3. Update method parameters:
   - Replace space keys with space IDs
   - Update parameter names according to v2 method signatures
   - Update parameter values to use v2 format

4. Update response handling to account for the v2 response structure

5. Test your code thoroughly with the v2 API

6. Look for opportunities to use new v2-only features

## New v2-Only Features

The v2 API includes several features not available in v1:

1. **Whiteboards**: Create and manage whiteboards
   ```python
   # Create a whiteboard
   whiteboard = confluence.create_whiteboard(
       space_id="123456",
       title="My Whiteboard",
       template_key="timeline"
   )
   ```

2. **Custom Content**: Create and manage custom content types
   ```python
   # Create custom content
   content = confluence.create_custom_content(
       type="my.custom.type",
       title="My Custom Content",
       body="<p>Content</p>",
       space_id="123456"
   )
   ```

3. **Improved Comments**: Better support for inline and footer comments
   ```python
   # Get page comments
   comments = confluence.get_page_footer_comments(page_id="123456")
   
   # Create an inline comment
   comment = confluence.create_page_inline_comment(
       page_id="123456",
       body="This is an inline comment",
       inline_comment_properties={
           "textSelection": "text to comment on",
           "textSelectionMatchCount": 1,
           "textSelectionMatchIndex": 0
       }
   )
   ```

4. **Better Label Support**: Enhanced methods for working with labels
   ```python
   # Add page label
   label = confluence.add_page_label(page_id="123456", label="example-label")
   ```

5. **Content Properties**: More robust content property management
   ```python
   # Create page property
   property = confluence.create_page_property(
       page_id="123456",
       property_key="my-key",
       property_value={"data": "example"}
   )
   ```

For more examples, check the example files in the `examples/` directory.

## Conclusion

Migrating from v1 to v2 requires some changes, but the compatibility layer can help ease the transition. The v2 API offers many improvements and new features that make it worthwhile to update your code.

For questions or issues, please open an issue on the GitHub repository. 