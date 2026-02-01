Confluence module
=================

The Confluence module provides both Cloud and Server implementations with dedicated APIs for each platform. The Cloud implementation includes comprehensive support for both Confluence Cloud v1 and v2 APIs with complete backward compatibility, ADF (Atlassian Document Format) content support, and cursor-based pagination.

Implementation Overview
-----------------------

The Confluence implementation follows a structured pattern with dedicated Cloud and Server classes:

.. code-block:: python

    from atlassian.confluence import ConfluenceCloud, ConfluenceServer

    # For Confluence Cloud (with v1/v2 dual API support)
    confluence_cloud = ConfluenceCloud(
        url="https://your-domain.atlassian.net",
        token="your-api-token"
    )

    # For Confluence Server (v1 API)
    confluence_server = ConfluenceServer(
        url="https://your-confluence-server.com",
        username="your-username",
        password="your-password"
    )

.. note::
   For comprehensive ADF (Atlassian Document Format) documentation, see :doc:`confluence_adf`.
   For detailed v2 API migration guidance, see the `Confluence v2 Migration Guide <confluence_v2_migration.html>`_.

Confluence Cloud v2 API Support
-------------------------------

The library provides comprehensive support for Confluence Cloud v2 API with complete backward compatibility. All existing code continues to work unchanged while new v2 features are available on demand.

**Key v2 API Features:**

- **ADF Content Support**: Native Atlassian Document Format for rich content
- **Cursor-Based Pagination**: Efficient handling of large result sets
- **Enhanced Performance**: Better API response times and reliability
- **Modern Cloud Features**: Access to latest Confluence Cloud capabilities

**Backward Compatibility Guarantee:**

All existing method signatures and behaviors are preserved. Your existing code will continue to work exactly as before without any changes required.

v2 API Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlassian.confluence import ConfluenceCloud

    # Option 1: Default behavior (v1 API, fully backward compatible)
    confluence = ConfluenceCloud(
        url="https://your-domain.atlassian.net",
        token="your-api-token"
    )

    # Option 2: Enable v2 API for enhanced features
    confluence = ConfluenceCloud(
        url="https://your-domain.atlassian.net",
        token="your-api-token"
    )
    confluence.enable_v2_api()  # Prefer v2 API when available

    # Option 3: Force v2 API usage
    confluence = ConfluenceCloud(
        url="https://your-domain.atlassian.net",
        token="your-api-token",
        force_v2_api=True
    )

    # Option 4: Enable v2 API after initialization
    confluence.enable_v2_api(force=True)  # Force all operations to use v2 API

Cloud vs Server Differences
---------------------------

| Feature | Cloud | Server |
| Authentication | API Token | Username/Password |
| API Version | v1/v2 dual support | v1.0 |
| API Root | `wiki/api/v1` or `wiki/api/v2` | `rest/api/1.0` |
| Content IDs | UUID strings | Numeric IDs |
| Space IDs | UUID strings | Space keys |
| Content Format | Storage/ADF | Storage |
| Pagination | Offset/Cursor-based | Offset-based |

v2 API Methods (Confluence Cloud)
---------------------------------

The v2 API provides enhanced methods with native ADF support and cursor-based pagination.

Content Management with ADF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create page with ADF content
    adf_content = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Hello, World!"}
                ]
            }
        ]
    }
    
    page = confluence.create_page_with_adf(
        space_id="SPACE123",
        title="My ADF Page",
        adf_content=adf_content,
        parent_id="parent-page-id"  # Optional
    )

    # Update page with ADF content
    updated_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Updated content!"}
                ]
            }
        ]
    }
    
    updated_page = confluence.update_page_with_adf(
        page_id="123456",
        title="Updated Title",
        adf_content=updated_adf,
        version=2  # For optimistic locking
    )

    # Get page with ADF content
    page = confluence.get_page_with_adf(
        page_id="123456",
        expand=['body', 'version', 'space']
    )
    
    # Access ADF content
    adf_body = page['body']['atlas_doc_format']['value']

Cursor-Based Pagination
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Search pages with cursor-based pagination
    results = confluence.search_pages_with_cursor(
        cql="type=page AND space=DEMO",
        limit=50
    )
    
    pages = results['results']
    
    # Get next page using cursor
    if 'next' in results['_links']:
        next_cursor = results['_links']['next']['cursor']
        next_results = confluence.search_pages_with_cursor(
            cql="type=page AND space=DEMO",
            limit=50,
            cursor=next_cursor
        )

    # Iterate through all results
    all_pages = []
    cursor = None
    
    while True:
        results = confluence.search_pages_with_cursor(
            cql="type=page AND space=DEMO",
            limit=100,
            cursor=cursor
        )
        
        all_pages.extend(results['results'])
        
        # Check if there are more results
        if 'next' not in results.get('_links', {}):
            break
        
        cursor = results['_links']['next']['cursor']

