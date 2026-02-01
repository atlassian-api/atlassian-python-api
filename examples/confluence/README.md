# Confluence Examples

This directory contains comprehensive examples demonstrating how to use the Confluence API client with both Cloud and Server implementations, including the new v2 API features.

## Structure

```
examples/confluence/
├── README.md
├── cloud/
│   ├── confluence_cloud_content_management.py
│   ├── confluence_v2_api_basics.py
│   ├── confluence_adf_content_examples.py
│   ├── confluence_v1_to_v2_migration.py
│   ├── confluence_cursor_pagination.py
│   ├── confluence_error_handling.py
│   └── confluence_dual_api_configuration.py
└── server/
    └── confluence_server_content_management.py
```

## Examples

### Confluence Cloud

#### Basic Cloud API Usage

**`confluence_cloud_content_management.py`** - Basic Confluence Cloud operations:
- Initializing the Confluence Cloud client
- Getting spaces and space content
- Retrieving pages and page details
- Working with page children, labels, comments, and attachments
- Searching for content
- Getting user information

#### v2 API Examples

**`confluence_v2_api_basics.py`** - Fundamental v2 API operations:
- v2 API client initialization and configuration
- Basic page operations (create, read, update, delete)
- ADF (Atlassian Document Format) content handling
- Cursor-based pagination
- Error handling and best practices

**`confluence_adf_content_examples.py`** - ADF content creation and manipulation:
- Creating various ADF content types (headings, paragraphs, lists, tables)
- Working with text formatting (bold, italic, links, code)
- Using panels, code blocks, and other advanced elements
- Converting between different content formats
- Best practices for ADF content creation

**`confluence_v1_to_v2_migration.py`** - Migration from v1 to v2 API:
- API endpoint differences
- Content format changes (Storage Format → ADF)
- Pagination changes (offset-based → cursor-based)
- Response structure differences
- Migration strategies and best practices

**`confluence_cursor_pagination.py`** - Cursor-based pagination:
- Basic cursor pagination for pages and spaces
- Handling pagination state and continuation
- Performance comparison with offset-based pagination
- Best practices for large dataset processing
- Memory-efficient iteration patterns

**`confluence_error_handling.py`** - Comprehensive error handling:
- Common API error types and handling
- Authentication and authorization errors
- Rate limiting and throttling
- Content validation errors
- Debugging and logging strategies
- Retry mechanisms and recovery patterns

**`confluence_dual_api_configuration.py`** - Dual API usage:
- Configuring dual API support
- Switching between v1 and v2 APIs dynamically
- API feature comparison and selection
- Migration strategies and compatibility
- Performance considerations

#### Prerequisites for Cloud Examples
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

#### Usage
```bash
cd examples/confluence/cloud
python [example_name].py
```

#### Configuration
Update the following variables in each script:
- `CONFLUENCE_URL`: Your Confluence Cloud domain (e.g., `https://your-domain.atlassian.net`)
- `API_TOKEN`: Your API token
- `TEST_SPACE_KEY`: A test space key (optional, defaults to "DEMO")

You can also set configuration via environment variables:
```bash
export CONFLUENCE_URL='https://your-domain.atlassian.net'
export CONFLUENCE_TOKEN='your-api-token'
export TEST_SPACE_KEY='DEMO'
```

### Confluence Server

**`confluence_server_content_management.py`** - Server API operations:
- Initializing the Confluence Server client
- Getting spaces and space content
- Working with pages, blog posts, and drafts
- Managing page labels, comments, and attachments
- Searching with CQL (Confluence Query Language)
- User and group management
- Trash and draft content management

**Prerequisites:**
- Confluence Server instance
- Username and password credentials

**Usage:**
```bash
cd examples/confluence/server
python confluence_server_content_management.py
```

**Configuration:**
Update the following in the script:
- `url`: Your Confluence Server URL (e.g., `https://your-confluence-server.com`)
- `username`: Your username
- `password`: Your password

## API Differences

### Cloud vs Server

| Feature | Cloud | Server |
|---------|-------|--------|
| Authentication | API Token | Username/Password |
| API Version | v1/v2 (dual support) | v1.0 |
| API Root | `wiki/rest/api` (v1), `wiki/api/v2` (v2) | `rest/api/1.0` |
| Pagination | Offset-based (v1), Cursor-based (v2) | Offset-based |
| Content IDs | Numeric (v1), UUID strings (v2) | Numeric IDs |
| Space IDs | Space keys (v1), UUID strings (v2) | Space keys |
| Content Format | Storage Format (v1), ADF (v2) | Storage Format |

### v1 vs v2 API (Cloud Only)

