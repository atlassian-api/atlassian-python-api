Confluence Cloud v2 API Migration Guide
========================================

This guide explains how to migrate from Confluence Cloud v1 API to v2 API while maintaining backward compatibility.

Overview
--------

The atlassian-python-api library now supports both Confluence Cloud v1 and v2 APIs with complete backward compatibility. All existing code will continue to work unchanged, while new features are available through v2 API support.

Backward Compatibility Guarantee
--------------------------------

**All existing method signatures and behaviors are preserved.** Your existing code will continue to work exactly as before without any changes required.

What's Preserved
~~~~~~~~~~~~~~~

- All method signatures remain unchanged
- All parameter names and types remain the same
- All return value formats remain consistent
- All error handling behavior remains the same
- Default behavior uses v1 API (no breaking changes)

Migration Options
-----------------

Option 1: No Changes Required (Recommended for Most Users)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your existing code continues to work unchanged:

.. code-block:: python

    from atlassian import ConfluenceCloud

    # This continues to work exactly as before
    confluence = ConfluenceCloud(url="https://your-domain.atlassian.net", token="your-token")

    # All existing methods work unchanged
    page = confluence.get_content("123456")
    spaces = confluence.get_spaces()
    results = confluence.search_content("type=page AND space=DEMO")

Option 2: Enable v2 API for Enhanced Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enable v2 API support for new features while maintaining compatibility:

.. code-block:: python

    from atlassian import ConfluenceCloud

    # Enable v2 API support
    confluence = ConfluenceCloud(url="https://your-domain.atlassian.net", token="your-token")
    confluence.enable_v2_api()  # Prefer v2 API when available

    # Existing methods now use v2 API when beneficial
    results = confluence.search_content("type=page", limit=100)  # Uses cursor pagination

Option 3: Force v2 API Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Force all operations to use v2 API:

.. code-block:: python

    from atlassian import ConfluenceCloud

    # Force v2 API usage
    confluence = ConfluenceCloud(
        url="https://your-domain.atlassian.net", 
        token="your-token",
        force_v2_api=True
    )

    # Or enable after initialization
    confluence.enable_v2_api(force=True)

Option 4: Use v2-Specific Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use new v2-specific methods for enhanced functionality:

.. code-block:: python

    from atlassian import ConfluenceCloud

    confluence = ConfluenceCloud(url="https://your-domain.atlassian.net", token="your-token")

    # Create page with native ADF content
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

    page = confluence.create_page_with_adf("SPACE123", "My Page", adf_content)

    # Search with cursor-based pagination
    results = confluence.search_pages_with_cursor("type=page AND space=DEMO", limit=50)

Key Benefits of v2 API
----------------------

1. Cursor-Based Pagination
~~~~~~~~~~~~~~~~~~~~~~~~~

v2 API provides cursor-based pagination for better performance with large result sets:

.. code-block:: python

    # v1 API (offset-based, slower for large datasets)
    results = confluence.search_content("type=page", limit=50, start=1000)

    # v2 API (cursor-based, faster and more reliable)
    results = confluence.search_pages_with_cursor("type=page", limit=50, cursor="cursor_token")

2. Native ADF Support
~~~~~~~~~~~~~~~~~~~~

v2 API supports Atlassian Document Format (ADF) natively:

.. code-block:: python

    # v1 API (storage format)
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

    # v2 API (native ADF)
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

3. Enhanced Performance
~~~~~~~~~~~~~~~~~~~~~~

v2 API provides better performance for:

- Large search result sets
- Bulk operations
- Content with rich formatting

Migration Warnings
------------------

The library provides helpful warnings when v2 API would provide better performance:

.. code-block:: python

    # This will issue a warning for large pagination requests
    results = confluence.search_content("type=page", limit=200, start=1000)
    # Warning: search_content() will continue to work but consider using 
    # search_pages_with_cursor() for cursor-based pagination and better 
    # performance with large result sets.

To disable warnings, enable v2 API support:

.. code-block:: python

    confluence.enable_v2_api()  # No more warnings

API Version Information
----------------------

Check your current API configuration:

.. code-block:: python

    info = confluence.get_api_version_info()
    print(info)
    # {
    #     'v1_available': True,
    #     'v2_available': True,
    #     'force_v2_api': False,
    #     'prefer_v2_api': False,
    #     'current_default': 'v1'
    # }

Method Mapping
--------------

Content Management
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - v1 Method
     - v2 Equivalent
     - Notes
   * - ``get_content()``
     - ``get_page_with_adf()``
     - v2 returns ADF content
   * - ``create_content()``
     - ``create_page_with_adf()``
     - v2 accepts ADF content
   * - ``update_content()``
     - ``update_page_with_adf()``
     - v2 accepts ADF content
   * - ``search_content()``
     - ``search_pages_with_cursor()``
     - v2 uses cursor pagination

Pagination
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - v1 Approach
     - v2 Approach
     - Benefits
   * - ``limit=50, start=100``
     - ``limit=50, cursor="token"``
     - Better performance, no offset limits
   * - Offset-based
     - Cursor-based
     - Consistent results, handles large datasets

Best Practices
--------------

1. Gradual Migration
~~~~~~~~~~~~~~~~~~~

Start by enabling v2 API support without changing your code:

.. code-block:: python

    # Step 1: Enable v2 API
    confluence.enable_v2_api()

    # Step 2: Your existing code benefits from v2 performance
    # (no code changes required)

    # Step 3: Gradually adopt v2-specific methods for new features

2. Use v2 for New Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For new applications, consider using v2-specific methods:

.. code-block:: python

    # New development - use v2 methods directly
    page = confluence.create_page_with_adf(space_id, title, adf_content)
    results = confluence.search_pages_with_cursor(cql, limit=50)

3. Handle Both Formats
~~~~~~~~~~~~~~~~~~~~~

If you need to support both v1 and v2 responses:

.. code-block:: python

    def get_page_content(confluence, page_id):
        """Get page content, handling both v1 and v2 formats."""
        if confluence.get_api_version_info()['current_default'] == 'v2':
            page = confluence.get_page_with_adf(page_id, expand=['body'])
            return page['body']['atlas_doc_format']['value']
        else:
            page = confluence.get_content(page_id, expand='body.storage')
            return page['body']['storage']['value']

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. **"v2 API client not available" Error**
   
   - Ensure you have proper authentication configured
   - Check that your Confluence Cloud instance supports v2 API

2. **Different Response Formats**
   
   - v2 API returns different data structures
   - Use v2-specific methods for consistent v2 format
   - Use existing methods for v1 format compatibility

3. **Pagination Differences**
   
   - v1 uses ``start`` and ``limit`` parameters
   - v2 uses ``cursor`` and ``limit`` parameters
   - Use appropriate method for your pagination needs

Getting Help
~~~~~~~~~~~

- Check the API version info: ``confluence.get_api_version_info()``
- Enable debug logging to see which API version is being used
- Refer to official Confluence Cloud REST API v2 documentation
- See the :doc:`confluence` troubleshooting section for detailed solutions

Summary
-------

The dual API support provides:

- **Complete backward compatibility** - existing code works unchanged
- **Optional v2 features** - enable when you need enhanced functionality
- **Gradual migration path** - migrate at your own pace
- **Performance benefits** - better pagination and content handling
- **Future-proofing** - ready for v2 API adoption

Choose the migration approach that best fits your needs, from no changes required to full v2 API adoption.