ADF Content Creation Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Simple text paragraph
    simple_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Simple paragraph text"}
                ]
            }
        ]
    }

    # Formatted text with marks
    formatted_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Bold text",
                        "marks": [{"type": "strong"}]
                    },
                    {"type": "text", "text": " and "},
                    {
                        "type": "text",
                        "text": "italic text",
                        "marks": [{"type": "em"}]
                    }
                ]
            }
        ]
    }

    # Heading with content
    heading_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [
                    {"type": "text", "text": "Main Heading"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Paragraph under heading"}
                ]
            }
        ]
    }

    # Bullet list
    list_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "First item"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Second item"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Create pages with different ADF structures
    confluence.create_page_with_adf("SPACE123", "Simple Page", simple_adf)
    confluence.create_page_with_adf("SPACE123", "Formatted Page", formatted_adf)
    confluence.create_page_with_adf("SPACE123", "Structured Page", heading_adf)
    confluence.create_page_with_adf("SPACE123", "List Page", list_adf)

ADF Utility Functions
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlassian.adf import (
        create_simple_adf_document,
        convert_text_to_adf,
        validate_adf_document,
        ADFDocument,
        ADFParagraph,
        ADFText,
        ADFHeading
    )

    # Create ADF from plain text
    adf_doc = convert_text_to_adf("Hello, World!")
    
    # Validate ADF structure
    is_valid = validate_adf_document(adf_doc)
    
    # Build ADF using classes
    document = ADFDocument()
    heading = ADFHeading(level=1, content=[ADFText("My Heading")])
    paragraph = ADFParagraph([ADFText("Some content")])
    
    document.add_content(heading)
    document.add_content(paragraph)
    
    adf_dict = document.to_dict()
    
    # Create page with programmatically built ADF
    page = confluence.create_page_with_adf("SPACE123", "Built Page", adf_dict)

Migration from v1 to v2 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # v1 API approach (still works)
    content_data = {
        "type": "page",
        "title": "My Page",
        "space": {"key": "DEMO"},
        "body": {
            "storage": {
                "value": "<p>Hello, World!</p>",
                "representation": "storage"
            }
        }
    }
    page = confluence.create_content(content_data)

    # v2 API approach (enhanced)
    adf_content = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Hello, World!"}]
            }
        ]
    }
    page = confluence.create_page_with_adf("SPACE123", "My Page", adf_content)

    # Gradual migration approach
    confluence.enable_v2_api()  # Enable v2 features
    
    # Existing methods now benefit from v2 performance
    results = confluence.search_content("type=page", limit=100)  # Uses cursor pagination
    
    # New methods provide v2-specific features
    results = confluence.search_pages_with_cursor("type=page", limit=100)

API Version Information
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Check current API configuration
    info = confluence.get_api_version_info()
    print(info)
    # {
    #     'v1_available': True,
    #     'v2_available': True,
    #     'force_v2_api': False,
    #     'prefer_v2_api': False,
    #     'current_default': 'v1'
    # }

    # Enable v2 API and check again
    confluence.enable_v2_api()
    info = confluence.get_api_version_info()
    print(info['current_default'])  # 'v2'

Common Operations
-----------------

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

v2 API Best Practices
---------------------

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Use cursor-based pagination for large result sets
    # Better performance than offset-based pagination
    results = confluence.search_pages_with_cursor(
        cql="type=page AND space=DEMO",
        limit=250  # Maximum allowed
    )

    # Request only needed fields to reduce response size
    page = confluence.get_page_with_adf(
        page_id="123456",
        expand=['body']  # Only get body content
    )

    # Batch operations when possible
    pages_to_create = [
        ("Page 1", adf_content_1),
        ("Page 2", adf_content_2),
        ("Page 3", adf_content_3)
    ]
    
    created_pages = []
    for title, content in pages_to_create:
        page = confluence.create_page_with_adf("SPACE123", title, content)
        created_pages.append(page)

