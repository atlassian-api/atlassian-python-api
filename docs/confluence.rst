Confluence module
=================

Get page info
-------------

.. code-block:: python

    # Check page exists
    confluence.page_exists(space, title)

    # Provide content by type (page, blog, comment)
    confluence.get_page_child_by_type(page_id, type='page', start=None, limit=None)

    # Provide content id from search result by title and space
    confluence.get_page_id(space, title)

    # Provide space key from content id
    confluence.get_page_space(page_id)

    # Returns the list of labels on a piece of Content
    confluence.get_page_by_title(space, title, start=None, limit=None)

    # Get page by ID
    confluence.get_page_by_id(page_id, expand=None)

    # The list of labels on a piece of Content
    confluence.get_page_labels(page_id, prefix=None, start=None, limit=None)

    # Get draft page by ID
    confluence.get_draft_page_by_id(page_id, status='draft')

    # Get all page by label
    confluence.get_all_pages_by_label(label, start=0, limit=50)

    # Get all pages from Space
    # contet_type can be 'page' or 'blogpost'. Defaults to 'page'
    # expand is a comma separated list of properties to expand on the content.
    # max limit is 100. For more you have to loop over start values.
    confluence.get_all_pages_from_space(space, start=0, limit=100, status=None, expand=None, content_type='page')

    # Get list of pages from trash
    confluence.get_all_pages_from_space_trash(space, start=0, limit=500, status='trashed', content_type='page')

    # Get list of draft pages from space
    # Use case is cleanup old drafts from Confluence
    confluence.get_all_draft_pages_from_space(space, start=0, limit=500, status='draft')

    # Search list of draft pages by space key
    # Use case is cleanup old drafts from Confluence
    confluence.get_all_draft_pages_from_space_through_cql(space, start=0, limit=500, status='draft')

    # Info about all restrictions by operation
    confluence.get_all_restictions_for_content(content_id)

Page actions
------------

.. code-block:: python

    # Create page from scratch
    confluence.create_page(space, title, body, parent_id=None, type='page', representation='storage')

    # Remove page
    confluence.remove_page(page_id, status=None)

    # Remove page from trash
    confluence.remove_page_from_trash(page_id)

    # Remove page as draft
    confluence.remove_page_as_draft(page_id)

    # Update page if already exist
    confluence.update_page(page_id, title, body, parent_id=None, type='page', representation='storage', minor_edit=False)

    # Update page or create page if it is not exists
    confluence.update_or_create(parent_id, title, body, representation='storage')

    # Set the page (content) property e.g. add hash parameters
    confluence.set_page_property(page_id, data)

    # Delete the page (content) property e.g. delete key of hash
    confluence.delete_page_property(page_id, page_property)

    # Get the page (content) property e.g. get key of hash
    confluence.get_page_property(page_id, page_property_key)

    # Get the page (content) properties
    confluence.get_page_properties(page_id)

    # Get page ancestors
    confluence.get_page_ancestors(page_id)

    # Attach (upload) a file to a page, if it exists it will update the
    # automatically version the new file and keep the old one
    confluence.attach_file(filename, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Attach (upload) a content to a page, if it exists it will update the
    # automatically version the new file and keep the old one
    confluence.attach_content(content, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Export page as PDF
    # api_version needs to be set to 'cloud' when exporting from Confluence Cloud. 
    confluence.export_page(page_id)

    # Set a label on the page
    confluence.set_page_label(page_id, label)

    # Delete Confluence page label
    confluence.remove_page_label(page_id, label)
    
Get spaces info
---------------

.. code-block:: python

    # Get all spaces with provided limit
    confluence.get_all_spaces(start=0, limit=500)

    # Get information about a space through space key
    confluence.get_space(space_key, expand='description.plain,homepage')

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

    # Compare content and check is already updated or not
    confluence.is_page_content_is_already_updated(page_id, body)

