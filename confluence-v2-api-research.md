# Confluence Cloud REST API v2 Research Analysis

## Executive Summary

The Confluence Cloud REST API v2 represents a significant architectural shift from v1, designed to address performance issues, improve predictability, and support modern OAuth 2.0 scopes. This research documents the key differences, requirements, and implementation considerations for migrating from v1 to v2.

## Key Differences Between v1 and v2 APIs

### 1. Pagination System

**v1 API - Offset-based Pagination:**
- Uses `start` and `limit` parameters
- Example: `GET /wiki/rest/api/content?start=0&limit=25`
- Issues: Missing data during pagination, poor performance with high offsets
- Allows parallel requests for faster bulk operations

**v2 API - Cursor-based Pagination:**
- Uses `limit` and `cursor` parameters
- Example: `GET /wiki/api/v2/pages?limit=5`
- Response includes Link header with next URL containing cursor token
- Format: `</wiki/api/v2/pages?limit=5&cursor=<cursor token>>; rel="next"`
- Also available in `_links.next` property of response body
- Benefits: Better latency, prevents missing data issues
- Limitation: No parallel pagination, sequential only

### 2. Endpoint Specialization

**v1 API - Generic Endpoints:**
- Single `/rest/api/content` endpoint for all content types
- Uses `type` parameter to filter (pages, blogposts, etc.)
- Relies heavily on `expand` parameter for additional data
- Example: `GET /rest/api/content?type=page&expand=space,history,body.storage`

**v2 API - Specialized Endpoints:**
- Separate endpoints for each content type:
  - `/wiki/api/v2/pages` - Pages only
  - `/wiki/api/v2/blogposts` - Blog posts only
  - `/wiki/api/v2/comments` - Comments only
  - `/wiki/api/v2/attachments` - Attachments only
- Eliminates complex expand parameters
- More predictable behavior and better optimization

### 3. Content Body Formats

**v1 API:**
- Primary format: `storage` (Confluence storage format)
- Limited ADF support through undocumented methods
- Expand parameter: `expand=body.storage`

**v2 API:**
- Native support for multiple body formats:
  - `storage` - Traditional Confluence storage format
  - `atlas_doc_format` - Atlassian Document Format (ADF)
  - `view` - Rendered view format
- Query parameter: `body-format=ATLAS_DOC_FORMAT`
- Example: `GET /wiki/api/v2/pages/{id}?body-format=ATLAS_DOC_FORMAT`

### 4. Response Structure Changes

**v1 API Response:**
```json
{
  "results": [...],
  "start": 0,
  "limit": 25,
  "size": 25,
  "_links": {
    "base": "...",
    "context": "...",
    "next": "...",
    "prev": "..."
  }
}
```

**v2 API Response:**
```json
{
  "results": [...],
  "_links": {
    "next": "<string>",
    "base": "<string>"
  }
}
```

### 5. Authentication and Authorization

**v1 API:**
- Basic authentication
- API tokens
- Limited OAuth 2.0 scope support

**v2 API:**
- Enhanced OAuth 2.0 granular scopes support
- Better compatibility with modern authentication patterns
- Same basic auth and API token support

## Atlassian Document Format (ADF) Requirements

### What is ADF?
- JSON-based document format used by modern Atlassian products
- Structured representation of rich content (text, images, tables, etc.)
- Replaces traditional storage format for new features

### ADF Structure Example:
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Some text in a paragraph"
        }
      ]
    }
  ]
}
```

### ADF in v2 API:
- Native support in response body: `"atlas_doc_format": {}`
- Query parameter: `body-format=ATLAS_DOC_FORMAT`
- Content creation: `"representation": "atlas_doc_format"`

## Cursor-based Pagination Implementation Requirements

### Basic Implementation Pattern:
```python
def get_all_pages_v2(self, space_id=None, limit=25):
    """Get all pages using v2 cursor pagination"""
    all_pages = []
    url = f"{self.url}/wiki/api/v2/pages"
    params = {"limit": limit}
    
    if space_id:
        params["space-id"] = space_id
    
    while url:
        response = self.get(url, params=params)
        data = response.json()
        
        all_pages.extend(data.get("results", []))
        
        # Get next URL from _links or Link header
        next_link = data.get("_links", {}).get("next")
        if next_link:
            url = f"{self.url}{next_link}"
            params = {}  # Parameters are in the next URL
        else:
            url = None
    
    return all_pages
```

### Key Implementation Considerations:
1. **Sequential Processing**: Cannot parallelize pagination requests
2. **Cursor Management**: Cursors are opaque tokens, cannot be manipulated
3. **Link Header Parsing**: Must handle both `_links.next` and Link header
4. **Parameter Handling**: Next URL contains all required parameters

## Migration Challenges and Considerations

### 1. Breaking Changes
- **Endpoint URLs**: Complete change from `/rest/api/` to `/wiki/api/v2/`
- **Pagination Logic**: Must rewrite all pagination code
- **Response Parsing**: Different response structure
- **Content Type Separation**: Pages and blog posts require separate calls

### 2. Performance Implications
- **Positive**: Better latency for individual requests
- **Negative**: Loss of parallel pagination capability
- **Neutral**: Cursor pagination prevents data inconsistency

### 3. Feature Gaps (Historical)
Based on community feedback, several gaps existed but have been addressed:
- Content properties endpoints (resolved)
- Space labels support (resolved)
- Depth parameter for child content (resolved)
- Favorited spaces filters (resolved)

### 4. Current Limitations
- **No Total Count**: Cursor pagination doesn't provide total result count
- **Sequential Only**: Cannot perform parallel pagination requests
- **Cursor Opacity**: Cannot jump to specific pages or calculate progress

## Deprecation Timeline

### Historical Timeline:
- **August 2023**: v1 deprecation announced
- **January 1, 2024**: Original sunset date (postponed)
- **February 1, 2024**: Content property endpoints sunset (postponed)
- **June 2024**: Revised sunset date (postponed)
- **April 30, 2025**: Current planned sunset date

### Current Status:
- v1 APIs marked as deprecated but still functional
- v2 APIs are production-ready and feature-complete
- Migration strongly recommended before April 2025

## Implementation Recommendations

### 1. Gradual Migration Strategy
- Implement v2 endpoints alongside existing v1 methods
- Use feature flags or configuration to switch between versions
- Maintain backward compatibility during transition period

### 2. Pagination Abstraction
- Create unified pagination interface that works with both v1 and v2
- Abstract cursor vs offset differences in implementation layer
- Provide migration path for existing code

### 3. Content Format Support
- Add ADF format support for modern content handling
- Maintain storage format compatibility for legacy content
- Provide conversion utilities between formats

### 4. Testing Strategy
- Comprehensive testing of pagination edge cases
- Validate ADF content parsing and generation
- Performance testing to compare v1 vs v2 response times

## Conclusion

The v2 API represents a significant improvement in terms of performance, predictability, and modern authentication support. However, the migration requires substantial code changes, particularly around pagination logic and endpoint structure. The loss of parallel pagination capability may impact performance for bulk operations, but the overall benefits of cursor-based pagination and endpoint specialization outweigh these concerns.

The implementation should prioritize:
1. Cursor-based pagination support
2. ADF format handling
3. Specialized endpoint integration
4. Backward compatibility during migration period

Content was rephrased for compliance with licensing restrictions.