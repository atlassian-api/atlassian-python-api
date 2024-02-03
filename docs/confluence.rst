Confluence module
=================

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
    confluence.get_all_pages_by_label(label, start=0, limit=50)

    # Get all pages from Space
    # content_type can be 'page' or 'blogpost'. Defaults to 'page'
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
    confluence.attach_file(filename, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Attach (upload) a content to a page, if it exists it will update the
    # automatically version the new file and keep the old one
    confluence.attach_content(content, name=None, content_type=None, page_id=None, title=None, space=None, comment=None)

    # Download attachments from a page to local system. If download_path is None, current working directory will be used.
    confluence.download_attachments_from_page(page_id, download_path=None)

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
    confluence.get_page_tables(page_id)

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