| Aspect | v1 API | v2 API |
|--------|--------|--------|
| **Content Format** | Storage Format (XHTML-like) | ADF (Atlassian Document Format) |
| **Pagination** | Offset-based (`start`/`limit`) | Cursor-based (`cursor`) |
| **Performance** | Standard | Enhanced |
| **Response Structure** | Nested expansion model | Flatter, more consistent |
| **ID Format** | Numeric IDs | UUID strings |
| **Space Reference** | Space keys | Space IDs |
| **Best For** | Legacy integrations, complex content | New integrations, high performance |

### Common Operations

Both Cloud and Server implementations support:

- Content management (create, read, update, delete)
- Space management
- User and group management
- Label management
- Attachment handling
- Comment management
- Search functionality
- Page properties
- Export capabilities

### Server-Specific Features

The Server implementation includes additional features:

- Draft content management
- Trash content management
- Reindex operations
- Space permissions
- Space settings

### Cloud v2 API Features

The Cloud v2 API provides:

- Native ADF content support
- Cursor-based pagination for better performance
- Optimized response structures
- Enhanced error handling
- Better support for large datasets

## Getting Started

### For New Projects
1. **Cloud**: Start with v2 API examples for best performance and modern features
2. **Server**: Use the server examples for on-premises installations

### For Existing Projects
1. **Cloud**: Consider migrating from v1 to v2 using the migration example
2. **Server**: Continue using existing patterns, v2 API not available

### Example Learning Path

1. **Start with basics**: `confluence_cloud_content_management.py`
2. **Learn v2 API**: `confluence_v2_api_basics.py`
3. **Master ADF content**: `confluence_adf_content_examples.py`
4. **Handle pagination**: `confluence_cursor_pagination.py`
5. **Implement error handling**: `confluence_error_handling.py`
6. **Plan migration**: `confluence_v1_to_v2_migration.py`
7. **Configure dual API**: `confluence_dual_api_configuration.py`

## Error Handling

All examples include comprehensive error handling patterns. Key areas covered:

- **Authentication errors**: Invalid tokens, expired credentials
- **Authorization errors**: Insufficient permissions
- **Validation errors**: Invalid content structure, missing fields
- **Rate limiting**: API throttling and backoff strategies
- **Network issues**: Connectivity problems, timeouts
- **Content errors**: ADF validation, format conversion

## Rate Limiting

Be aware of API rate limits:
- **Cloud**: Varies by plan, typically 1000 requests per hour
- **Server**: Depends on server configuration
- **Best practices**: Implement exponential backoff, use cursor pagination, cache data

## Security Notes

- Never commit credentials to version control
- Use environment variables or secure credential storage
- API tokens for Cloud are preferred over username/password
- Consider using OAuth 2.0 for production applications
- Validate and sanitize all user input

## Performance Tips

### For v1 API
- Use appropriate `expand` parameters to get needed data in one call
- Implement proper pagination with `start` and `limit`
- Cache frequently accessed data
- Use bulk operations when available

### For v2 API
- Leverage cursor-based pagination for large datasets
- Use ADF format for better performance
- Take advantage of optimized response structures
- Implement proper error handling and retry logic

## Content Format Guide

### Storage Format (v1 API)
```xml
<h1>Heading</h1>
<p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
<ac:structured-macro ac:name="info">
    <ac:rich-text-body>
        <p>This is an info panel.</p>
    </ac:rich-text-body>
</ac:structured-macro>
```

### ADF Format (v2 API)
```json
{
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [{"type": "text", "text": "Heading"}]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "This is a "},
                {"type": "text", "text": "paragraph", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " with "},
                {"type": "text", "text": "formatting", "marks": [{"type": "em"}]},
                {"type": "text", "text": "."}
            ]
        },
        {
            "type": "panel",
            "attrs": {"panelType": "info"},
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "This is an info panel."}]
                }
            ]
        }
    ]
}
```

## Additional Resources

- [Confluence Cloud REST API v1](https://developer.atlassian.com/cloud/confluence/rest/v1/intro/)
- [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Confluence Server REST API](https://developer.atlassian.com/server/confluence/rest/v1002/intro/)
- [ADF (Atlassian Document Format)](https://developer.atlassian.com/cloud/confluence/adf/)
- [CQL (Confluence Query Language)](https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/)
- [Atlassian Python API Documentation](https://atlassian-python-api.readthedocs.io/)

## Contributing

When contributing new examples:

1. Follow the existing naming convention: `confluence_[feature]_[description].py`
2. Include comprehensive docstrings and comments
3. Add error handling and best practices
4. Update this README with example descriptions
5. Test with both small and large datasets
6. Include configuration via environment variables