Content Format Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlassian.request_utils import detect_content_format, is_adf_content

    # Detect content format automatically
    content_format = detect_content_format(content)
    
    if content_format == "adf":
        # Content is already in ADF format
        page = confluence.create_page_with_adf("SPACE123", "Title", content)
    elif content_format == "storage":
        # Convert storage format to ADF (basic conversion)
        from atlassian.adf import convert_storage_to_adf
        adf_content = convert_storage_to_adf(content)
        page = confluence.create_page_with_adf("SPACE123", "Title", adf_content)
    else:
        # Treat as plain text
        from atlassian.adf import convert_text_to_adf
        adf_content = convert_text_to_adf(content)
        page = confluence.create_page_with_adf("SPACE123", "Title", adf_content)

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

    try:
        page = confluence.create_page_with_adf("SPACE123", "Title", adf_content)
    except RuntimeError as e:
        if "v2 API client not available" in str(e):
            # Fall back to v1 API
            confluence.disable_v2_api()
            # Use v1 API methods instead
            page = confluence.create_content(v1_content_data)
        else:
            raise

    # Validate ADF content before submission
    from atlassian.adf import validate_adf_document
    
    if not validate_adf_document(adf_content):
        raise ValueError("Invalid ADF content structure")
    
    page = confluence.create_page_with_adf("SPACE123", "Title", adf_content)

Version Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Always use version numbers for updates to prevent conflicts
    page = confluence.get_page_with_adf("123456", expand=['version'])
    current_version = page['version']['number']
    
    # Update with version for optimistic locking
    updated_page = confluence.update_page_with_adf(
        page_id="123456",
        title="Updated Title",
        adf_content=new_content,
        version=current_version + 1
    )

Troubleshooting v2 API
---------------------

This section covers common issues when working with Confluence Cloud v2 API and their solutions.

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. "v2 API client not available" Error**

This error occurs when the v2 API client is not properly initialized or configured.

.. code-block:: python

    # Check if v2 API is properly configured
    info = confluence.get_api_version_info()
    print(f"v2 available: {info['v2_available']}")
    
    if not info['v2_available']:
        # Reinitialize v2 client
        confluence.enable_v2_api()
        
        # Verify it's now available
        info = confluence.get_api_version_info()
        if not info['v2_available']:
            print("v2 API initialization failed - check authentication and URL")

**Solution Steps:**
- Verify your Confluence Cloud URL is correct
- Ensure you're using a valid API token (not password)
- Check that your Confluence instance supports v2 API
- Try reinitializing the client with ``confluence.enable_v2_api()``

**2. Invalid ADF Content Structure**

ADF content must follow a specific structure. Common validation errors include missing required fields or incorrect node types.

.. code-block:: python

    from atlassian.adf import validate_adf_document
    
    # Always validate ADF before submission
    adf_content = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Hello, World!"}]
            }
        ]
    }
    
    if not validate_adf_document(adf_content):
        print("Invalid ADF structure")
        # Common fixes:
        # - Ensure version is 1
        # - Ensure type is "doc"
        # - Ensure content is a list
        # - Check all node types are valid
        
        # Fix common issues automatically
        fixed_adf = {
            "version": 1,
            "type": "doc",
            "content": adf_content.get("content", [])
        }

**Common ADF Structure Issues:**
- Missing ``version`` field (must be 1)
- Missing ``type`` field (must be "doc")
- ``content`` is not a list
- Invalid node types in content
- Missing required attributes (e.g., ``level`` for headings)

**3. Cursor Pagination Issues**

Cursor-based pagination can fail if cursors are malformed or expired.

.. code-block:: python

    def get_all_pages_safe(confluence, cql, limit=100):
        """Safely retrieve all pages with cursor pagination."""
        all_results = []
        cursor = None
        max_iterations = 1000  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            try:
                results = confluence.search_pages_with_cursor(
                    cql=cql,
                    limit=limit,
                    cursor=cursor
                )
                
                # Extract results
                page_results = results.get('results', [])
                if not page_results:
                    break
                    
                all_results.extend(page_results)
                
                # Check for next page
                next_link = results.get('_links', {}).get('next')
                if not next_link:
                    break
                    
                cursor = next_link.get('cursor')
                if not cursor:
                    break
                    
                iteration += 1
                
            except Exception as e:
                print(f"Error during pagination at iteration {iteration}: {e}")
                # Log the cursor that failed
                print(f"Failed cursor: {cursor}")
                break
        
        return all_results

**Cursor Pagination Best Practices:**
- Always check for the existence of ``_links.next`` before continuing
- Validate cursor values before using them
- Implement maximum iteration limits to prevent infinite loops
- Handle network errors gracefully
- Log failed cursors for debugging

**4. Content Format Conversion Issues**

Converting between different content formats (storage, ADF, wiki) can cause issues.

