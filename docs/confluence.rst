Confluence module
=================

The Confluence module now provides both Cloud and Server implementations
with dedicated APIs for each platform.

New Implementation
------------------

The new Confluence implementation follows the same pattern as other modules
with dedicated Cloud and Server classes:

.. code-block:: python

    from atlassian.confluence import ConfluenceCloud, ConfluenceServer

    # For Confluence Cloud
    confluence_cloud = ConfluenceCloud(
        url="https://your-domain.atlassian.net",
        token="your-api-token"
    )

    # For Confluence Server
    confluence_server = ConfluenceServer(
        url="https://your-confluence-server.com",
        username="your-username",
        password="your-password"
    )

Cloud vs Server Differences
---------------------------

| Feature | Cloud | Server |
| Authentication | API Token | Username/Password |
| API Version | v2 | v1.0 |
| API Root | `wiki/api/v2` | `rest/api/1.0` |
| Content IDs | UUID strings | Numeric IDs |
| Space IDs | UUID strings | Space keys |

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
    # Cloud uses V2 space/page lookups; Server/Data Center keeps its REST API.
    confluence.page_exists(space, title, type=None)

    # Resolve direct, display, and shared short page URLs to a page ID.
    page_id = confluence.get_page_id_by_url("https://confluence.example.com/x/-_Z3")

    # For Server/Data Center, use this paginated helper for all group members.
    members = confluence.get_all_members("confluence-users")

    # Returns only space names and follows the space-directory pagination.
    space_names = confluence.get_space_names()

    # Provide content by type (page, blog, comment)
    confluence.get_page_child_by_type(page_id, type='page', start=None, limit=None, expand=None)

    # Get child information without listing or paginating every child.
    child_count = confluence.get_page_child_count(page_id)
    has_children = confluence.page_has_children(page_id)

    # Stream all CQL matches without accumulating them in memory.
    for result in confluence.iter_cql('type=page', limit=250):
        process(result)

    # Use this only when a complete in-memory list is required.
    all_results = confluence.cql_all('type=page', limit=250)

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
    # Server/Data Center: ``space`` is the space KEY, not its display name.
    # Personal-space keys commonly look like ``~<account-id>``.
    confluence.create_page(space, title, body, parent_id=None, type='page', representation='storage', editor='v2', full_width=False)

    # Check that the supplied credentials are accepted. This does not by itself
    # grant create permission in a particular space.
    confluence.get_current_user()

    # Cloud V2 uses a space ID rather than a key. Resolve it first, then create.
    from atlassian import ConfluenceV2
    cloud = ConfluenceV2(url, username=email, password=api_token)
    space_id = cloud.get_space_by_key('SPACEKEY')['id']
    cloud.create_page(space_id=space_id, title=title, body=body)

    # Server/Data Center: retain template macros and replace explicit placeholders.
    confluence.create_page_from_template(
        space, title, template_id, replacements={"{{REPORT_MONTH}}": "August"}
    )

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

    # Server/Data Center updates use the configured REST API root and send a JSON body.

    # Get every contributor for a collaboratively edited page revision.
    contributors = confluence.get_page_version_contributors(page_id, version_number)

    # Update page or create page if it is not exists. parent_id is optional;
    # use a space key to create or update a top-level page.
    confluence.update_or_create(parent_id, title, body, representation='storage', full_width=False)
    confluence.update_or_create(title=title, body=body, space='SPACEKEY')

    # Preserve Confluence storage macros when updating tables. Do not round-trip
    # a page containing images through pandas.read_html(...).to_html(), because
    # pandas represents embedded image cells as missing values and serializes
    # them as ``NaN``. Fetch body.storage, update only the intended markup, and
    # pass the resulting storage XHTML to update_page/update_existing_page.

    # Archived pages must be restored/unarchived before update_or_create() can update them.

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

    # Get every page (content) property. Pagination is handled automatically;
    # limit controls the size of each request, not the final result size.
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
    # Downloads every attachment, following Confluence pagination automatically.
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

    # Server/Data Center only: legacy Word exporter. The returned bytes are a
    # Word-readable multipart HTML export, not a .docx document.
    word_export = confluence.get_page_as_word(page_id)

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

Storage-format updates
~~~~~~~~~~~~~~~~~~~~~~

``representation='storage'`` expects Confluence storage XHTML, including
``ac:`` and ``ri:`` macros already present in the page. It is not generic
browser HTML. Fetch ``body.storage``, preserve macros, and replace only the
dynamic values you own.

.. code-block:: python

    from xml.sax.saxutils import escape

    page = confluence.get_page_by_id(page_id, expand='body.storage')
    storage = page['body']['storage']['value']

    # Escape dynamic text only. Do not escape the complete document: that
    # would turn <ac:...> macros into literal text.
    storage = storage.replace('{{SUMMARY}}', escape('Revenue & growth'))
    confluence.update_page(page_id, page['title'], storage, representation='storage')

A literal ``&`` must be ``&amp;``. Existing entities such as ``&quot;`` are
already valid storage XML and must not be escaped a second time. Parentheses do
not require XML escaping. ``representation='wiki'`` is legacy wiki markup;
prefer storage XHTML for pages users will edit in the browser.

