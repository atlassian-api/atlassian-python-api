# Confluence v2 API Migration Guide

## URL Requirements

**Important:** The URL format is different in v2. You must provide the complete URL as required by your Confluence instance:

- For Confluence Cloud, include `/wiki` in the URL: `https://your-instance.atlassian.net/wiki`
- For Confluence Server/Data Center, use the base URL as appropriate for your installation

The library no longer automatically adds `/wiki` to cloud URLs. Instead, it uses the URL exactly as provided.

## Introduction

The Confluence v2 API is the latest REST API version for Confluence Cloud that offers several advantages over the v1 API:

- More consistent endpoint patterns
- Improved pagination with cursor-based pagination
- New content types (whiteboards, custom content)
- Enhanced property management
- Better performance

While the v1 API is still supported, we recommend migrating to the v2 API for new development and gradually updating existing code.

## Getting Started with v2 API

### Instantiating a v2 API Client

The simplest way to use the v2 API is to specify the API version when creating your Confluence instance:

```python
from atlassian import Confluence

# Create a v2 API client
confluence = Confluence(
    url="https://your-instance.atlassian.net/wiki",
    username="your-email@example.com",
    password="your-api-token",
    api_version=2,  # Specify API version 2
    cloud=True      # v2 API is only available for cloud instances
)
```

Or use the factory method:

```python
from atlassian import Confluence

# Create a v2 API client using the factory method
confluence = Confluence.factory(
    url="https://your-instance.atlassian.net/wiki",
    username="your-email@example.com",
    password="your-api-token",
    api_version=2,
    cloud=True
)
```

### Compatibility Layer

The library includes a compatibility layer to make migration easier. You can use many v1 method names with a v2 client, and you'll receive deprecation warnings suggesting the v2 method name to use instead.

```python
# This will work but show a deprecation warning
pages = confluence.get_all_pages_from_space("SPACEKEY")

# The warning will suggest using the v2 method name instead
pages = confluence.get_pages(space_key="SPACEKEY")
```

## Key Method Changes

Below are the most common method name changes between v1 and v2:

| v1 Method | v2 Method | Notes |
|-----------|-----------|-------|
| `get_page_by_id(page_id)` | `get_page_by_id(page_id)` | Same name, different response structure |
| `get_all_pages_from_space(space)` | `get_pages(space_key=space)` | Parameter name changes |
| `get_page_child_by_type(page_id, type="page")` | `get_child_pages(page_id)` | Simpler, focused on pages |
| `create_page(space, title, body)` | `create_page(space_id, title, body)` | Parameter `space` renamed to `space_id` |
| `update_page(page_id, title, body, version)` | `update_page(page_id, title, body, version)` | Same name, requires version number |
| `update_or_create(page_id, title, body, ...)` | No direct equivalent | Use separate create/update methods |
| `get_content_properties(page_id)` | `get_page_properties(page_id)` | More specific naming |
| `get_content_property(page_id, key)` | `get_page_property_by_key(page_id, key)` | More specific naming |

## Response Structure Changes

The response structure differs significantly between v1 and v2 APIs:

### v1 Example Response

```json
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
  "version": {
    "number": 1
  },
  "space": {
    "key": "SPACEKEY",
    "name": "Space Name"
  },
  "_links": {
    "self": "https://your-instance.atlassian.net/wiki/rest/api/content/123456"
  }
}
```

### v2 Example Response

```json
{
  "id": "123456",
  "status": "current",
  "title": "Page Title",
  "body": {
    "storage": {
      "value": "<p>Content</p>",
      "representation": "storage"
    }
  },
  "version": {
    "number": 1,
    "message": "",
    "createdAt": "2023-01-01T12:00:00.000Z",
    "authorId": "user123"
  },
  "spaceId": "SPACEKEY",
  "_links": {
    "webui": "/spaces/SPACEKEY/pages/123456/Page+Title",
    "tinyui": "/x/ABCDE",
    "self": "https://your-instance.atlassian.net/wiki/api/v2/pages/123456"
  }
}
```

Key differences:
- The `type` field is no longer included as v2 endpoints are type-specific
- `space` is now represented as `spaceId` and is just the key, not an object
- `_links` structure provides more useful links
- The v2 API version returns additional fields and metadata

## Pagination Changes

### v1 API Pagination

```python
# v1 style pagination with start and limit
pages = confluence.get_all_pages_from_space("SPACEKEY", start=0, limit=100)
```

### v2 API Pagination