.. code-block:: python

    from atlassian.request_utils import detect_content_format
    from atlassian.adf import convert_text_to_adf, validate_adf_document
    
    def safe_create_page(confluence, space_id, title, content):
        """Safely create a page handling different content formats."""
        try:
            # Detect content format
            content_format = detect_content_format(content)
            
            if content_format == "adf":
                # Validate ADF content
                if validate_adf_document(content):
                    return confluence.create_page_with_adf(space_id, title, content)
                else:
                    raise ValueError("Invalid ADF content structure")
            
            elif content_format == "storage":
                # Convert storage to ADF (basic conversion)
                try:
                    from atlassian.adf import convert_storage_to_adf
                    adf_content = convert_storage_to_adf(content)
                    return confluence.create_page_with_adf(space_id, title, adf_content)
                except Exception:
                    # Fall back to v1 API
                    return confluence.create_content({
                        "type": "page",
                        "title": title,
                        "space": {"id": space_id},
                        "body": {
                            "storage": {
                                "value": content,
                                "representation": "storage"
                            }
                        }
                    })
            
            else:
                # Treat as plain text
                adf_content = convert_text_to_adf(str(content))
                return confluence.create_page_with_adf(space_id, title, adf_content)
                
        except Exception as e:
            print(f"Failed to create page: {e}")
            # Last resort: use v1 API with basic content
            try:
                return confluence.create_content({
                    "type": "page",
                    "title": title,
                    "space": {"id": space_id},
                    "body": {
                        "storage": {
                            "value": f"<p>{str(content)}</p>",
                            "representation": "storage"
                        }
                    }
                })
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                raise

**5. Authentication and Permission Issues**

v2 API requires proper authentication and permissions.

.. code-block:: python

    def test_v2_api_access(confluence):
        """Test v2 API access and permissions."""
        try:
            # Test basic v2 API access
            info = confluence.get_api_version_info()
            print(f"API Info: {info}")
            
            if not info['v2_available']:
                print("v2 API not available - check authentication")
                return False
            
            # Test actual v2 API call
            try:
                # Try a simple v2 API operation
                results = confluence.search_pages_with_cursor(
                    cql="type=page",
                    limit=1
                )
                print("v2 API access successful")
                return True
                
            except Exception as api_error:
                print(f"v2 API call failed: {api_error}")
                # Check if it's a permission issue
                if "403" in str(api_error) or "Forbidden" in str(api_error):
                    print("Permission denied - check API token permissions")
                elif "401" in str(api_error) or "Unauthorized" in str(api_error):
                    print("Authentication failed - check API token validity")
                return False
                
        except Exception as e:
            print(f"Failed to test v2 API access: {e}")
            return False

**6. Space ID vs Space Key Confusion**

v2 API uses Space IDs (UUIDs) while v1 API uses Space Keys (strings).

.. code-block:: python

    def get_space_info(confluence, space_identifier):
        """Get space information handling both ID and key formats."""
        try:
            # Try as space key first (v1 API)
            if isinstance(space_identifier, str) and not space_identifier.startswith('~'):
                # Looks like a space key
                space = confluence.get_space(space_identifier)
                return {
                    'id': space.get('id'),
                    'key': space.get('key'),
                    'name': space.get('name'),
                    'type': space.get('type')
                }
            else:
                # Assume it's a space ID
                # v2 API call to get space by ID
                # (Implementation depends on available v2 methods)
                return {'id': space_identifier}
                
        except Exception as e:
            print(f"Failed to get space info for '{space_identifier}': {e}")
            return None

    # Usage example
    space_info = get_space_info(confluence, "DEMO")  # Space key
    if space_info:
        space_id = space_info['id']
        # Use space_id for v2 API calls
        page = confluence.create_page_with_adf(space_id, "Title", adf_content)

Debug Mode and Logging
~~~~~~~~~~~~~~~~~~~~~

Enable detailed logging to troubleshoot v2 API issues:

.. code-block:: python

    import logging
    
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('atlassian')
    logger.setLevel(logging.DEBUG)
    
    # This will show detailed API calls and responses
    confluence.enable_v2_api()
    page = confluence.get_content("123456")
    
    # You'll see output like:
    # DEBUG:atlassian:Using v2 API for get_content
    # DEBUG:atlassian:GET https://domain.atlassian.net/wiki/api/v2/pages/123456

**Custom Debug Helper:**

.. code-block:: python

    def debug_api_call(confluence, operation_name, *args, **kwargs):
        """Debug wrapper for API calls."""
        print(f"=== DEBUG: {operation_name} ===")
        
        # Show API version info
        info = confluence.get_api_version_info()
        print(f"API Config: {info}")
        
        # Show arguments
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
        
        try:
            # Execute the operation
            method = getattr(confluence, operation_name)
            result = method(*args, **kwargs)
            print(f"Success: {type(result)}")
            return result
        except Exception as e:
            print(f"Error: {e}")
            print(f"Error type: {type(e)}")
            raise

    # Usage
    page = debug_api_call(confluence, 'get_content', '123456')