JSON in a code-block macro
~~~~~~~~~~~~~~~~~~~~~~~~~~

Confluence code blocks are storage-format macros. Serialize structured output
with the standard library, place it in an ``ac:plain-text-body`` CDATA section,
and set the code language to ``json``. This preserves indentation and enables
JSON syntax highlighting in the Confluence editor.

.. code-block:: python

    import json

    def confluence_json_code_block(server_output):
        json_text = json.dumps(server_output, indent=2, sort_keys=True, ensure_ascii=False)

        # CDATA cannot contain ``]]>``. Split that sequence so arbitrary JSON
        # string values remain valid Confluence storage XML.
        json_text = json_text.replace("]]>", "]]]]><![CDATA[>")

        return (
            '<ac:structured-macro ac:name="code" ac:schema-version="1">'
            '<ac:parameter ac:name="language">json</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{json_text}]]></ac:plain-text-body>'
            '</ac:structured-macro>'
        )

    page = confluence.get_page_by_id(page_id, expand='body.storage')
    body = page['body']['storage']['value']
    body = body.replace('{{SERVER_OUTPUT}}', confluence_json_code_block(server_output))
    confluence.update_page(page_id, page['title'], body, representation='storage')

The placeholder must be part of an existing storage-format page template. Do
not use ``html.escape`` on the returned macro: doing so would display the macro
as literal text instead of rendering a code block.

Word document imports
~~~~~~~~~~~~~~~~~~~~~

Confluence Server/Data Center's **Import Word document** action is provided by
the Office Connector user interface. It is not exposed as a supported REST API,
and Confluence Cloud's REST APIs likewise do not accept a ``.doc`` or ``.docx``
file as a page body. Consequently, this package intentionally has no
``import_word_document()`` method: using an internal browser endpoint would be
fragile and could lose document content.

For a faithful, one-off import (including the UI options to replace a page or
split a document by headings), use the Confluence web interface. For automated
workflows, convert the document with a tool chosen and controlled by your
application, validate the resulting storage XHTML, and then use the normal page
methods. Conversion of Word styles, images, tables, and macros is outside the
scope of the REST API and must be validated for the documents you support.

.. code-block:: python

    # ``storage_xhtml`` is produced and validated by your own DOCX conversion
    # step. It is Confluence storage XHTML, not the original DOCX bytes.
    page = confluence.create_page(space_key, title, storage_xhtml,
                                  representation='storage')

    # Optionally retain the original source document as an attachment. This
    # uploads the file; it does not convert it into page content.
    confluence.attach_file('report.docx', page_id=page['id'])

Confluence Whiteboards
----------------------

Whiteboards are available through Confluence Cloud REST API V2 only. Use
``ConfluenceV2`` (or ``ConfluenceCloud``) and a token with the relevant
``read:whiteboard:confluence``, ``write:whiteboard:confluence``, and
``delete:whiteboard:confluence`` scopes.

.. code-block:: python

    from atlassian import ConfluenceV2

    confluence = ConfluenceV2(url, username=email, password=api_token)

    # Create a whiteboard in a space. ``private`` is an optional API query
    # parameter; parent_id, template_key, and locale are optional body fields.
    whiteboard = confluence.create_whiteboard(
        space_id, title='Planning', parent_id=page_id, private=True
    )

    # Fetch it, optionally expanding related information.
    whiteboard = confluence.get_whiteboard(
        whiteboard['id'], include_collaborators=True,
        include_direct_children=True, include_operations=True,
        include_properties=True,
    )

    # Deletion moves the whiteboard to trash, where Confluence can restore it.
    confluence.delete_whiteboard(whiteboard['id'])

``get_whiteboard_by_id()`` remains as a compatible alias for
``get_whiteboard()``. Whiteboards are not supported by Confluence Server or
Data Center.

Confluence Cloud GraphQL search
-------------------------------

``ConfluenceV2`` also supports the Atlassian GraphQL Gateway for Cloud-only
use cases such as advanced search. GraphQL has a continuously evolving schema,
so REST/CQL ``search()`` remains unchanged and GraphQL responses are returned
without translation. Use a tenanted ``*.atlassian.net`` URL with an API token;
the GraphQL gateway is not available on Confluence Server or Data Center.

.. code-block:: python

    from atlassian import ConfluenceV2

    confluence = ConfluenceV2(url, username=email, password=api_token)

    # Find this once from https://your-site.atlassian.net/_edge/tenant_info.
    cloud_id = "your-confluence-cloud-id"
    response = confluence.search_graphql("deployment guide", cloud_id)

    # GraphQL may return HTTP 200 with an errors field, so inspect it first.
    if response.get("errors"):
        raise RuntimeError(response["errors"])
    search = response["data"]["search"]["search"]
    for edge in search["edges"]:
        print(edge["node"]["title"], edge["node"]["url"])

For custom queries or mutations, call ``confluence.graphql(query, variables)``.
The GraphQL Gateway has its own query-cost rate limit, separate from REST API
limits.