```python
# v2 style pagination with cursor
pages = confluence.get_pages(space_key="SPACEKEY", limit=100)

# For subsequent pages, use the cursor from _links.next
if "_links" in pages and "next" in pages["_links"]:
    next_url = pages["_links"]["next"]
    # Extract cursor from the URL
    cursor = next_url.split("cursor=")[1].split("&")[0]
    next_pages = confluence.get_pages(space_key="SPACEKEY", limit=100, cursor=cursor)
```

## New Features in v2 API

### Whiteboards

```python
# Create a whiteboard
whiteboard = confluence.create_whiteboard(
    space_id="SPACEKEY",
    title="My Whiteboard",
    content='{"version":1,"type":"doc",...}' # Simplified for example
)

# Get whiteboard by ID
whiteboard = confluence.get_whiteboard_by_id(whiteboard_id)

# Get whiteboard children
children = confluence.get_whiteboard_children(whiteboard_id)

# Get whiteboard ancestors
ancestors = confluence.get_whiteboard_ancestors(whiteboard_id)

# Delete whiteboard
response = confluence.delete_whiteboard(whiteboard_id)
```

### Custom Content

```python
# Create custom content
custom_content = confluence.create_custom_content(
    space_id="SPACEKEY",
    title="My Custom Content",
    body="<p>Custom content body</p>",
    type="custom_content_type"
)

# Get custom content by ID
content = confluence.get_custom_content_by_id(content_id)

# Update custom content
updated = confluence.update_custom_content(
    content_id=content_id,
    title="Updated Title",
    body="<p>Updated body</p>",
    version=content["version"]["number"]
)

# Get custom content properties
properties = confluence.get_custom_content_properties(content_id)

# Delete custom content
response = confluence.delete_custom_content(content_id)
```

### Labels

```python
# Get page labels
labels = confluence.get_page_labels(page_id)

# Add label to page
response = confluence.add_page_label(page_id, "important")

# Delete label from page
response = confluence.delete_page_label(page_id, "important")

# Get space labels
space_labels = confluence.get_space_labels(space_key)

# Add label to space
response = confluence.add_space_label(space_key, "team")

# Delete label from space
response = confluence.delete_space_label(space_key, "team")
```

### Comments

```python
# Get page footer comments
comments = confluence.get_page_footer_comments(page_id)

# Get page inline comments
inline_comments = confluence.get_page_inline_comments(page_id)

# Create a footer comment
comment = confluence.create_page_footer_comment(
    page_id=page_id,
    body="<p>This is a footer comment</p>"
)

# Create an inline comment
inline_comment = confluence.create_page_inline_comment(
    page_id=page_id,
    body="<p>This is an inline comment</p>",
    inline_comment_properties={
        "highlight": "text to highlight",
        "position": "after"
    }
)

# Update a comment
updated_comment = confluence.update_comment(
    comment_id=comment_id,
    body="<p>Updated comment</p>",
    version=comment["version"]["number"]
)

# Delete a comment
response = confluence.delete_comment(comment_id)
```

## Migration Checklist

- [ ] Update your client initialization to specify `api_version=2`
- [ ] Update method names according to the mapping table above
- [ ] Adjust your code to handle the new response structures
- [ ] Update pagination handling to use cursor-based pagination
- [ ] Test thoroughly with a small portion of your code before full migration
- [ ] Watch for deprecation warnings to identify methods that need updating
- [ ] Take advantage of new v2 features when applicable
- [ ] Update error handling to accommodate v2-specific error responses

## Troubleshooting

### Common Issues

1. **Missing Fields**: If your code expects certain fields that exist in v1 but not in v2, update your code to use the v2 equivalent fields.

2. **Parameter Changes**: Many methods have slight parameter name changes (e.g., `space` to `space_id`). Check the method documentation.

3. **Version Requirements**: The v2 API requires providing the content version number for updates. Always fetch the current version before updating.

4. **Cloud Only**: The v2 API is only available for Confluence Cloud. Server/Data Center instances must use v1.

### Getting Help

If you encounter issues during migration, consider:

1. Checking the [API documentation](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
2. Reviewing the example files in the `examples/` directory
3. Filing an issue in the [GitHub repository](https://github.com/atlassian-api/atlassian-python-api/issues)

## Conclusion

Migrating to the Confluence v2 API provides access to improved functionality and new features. While the process requires some code changes, the compatibility layer makes the transition smoother by supporting v1 method names with deprecation warnings.

We recommend a gradual migration approach, starting with updating your client initialization to use v2, and then incrementally updating method names and handling the new response structures. 