Migration Warnings and Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The library provides helpful warnings when v2 API would provide better performance:

.. code-block:: python

    import warnings
    
    # Capture migration warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This will issue a warning for large pagination requests
        results = confluence.search_content("type=page", limit=200, start=1000)
        
        if w:
            for warning in w:
                print(f"Warning: {warning.message}")
                print(f"Category: {warning.category}")
                # Example output:
                # Warning: search_content() will continue to work but consider using 
                # search_pages_with_cursor() for cursor-based pagination and better 
                # performance with large result sets.
    
    # Disable warnings by enabling v2 API
    confluence.enable_v2_api()  # No more warnings

**Handling Backward Compatibility:**

.. code-block:: python

    def get_page_content_compatible(confluence, page_id):
        """Get page content with backward compatibility."""
        info = confluence.get_api_version_info()
        
        if info['current_default'] == 'v2' or info['prefer_v2_api']:
            # Use v2 API
            try:
                page = confluence.get_page_with_adf(page_id, expand=['body'])
                return {
                    'format': 'adf',
                    'content': page['body']['atlas_doc_format']['value']
                }
            except Exception:
                # Fall back to v1
                pass
        
        # Use v1 API
        page = confluence.get_content(page_id, expand='body.storage')
        return {
            'format': 'storage',
            'content': page['body']['storage']['value']
        }

Performance Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Slow Pagination Performance**

.. code-block:: python

    # Slow: Large offset-based pagination
    results = confluence.search_content("type=page", limit=50, start=5000)
    
    # Fast: Cursor-based pagination
    confluence.enable_v2_api()
    results = confluence.search_pages_with_cursor("type=page", limit=50)

**2. Large Content Handling**

.. code-block:: python

    # For large ADF documents, validate structure first
    def create_large_page_safely(confluence, space_id, title, adf_content):
        """Create large pages with validation and chunking if needed."""
        
        # Validate ADF structure
        if not validate_adf_document(adf_content):
            raise ValueError("Invalid ADF structure")
        
        # Check content size (rough estimate)
        import json
        content_size = len(json.dumps(adf_content))
        
        if content_size > 1024 * 1024:  # 1MB
            print(f"Warning: Large content size ({content_size} bytes)")
            # Consider splitting into multiple pages
        
        try:
            return confluence.create_page_with_adf(space_id, title, adf_content)
        except Exception as e:
            if "too large" in str(e).lower():
                print("Content too large - consider splitting into multiple pages")
            raise

Error Code Reference
~~~~~~~~~~~~~~~~~~~

Common HTTP error codes and their meanings in v2 API context:

**400 Bad Request**
- Invalid ADF content structure
- Missing required parameters
- Malformed cursor tokens

**401 Unauthorized**
- Invalid API token
- Expired authentication
- Missing authentication headers

**403 Forbidden**
- Insufficient permissions for the operation
- Space access denied
- API token lacks required scopes

**404 Not Found**
- Page, space, or resource doesn't exist
- Invalid page/space ID format
- Resource has been deleted

**409 Conflict**
- Page title already exists in space
- Version conflict (optimistic locking)
- Concurrent modification detected

**413 Payload Too Large**
- ADF content exceeds size limits
- Attachment too large
- Request body too large

**429 Too Many Requests**
- Rate limiting exceeded
- Too many concurrent requests
- API quota exceeded

**500 Internal Server Error**
- Confluence server error
- ADF processing error
- Temporary service unavailability

Getting Additional Help
~~~~~~~~~~~~~~~~~~~~~~

If you encounter issues not covered in this troubleshooting guide:

1. **Enable Debug Logging**: Use the debug logging examples above to get detailed information
2. **Check API Version Info**: Use ``get_api_version_info()`` to verify your configuration
3. **Validate ADF Content**: Use ``validate_adf_document()`` for content issues
4. **Test with Simple Examples**: Start with basic operations before complex ones
5. **Check Official Documentation**: Refer to Confluence Cloud REST API v2 documentation
6. **Community Support**: Use the project's Discord chat or GitHub issues

**Useful Debug Commands:**