Confluence Cloud tasks
----------------------

.. code-block:: python

    from atlassian import ConfluenceV2

    confluence = ConfluenceV2(url, username=email, password=api_token)

    # Retrieves every result page.  Filters accept account IDs, content IDs,
    # and Unix epoch milliseconds for the date-range arguments.
    tasks = confluence.get_tasks(status="incomplete", page_ids=[page_id])

    task = confluence.get_task(task_id, body_format="storage")
    confluence.update_task(task_id, "complete")

    # Scoped tokens require read:task:confluence or write:task:confluence.


Template actions
----------------

.. code-block:: python

    # Updating a content template
    template_id = "<string>"
    name = "<string>"
    # Use the complete storage body returned by get_content_template(), or
    # construct it in the same shape.
    body = {"storage": {"value": "<string>", "representation": "storage"}}
    template_type = "page"
    description = "<string>"
    labels = [{"prefix": "<string>", "name": "<string>", "id": "<string>", "label": "<string>"}]
    space = "<key_string>"

    confluence.create_or_update_template(name, body, template_type, template_id, description, labels, space)

    # Creating a new content template
    name = "<string>"
    body = {"storage": {"value": "<string>", "representation": "storage"}}
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

Consistent return values
------------------------

For Server and Data Center, ``get_tables_from_page`` always returns a
dictionary with ``page_id``, ``number_of_tables_in_page``, and
``tables_content``. Pages without tables use a count of zero and an empty
list. ``download_attachments_from_page`` likewise returns an empty dictionary
in memory mode, or ``{"attachments_downloaded": 0, "path": ...}`` on disk
when no attachments match.

``attach_content`` and ``update_page`` raise ``ApiNotFoundError`` when the
target page cannot be resolved instead of returning ``None``. Title lookups
remain search-result responses; an empty ``results`` collection means that no
matching page exists.

Content history
---------------

``get_content_history_by_version_number`` and the history-removal methods use
the supported Server/Data Center ``/rest/api/content/{id}/version/{number}``
endpoint. ``remove_page_history_keep_version`` also tolerates historical gaps,
so rerunning it after a partial cleanup does not fail on an already-deleted
version.

For Confluence Cloud V2, use ``get_page_versions`` or ``get_page_version`` to
read page history. The published V2 API does not provide a delete-version
operation, so deletion requires the compatible V1 endpoint and appropriate
permission.

Scoped Cloud API tokens
-----------------------

Scoped Confluence Cloud API tokens use the Atlassian API gateway and the v2
API. Pass the gateway URL containing the cloud ID; ``Confluence`` selects the
v2 Cloud client automatically and does not append ``/wiki``.

.. code-block:: python

    confluence = Confluence(
        url="https://api.atlassian.com/ex/confluence/<cloud-id>",
        username="user@example.com",
        password="scoped-api-token",
        cloud=True,
    )

    page = confluence.get_page_by_id("<page-id>")

Confluence Cloud databases
--------------------------

Confluence Cloud v2 supports database lifecycle metadata: create, retrieve by
ID, and move to trash. Use ``ConfluenceV2`` (or a gateway URL as above) for
these endpoints. The public API does not currently expose database records,
fields, views, or queries.

.. code-block:: python

    from atlassian import ConfluenceV2

    confluence = ConfluenceV2(
        url="https://your-domain.atlassian.net/wiki",
        username="user@example.com",
        password="api-token",
    )

    database = confluence.create_database(
        space_id="<space-id>",
        title="Release tracker",
        parent_id="<parent-page-or-folder-id>",
        private=False,
    )
    details = confluence.get_database(database["id"], include_properties=True)
    confluence.delete_database(database["id"])

Scoped tokens require the corresponding ``write:database:confluence``,
``read:database:confluence``, or ``delete:database:confluence`` scope.

Confluence Cloud folders
------------------------

Confluence Cloud v2 supports creating, retrieving, and moving folders to
trash. A folder may have a page or another folder as its parent. Use
``ConfluenceV2`` (or a gateway URL as above).

.. code-block:: python

    folder = confluence.create_folder(
        space_id="<space-id>",
        title="Release assets",
        parent_id="<parent-page-or-folder-id>",
    )
    details = confluence.get_folder(folder["id"], include_direct_children=True)
    confluence.delete_folder(folder["id"])

Scoped tokens require the corresponding ``write:folder:confluence``,
``read:folder:confluence``, or ``delete:folder:confluence`` scope.

Cloud group members
-------------------

Confluence Cloud group membership uses the group **ID**, not its display name.
The API returns group IDs from ``get_all_groups``.  The legacy Server/Data
Center methods continue to use group names.

.. code-block:: python

    for group in confluence.get_all_groups(start=0, limit=1000):
        members = confluence.get_all_members(group["id"])

License endpoints
-----------------

``get_license_details`` and the related license-seat methods are available for
Confluence Server and Data Center only. Confluence Cloud does not expose an
equivalent license REST API; Cloud clients receive ``ApiNotAcceptable`` instead
of an HTTP 404.
