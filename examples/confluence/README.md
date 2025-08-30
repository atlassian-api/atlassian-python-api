# Confluence Examples

This directory contains examples demonstrating how to use the new Confluence API client with both Cloud and Server implementations.

## Structure

```
examples/confluence/
├── README.md
├── cloud/
│   └── confluence_cloud_content_management.py
└── server/
    └── confluence_server_content_management.py
```

## Examples

### Confluence Cloud

The `confluence_cloud_content_management.py` example demonstrates:

- Initializing the Confluence Cloud client
- Getting spaces and space content
- Retrieving pages and page details
- Working with page children, labels, comments, and attachments
- Searching for content
- Getting user information

**Prerequisites:**
- Confluence Cloud instance
- API token (not username/password)

**Usage:**
```bash
cd examples/confluence/cloud
python confluence_cloud_content_management.py
```

**Configuration:**
Update the following in the script:
- `url`: Your Confluence Cloud domain (e.g., `https://your-domain.atlassian.net`)
- `token`: Your API token

### Confluence Server

The `confluence_server_content_management.py` example demonstrates:

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
| API Version | v2 | v1.0 |
| API Root | `wiki/api/v2` | `rest/api/1.0` |
| Pagination | `_links.next.href` | `_links.next.href` |
| Content IDs | UUID strings | Numeric IDs |
| Space IDs | UUID strings | Space keys |

### Common Operations

Both implementations support:

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

## Error Handling

All examples include basic error handling. In production applications, you should implement more robust error handling based on your specific requirements.

## Rate Limiting

Be aware of API rate limits:
- **Cloud**: Varies by plan, typically 1000 requests per hour
- **Server**: Depends on server configuration

## Security Notes

- Never commit credentials to version control
- Use environment variables or secure credential storage
- API tokens for Cloud are preferred over username/password
- Consider using OAuth 2.0 for production applications

## Additional Resources

- [Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Confluence Server REST API](https://developer.atlassian.com/server/confluence/rest/v1002/intro/)
- [CQL (Confluence Query Language)](https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/)