.. code-block:: python

    # Quick diagnostic
    def diagnose_confluence_setup(confluence):
        """Run basic diagnostics on Confluence setup."""
        print("=== Confluence Setup Diagnostics ===")
        
        # API version info
        info = confluence.get_api_version_info()
        print(f"API Version Info: {info}")
        
        # Test basic connectivity
        try:
            spaces = confluence.get_all_spaces(limit=1)
            print(f"Basic connectivity: OK (found {len(spaces)} spaces)")
        except Exception as e:
            print(f"Basic connectivity: FAILED - {e}")
        
        # Test v2 API if available
        if info.get('v2_available'):
            try:
                results = confluence.search_pages_with_cursor("type=page", limit=1)
                print("v2 API access: OK")
            except Exception as e:
                print(f"v2 API access: FAILED - {e}")
        else:
            print("v2 API: Not available")
        
        print("=== End Diagnostics ===")

    # Run diagnostics
    diagnose_confluence_setup(confluence)

Server-Specific Features
------------------------

The Server implementation includes additional features:

- Draft content management
- Trash content management
- Reindex operations
- Space permissions
- Space settings

Legacy Implementation
---------------------

The original Confluence implementation is still available
for backward compatibility.

Get page info
-------------

.. code-block:: python

    # Check page exists
    # type of the page, 'page' or 'blogpost'. Defaults to 'page'
    confluence.page_exists(space, title, type=None)

    # Provide content by type (page, blog, comment)
    confluence.get_page_child_by_type(page_id, type='page', start=None, limit=None, expand=None)

    # Provide content id from search result by title and space
    confluence.get_page_id(space, title)

    # Provide space key from content id
    confluence.get_page_space(page_id)

    # Returns the list of labels on a piece of Content
    confluence.get_page_by_title(space, title, start=None, limit=None)

    # Get page by ID
    # Example request URI(s):
    #    http://example.com/confluence/rest/api/content/1234?expand=space,body.view,version,container
    #    http://example.com/confluence/rest/api/content/1234?status=any
    #    page_id: Content ID
    #    status: (str) list of Content statuses to filter results on. Default value: [current]
    #    version: (int)
    #    expand: OPTIONAL: A comma separated list of properties to expand on the content.
    #                   Default value: history,space,version
    #                   We can also specify some extensions such as extensions.inlineProperties
    #                   (for getting inline comment-specific properties) or extensions.resolution
    #                   for the resolution status of each comment in the results
    confluence.get_page_by_id(page_id, expand=None, status=None, version=None)

    # The list of labels on a piece of Content
    confluence.get_page_labels(page_id, prefix=None, start=None, limit=None)

    # Get draft page by ID
    confluence.get_draft_page_by_id(page_id, status='draft')

    # Get all page by label
    confluence.get_all_pages_by_label(label, start=0, limit=50, expand=None)

    # Get all pages from Space
    # content_type can be 'page' or 'blogpost'. Defaults to 'page'
    # expand is a comma separated list of properties to expand on the content.
    # max limit is 100. For more you have to loop over start values.
    confluence.get_all_pages_from_space(space, start=0, limit=100, status=None, expand=None, content_type='page')

    # Get all pages from space as Generator
    confluence.get_all_pages_from_space_as_generator(space, start=0, limit=100, status=None, expand=None, content_type='page')

    # Get list of pages from trash
    confluence.get_all_pages_from_space_trash(space, start=0, limit=500, status='trashed', content_type='page')

    # Get list of draft pages from space
    # Use case is cleanup old drafts from Confluence
    confluence.get_all_draft_pages_from_space(space, start=0, limit=500, status='draft')

    # Search list of draft pages by space key
    # Use case is cleanup old drafts from Confluence
    confluence.get_all_draft_pages_from_space_through_cql(space, start=0, limit=500, status='draft')

    # Info about all restrictions by operation
    confluence.get_all_restrictions_for_content(content_id)

Page actions
------------

