Assets Cloud
============

Use ``AssetsCloud`` for Jira Service Management Assets Cloud. The client
discovers the Assets workspace and routes requests through the workspace API:

.. code-block:: python

    from atlassian import AssetsCloud

    assets = AssetsCloud(
        "https://example.atlassian.net",
        username="email@example.com",
        password="api-token",
        cloud=True,
    )

    objects = assets.aql('objectType = "Server"', max_results=50)
    objects_page = assets.get_aql_objects("objectType = Server", page=1, result_per_page=50)
    iql_objects_page = assets.get_iql_objects("objectType = Server", page=1, result_per_page=50)
    server = assets.get_object("10001")
    owner = assets.get_object_attribute_value("10001", attribute_id="12345")
    schemas = assets.list_object_schema()

The Cloud client also supports import sources, object schemas and types,
object-type attributes, status/reference configuration, import schedules,
icons, usage, dataset export/import, and issue-type screen schemes. Request
payloads are passed through unchanged so they remain compatible with the
Assets schema enabled in each Jira site.

.. code-block:: python

    schema = assets.create_object_schema("OPS", "Operations assets")
    assets.create_object_type({"name": "Server", "objectSchemaId": schema["id"]})
    csv_bytes = assets.export_dataset(testIssueKey="TEST-1")

``Assets`` remains an alias for the legacy Insight/server client. Existing
server methods and URLs are unchanged.

Assets Data Center / Server
---------------------------

For Assets 10.x on Jira Server/Data Center, use the explicit server client. It
uses the ``/rest/assets/1.0`` root and supports the same object, schema,
object-type, import, configuration, and progress helpers:

.. code-block:: python

    from atlassian import AssetsServer

    assets = AssetsServer(
        "https://jira.example.com",
        username="admin",
        password="password",
    )
    assets_objects = assets.get_aql_objects(
        query='objectType = "Server"',
        page=1,
        result_per_page=25,
    )
    assets.update_object_type("10001", {"name": "Servers"})

``AssetsDataCenter`` is retained as an alias for ``AssetsServer``. The older
``Assets``/``Insight`` classes remain unchanged for integrations using the
legacy Insight REST root.