.. code-block:: python

    # Create page from scratch
    confluence.create_page(space, title, body, parent_id=None, type='page', representation='storage', editor='v2', full_width=False)

    # This method removes a page, if it has recursive flag, method removes including child pages
    confluence.remove_page(page_id, status=None, recursive=False)

    # Remove any content
    confluence.remove_content(content_id):

    # Remove page from trash
    confluence.remove_page_from_trash(page_id)

    # Remove page as draft
    confluence.remove_page_as_draft(page_id)

    # Update page if already exist
    confluence.update_page(page_id, title, body, parent_id=None, type='page', representation='storage', minor_edit=False, full_width=False)

    # Update page or create page if it is not exists
    confluence.update_or_create(parent_id, title, body, representation='storage', full_width=False)

    # Append body to page if already exist
    confluence.append_page(page_id, title, append_body, parent_id=None, type='page', representation='storage', minor_edit=False)

    # Set the page (content) property e.g. add hash parameters
    confluence.set_page_property(page_id, data)

    # Delete the page (content) property e.g. delete key of hash
    confluence.delete_page_property(page_id, page_property)

    # Move page
    confluence.move_page(space_key, page_id, target_title, position="append")

    # Get the page (content) property e.g. get key of hash
    confluence.get_page_property(page_id, page_property_key)

    # Get the page (content) properties
    confluence.get_page_properties(page_id)

    # Get page ancestors
    confluence.get_page_ancestors(page_id)

    # Attach (upload) a file to a page, if it exists it will update the
    # automatically version the new file and keep the old one
    # content_type is default to "application/binary"
    confluence.attach_file(filename, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Attach (upload) a content to a page, if it exists it will update the
    # automatically version the new file and keep the old one
    # content_type is default to "application/binary"
    confluence.attach_content(content, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Download attachments from a page to local system. If path is None, current working directory will be used.
    confluence.download_attachments_from_page(page_id, path=None)

    # Remove completely a file if version is None or delete version
    confluence.delete_attachment(page_id, filename, version=None)

    # Remove completely a file if version is None or delete version
    confluence.delete_attachment_by_id(attachment_id, version)

    # Keep last versions
    confluence.remove_page_attachment_keep_version(page_id, filename, keep_last_versions)

    # Get attachment history
    confluence.get_attachment_history(attachment_id, limit=200, start=0)

    # Get attachment for content
    confluence.get_attachments_from_content(page_id, start=0, limit=50, expand=None, filename=None, media_type=None)

    # Check has unknown attachment error on page
    confluence.has_unknown_attachment_error(page_id)

    # Export page as PDF
    # api_version needs to be set to 'cloud' when exporting from Confluence Cloud
    .
    confluence.export_page(page_id)

    # Set a label on the page
    confluence.set_page_label(page_id, label)

    # Delete Confluence page label
    confluence.remove_page_label(page_id, label)

    # Add comment into page
    confluence.add_comment(page_id, text)

     # Fetch tables from Confluence page
    confluence.get_tables_from_page(page_id)

    # Get regex matches from Confluence page
    confluence.scrap_regex_from_page(page_id, regex)

Confluence Whiteboards
----------------------

.. code-block:: python

    # Create  new whiteboard  - cloud only
    confluence.create_whiteboard(spaceId, title=None, parentId=None)

    # Delete existing whiteboard - cloud only
    confluence.delete_whiteboard(whiteboard_id)

    # Get whiteboard by id  - cloud only!
    confluence.get_whiteboard(whiteboard_id)


Template actions
----------------

.. code-block:: python

    # Updating a content template
    template_id = "<string>"
    name = "<string>"
    body = {"value": "<string>", "representation": "view"}
    template_type = "page"
    description = "<string>"
    labels = [{"prefix": "<string>", "name": "<string>", "id": "<string>", "label": "<string>"}]
    space = "<key_string>"

    confluence.create_or_update_template(name, body, template_type, template_id, description, labels, space)

    # Creating a new content template
    name = "<string>"
    body = {"value": "<string>", "representation": "view"}
    template_type = "page"
    description = "<string>"
    labels = [{"prefix": "<string>", "name": "<string>", "id": "<string>", "label": "<string>"}]
    space = "<key_string>"

    confluence.create_or_update_template(name, body, template_type, description=description, labels=labels, space=space)

    # Get a template by its ID
    confluence.get_content_template(template_id)

    # Get all global content templates
    confluence.get_content_templates()

    # Get content templates in a space
    confluence.get_content_templates(space)

    # Get all global blueprint templates
    confluence.get_blueprint_templates()

    # Get all blueprint templates in a space
    confluence.get_blueprint_templates(space)

    # Removing a template
    confluence.remove_template(template_id)

Get spaces info
---------------

.. code-block:: python

    # Get all spaces with provided limit
    # additional info, e.g. metadata, icon, description, homepage
    confluence.get_all_spaces(start=0, limit=500, expand=None)

    # Get information about a space through space key
    confluence.get_space(space_key, expand='description.plain,homepage')

    # Get space content (configuring by the expand property)
    confluence.get_space_content(space_key, depth="all", start=0, limit=500, content_type=None, expand="body.storage")

    # Get Space permissions set based on json-rpc call
    confluence.get_space_permissions(space_key)

    # Get Space export download url
    confluence.get_space_export(space_key, export_type)

Space
-----

.. code-block:: python

    # Archive the given Space identified by spaceKey.
    # This method is idempotent i.e.,
    # if the Space is already archived then no action will be taken.
    confluence.archive_space(space_key)

    # Get trash contents of space
    confluence.get_trashed_contents_by_space(space_key, cursor=None, expand=None, limit=100)

    # Remove all trash contents of space
    confluence.remove_trashed_contents_by_space(space_key)





Get space permissions
---------------------

.. code-block:: python

    # Returns list of permissions granted to users and groups in the particular space.
    confluence.get_all_space_permissions(space_key)

    # Sets permissions to multiple users/groups in the given space.
    confluence.set_permissions_to_multiple_items_for_space(self, space_key, user_key=None, group_name=None, operations=None)

    # Get permissions granted to anonymous user for the given space
    confluence.get_permissions_granted_to_anonymous_for_space(space_key)

    # Grant permissions to anonymous user in the given space.
    # Operation doesn't override existing permissions
    # will only add those one that weren't granted before.
    # Multiple permissions could be passed in one request.
    # Supported targetType and operationKey pairs:
    #    space read
    #    space administer
    #    space export
    #    space restrict
    #    space delete_own
    #    space delete_mail
    #    page create
    #    page delete
    #    blogpost create
    #    blogpost delete
    #    comment create
    #    comment delete
    #    attachment create
    #    attachment delete
    confluence.set_permissions_to_anonymous_for_space(space_key, operations=None)

    # Remove permissions granted to anonymous user for the given space
    confluence.remove_permissions_granted_to_anonymous_for_space(space_key)

    # Get permissions granted to group for the given space
    confluence.get_permissions_granted_to_group_for_space(space_key, user_key)

    # Grant permissions to group in the given space.
    # Operation doesn't override existing permissions
    # will only add those one that weren't granted before.
    # Multiple permissions could be passed in one request.
    # Supported targetType and operationKey pairs:
    #    space read
    #    space administer
    #    space export
    #    space restrict
    #    space delete_own
    #    space delete_mail
    #    page create
    #    page delete
    #    blogpost create
    #    blogpost delete
    #    comment create
    #    comment delete
    #    attachment create
    #    attachment delete
    confluence.set_permissions_to_group_for_space(space_key, user_key, operations=None)

    # Remove permissions granted to group for the given space
    confluence.remove_permissions_from_group_for_space(space_key, group_name)

    # Get permissions granted to user for the given space
    confluence.get_permissions_granted_to_user_for_space(space_key, user_key)

    # Grant permissions to user in the given space.
    confluence.set_permissions_to_user_for_space(space_key, user_key, operations=None)

    # Remove permissions granted to user for the given space
    confluence.remove_permissions_from_user_for_space(space_key, user_key)

    # Add permissions to a space
    confluence.add_space_permissions(space_key, user_key, group_name, operations)

    # Remove permissions from a space
    confluence.remove_space_permissions(space_key, user_key, group_name, permission)

Users and Groups
----------------

.. code-block:: python

    # Get all groups from Confluence User management
    confluence.get_all_groups(start=0, limit=1000)

    # Get a paginated collection of users in the given group
    confluence.get_group_members(group_name='confluence-users', start=0, limit=1000)

    # Get information about a user through username
    confluence.get_user_details_by_username(username, expand=None)

    # Get information about a user through user key
    confluence.get_user_details_by_userkey(userkey, expand=None)

    # Change a user's password
    confluence.change_user_password(username, password)

    # Change calling user's password
    confluence.change_my_password(oldpass, newpass)

    # Add given user to a group
    confluence.add_user_to_group(username, group_name)

    # Remove given user from a group
    confluence.remove_user_from_group(username, group_name)

CQL
---

.. code-block:: python

    # Get results from cql search result with all related fields
    confluence.cql(cql, start=0, limit=None, expand=None, include_archived_spaces=None, excerpt=None)

Other actions
-------------

.. code-block:: python

    # Clean all caches from cache management
    confluence.clean_all_caches()

    # Clean caches from cache management
    # e.g.
    # com.gliffy.cache.gon
    # org.hibernate.cache.internal.StandardQueryCache_v5
    confluence.clean_package_cache(cache_name='com.gliffy.cache.gon')

    # Convert to Confluence XHTML format from wiki style
    confluence.convert_wiki_to_storage(wiki)

    # Get page history
    confluence.history(page_id)

    # Get content history by version number
    confluence.get_content_history_by_version_number(content_id, version_number)

    # Remove content history. It works as experimental method
    confluence.remove_content_history(page_id, version_number)

    # Compare content and check is already updated or not
    confluence.is_page_content_is_already_updated(page_id, body)

    # Add inline task setting checkbox method
    confluence.set_inline_tasks_checkbox(page_id, task_id, status)

